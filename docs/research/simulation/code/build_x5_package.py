from pathlib import Path
import numpy as np, pandas as pd, json, csv, math, re, hashlib, zipfile, shutil, os
from datetime import datetime, timedelta, timezone

BASE = Path('/mnt/data')
SRC = BASE / 'Pasted markdown(20260903-191241).md'
OUT = BASE / 'x5_all_data_package'
ZIP = BASE / 'x5_all_data.zip'
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)

# ---------- helpers ----------
def write_csv(df, path):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8-sig')

def sha256(path):
    h = hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def largest_remainder_counts(n, probs):
    probs=np.array(probs,dtype=float); probs=probs/probs.sum()
    raw=probs*n; base=np.floor(raw).astype(int); rem=n-base.sum()
    if rem>0:
        idx=np.argsort(-(raw-base))[:rem]; base[idx]+=1
    return base

def sigmoid(x): return 1/(1+np.exp(-x))

def sample_weighted(rng, labels, probs, size):
    p=np.array(probs,dtype=float); p=p/p.sum(); return rng.choice(labels,size=size,p=p)

# ---------- preserve/extract source materials ----------
text = SRC.read_text(encoding='utf-8')
source_dir = OUT/'source'
source_dir.mkdir()
shutil.copy2(SRC, source_dir/'original_prompt_package.md')

m = re.search(r'<primary_prompt source="([^"]+)">\n(.*?)\n</primary_prompt>', text, flags=re.S)
if m:
    p=source_dir/m.group(1); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(m.group(2).strip()+"\n",encoding='utf-8')
for m in re.finditer(r'<source path="([^"]+)">\n(.*?)\n</source>', text, flags=re.S):
    rel=m.group(1); content=m.group(2).strip()+"\n"
    # unwrap single code fence for csv
    cm=re.fullmatch(r'```(?:csv)?\n(.*?)\n```\n?', content, flags=re.S)
    if cm: content=cm.group(1)+"\n"
    p=source_dir/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding='utf-8')

# ---------- assumptions / source ledger ----------
ledger = pd.DataFrame([
    ['adult_age_band','18-24','8.990%','2024-01-01','Russia 18+','DERIVED','ROSSTAT_AGE_2024','Replace only if newer official age structure is deliberately adopted'],
    ['adult_age_band','25-34','15.057%','2024-01-01','Russia 18+','DERIVED','ROSSTAT_AGE_2024','same'],
    ['adult_age_band','35-44','21.112%','2024-01-01','Russia 18+','DERIVED','ROSSTAT_AGE_2024','same'],
    ['adult_age_band','45-54','17.104%','2024-01-01','Russia 18+','DERIVED','ROSSTAT_AGE_2024','same'],
    ['adult_age_band','55-64','16.225%','2024-01-01','Russia 18+','DERIVED','ROSSTAT_AGE_2024','same'],
    ['adult_age_band','65+','21.511%','2024-01-01','Russia 18+','DERIVED','ROSSTAT_AGE_2024','same'],
    ['internet_use','age-conditional','see source priors','2025','Russia 18+','PUBLIC_PROXY','ROSSTAT_ICT_2025','Do not treat as X5 app penetration'],
    ['loyalty_member_probability','base','0.78','simulation','synthetic adults','ASSUMPTION','none','Replace with X5 loyalty penetration in pilot population'],
    ['app_user_probability','base conditional model','scenario model','simulation','loyalty members','ASSUMPTION','none','Replace with observed X5 app activity model'],
    ['visit_frequency','archetype rates','0.28–4.2 visits/week','simulation','synthetic users','ASSUMPTION','none','Fit from receipt history'],
    ['basket_value','archetype medians','520–1100 RUB','simulation','synthetic receipts','ASSUMPTION','none','Fit from receipt distribution'],
    ['contribution_margin_rate','base','0.20','simulation','net sales','ASSUMPTION','none','Replace with finance-approved contribution margin'],
    ['return_probability','base','0.010','simulation','receipts','ASSUMPTION','none','Replace with observed return/cancellation rate'],
    ['true_treatment_effect','base','heterogeneous ~ -3% to +12%','simulation','potential outcomes','LATENT_GROUND_TRUTH','none','Not estimated from synthetic data; vary in scenarios'],
    ['yard_size','base','3–7','simulation','yard','ASSUMPTION','dvor-spec','Validate UX and power implications'],
    ['yard_min_pool','base','20','simulation','active store pool','ASSUMPTION','dvor-spec','Privacy/legal validation required'],
    ['yard_backup_coef','base','0.70','simulation','yard cycle','ASSUMPTION','dvor-spec','A/B or product validation'],
    ['reward_rub','base','80 RUB-equivalent/cycle','simulation','completed member-cycle','ASSUMPTION','none','Optimize against incremental margin'],
    ['brand_funding_probability','base','0.30','simulation','reward','ASSUMPTION','none','Replace with commercial agreements'],
    ['fraud_prevalence','base','1.0% users','simulation','synthetic users','LATENT_GROUND_TRUTH','none','Stress-test and replace with observed prevalence estimate'],
], columns=['parameter','variant','value_or_range','reference_date','population_or_unit','status','source_key','replacement_rule'])
write_csv(ledger, OUT/'config/source_ledger.csv')

scenario_yaml = '''version: 1
note: "Synthetic scenario inputs; not a forecast of X5 outcomes."
scenarios:
  conservative:
    causal_uplift_mean: 0.02
    reward_rub: 100
    margin_rate: 0.16
    cannibalization: 0.30
    fraud_prevalence: 0.015
    group_harm_probability: 0.15
  base:
    causal_uplift_mean: 0.06
    reward_rub: 80
    margin_rate: 0.20
    cannibalization: 0.15
    fraud_prevalence: 0.010
    group_harm_probability: 0.08
  upside:
    causal_uplift_mean: 0.10
    reward_rub: 60
    margin_rate: 0.24
    cannibalization: 0.08
    fraud_prevalence: 0.007
    group_harm_probability: 0.04
  stress_low_completion:
    causal_uplift_mean: 0.01
    reward_rub: 80
    margin_rate: 0.20
    cannibalization: 0.20
    fraud_prevalence: 0.010
    group_harm_probability: 0.12
  stress_high_fraud:
    causal_uplift_mean: 0.06
    reward_rub: 80
    margin_rate: 0.20
    cannibalization: 0.15
    fraud_prevalence: 0.050
    group_harm_probability: 0.08
  stress_group_harm:
    causal_uplift_mean: 0.01
    reward_rub: 80
    margin_rate: 0.20
    cannibalization: 0.15
    fraud_prevalence: 0.010
    group_harm_probability: 0.30
'''
(OUT/'config').mkdir(exist_ok=True)
(OUT/'config/scenarios.yaml').write_text(scenario_yaml,encoding='utf-8')

# ---------- simulation generator ----------
AGE_BANDS=['18-24','25-34','35-44','45-54','55-64','65+']
AGE_P=[.08990,.15057,.21112,.17104,.16225,.21511]
MALE_P=dict(zip(AGE_BANDS,[.51564,.50136,.48818,.47246,.43898,.34852]))
URBAN_P=dict(zip(AGE_BANDS,[.75034,.76484,.77638,.75438,.71691,.74551]))
INTERNET_P={'18-24':.9893,'25-34':.9931,'35-44':.9917,'45-54':.9855,'55-64':.9502,'65+':.67}
FD_LABELS=['Central','Northwestern','Southern','North Caucasian','Volga','Ural','Siberian','Far Eastern']
FD_P=[.27505,.09470,.11375,.07014,.19528,.08390,.11336,.05382]
ARCH=['shopper','runner','promo_hunter','family','sleeper']
ARCH_BASE={'shopper':1.10,'runner':4.20,'promo_hunter':2.00,'family':2.20,'sleeper':0.28}
ARCH_BASKET={'shopper':950,'runner':520,'promo_hunter':700,'family':1100,'sleeper':760}
ARCH_DISCOUNT={'shopper':.10,'runner':.07,'promo_hunter':.24,'family':.12,'sleeper':.10}
CAT=['Dairy','Bakery','Produce','Meat','Fish','Grocery','Beverages','Household','Personal Care','Baby','Frozen','Snacks']
CAT_P=np.array([.12,.09,.13,.10,.04,.15,.08,.08,.06,.04,.05,.06]); CAT_P=CAT_P/CAT_P.sum()

START=pd.Timestamp('2026-01-05')
TREAT_START=START+pd.Timedelta(weeks=26)
END=START+pd.Timedelta(weeks=34)


def make_population(n, seed):
    rng=np.random.default_rng(seed)
    counts=largest_remainder_counts(n,AGE_P)
    age=np.concatenate([[a]*c for a,c in zip(AGE_BANDS,counts)])
    rng.shuffle(age)
    sex=np.array(['M' if rng.random()<MALE_P[a] else 'F' for a in age])
    urban=np.array([rng.random()<URBAN_P[a] for a in age])
    fd=sample_weighted(rng,FD_LABELS,FD_P,n)
    internet=np.array([rng.random()<INTERNET_P[a] for a in age])
    online_proxy=np.clip(np.array([INTERNET_P[a] for a in age]) - np.where(age=='65+',.25,.12),.05,.95)
    digital=np.clip(.55*internet.astype(float)+.45*online_proxy+rng.normal(0,.08,n),0,1)
    loyalty=rng.random(n)<.78
    app_p=np.clip(sigmoid(-1.1+2.2*digital+0.35*urban.astype(float)-0.35*(age=='65+')),.05,.95)
    app=loyalty & (rng.random(n)<app_p)
    # simplified household/life stage
    hh_size=[]; child18=[]; child3=[]
    for a in age:
        if a=='18-24': probs=[.38,.38,.18,.06]
        elif a in ('25-34','35-44'): probs=[.20,.31,.32,.17]
        elif a=='45-54': probs=[.25,.39,.25,.11]
        elif a=='55-64': probs=[.34,.45,.16,.05]
        else: probs=[.50,.42,.07,.01]
        s=rng.choice([1,2,3,4],p=probs); hh_size.append(s)
        pchild={'18-24':.08,'25-34':.42,'35-44':.48,'45-54':.24,'55-64':.05,'65+':.01}[a]
        c=rng.random()<pchild; child18.append(c)
        p3={'18-24':.02,'25-34':.20,'35-44':.12,'45-54':.02,'55-64':.002,'65+':.0}[a]
        child3.append(c and rng.random()<p3/max(pchild,1e-9))
    hh_size=np.array(hh_size); child18=np.array(child18); child3=np.array(child3)
    # archetype probabilities, life stage affects family
    arche=[]
    for i,a in enumerate(age):
        p=np.array([.30,.20,.22,.18,.10],dtype=float)
        if child18[i]: p += np.array([-.05,-.05,-.05,.18,-.03])
        if a=='65+': p += np.array([.05,-.12,.02,-.02,.07])
        if digital[i]>.8: p += np.array([0,.03,.03,0,-.02])
        p=np.clip(p,.01,None); p=p/p.sum(); arche.append(rng.choice(ARCH,p=p))
    arche=np.array(arche)
    activity_mult=rng.lognormal(mean=0,sigma=.34,size=n)
    baseline_rate=np.array([ARCH_BASE[x] for x in arche])*activity_mult
    baseline_rate=np.clip(baseline_rate,.05,8.0)
    basket_base=np.array([ARCH_BASKET[x] for x in arche])*rng.lognormal(0,.18,n)
    promo_sens=np.clip(np.array([.75 if x=='promo_hunter' else .35 for x in arche])+rng.normal(0,.12,n),0,1)
    # stores: ~65 users/store, stratified weakly by FD/urban not exact realism
    nstores=max(8,round(n/65))
    stores=pd.DataFrame({'store_id':[f'S{i:04d}' for i in range(1,nstores+1)]})
    stores['federal_district']=sample_weighted(rng,FD_LABELS,FD_P,nstores)
    stores['urban']=rng.random(nstores)<.76
    # assign each user preferably matching fd+urban; fallback random
    by={(d,u):g['store_id'].tolist() for (d,u),g in stores.groupby(['federal_district','urban'])}
    home=[]
    for d,u in zip(fd,urban):
        cand=by.get((d,bool(u))) or by.get((d,not bool(u))) or stores['store_id'].tolist()
        home.append(rng.choice(cand))
    # fraud latent ground truth
    fraud=rng.random(n)<.01
    personas=np.array(['none']*n,dtype=object)
    fp=['star','ring','account_cycling','clone_receipts']
    personas[fraud]=rng.choice(fp,size=fraud.sum(),p=[.28,.27,.25,.20])
    users=pd.DataFrame({
        'user_id':[f'U{i:06d}' for i in range(1,n+1)],'age_band':age,'sex':sex,'urban':urban.astype(int),'federal_district':fd,
        'digital_readiness':np.round(digital,4),'loyalty_member':loyalty.astype(int),'app_user':app.astype(int),'home_store_id':home,
        'archetype':arche,'baseline_visit_rate_week':np.round(baseline_rate,4),'basket_base_rub':np.round(basket_base,2),
        'promo_sensitivity':np.round(promo_sens,4),'has_child_under_18':child18.astype(int),'has_child_under_3':child3.astype(int),
        'fraud_persona_hidden':personas
    })
    households=pd.DataFrame({'household_id':[f'H{i:06d}' for i in range(1,n+1)],'user_id':users.user_id,'household_size':hh_size,
                             'has_child_under_18':child18.astype(int),'has_child_under_3':child3.astype(int),'generation_simplification':'one modeled adult per household'})
    return users, households, stores, rng


def form_yards(users,rng,min_pool=20):
    eligible=(users.app_user.eq(1)&users.loyalty_member.eq(1)&(users.baseline_visit_rate_week>=.25))
    yards=[]; members=[]; yid=1
    for store,g in users[eligible].groupby('home_store_id'):
        if len(g)<min_pool: continue
        gg=g.sort_values('baseline_visit_rate_week')
        ids=gg.user_id.tolist(); rates=gg.baseline_visit_rate_week.to_numpy()
        i=0
        local=[]
        while i+3<=len(ids):
            remaining=len(ids)-i
            size=int(rng.integers(3,8))
            if remaining-size in (1,2): size=max(3,size-(3-(remaining-size)))
            size=min(size,remaining)
            if size<3: break
            chunk=gg.iloc[i:i+size]
            ratio=chunk.baseline_visit_rate_week.max()/max(chunk.baseline_visit_rate_week.min(),.05)
            if ratio>2.5 and size>3:
                size=3; chunk=gg.iloc[i:i+size]; ratio=chunk.baseline_visit_rate_week.max()/max(chunk.baseline_visit_rate_week.min(),.05)
            if ratio<=2.5:
                yard_id=f'Y{yid:05d}'; yid+=1
                local.append((yard_id,chunk.baseline_visit_rate_week.mean()))
                yards.append([yard_id,store,len(chunk),float(chunk.baseline_visit_rate_week.mean()),float(ratio)])
                for uid in chunk.user_id: members.append([yard_id,uid])
                i+=size
            else:
                i+=1
        # unmatched remainder intentionally left out
    ydf=pd.DataFrame(yards,columns=['yard_id','store_id','member_count','mean_baseline_visits_week','max_min_frequency_ratio'])
    mdf=pd.DataFrame(members,columns=['yard_id','user_id'])
    # paired-ish assignment within store based on baseline
    assigns=[]
    for store,g in ydf.groupby('store_id'):
        gg=g.sort_values('mean_baseline_visits_week').reset_index(drop=True)
        for j in range(0,len(gg),2):
            pair=gg.iloc[j:j+2]
            if len(pair)==2:
                first_treat=bool(rng.integers(0,2))
                assigns.append([pair.iloc[0].yard_id,'test' if first_treat else 'control'])
                assigns.append([pair.iloc[1].yard_id,'control' if first_treat else 'test'])
            else:
                assigns.append([pair.iloc[0].yard_id,'test' if rng.random()<.5 else 'control'])
    adf=pd.DataFrame(assigns,columns=['yard_id','assignment'])
    if not ydf.empty: ydf=ydf.merge(adf,on='yard_id',how='left')
    return ydf,mdf


def simulate_weekly(users,yards,members,rng):
    n=len(users)
    assignment=pd.DataFrame({'user_id':users.user_id,'assignment':'not_in_experiment','yard_id':pd.Series([None]*n,dtype='object')})
    if len(members):
        assignment=assignment.set_index('user_id')
        mm=members.merge(yards[['yard_id','assignment']],on='yard_id',how='left')
        for r in mm.itertuples(index=False):
            assignment.loc[r.user_id,'assignment']=r.assignment; assignment.loc[r.user_id,'yard_id']=r.yard_id
        assignment=assignment.reset_index()
    assignment['assignment_ts']=pd.Timestamp('2026-07-01T09:00:00')
    assignment['treatment_start_ts']=TREAT_START
    u=users.merge(assignment,on='user_id',how='left')
    # potential response latent variables
    arche_eff={'shopper':.055,'runner':.035,'promo_hunter':.075,'family':.070,'sleeper':.10}
    user_eff=np.array([arche_eff[a] for a in u.archetype]) + .03*(u.digital_readiness.to_numpy()-.65)
    harm=rng.random(n)<.08
    user_eff=user_eff - harm*.06 + rng.normal(0,.018,n)
    user_eff=np.clip(user_eff,-.08,.16)
    optin_p=np.clip(.40+.35*u.digital_readiness.to_numpy()+.08*(u.archetype=='family').to_numpy()-.08*(u.archetype=='sleeper').to_numpy(),.15,.90)
    optin=rng.random(n)<optin_p
    # control/non-experiment have latent opt-in too, but no observed treatment
    rows=[]
    base_rate=u.baseline_visit_rate_week.to_numpy()
    for w in range(34):
        week_start=START+pd.Timedelta(weeks=w)
        seasonal=1.0 + 0.06*np.sin(2*np.pi*w/13) + (0.05 if w in (0,17,33) else 0)
        lam=np.clip(base_rate*seasonal,.01,None)
        y0=rng.poisson(lam)
        # treatment potential after week 26 only, extra/harm increments on common y0
        if w>=26:
            pos=np.clip(user_eff,0,None)*lam*optin
            neg=np.clip(-user_eff,0,None)*lam*optin
            plus=rng.poisson(pos)
            minus=rng.binomial(np.minimum(y0,1),np.clip(neg,0,.5))
            y1=np.maximum(0,y0+plus-minus)
        else:
            y1=y0.copy()
        is_test=(u.assignment.to_numpy()=='test')
        observed=np.where((w>=26)&is_test,y1,y0)
        for i,uid in enumerate(u.user_id):
            rows.append([uid,w,week_start,u.assignment.iloc[i],u.yard_id.iloc[i],int(y0[i]),int(y1[i]),int(observed[i]),float(user_eff[i]),int(optin[i])])
    weekly=pd.DataFrame(rows,columns=['user_id','week_index','week_start','assignment','yard_id','y0_visits','y1_visits','observed_visits','latent_effect_rate','latent_opt_in'])
    return assignment,weekly


def generate_receipts(users,weekly,rng,detailed_items=False):
    user_idx=users.set_index('user_id')
    recs=[]; items=[]; rid=1; iid=1
    for row in weekly.itertuples(index=False):
        cnt=row.observed_visits
        if cnt<=0: continue
        ur=user_idx.loc[row.user_id]
        for j in range(cnt):
            ts=pd.Timestamp(row.week_start)+pd.Timedelta(days=int(rng.integers(0,7)),hours=int(rng.integers(8,22)),minutes=int(rng.integers(0,60)))
            basket=float(ur.basket_base_rub*rng.lognormal(0,.28))
            basket=max(80,basket)
            # treatment may shift basket very slightly; keep effect primarily frequency-based
            if row.assignment=='test' and row.week_index>=26: basket*=rng.normal(1.01,.03)
            discount_rate=float(np.clip(ARCH_DISCOUNT[ur.archetype]+.10*ur.promo_sensitivity+rng.normal(0,.035),0,.38))
            paid=round(basket,2)
            regular=round(paid/(1-discount_rate),2)
            discount=round(regular-paid,2)
            ret=bool(rng.random()<.010)
            return_amt=paid if ret else 0.0
            net=round(paid-return_amt,2)
            margin_rate=float(np.clip(.20+rng.normal(0,.025),.10,.30))
            cm=round(net*margin_rate,2)
            receipt_id=f'R{rid:09d}'; rid+=1
            recs.append([receipt_id,row.user_id,ur.home_store_id,ts,row.week_index,row.assignment,paid,regular,discount,ret,return_amt,net,margin_rate,cm])
            if detailed_items:
                k=int(np.clip(rng.poisson(4)+1,1,10))
                shares=rng.dirichlet(np.ones(k))
                line_paid=np.round(shares*paid,2)
                # force exact paid total by adjusting last line
                line_paid[-1]=round(paid-float(line_paid[:-1].sum()),2)
                for lp in line_paid:
                    cat=rng.choice(CAT,p=CAT_P)
                    dr=float(np.clip(discount_rate+rng.normal(0,.03),0,.45))
                    reg=round(lp/(1-dr),2) if lp>0 else 0
                    sku=f'{cat[:3].upper()}_{int(rng.integers(1,51)):03d}'
                    items.append([f'I{iid:010d}',receipt_id,row.user_id,sku,cat,1,reg,round(float(lp),2),round(reg-float(lp),2),int(dr>.08)])
                    iid+=1
    receipts=pd.DataFrame(recs,columns=['receipt_id','user_id','store_id','ts','week_index','assignment','total_paid_rub','regular_total_rub','discount_total_rub','is_returned','return_amount_rub','net_sales_rub','contribution_margin_rate','contribution_margin_rub'])
    idf=pd.DataFrame(items,columns=['item_id','receipt_id','user_id','sku','category','qty','price_regular_rub','price_paid_rub','discount_rub','promo_flag']) if detailed_items else pd.DataFrame()
    return receipts,idf


def make_products(seed=9001):
    rng=np.random.default_rng(seed); rows=[]
    for cat in CAT:
        for i in range(1,51):
            rows.append([f'{cat[:3].upper()}_{i:03d}',cat,f'Brand_{int(rng.integers(1,21)):02d}',round(float(rng.uniform(40,900)),2)])
    return pd.DataFrame(rows,columns=['sku','category','brand','reference_price_rub'])


def make_challenges_rewards(users,yards,members,weekly,receipts,rng):
    if yards.empty or members.empty:
        empty=pd.DataFrame(); return empty,empty,empty,empty,empty,empty
    test_yards=set(yards.loc[yards.assignment=='test','yard_id'])
    mm=members[members.yard_id.isin(test_yards)].merge(users[['user_id','baseline_visit_rate_week','digital_readiness','fraud_persona_hidden']],on='user_id',how='left')
    # fraud feature score map used for precision-first action (no label in feature table exported later)
    candidates=[]; decisions=[]; events=[]; rewards=[]; ledger=[]; cycles=[]
    cid=1; eid=1; rewid=1; lid=1
    weekly_idx=weekly.set_index(['user_id','week_index'])
    for cycle in range(4):
        w0=26+2*cycle; w1=w0+1; cstart=START+pd.Timedelta(weeks=w0); cend=cstart+pd.Timedelta(weeks=2)
        cycle_members=[]
        for r in mm.itertuples(index=False):
            base2=max(1.0,2*r.baseline_visit_rate_week)
            uplift=float(np.clip(.30-.10*np.log1p(r.baseline_visit_rate_week),.15,.35))
            target=max(1,int(math.ceil(base2*(1+uplift))))
            chal=f'C{cid:08d}'; cid+=1
            candidates.append([chal,r.user_id,r.yard_id,cycle,cstart,cend,'visit_frequency',target,uplift,'ASSUMPTION'])
            accept_p=np.clip(.35+.45*r.digital_readiness,.15,.85)
            accepted=bool(rng.random()<accept_p)
            decisions.append([chal,r.user_id,pd.Timestamp(cstart)+pd.Timedelta(hours=1),int(accepted),'rule_based_v1','digital_readiness + reachability'])
            obs0=int(weekly_idx.loc[(r.user_id,w0),'observed_visits']); obs1=int(weekly_idx.loc[(r.user_id,w1),'observed_visits']); prog=obs0+obs1
            if accepted:
                events.append([f'CE{eid:09d}',chal,r.user_id,cstart,'shown',0]); eid+=1
                events.append([f'CE{eid:09d}',chal,r.user_id,cstart+pd.Timedelta(days=7),'progress',obs0]); eid+=1
                events.append([f'CE{eid:09d}',chal,r.user_id,cend-pd.Timedelta(minutes=1),'completed' if prog>=target else 'expired',prog]); eid+=1
            complete=accepted and prog>=target
            cycle_members.append((r.user_id,r.yard_id,target,prog,complete,r.fraud_persona_hidden))
            if complete:
                amount=round(80*(1+min(.20,max(0,(prog-target)/max(target,1))*.10)),2)
                funded='brand:synthetic' if rng.random()<.30 else 'x5'
                reward_id=f'RW{rewid:08d}'; rewid+=1
                issue_ts=cend
                # approximate fraud score; ground truth isn't an input column to exported policy features
                risky=(r.fraud_persona_hidden!='none' and rng.random()<.78)
                status='reversed' if risky else ('pending' if issue_ts+pd.Timedelta(days=7)>END else 'final')
                rewards.append([reward_id,r.user_id,chal,r.yard_id,amount,funded,issue_ts,status])
                ledger.append([f'L{lid:09d}',reward_id,r.user_id,issue_ts,'issue_pending',amount,'pending']); lid+=1
                if status=='reversed':
                    ledger.append([f'L{lid:09d}',reward_id,r.user_id,issue_ts+pd.Timedelta(days=2),'reverse',-amount,'reversed']); lid+=1
                elif status=='final':
                    ledger.append([f'L{lid:09d}',reward_id,r.user_id,issue_ts+pd.Timedelta(days=7),'settle_final',0.0,'final']); lid+=1
        # yard cycle state
        if cycle_members:
            tmp=pd.DataFrame(cycle_members,columns=['user_id','yard_id','target','progress','complete','fraud_persona_hidden'])
            for y,g in tmp.groupby('yard_id'):
                goal=int(g.target.sum()); actual=int(g.progress.sum())
                deficits=np.maximum(g.target.to_numpy()-g.progress.to_numpy(),0).sum()
                surplus=np.maximum(g.progress.to_numpy()-g.target.to_numpy(),0).sum()
                effective=actual + int(round(.70*min(surplus,deficits)))
                cycles.append([y,cycle,cstart,cend,goal,actual,int(deficits),int(surplus),.70,int(effective>=goal)])
    return (pd.DataFrame(candidates,columns=['challenge_id','user_id','yard_id','cycle','start_ts','end_ts','challenge_type','target_visits','target_uplift','evidence_status']),
            pd.DataFrame(decisions,columns=['challenge_id','user_id','decision_ts','accepted','policy_version','explanation']),
            pd.DataFrame(events,columns=['challenge_event_id','challenge_id','user_id','event_ts','event_type','progress_visits']),
            pd.DataFrame(rewards,columns=['reward_id','user_id','challenge_id','yard_id','amount_rub_equivalent','funded_by','issued_ts','final_status']),
            pd.DataFrame(ledger,columns=['ledger_id','reward_id','user_id','event_ts','event_type','amount_delta_rub','status_after']),
            pd.DataFrame(cycles,columns=['yard_id','cycle','start_ts','end_ts','goal_visits','actual_visits','total_deficit','total_surplus','backup_coef','completed']))


def make_referrals_fraud(users,yards,members,rng):
    member_map=members.set_index('user_id').yard_id.to_dict() if not members.empty else {}
    userids=users.user_id.to_numpy(); n=len(users)
    ref=[]; refid=1
    # benign referrals among members/app users
    candidates=users[users.app_user.eq(1)].user_id.to_numpy()
    for uid in candidates:
        if rng.random()<.055:
            k=int(rng.integers(1,3))
            for _ in range(k):
                invitee=str(rng.choice(userids))
                if invitee==uid: continue
                ts=TREAT_START+pd.Timedelta(days=int(rng.integers(0,50)),hours=int(rng.integers(8,22)))
                qual=bool(rng.random()<.35)
                qts=ts+pd.Timedelta(days=int(rng.integers(3,16))) if qual else pd.NaT
                ref.append([f'REF{refid:08d}',uid,invitee,member_map.get(uid),ts,qts,'qualified' if qual else 'invited']); refid+=1
    # fraud patterns using latent personas
    fraud_users=users[users.fraud_persona_hidden.ne('none')]
    for r in fraud_users.itertuples(index=False):
        if r.fraud_persona_hidden=='star':
            k=15
        elif r.fraud_persona_hidden=='ring': k=5
        else: k=3
        for j in range(k):
            invitee=str(rng.choice(userids));
            if invitee==r.user_id: continue
            ts=TREAT_START+pd.Timedelta(days=int(rng.integers(0,12)),hours=int(rng.integers(0,24)))
            qual=(r.fraud_persona_hidden=='account_cycling' and j==0)
            qts=ts+pd.Timedelta(days=1) if qual else pd.NaT
            ref.append([f'REF{refid:08d}',r.user_id,invitee,member_map.get(r.user_id),ts,qts,'qualified' if qual else 'invited']); refid+=1
    referrals=pd.DataFrame(ref,columns=['referral_event_id','inviter_user_id','invitee_user_id','yard_id','created_ts','qualified_ts','status'])
    # features, deliberately exclude ground truth
    feat=[]
    counts=referrals.groupby('inviter_user_id').size().to_dict() if not referrals.empty else {}
    qualrate=(referrals.assign(q=referrals.status.eq('qualified')).groupby('inviter_user_id').q.mean().to_dict() if not referrals.empty else {})
    for r in users.itertuples(index=False):
        c=counts.get(r.user_id,0); qr=qualrate.get(r.user_id,0)
        velocity=min(1,c/15)
        empty_rate=np.clip(1-qr+rng.normal(0,.08),0,1) if c else 0
        mutual=np.clip(rng.beta(1,15)+(0.45 if r.fraud_persona_hidden=='ring' else 0),0,1)
        clone=np.clip(rng.beta(1,20)+(0.65 if r.fraud_persona_hidden=='clone_receipts' else 0),0,1)
        score=float(np.clip(.35*velocity+.25*empty_rate+.20*mutual+.20*clone,0,1))
        reasons=[]
        if velocity>.65: reasons.append('high_invite_velocity')
        if empty_rate>.75: reasons.append('low_qualified_share')
        if mutual>.35: reasons.append('mutual_edges')
        if clone>.35: reasons.append('receipt_similarity')
        feat.append([r.user_id,c,round(velocity,4),round(empty_rate,4),round(mutual,4),round(clone,4),round(score,4),'|'.join(reasons)])
    features=pd.DataFrame(feat,columns=['user_id','invite_count','invite_velocity_2w','empty_invitee_rate','mutual_edge_density','receipt_similarity','fraud_score','reason_codes'])
    # ground truth cases, including benign difficult negatives
    gt=[]; gid=1
    for r in users[users.fraud_persona_hidden.ne('none')].itertuples(index=False):
        gt.append([f'F{gid:07d}',r.user_id,r.fraud_persona_hidden,1,TREAT_START+pd.Timedelta(days=int(rng.integers(0,50)))]); gid+=1
    benign=users[users.fraud_persona_hidden.eq('none')].sample(n=min(max(10,len(users)//50),len(users)),random_state=123)
    for r in benign.itertuples(index=False):
        gt.append([f'F{gid:07d}',r.user_id,'benign_edge_case',0,TREAT_START+pd.Timedelta(days=int(rng.integers(0,50)))]); gid+=1
    ground=pd.DataFrame(gt,columns=['fraud_event_id','user_id','scenario_type','is_fraud_ground_truth','event_ts'])
    return referrals,features,ground


def summarize(n, users, yards, members, assignment, weekly, receipts, rewards, ledger, yard_cycles, fraud_features, fraud_gt):
    exp=assignment[assignment.assignment.isin(['test','control'])]
    post=weekly[(weekly.week_index>=26)&weekly.user_id.isin(exp.user_id)]
    userpost=post.groupby(['user_id','assignment'],as_index=False).observed_visits.sum()
    means=userpost.groupby('assignment').observed_visits.mean().to_dict()
    test=means.get('test',np.nan); ctrl=means.get('control',np.nan)
    uplift=(test-ctrl)/ctrl if ctrl and not np.isnan(ctrl) else np.nan
    true=post.assign(delta=post.y1_visits-post.y0_visits).groupby('user_id').delta.sum().mean() if len(post) else np.nan
    rpost=receipts[receipts.week_index>=26]
    per=rpost.groupby('user_id').agg(cm=('contribution_margin_rub','sum'),sales=('net_sales_rub','sum')).reindex(exp.user_id).fillna(0).reset_index().merge(exp[['user_id','assignment']],on='user_id')
    cmmeans=per.groupby('assignment').cm.mean().to_dict(); inc_cm=cmmeans.get('test',0)-cmmeans.get('control',0)
    if rewards.empty: reward_x5=0; reward_all=0
    else:
        active=rewards[rewards.final_status!='reversed']
        reward_all=active.amount_rub_equivalent.sum()
        reward_x5=active.loc[active.funded_by.eq('x5'),'amount_rub_equivalent'].sum()
    tcount=max((exp.assignment=='test').sum(),1)
    net_inc_cm_per_test=inc_cm-reward_x5/tcount
    # fraud precision @ .65
    gtmap=fraud_gt.groupby('user_id').is_fraud_ground_truth.max().to_dict() if not fraud_gt.empty else {}
    pred=fraud_features.fraud_score>=.65
    actual=fraud_features.user_id.map(gtmap).fillna(0).astype(int).eq(1)
    tp=int((pred&actual).sum()); fp=int((pred&~actual).sum()); fn=int((~pred&actual).sum())
    precision=tp/max(tp+fp,1); recall=tp/max(tp+fn,1)
    return {
        'n_users':n,'n_app_users':int(users.app_user.sum()),'n_experiment_users':int(len(exp)),'n_yards':int(len(yards)),
        'test_users':int((exp.assignment=='test').sum()),'control_users':int((exp.assignment=='control').sum()),
        'post_visits_per_user_test':test,'post_visits_per_user_control':ctrl,'observed_frequency_uplift_relative':uplift,
        'mean_true_incremental_visits_8w':true,'incremental_contribution_margin_per_user_rub':inc_cm,
        'x5_reward_cost_total_rub':float(reward_x5),'all_reward_cost_total_rub':float(reward_all),'net_incremental_cm_per_test_user_rub':float(net_inc_cm_per_test),
        'yard_cycle_completion_rate':float(yard_cycles.completed.mean()) if not yard_cycles.empty else np.nan,
        'fraud_precision_at_0_65':precision,'fraud_recall_at_0_65':recall,'receipt_count':int(len(receipts))
    }


def run_reference(n,seed,detailed_items):
    out=OUT/f'data/reference_{n}'
    out.mkdir(parents=True,exist_ok=True)
    users,households,stores,rng=make_population(n,seed)
    yards,members=form_yards(users,rng)
    assignment,weekly=simulate_weekly(users,yards,members,rng)
    receipts,items=generate_receipts(users,weekly,rng,detailed_items=detailed_items)
    challenges,decisions,cevents,rewards,ledger,ycycles=make_challenges_rewards(users,yards,members,weekly,receipts,rng)
    referrals,ff,fg=make_referrals_fraud(users,yards,members,rng)
    # hide ground truth persona in ordinary users export; put it separately
    user_export=users.drop(columns=['fraud_persona_hidden'])
    fraud_personas=users[['user_id','fraud_persona_hidden']].rename(columns={'fraud_persona_hidden':'fraud_persona_ground_truth'})
    tables={
        'users.csv':user_export,'households.csv':households,'stores.csv':stores,'experiment_assignments.csv':assignment,
        'yards.csv':yards,'memberships.csv':members,'weekly_outcomes.csv':weekly,'receipts.csv':receipts,
        'challenge_candidates.csv':challenges,'challenge_decisions.csv':decisions,'challenge_events.csv':cevents,
        'rewards.csv':rewards,'reward_ledger.csv':ledger,'yard_cycles.csv':ycycles,'referral_events.csv':referrals,
        'fraud_features.csv':ff,'fraud_events_ground_truth.csv':fg,'fraud_personas_ground_truth.csv':fraud_personas
    }
    if detailed_items: tables['items.csv']=items
    for name,df in tables.items(): write_csv(df,out/name)
    # catalog only once per ref folder for self-containment
    write_csv(make_products(),out/'products.csv')
    # summary
    summary=summarize(n,users,yards,members,assignment,weekly,receipts,rewards,ledger,ycycles,ff,fg)
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    return summary, tables

summaries=[]; validation=[]
for n,seed,ditems in [(1000,260903,True),(10000,260904,False)]:
    summary,tables=run_reference(n,seed,ditems); summaries.append(summary)
    # validation by re-reading local dfs
    users=tables['users.csv']; households=tables['households.csv']; stores=tables['stores.csv']; assignment=tables['experiment_assignments.csv']; weekly=tables['weekly_outcomes.csv']; receipts=tables['receipts.csv']; ledger=tables['reward_ledger.csv']; rewards=tables['rewards.csv']; ff=tables['fraud_features.csv']
    def add(check,passed,detail): validation.append([n,check,bool(passed),detail])
    add('unique_user_id',users.user_id.is_unique,f'{users.user_id.nunique()}/{len(users)} unique')
    add('age_quota_sum',len(users)==n,f'n={len(users)}')
    target=dict(zip(AGE_BANDS,largest_remainder_counts(n,AGE_P)))
    actual=users.age_band.value_counts().to_dict(); add('age_quota_exact',all(actual.get(a,0)==target[a] for a in AGE_BANDS),str(actual))
    add('assignment_precedes_treatment',(pd.to_datetime(assignment.assignment_ts)<pd.to_datetime(assignment.treatment_start_ts)).all(),'assignment_ts < treatment_start_ts')
    add('no_fraud_label_in_features','is_fraud_ground_truth' not in ff.columns and 'fraud_persona' not in '|'.join(ff.columns),'fraud policy features exclude ground-truth labels')
    add('receipt_user_fk',receipts.user_id.isin(users.user_id).all(),'all receipt user_ids present')
    add('receipt_store_fk',receipts.store_id.isin(stores.store_id).all(),'all store_ids present')
    if ditems:
        items=tables['items.csv']
        recon=items.groupby('receipt_id').price_paid_rub.sum().round(2)
        r=receipts.set_index('receipt_id').total_paid_rub.round(2)
        diff=(recon-r.reindex(recon.index)).abs().max()
        add('items_to_receipts_reconcile',diff<=0.02,f'max_abs_diff={diff}')
    if len(rewards):
        net=ledger.groupby('reward_id').amount_delta_rub.sum().round(2)
        exp=rewards.set_index('reward_id').apply(lambda r: 0.0 if r.final_status=='reversed' else r.amount_rub_equivalent,axis=1).round(2)
        diff=(net-exp.reindex(net.index)).abs().max()
        add('reward_ledger_reconcile',diff<=0.01,f'max_abs_diff={diff}')
    else: add('reward_ledger_reconcile',True,'no rewards')
    # A/A pseudo-null on y0 among experiment users, deterministic split by hash parity
    expuids=set(assignment.loc[assignment.assignment.isin(['test','control']),'user_id'])
    aa=weekly[(weekly.week_index>=26)&weekly.user_id.isin(expuids)].groupby('user_id').y0_visits.sum().reset_index()
    aa['grp']=aa.user_id.str.extract(r'(\d+)').astype(int)[0]%2
    aam=aa.groupby('grp').y0_visits.mean(); aadiff=float(aam.get(1,0)-aam.get(0,0))
    add('aa_null_reasonable',abs(aadiff)<0.8,f'8w mean diff={aadiff:.4f} visits')

write_csv(pd.DataFrame(summaries),OUT/'results/reference_metrics.csv')
write_csv(pd.DataFrame(validation,columns=['n_users','check','passed','detail']),OUT/'results/validation_checks.csv')

# ---------- Monte Carlo metrics only ----------
def mc_one(n,seed):
    rng=np.random.default_rng(seed)
    rate=np.clip(rng.lognormal(np.log(1.8),.55,n),.05,8)
    groups=np.arange(n)//5
    ug=np.unique(groups); treatg=set(rng.choice(ug,size=len(ug)//2,replace=False))
    treat=np.array([g in treatg for g in groups])
    y0=rng.poisson(rate*8)
    eff=np.clip(rng.normal(.06,.035,n),-.04,.16)
    y1=y0+rng.poisson(np.clip(rate*8*eff,0,None))-rng.binomial(np.minimum(y0,1),np.clip(-eff,0,.5))
    obs=np.where(treat,y1,y0)
    mt=obs[treat].mean(); mc=obs[~treat].mean(); est=mt-mc
    true=(y1-y0)[treat].mean()
    return [n,seed,mt,mc,est,true,est-true]
mc=[]
for n in [1000,10000]:
    for rep in range(45): mc.append(mc_one(n,880000+n+rep))
mcdf=pd.DataFrame(mc,columns=['n_users','seed','mean_visits_test_8w','mean_visits_control_8w','estimated_itt_visits','true_att_visits','estimation_error_visits'])
write_csv(mcdf,OUT/'results/monte_carlo_45x2.csv')
mcsummary=mcdf.groupby('n_users').agg(reps=('seed','count'),mean_est=('estimated_itt_visits','mean'),sd_est=('estimated_itt_visits','std'),p025=('estimated_itt_visits',lambda s:s.quantile(.025)),p975=('estimated_itt_visits',lambda s:s.quantile(.975)),rmse=('estimation_error_visits',lambda s:float(np.sqrt(np.mean(s**2))))).reset_index()
write_csv(mcsummary,OUT/'results/monte_carlo_summary.csv')

# ---------- 17 one-factor sensitivity runs ----------
base={'causal_uplift':.06,'reward_rub':80,'margin_rate':.20,'cannibalization':.15}
runs=[('base','base',None)]
vals={
 'causal_uplift':[-.02,0,.03,.08],
 'reward_rub':[40,60,100,140],
 'margin_rate':[.12,.16,.24,.28],
 'cannibalization':[0,.10,.30,.50]
}
for p,vs in vals.items():
    for v in vs: runs.append((p,f'{p}={v}',v))
rows=[]
# deterministic economic translation for comparison only
baseline_visits_8w=14.4; basket=760; completion=.48
for p,label,v in runs:
    cfg=base.copy()
    if p!='base': cfg[p]=v
    incremental_visits=baseline_visits_8w*cfg['causal_uplift']*(1-cfg['cannibalization'])
    inc_cm=incremental_visits*basket*cfg['margin_rate']
    reward_cost=completion*cfg['reward_rub']
    net=inc_cm-reward_cost
    rows.append([label,cfg['causal_uplift'],cfg['reward_rub'],cfg['margin_rate'],cfg['cannibalization'],incremental_visits,inc_cm,reward_cost,net])
sens=pd.DataFrame(rows,columns=['run','causal_uplift','reward_rub','margin_rate','cannibalization','incremental_visits_8w_per_user','incremental_cm_rub_per_user','reward_cost_rub_per_user','net_incremental_cm_rub_per_user'])
write_csv(sens,OUT/'results/sensitivity_17_runs.csv')

# ---------- charts ----------
try:
    import matplotlib.pyplot as plt
    figdir=OUT/'figures'; figdir.mkdir(exist_ok=True)
    s1000=pd.read_csv(OUT/'data/reference_1000/users.csv')
    order=AGE_BANDS; vc=s1000.age_band.value_counts().reindex(order)
    plt.figure(figsize=(8,4.8)); plt.bar(order,vc.values); plt.title('Synthetic age quotas — n=1,000'); plt.ylabel('Users'); plt.xlabel('Age band'); plt.tight_layout(); plt.savefig(figdir/'age_quota_1000.png',dpi=150); plt.close()
    d=mcdf[mcdf.n_users==10000].estimated_itt_visits
    plt.figure(figsize=(8,4.8)); plt.hist(d,bins=12); plt.title('Monte Carlo estimated ITT — n=10,000'); plt.xlabel('Incremental visits per user over 8 weeks'); plt.ylabel('Replications'); plt.tight_layout(); plt.savefig(figdir/'mc_itt_n10000.png',dpi=150); plt.close()
    plt.figure(figsize=(8,4.8)); plt.plot(range(len(sens)),sens.net_incremental_cm_rub_per_user,marker='o'); plt.axhline(0); plt.title('One-factor sensitivity: net incremental CM'); plt.xlabel('Sensitivity run index'); plt.ylabel('RUB per user'); plt.tight_layout(); plt.savefig(figdir/'sensitivity_net_cm.png',dpi=150); plt.close()
except Exception as e:
    (OUT/'figures_error.txt').write_text(str(e),encoding='utf-8')

# ---------- README / schema notes ----------
readme=f'''# X5 synthetic loyalty simulation — all data package

Generated: {datetime.now(timezone.utc).isoformat()}

This archive is a reproducible **synthetic scenario-analysis package**, not a forecast or evidence of real X5 uplift.
The source prompt explicitly separates official demographic priors, public digital proxies, app-selection assumptions, behavioral DGP, latent causal effect, and observed experiment estimates.

## Contents

- `source/` — original self-contained Markdown plus extracted embedded source documents/CSVs.
- `config/` — source ledger and 6 scenario configs.
- `data/reference_1000/` — full reference data for 1,000 users, including receipt items.
- `data/reference_10000/` — reference data for 10,000 users; receipt-level detail included, item-level intentionally omitted to keep the archive practical.
- `results/` — reference metrics, validation checks, 45x2 Monte Carlo metrics, 17 one-factor sensitivity runs.
- `figures/` — diagnostic plots.
- `code/` — exact generator script used to build this package.
- `MANIFEST.csv` — path, size, SHA-256 for every file in the package.

## Key modeling conventions

- 26 pre-treatment weeks + 8 experiment weeks.
- Demographic age quotas use the supplied 18+ Rosstat-derived weights.
- X5 loyalty/app penetration, basket, frequency, margin, reward economics, treatment effect and fraud prevalence are assumptions/latent scenario inputs.
- Candidate Yards are store-based groups of 3–7, only where the active pool is at least 20, with frequency ratio <=2.5.
- Assignment occurs before treatment. Yard members receive cluster test/control assignment.
- `weekly_outcomes.csv` contains `y0_visits`, `y1_visits` and observed visits, so the true synthetic causal effect is explicit.
- Fraud ground truth is stored separately from observable fraud features.
- Reward ledger uses pending/final/reversed state transitions and signed deltas.

## Important limitation

The 10,000-user dataset includes all modeled entities at receipt level, but not line-item rows. The 1,000-user run includes line items and can be used for item-to-receipt reconciliation and demos. This follows the practical proof-of-concept boundary rather than claiming a production-scale synthetic transaction lake.
'''
(OUT/'README.md').write_text(readme,encoding='utf-8')
(OUT/'code').mkdir(exist_ok=True)
shutil.copy2(BASE/'build_x5_package.py',OUT/'code/build_x5_package.py')

# data dictionary from selected files
schemas=[]
for n in [1000,10000]:
    folder=OUT/f'data/reference_{n}'
    for f in folder.glob('*.csv'):
        try:
            df=pd.read_csv(f,nrows=5)
            for c in df.columns: schemas.append([n,f.name,c,str(df[c].dtype)])
        except Exception: pass
write_csv(pd.DataFrame(schemas,columns=['n_users','table','column','sample_inferred_dtype']),OUT/'DATA_DICTIONARY.csv')

# ---------- manifest and zip ----------
manifest=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file():
        manifest.append([str(p.relative_to(OUT)),p.stat().st_size,sha256(p)])
write_csv(pd.DataFrame(manifest,columns=['path','bytes','sha256']),OUT/'MANIFEST.csv')
# regenerate manifest including itself (hash blank for manifest to avoid recursive hash issue)
manifest=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file():
        manifest.append([str(p.relative_to(OUT)),p.stat().st_size,'' if p.name=='MANIFEST.csv' else sha256(p)])
write_csv(pd.DataFrame(manifest,columns=['path','bytes','sha256']),OUT/'MANIFEST.csv')

if ZIP.exists(): ZIP.unlink()
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file(): z.write(p,p.relative_to(OUT.parent))

# integrity test
with zipfile.ZipFile(ZIP,'r') as z:
    bad=z.testzip(); names=z.namelist()
print(json.dumps({'zip':str(ZIP),'zip_bytes':ZIP.stat().st_size,'files_in_zip':len(names),'bad_member':bad,'package_dir':str(OUT),'reference_summaries':summaries},ensure_ascii=False,indent=2,default=str))
