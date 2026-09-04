from pathlib import Path
import numpy as np, pandas as pd, json, math, hashlib, zipfile, shutil, os, re
from datetime import datetime, timezone
BASE=Path('/mnt/data'); OUT=BASE/'x5_all_data_package'; ZIP=BASE/'x5_all_data.zip'

def write_csv(df,path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); df.to_csv(path,index=False,encoding='utf-8-sig')
def largest_remainder_counts(n, probs):
    probs=np.array(probs,dtype=float); probs=probs/probs.sum(); raw=probs*n; base=np.floor(raw).astype(int); rem=n-base.sum();
    if rem>0: base[np.argsort(-(raw-base))[:rem]]+=1
    return base
def sigmoid(x): return 1/(1+np.exp(-x))
def sample_weighted(rng,labels,probs,size):
    p=np.array(probs,dtype=float); p=p/p.sum(); return rng.choice(labels,size=size,p=p)
def sha256(path):
    h=hashlib.sha256();
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

# Load definitions from the original builder without running its top-level build.
text=(BASE/'build_x5_package.py').read_text(encoding='utf-8')
seg=text.split('# ---------- simulation generator ----------',1)[1].split('summaries=[]; validation=[]',1)[0]
exec(seg, globals())

# Optimized weekly simulation for n=10k
def simulate_weekly_fast(users,yards,members,rng):
    n=len(users)
    assignment=pd.DataFrame({'user_id':users.user_id,'assignment':'not_in_experiment','yard_id':pd.Series([None]*n,dtype='object')})
    if len(members):
        mm=members.merge(yards[['yard_id','assignment']],on='yard_id',how='left')
        mp_a=mm.set_index('user_id').assignment.to_dict(); mp_y=mm.set_index('user_id').yard_id.to_dict()
        assignment['assignment']=assignment.user_id.map(mp_a).fillna('not_in_experiment')
        assignment['yard_id']=assignment.user_id.map(mp_y)
    assignment['assignment_ts']=pd.Timestamp('2026-07-01T09:00:00'); assignment['treatment_start_ts']=TREAT_START
    u=users.merge(assignment,on='user_id',how='left')
    arche_eff={'shopper':.055,'runner':.035,'promo_hunter':.075,'family':.070,'sleeper':.10}
    user_eff=np.array([arche_eff[a] for a in u.archetype]) + .03*(u.digital_readiness.to_numpy()-.65)
    harm=rng.random(n)<.08; user_eff=np.clip(user_eff-harm*.06+rng.normal(0,.018,n),-.08,.16)
    optin_p=np.clip(.40+.35*u.digital_readiness.to_numpy()+.08*(u.archetype=='family').to_numpy()-.08*(u.archetype=='sleeper').to_numpy(),.15,.90)
    optin=rng.random(n)<optin_p
    base_rate=u.baseline_visit_rate_week.to_numpy(); is_test=(u.assignment.to_numpy()=='test')
    frames=[]
    for w in range(34):
        week_start=START+pd.Timedelta(weeks=w); seasonal=1.0+0.06*np.sin(2*np.pi*w/13)+(0.05 if w in (0,17,33) else 0)
        lam=np.clip(base_rate*seasonal,.01,None); y0=rng.poisson(lam)
        if w>=26:
            plus=rng.poisson(np.clip(user_eff,0,None)*lam*optin)
            minus=rng.binomial(np.minimum(y0,1),np.clip(np.clip(-user_eff,0,None)*lam*optin,0,.5))
            y1=np.maximum(0,y0+plus-minus)
        else: y1=y0.copy()
        observed=np.where((w>=26)&is_test,y1,y0)
        frames.append(pd.DataFrame({'user_id':u.user_id.to_numpy(),'week_index':w,'week_start':week_start,'assignment':u.assignment.to_numpy(),'yard_id':u.yard_id.to_numpy(),
                                    'y0_visits':y0.astype(int),'y1_visits':y1.astype(int),'observed_visits':observed.astype(int),'latent_effect_rate':user_eff,'latent_opt_in':optin.astype(int)}))
    return assignment,pd.concat(frames,ignore_index=True)

def generate_receipts_fast(users,weekly,rng):
    counts=weekly.observed_visits.to_numpy(dtype=int); total=int(counts.sum()); idx=np.repeat(np.arange(len(weekly)),counts)
    w=weekly.iloc[idx].reset_index(drop=True)
    attrs=users.set_index('user_id').loc[w.user_id,['home_store_id','basket_base_rub','archetype','promo_sensitivity']].reset_index(drop=True)
    # random timestamp within week
    days=rng.integers(0,7,total); hours=rng.integers(8,22,total); mins=rng.integers(0,60,total)
    ts=pd.to_datetime(w.week_start)+pd.to_timedelta(days,unit='D')+pd.to_timedelta(hours,unit='h')+pd.to_timedelta(mins,unit='m')
    basket=attrs.basket_base_rub.to_numpy()*rng.lognormal(0,.28,total)
    test_post=(w.assignment.eq('test') & w.week_index.ge(26)).to_numpy(); basket*=np.where(test_post,rng.normal(1.01,.03,total),1.0); basket=np.maximum(80,basket)
    arch_disc=np.array([ARCH_DISCOUNT[a] for a in attrs.archetype]); promo=attrs.promo_sensitivity.to_numpy()
    dr=np.clip(arch_disc+.10*promo+rng.normal(0,.035,total),0,.38)
    paid=np.round(basket,2); regular=np.round(paid/(1-dr),2); discount=np.round(regular-paid,2)
    ret=rng.random(total)<.010; return_amt=np.where(ret,paid,0.0); net=np.round(paid-return_amt,2)
    margin_rate=np.clip(.20+rng.normal(0,.025,total),.10,.30); cm=np.round(net*margin_rate,2)
    receipts=pd.DataFrame({'receipt_id':[f'R{i:09d}' for i in range(1,total+1)],'user_id':w.user_id.to_numpy(),'store_id':attrs.home_store_id.to_numpy(),'ts':ts,
                           'week_index':w.week_index.to_numpy(),'assignment':w.assignment.to_numpy(),'total_paid_rub':paid,'regular_total_rub':regular,'discount_total_rub':discount,
                           'is_returned':ret,'return_amount_rub':return_amt,'net_sales_rub':net,'contribution_margin_rate':margin_rate,'contribution_margin_rub':cm})
    return receipts

n=10000; seed=260904; out=OUT/'data/reference_10000'; out.mkdir(parents=True,exist_ok=True)
users,households,stores,rng=make_population(n,seed)
yards,members=form_yards(users,rng)
assignment,weekly=simulate_weekly_fast(users,yards,members,rng)
receipts=generate_receipts_fast(users,weekly,rng)
challenges,decisions,cevents,rewards,ledger,ycycles=make_challenges_rewards(users,yards,members,weekly,receipts,rng)
referrals,ff,fg=make_referrals_fraud(users,yards,members,rng)
user_export=users.drop(columns=['fraud_persona_hidden']); fraud_personas=users[['user_id','fraud_persona_hidden']].rename(columns={'fraud_persona_hidden':'fraud_persona_ground_truth'})
tables={'users.csv':user_export,'households.csv':households,'stores.csv':stores,'experiment_assignments.csv':assignment,'yards.csv':yards,'memberships.csv':members,'weekly_outcomes.csv':weekly,
        'receipts.csv':receipts,'challenge_candidates.csv':challenges,'challenge_decisions.csv':decisions,'challenge_events.csv':cevents,'rewards.csv':rewards,'reward_ledger.csv':ledger,
        'yard_cycles.csv':ycycles,'referral_events.csv':referrals,'fraud_features.csv':ff,'fraud_events_ground_truth.csv':fg,'fraud_personas_ground_truth.csv':fraud_personas,'products.csv':make_products()}
for name,df in tables.items(): write_csv(df,out/name)
summary=summarize(n,users,yards,members,assignment,weekly,receipts,rewards,ledger,ycycles,ff,fg)
(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,default=str),encoding='utf-8')

# Load 1k summary and create combined results + validations
summaries=[json.loads((OUT/'data/reference_1000/summary.json').read_text(encoding='utf-8')),summary]
write_csv(pd.DataFrame(summaries),OUT/'results/reference_metrics.csv')
validation=[]
for n0 in [1000,10000]:
    f=OUT/f'data/reference_{n0}'
    us=pd.read_csv(f/'users.csv'); st=pd.read_csv(f/'stores.csv'); asg=pd.read_csv(f/'experiment_assignments.csv'); wk=pd.read_csv(f/'weekly_outcomes.csv'); rec=pd.read_csv(f/'receipts.csv'); ffeat=pd.read_csv(f/'fraud_features.csv'); rew=pd.read_csv(f/'rewards.csv'); led=pd.read_csv(f/'reward_ledger.csv')
    def add(check,passed,detail): validation.append([n0,check,bool(passed),detail])
    add('unique_user_id',us.user_id.is_unique,f'{us.user_id.nunique()}/{len(us)} unique')
    target=dict(zip(AGE_BANDS,largest_remainder_counts(n0,AGE_P))); actual=us.age_band.value_counts().to_dict(); add('age_quota_exact',all(actual.get(a,0)==target[a] for a in AGE_BANDS),str(actual))
    add('assignment_precedes_treatment',(pd.to_datetime(asg.assignment_ts)<pd.to_datetime(asg.treatment_start_ts)).all(),'assignment_ts < treatment_start_ts')
    add('no_fraud_label_in_features','is_fraud_ground_truth' not in ffeat.columns and 'fraud_persona' not in '|'.join(ffeat.columns),'ground truth separated')
    add('receipt_user_fk',rec.user_id.isin(us.user_id).all(),'all receipt users valid'); add('receipt_store_fk',rec.store_id.isin(st.store_id).all(),'all receipt stores valid')
    if (f/'items.csv').exists():
        it=pd.read_csv(f/'items.csv',usecols=['receipt_id','price_paid_rub']); recon=it.groupby('receipt_id').price_paid_rub.sum().round(2); r=rec.set_index('receipt_id').total_paid_rub.round(2); diff=(recon-r.reindex(recon.index)).abs().max(); add('items_to_receipts_reconcile',diff<=0.02,f'max_abs_diff={diff}')
    if len(rew):
        net=led.groupby('reward_id').amount_delta_rub.sum().round(2); exp=rew.set_index('reward_id').apply(lambda r:0.0 if r.final_status=='reversed' else r.amount_rub_equivalent,axis=1).round(2); diff=(net-exp.reindex(net.index)).abs().max(); add('reward_ledger_reconcile',diff<=0.01,f'max_abs_diff={diff}')
    expuids=set(asg.loc[asg.assignment.isin(['test','control']),'user_id']); aa=wk[(wk.week_index>=26)&wk.user_id.isin(expuids)].groupby('user_id').y0_visits.sum().reset_index(); aa['grp']=aa.user_id.str.extract(r'(\d+)').astype(int)[0]%2; aam=aa.groupby('grp').y0_visits.mean(); aadiff=float(aam.get(1,0)-aam.get(0,0)); add('aa_null_reasonable',abs(aadiff)<0.8,f'8w mean diff={aadiff:.4f} visits')
write_csv(pd.DataFrame(validation,columns=['n_users','check','passed','detail']),OUT/'results/validation_checks.csv')

# MC + sensitivity if absent
if not (OUT/'results/monte_carlo_45x2.csv').exists():
    def mc_one(n,seed):
        rng=np.random.default_rng(seed); rate=np.clip(rng.lognormal(np.log(1.8),.55,n),.05,8); groups=np.arange(n)//5; ug=np.unique(groups); treatg=set(rng.choice(ug,size=len(ug)//2,replace=False)); treat=np.array([g in treatg for g in groups]); y0=rng.poisson(rate*8); eff=np.clip(rng.normal(.06,.035,n),-.04,.16); y1=y0+rng.poisson(np.clip(rate*8*eff,0,None))-rng.binomial(np.minimum(y0,1),np.clip(-eff,0,.5)); obs=np.where(treat,y1,y0); mt=obs[treat].mean(); mc=obs[~treat].mean(); est=mt-mc; true=(y1-y0)[treat].mean(); return [n,seed,mt,mc,est,true,est-true]
    mc=[]
    for n0 in [1000,10000]:
        for rep in range(45): mc.append(mc_one(n0,880000+n0+rep))
    mcdf=pd.DataFrame(mc,columns=['n_users','seed','mean_visits_test_8w','mean_visits_control_8w','estimated_itt_visits','true_att_visits','estimation_error_visits']); write_csv(mcdf,OUT/'results/monte_carlo_45x2.csv'); mcsummary=mcdf.groupby('n_users').agg(reps=('seed','count'),mean_est=('estimated_itt_visits','mean'),sd_est=('estimated_itt_visits','std'),p025=('estimated_itt_visits',lambda s:s.quantile(.025)),p975=('estimated_itt_visits',lambda s:s.quantile(.975)),rmse=('estimation_error_visits',lambda s:float(np.sqrt(np.mean(s**2))))).reset_index(); write_csv(mcsummary,OUT/'results/monte_carlo_summary.csv')
else: mcdf=pd.read_csv(OUT/'results/monte_carlo_45x2.csv')
if not (OUT/'results/sensitivity_17_runs.csv').exists():
    base={'causal_uplift':.06,'reward_rub':80,'margin_rate':.20,'cannibalization':.15}; runs=[('base','base',None)]; vals={'causal_uplift':[-.02,0,.03,.08],'reward_rub':[40,60,100,140],'margin_rate':[.12,.16,.24,.28],'cannibalization':[0,.10,.30,.50]}
    for p,vs in vals.items():
        for v in vs:runs.append((p,f'{p}={v}',v))
    rows=[]; baseline_visits_8w=14.4; basket=760; completion=.48
    for p,label,v in runs:
        cfg=base.copy();
        if p!='base':cfg[p]=v
        incremental_visits=baseline_visits_8w*cfg['causal_uplift']*(1-cfg['cannibalization']); inc_cm=incremental_visits*basket*cfg['margin_rate']; reward_cost=completion*cfg['reward_rub']; net=inc_cm-reward_cost; rows.append([label,cfg['causal_uplift'],cfg['reward_rub'],cfg['margin_rate'],cfg['cannibalization'],incremental_visits,inc_cm,reward_cost,net])
    sens=pd.DataFrame(rows,columns=['run','causal_uplift','reward_rub','margin_rate','cannibalization','incremental_visits_8w_per_user','incremental_cm_rub_per_user','reward_cost_rub_per_user','net_incremental_cm_rub_per_user']); write_csv(sens,OUT/'results/sensitivity_17_runs.csv')
else:sens=pd.read_csv(OUT/'results/sensitivity_17_runs.csv')

# figures
try:
    import matplotlib.pyplot as plt
    figdir=OUT/'figures'; figdir.mkdir(exist_ok=True)
    s1000=pd.read_csv(OUT/'data/reference_1000/users.csv'); vc=s1000.age_band.value_counts().reindex(AGE_BANDS); plt.figure(figsize=(8,4.8)); plt.bar(AGE_BANDS,vc.values); plt.title('Synthetic age quotas — n=1,000'); plt.ylabel('Users'); plt.xlabel('Age band'); plt.tight_layout(); plt.savefig(figdir/'age_quota_1000.png',dpi=150); plt.close()
    d=mcdf[mcdf.n_users==10000].estimated_itt_visits; plt.figure(figsize=(8,4.8)); plt.hist(d,bins=12); plt.title('Monte Carlo estimated ITT — n=10,000'); plt.xlabel('Incremental visits per user over 8 weeks'); plt.ylabel('Replications'); plt.tight_layout(); plt.savefig(figdir/'mc_itt_n10000.png',dpi=150); plt.close()
    plt.figure(figsize=(8,4.8)); plt.plot(range(len(sens)),sens.net_incremental_cm_rub_per_user,marker='o'); plt.axhline(0); plt.title('One-factor sensitivity: net incremental CM'); plt.xlabel('Sensitivity run index'); plt.ylabel('RUB per user'); plt.tight_layout(); plt.savefig(figdir/'sensitivity_net_cm.png',dpi=150); plt.close()
except Exception as e:(OUT/'figures_error.txt').write_text(str(e),encoding='utf-8')

# README, code, dictionary, manifest
readme=f'''# X5 synthetic loyalty simulation — all data package\n\nGenerated: {datetime.now(timezone.utc).isoformat()}\n\nThis archive is a reproducible **synthetic scenario-analysis package**, not a forecast or evidence of real X5 uplift.\n\n## Contents\n- `source/` — original self-contained Markdown and extracted embedded sources.\n- `config/` — source ledger and six scenario configs.\n- `data/reference_1000/` — full synthetic run including item-level data.\n- `data/reference_10000/` — full user/yard/challenge/reward/fraud/weekly/receipt-level run; item rows intentionally omitted for archive practicality.\n- `results/` — metrics, validations, Monte Carlo, sensitivity.\n- `figures/` — diagnostics.\n- `code/` — generators used to build the archive.\n- `MANIFEST.csv` — sizes and SHA-256 hashes.\n\nAll X5-specific behavioral/economic values are assumptions or latent scenario inputs until replaced by internal/pilot data.\n'''
(OUT/'README.md').write_text(readme,encoding='utf-8'); (OUT/'code').mkdir(exist_ok=True); shutil.copy2(BASE/'build_x5_package.py',OUT/'code/build_x5_package.py'); shutil.copy2(BASE/'continue_x5.py',OUT/'code/continue_x5.py')
schemas=[]
for n0 in [1000,10000]:
    folder=OUT/f'data/reference_{n0}'
    for f in folder.glob('*.csv'):
        try:
            df=pd.read_csv(f,nrows=5)
            for c in df.columns:schemas.append([n0,f.name,c,str(df[c].dtype)])
        except Exception:pass
write_csv(pd.DataFrame(schemas,columns=['n_users','table','column','sample_inferred_dtype']),OUT/'DATA_DICTIONARY.csv')
manifest=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file():manifest.append([str(p.relative_to(OUT)),p.stat().st_size,'' if p.name=='MANIFEST.csv' else sha256(p)])
write_csv(pd.DataFrame(manifest,columns=['path','bytes','sha256']),OUT/'MANIFEST.csv')
if ZIP.exists():ZIP.unlink()
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(OUT.parent))
with zipfile.ZipFile(ZIP,'r') as z:bad=z.testzip(); names=z.namelist()
print(json.dumps({'zip':str(ZIP),'zip_bytes':ZIP.stat().st_size,'files_in_zip':len(names),'bad_member':bad,'summary_10000':summary},ensure_ascii=False,indent=2,default=str))
