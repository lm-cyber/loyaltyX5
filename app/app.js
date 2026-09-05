import { CHAINS, PROFILES, ECON, SIMULATION, REFERRAL } from './data.js';
import { LOGOS } from './logos.js';
import {
  recommend, copyFor, fmt, referralEconomics, scoreFraud,
  FRAUD_THRESHOLDS, HOT_CHANCE,
} from './engine.js';

/* ================= состояние ================= */
const state = {
  chainId: 'ts5',
  profileId: 'P5_ROUTINE',
  tab: 'home',
  receipts: [],          // журнал начислений
  claimed: false,
};

const el = s => document.querySelector(s);
/* Склонение существительных после числительного */
const plural = (n, one, few, many) => {
  const a = Math.abs(n) % 100, b = a % 10;
  if (a > 10 && a < 20) return many;
  if (b > 1 && b < 5) return few;
  if (b === 1) return one;
  return many;
};

const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;' }[c]));

function profile() { return PROFILES.find(p => p.id === state.profileId); }
function chain()   { return CHAINS[state.chainId]; }

/* Профиль привязан к своей сети: переключение сети меняет профиль
   на подходящий, чтобы демонстрация оставалась осмысленной. */
function profilesFor(chainId) { return PROFILES.filter(p => p.chain === chainId); }

/* ================= селекторы ================= */
function renderPickers() {
  el('#chainPick').innerHTML = Object.values(CHAINS).map(c => `
    <button class="pick" data-chain="${c.id}" aria-pressed="${c.id === state.chainId}">
      <span class="dot" style="background:${c.primary}"></span>${esc(c.name)}
    </button>`).join('');

  el('#profPick').innerHTML = profilesFor(state.chainId).map(p => `
    <button class="pick" data-prof="${p.id}" aria-pressed="${p.id === state.profileId}">
      <span class="em">${p.avatarEmoji}</span>${esc(p.name)} <i>${esc(p.label)}</i>
    </button>`).join('');

  el('#chainPick').onclick = e => {
    const b = e.target.closest('[data-chain]'); if (!b) return;
    state.chainId = b.dataset.chain;
    const list = profilesFor(state.chainId);
    if (!list.some(p => p.id === state.profileId)) state.profileId = list[0].id;
    reset(); render();
  };
  el('#profPick').onclick = e => {
    const b = e.target.closest('[data-prof]'); if (!b) return;
    state.profileId = b.dataset.prof;
    reset(); render();
  };
}
function reset() { state.tab = 'home'; state.receipts = []; state.claimed = false; }

/* ================= скин телефона ================= */
function applySkin() {
  const c = chain();
  const dark = c.id === 'tsch';   // у Чижика жёлтый фон, тёмный текст
  el('#screen').style.cssText = `
    --sk-primary:${c.primary};
    --sk-primary-ink:${c.id === 'tsch' ? '#8A7500' : c.primary};
    --sk-on:${c.onPrimary};
    --sk-surface:${c.surface};
    --sk-card:${c.card};
    --sk-ink:${c.ink};
    --sk-muted:${dark ? '#6E6650' : '#6B7A73'};
    --sk-line:${dark ? '#EDE3B8' : '#E3EBE5'};
    --sk-soft:${dark ? '#FFF7D6' : c.surface};
  `;
}

/* ================= шапка приложения ================= */
function renderAppbar() {
  const c = chain(), p = profile();
  el('#appbar').innerHTML = `
    <div>
      <div class="applogo"><img src="${LOGOS[c.id]}" alt="${esc(c.name)}"></div>
      <div class="appsub">X5 Клуб · ${esc(c.tag)}</div>
    </div>
    <div class="balance"><b>${(p.stats.saved).toLocaleString('ru-RU')}</b><span>баллов</span></div>`;
}

/* ================= экраны ================= */
function renderHome(rec) {
  const c = chain(), p = profile();

  if (rec.noOffer) {
    return `
      <div class="hero">
        <div class="kicker">★ Постоянный покупатель</div>
        <h2>Вы в числе своих</h2>
        <p>Заданий на этой неделе нет — вы и так с нами. Держите повышенный кешбэк, он действует без всяких условий.</p>
      </div>
      <div class="card">
        <h3><span class="ic">✦</span>Ваши постоянные привилегии</h3>
        <div class="perk">
          <span class="emo">%</span>
          <div><b>Повышенный кешбэк на любимые категории</b><span>действует всегда, ничего выполнять не нужно</span></div>
        </div>
        <div class="perk">
          <span class="emo">⚡</span>
          <div><b>Ранний доступ к акциям</b><span>за день до всех остальных</span></div>
        </div>
        <div class="perk">
          <span class="emo">🎂</span>
          <div><b>Подарок в день рождения</b><span>выберете сами из подборки</span></div>
        </div>
      </div>
      <div class="card">
        <h3><span class="ic">◷</span>Что дальше</h3>
        <div class="muted">Новые задания появляются, когда мы находим для вас что-то действительно выгодное. Хотите получать их чаще — включите уведомления.</div>
        <button class="btn ghost" style="margin-top:11px">Включить уведомления</button>
      </div>
      <div class="card">
        <h3><span class="ic">🌱</span>Ваш прогресс</h3>
        ${avatarBlock(p)}
      </div>`;
  }

  const w = rec.winner;
  const copy = copyFor(w.key, c.id);
  let body = '';

  if (w.key === 'challenge') {
    const goal = copy.goal, done = Math.min(p.stats.streak, goal);
    body = `
      <div class="card">
        <h3><span class="ic">🎯</span>${esc(copy.title)}</h3>
        <div class="steps">
          ${Array.from({ length: goal }, (_, i) => {
            const st = i < done ? 'done' : i === done ? 'now' : '';
            return `<div class="step ${st}">${i < done ? '✓' : i + 1}</div>`;
          }).join('')}
        </div>
        <div style="font-size:12px;color:var(--sk-muted);line-height:1.45">${esc(copy.body)}</div>
        <div class="prize">
          <span class="emo">🎁</span>
          <div><b>${w.cand.reward} баллов на счёт</b><span>придут после ${goal}-й покупки</span></div>
        </div>
      </div>`;
  }

  if (w.key === 'hotchance') {
    const it = w.extra.hotItem;
    body = `
      <div class="card">
        <h3><span class="ic">🎁</span>${esc(copy.title)}</h3>
        <div style="font-size:12px;color:var(--sk-muted);line-height:1.45">${esc(copy.body)}</div>
        <div class="prize">
          <span class="emo">${it.emoji}</span>
          <div>
            <b>${esc(it.name)}</b>
            <span>${it.price} ₽ · осталось ${it.stock} шт</span>
            <div class="timer">⏱ забрать в течение ${it.hoursLeft} ч</div>
          </div>
        </div>
        <div class="fairnote">
          <span>ℹ️</span>
          <div>Выигрывает примерно <b>каждый ${Math.round(1 / HOT_CHANCE.pWin)}-й</b> — шанс честный и не меняется. Участие бесплатное. И без подарка вы не останетесь: не достанется этот — начислим баллы.</div>
        </div>
      </div>`;
  }

  if (w.key === 'stm') {
    const s = w.extra.swap, se = w.extra.swapEcon;
    body = `
      <div class="card">
        <h3><span class="ic">💚</span>${esc(copy.title)}</h3>
        <div style="font-size:12px;color:var(--sk-muted);line-height:1.45;margin-bottom:10px">${esc(copy.body)}</div>
        <div class="swap">
          <div class="swapbox">
            <div class="lbl">обычно берёте</div>
            <div class="nm">${esc(s.from)}</div>
            <div class="pr">${s.fromPrice} ₽</div>
          </div>
          <div class="swaparrow">→</div>
          <div class="swapbox">
            <div class="lbl">советуем</div>
            <div class="nm">${esc(s.to)}</div>
            <div class="pr">${s.toPrice} ₽</div>
          </div>
        </div>
        <div class="saveline">
          <b>−${se.savingRubles} ₽</b>
          <span>сэкономите на этой покупке</span>
        </div>
        <div class="fairnote">
          <span>📏</span>
          <div>Считаем честно — по цене за грамм, а не за упаковку. Так разница видна, даже если упаковки разного размера.</div>
        </div>
      </div>`;
  }

  if (w.key === 'league') {
    body = leagueCard(p, copy);
  }

  return `
    <div class="hero">
      <div class="kicker">${w.mechanic.icon} ${esc(w.mechanic.name)}</div>
      <h2>${esc(copy.title)}</h2>
      <p>${esc(copy.body)}</p>
    </div>
    ${body}
    <button class="why" id="whyBtn">
      <span>💡</span><div>Почему мне это предложили? <b>Показать разбор →</b></div>
    </button>
    <div class="card">
      <h3><span class="ic">🌱</span>Ваш прогресс</h3>
      ${avatarBlock(p)}
    </div>`;
}

function avatarBlock(p) {
  return `
    <div class="avatar">
      <div class="avaring">${p.avatarEmoji}</div>
      <div class="avameta" style="flex:1">
        <b>${esc(p.name)} · уровень ${p.stats.level}</b>
        <span>${p.stats.streak} недель подряд · сэкономлено ${p.stats.saved.toLocaleString('ru-RU')} ₽</span>
        <div class="xpbar"><i style="width:${p.stats.xp}%"></i></div>
      </div>
    </div>`;
}

function leagueCard(p, copy) {
  const L = p.league;
  const names = ['А. Морозова','Д. Ким','Н. Соколов','Вы','Р. Гаджиев','Л. Пак','И. Титова'];
  const start = Math.max(1, L.place - 3);
  const rows = names.map((n, i) => {
    const place = start + i;
    const me = place === L.place;
    const score = Math.round(L.score + (L.place - place) * 26);
    return `<div class="lgrow ${me ? 'me' : ''}">
      <span class="pl">${place}</span>
      <span class="nm">${me ? 'Вы' : esc(n)}</span>
      <span class="sc">${score}</span>
    </div>`;
  }).join('');

  return `
    <div class="card">
      <h3><span class="ic">🏆</span>${esc(copy.title)}</h3>
      <div style="font-size:12px;color:var(--sk-muted);line-height:1.45;margin-bottom:10px">${esc(copy.body)}</div>
      ${rows}
      <div class="fairnote">
        <span>⚖️</span>
        <div>Здесь соревнуются те, кто ходит в магазин примерно как вы. Очки — за ваш собственный прогресс, а не за размер чека, поэтому большая корзина не даёт преимущества.</div>
      </div>
      <div class="prize">
        <span class="emo">🥇</span>
        <div><b>${L.nextPlace - L.score} очков до ${L.place - 1}-го места</b><span>призы получают лучшие в группе</span></div>
      </div>
    </div>`;
}

function renderReferral() {
  const p = profile(), r = referralEconomics(p);
  return `
    <div class="hero">
      <div class="kicker">🤝 Приглашения</div>
      <h2>Зовите друзей</h2>
      <p>Вам ${r.rewardInviter} баллов, другу ${r.rewardInvitee} приветственных. Начислим после его первой покупки.</p>
    </div>
    <div class="card">
      <h3><span class="ic">📊</span>Ваши приглашения</h3>
      <div class="refrow">
        <div class="refstat"><b>${r.qualified}</b><span>уже с нами</span></div>
        <div class="refstat"><b>${r.pending}</b><span>скоро придут</span></div>
        <div class="refstat"><b>${r.earned}</b><span>баллов получено</span></div>
      </div>
      <div class="reflink"><b>ДВОР-${p.id.slice(0, 4)}${p.stats.level}${p.stats.streak}</b><span>скопировать</span></div>
      <button class="btn">Поделиться приглашением</button>
      <div class="fairnote">
        <span>🛡️</span>
        <div>Баллы придут, когда друг сделает первую покупку — у него есть на это ${r.qualifyWindowDays} дней. В этом месяце можно пригласить ещё ${r.remaining} ${plural(r.remaining, 'человека', 'человек', 'человек')}.</div>
      </div>
    </div>
    <div class="card">
      <h3><span class="ic">🎁</span>Что получит друг</h3>
      <div class="prize">
        <span class="emo">💚</span>
        <div><b>${r.rewardInvitee} приветственных баллов</b><span>на первую покупку от ${r.qualifyMinCheck} ₽</span></div>
      </div>
    </div>`;
}

function renderWallet() {
  const p = profile();
  const log = state.receipts;
  return `
    <div class="hero">
      <div class="kicker">🧾 Кошелёк</div>
      <h2>${p.stats.saved.toLocaleString('ru-RU')} баллов</h2>
      <p>1 балл = 10 копеек. Можно оплатить ими часть покупки на кассе.</p>
    </div>
    <div class="card">
      <h3><span class="ic">📜</span>История начислений</h3>
      ${log.length ? log.map(r => `
        <div class="lgrow">
          <span class="pl">${r.icon}</span>
          <span class="nm">${esc(r.title)}<br><span style="font-size:10px;color:var(--sk-muted);font-family:var(--mono)">${esc(r.status)}</span></span>
          <span class="sc" style="color:${r.ok ? 'inherit' : 'var(--bad)'}">${r.ok ? '+' + r.pts : '—'}</span>
        </div>`).join('')
        : `<div class="muted" style="padding:4px 2px">Здесь появятся ваши начисления.</div>`}
    </div>`;
}

/* ================= телефон ================= */
function renderPhone(rec) {
  applySkin();
  renderAppbar();

  const v = el('#viewport');
  v.innerHTML = state.tab === 'home'     ? renderHome(rec)
              : state.tab === 'referral' ? renderReferral()
              : renderWallet();

  const why = el('#whyBtn');
  if (why) why.onclick = () => {
    document.querySelector('#panelWhy').scrollIntoView({ behavior: 'smooth', block: 'center' });
    document.querySelector('#panelWhy').animate(
      [{ boxShadow: '0 0 0 0 rgba(15,123,62,.5)' }, { boxShadow: '0 0 0 12px rgba(15,123,62,0)' }],
      { duration: 900 });
  };

  const tabs = [
    { id: 'home',     ic: '◆', nm: 'Главная' },
    { id: 'referral', ic: '◉', nm: 'Друзья' },
    { id: 'wallet',   ic: '▤', nm: 'Кошелёк' },
  ];
  el('#tabbar').innerHTML = tabs.map(t =>
    `<button class="tab" data-tab="${t.id}" aria-selected="${state.tab === t.id}">
      <b>${t.ic}</b>${t.nm}
    </button>`).join('');
  el('#tabbar').onclick = e => {
    const b = e.target.closest('[data-tab]'); if (!b) return;
    state.tab = b.dataset.tab; render();
  };
}

/* ================= консоль ================= */
function renderConsole(rec) {
  const p = profile(), c = chain();
  el('#console').innerHTML = [
    panelDecision(rec, p, c),
    panelWhy(rec, p),
    panelEconomics(rec),
    panelReceipts(p),
    panelReferralEcon(p),
    panelSimulation(),
    panelPilot(),
  ].join('');
  wireReceipts();
}

function panelDecision(rec, p, c) {
  const w = rec.winner;
  return `
  <div class="panel">
    <div class="phead">
      <span class="num">1</span><h2>Кому и что показали</h2>
      <span class="right">${esc(p.id)} · ${esc(c.name)}</span>
    </div>
    <div class="pbody">
      <div class="lede">Профиль покупателя и итоговое решение системы: показать механику или промолчать.</div>
      ${w ? `
        <div class="verdict go">
          <span class="big">${fmt.rub(w.econ.enim)}</span>
          <div class="txt">
            Показываем <b>«${esc(w.mechanic.name)}»</b>${w.chainLead ? ' — ведущую механику этой сети' : ''}.
            Ожидаемая чистая дополнительная маржа положительна, награда укладывается в потолок.
          </div>
        </div>`
      : `
        <div class="verdict no">
          <span class="big">NO_OFFER</span>
          <div class="txt">${esc(rec.noOfferReason)}. <b>Платную механику не показываем.</b> Это защита маржи: награда оплатила бы покупку, которая случилась бы и так.</div>
        </div>`}
      <div style="font-size:12px;color:var(--ink-2);line-height:1.5">
        <b>${esc(p.name)} · ${esc(p.label)}.</b> ${esc(p.story)}
      </div>
      <div class="kpis" style="margin-top:12px">
        <div class="kpi"><div class="k">визитов / 28 дн</div><div class="v">${p.visits28}</div></div>
        <div class="kpi"><div class="k">средний чек</div><div class="v">${p.avgCheck}</div><div class="s">₽</div></div>
        <div class="kpi"><div class="k">доля СТМ</div><div class="v">${Math.round(p.stmShare * 100)}%</div></div>
        <div class="kpi"><div class="k">риск накрутки</div><div class="v ${p.fraudRisk > .5 ? 'bad' : ''}">${Math.round(p.fraudRisk * 100)}%</div></div>
      </div>
      ${p.safetyFlag ? `<div class="note warn"><span>🛡️</span><div><b>Safety-флаг.</b> В чеках регулярно алкоголь и табак. Эти категории — только ограничение: они никогда не становятся целью задания и не дают повышенную награду. Safety-фильтр работает до экономики и не может быть отменён.</div></div>` : ''}
      <div class="note"><span>🎨</span><div><b>Механика зависит и от сети.</b> ${esc(c.leadWhy)}</div></div>
    </div>
  </div>`;
}

function panelWhy(rec, p) {
  const rows = rec.rows.map(r => {
    const cls = r === rec.winner ? 'win' : r.verdict !== 'ELIGIBLE' ? 'dim' : '';
    const badge = r.verdict === 'ELIGIBLE' ? `<span class="pill ok">допущено</span>`
                : r.verdict === 'BLOCKED'  ? `<span class="pill wa">заблокировано</span>`
                : `<span class="pill no">не окупается</span>`;
    const codes = [...r.reasons, r.blockCode].filter(Boolean).map(x =>
      `<span class="code ${x.includes('POSITIVE') ? 'pos' : x.includes('NEGATIVE') || x.includes('BLOCK') ? 'neg' : ''}">${esc(x)}</span>`).join('');
    return `<tr class="${cls}">
      <td><div class="mech"><span class="ic">${r.mechanic.icon}</span>${esc(r.mechanic.name)}
        ${r.chainLead ? '<span class="lead">СЕТЬ</span>' : ''}</div></td>
      <td class="num-c">${fmt.pct(r.cand.p0)}</td>
      <td class="num-c">${fmt.pct(r.cand.p1)}</td>
      <td class="num-c">${fmt.pp(r.econ.uplift)}</td>
      <td class="num-c">${r.cand.reward ? r.cand.reward + ' ₽' : 'товар'}</td>
      <td class="num-c" style="font-weight:700;color:${r.econ.enim > 0 ? 'var(--ok)' : 'var(--bad)'}">${fmt.rub(r.econ.enim)}</td>
      <td>${badge}<div class="codes" style="margin-top:5px">${codes}</div></td>
    </tr>`;
  }).join('');

  return `
  <div class="panel" id="panelWhy">
    <div class="phead"><span class="num">2</span><h2>Почему выбрана именно эта механика</h2>
      <span class="right">4 кандидата · выбран 1</span></div>
    <div class="pbody">
      <div class="lede">Система оценивает все четыре механики сразу и выбирает одну. p₀ — вероятность, что человек придёт сам; p₁ — что придёт с механикой. Разница между ними и есть польза, ради которой мы платим.</div>
      <div class="scroll"><table>
        <thead><tr>
          <th>механика</th><th style="text-align:right">p₀ без</th><th style="text-align:right">p₁ с</th>
          <th style="text-align:right">прирост</th><th style="text-align:right">награда</th>
          <th style="text-align:right">ENIM</th><th>вердикт и причины</th>
        </tr></thead>
        <tbody>${rows}</tbody>
      </table></div>
      <div class="note"><span>🤖</span><div>
        <b>Здесь нет ML-модели — и это осознанно.</b> На синтетике модель предсказывала бы наши же допущения.
        p₀ и p₁ — прозрачные входные вероятности профиля, дальше идёт арифметика, которую можно проверить на бумаге.
        Роль языковой модели ограничена формулировкой текста: награду, категорию и экономику определяет движок.
      </div></div>
    </div>
  </div>`;
}

function panelEconomics(rec) {
  const r = rec.winner || rec.rows[0];
  const e = r.econ;
  const line = (lb, vl, cls) => `<div class="wf ${cls}"><span class="lb">${lb}</span><span class="vl">${fmt.rub(vl)}</span></div>`;

  return `
  <div class="panel">
    <div class="phead"><span class="num">3</span><h2>Сколько это стоит и что приносит</h2>
      <span class="right">на один показ · ${esc(r.mechanic.name)}</span></div>
    <div class="pbody">
      <div class="lede">Разложение до последней копейки: что заработали, что потратили и сколько осталось.</div>
      <div class="waterfall">
        ${line('Дополнительная маржа от прироста', e.grossCm, 'plus')}
        ${line('− «покупка была бы и так, просто позже»', -(e.grossCm - e.sustainedCm), 'minus')}
        ${e.writeOffSaving ? line('+ предотвращённое списание', e.writeOffSaving, 'plus') : ''}
        ${e.prizeCost ? line('− себестоимость приза', -e.prizeCost, 'minus') : ''}
        ${line('− награда (её получают все, кто выполнил)', -e.rewardCost, 'minus')}
        ${line('− коммуникация', -e.contactCost, 'minus')}
        ${line('− ожидаемые потери от накрутки', -e.fraudCost, 'minus')}
        ${line('− операционные', -e.opsCost, 'minus')}
        <div class="wf total"><span class="lb">Чистая дополнительная маржа</span><span class="vl">${fmt.rub(e.enim)}</span></div>
      </div>
      <div class="formula">ENIM = (p₁ − p₀) × маржа_события × (1 − перенос)
     ${e.writeOffSaving ? '+ P(списание) × стоимость × p₁ × p_выигрыша\n     − себестоимость_приза × p₁ × p_выигрыша\n     ' : ''}− p₁ × награда − коммуникация − накрутка − операционные</div>
      <div class="note"><span>⚠️</span><div>
        <b>Награда вычитается через p₁, а не через прирост.</b> Её получают все, кто выполнил задание, —
        включая тех, кто купил бы и без него. Считать награду только на приросте — самая частая ошибка,
        которая систематически завышает экономику. Потолок награды в base-сценарии — ${ECON.rMaxBase} ₽.
      </div></div>
      ${r.extra.hotEcon ? `<div class="note"><span>🥗</span><div>
        <b>«Горячий товар» не бесплатный.</b> Часть таких товаров продалась бы сама.
        Предотвращённая потеря ${fmt.rub(r.extra.hotEcon.savedLoss)} минус упущенная маржа
        ${fmt.rub(r.extra.hotEcon.lostMargin)} минус выдача ${fmt.rub(r.extra.hotEcon.handling)} =
        <b>${fmt.rub(r.extra.hotEcon.net)}</b> на единицу. Приз допускается, только если это больше нуля.
      </div></div>` : ''}
      ${r.extra.swapEcon ? `<div class="note"><span>💚</span><div>
        <b>Два условия одновременно.</b> Покупателю дешевле на ${r.extra.swapEcon.savingRubles} ₽,
        сети маржинальнее на ${fmt.rub(r.extra.swapEcon.marginDelta)}. Если товар дешевле,
        но маржа ниже — баллы не начисляются. В каталоге такая ловушка есть: спред дешевле масла
        на 80 ₽, но маржа падает на 19 ₽ → <span class="code neg">MARGIN_LOWER_THAN_BASELINE</span>.
      </div></div>` : ''}
    </div>
  </div>`;
}

function panelReceipts(p) {
  return `
  <div class="panel">
    <div class="phead"><span class="num">4</span><h2>Проверка чека на накрутку</h2>
      <span class="right">precision важнее recall</span></div>
    <div class="pbody">
      <div class="lede">Нажмите любую кнопку — событие пройдёт проверку. Три правила вместо большой системы: этого достаточно, чтобы поймать основные схемы накрутки.</div>
      <div class="simctl">
        <button class="simbtn" data-rc="valid">Обычный чек</button>
        <button class="simbtn danger" data-rc="dup">Тот же чек повторно</button>
        <button class="simbtn danger" data-rc="split">5 чеков за 8 минут</button>
        <button class="simbtn danger" data-rc="ref">14 приглашений, 1 покупка</button>
      </div>
      <div id="ledger" class="ledger">
        ${state.receipts.length ? '' : `<div style="font-size:12px;color:var(--ink-3)">Нажмите кнопку — событие пройдёт проверку и попадёт в журнал начислений.</div>`}
      </div>
      <div class="note"><span>🎯</span><div>
        <b>Порог блокировки объясним.</b> ${FRAUD_THRESHOLDS.pending} — задержка выплаты,
        ${FRAUD_THRESHOLDS.review} — ручная проверка, ${FRAUD_THRESHOLDS.block} — блокировка,
        но только при двух независимых семействах сигналов. Одного сигнала недостаточно:
        ошибочно заблокировать честного покупателя дороже, чем пропустить мошенника.
        Жёсткое правило одно — повторный чек.
      </div></div>
    </div>
  </div>`;
}

function panelReferralEcon(p) {
  const r = referralEconomics(p);
  return `
  <div class="panel">
    <div class="phead"><span class="num">5</span><h2>Сколько стоит приглашённый друг</h2>
      <span class="right">${r.qualified} квалифицировано</span></div>
    <div class="pbody">
      <div class="lede">Приглашение окупается, только если новый покупатель принесёт больше маржи, чем стоят обе награды.</div>
      <div class="kpis">
        <div class="kpi"><div class="k">награда за пару</div><div class="v">${r.costPerQualified}</div><div class="s">₽ приглашающий + друг</div></div>
        <div class="kpi"><div class="k">маржа нового за 90 дн</div><div class="v">${r.expectedCm}</div><div class="s">₽ с учётом удержания ${Math.round(r.pRetain*100)}%</div></div>
        <div class="kpi"><div class="k">чистыми с приглашения</div><div class="v ${r.profitable ? 'ok' : 'bad'}">${r.netPerQualified}</div><div class="s">₽</div></div>
        <div class="kpi"><div class="k">итого по профилю</div><div class="v ${r.net >= 0 ? 'ok' : 'bad'}">${r.net}</div><div class="s">₽</div></div>
      </div>
      <div class="note"><span>🛡️</span><div>
        <b>Награда только за покупку, никогда за регистрацию.</b> Это основная защита от накрутки:
        создать пустой аккаунт ничего не стоит, а совершить реальную покупку от ${r.qualifyMinCheck} ₽ — уже нет.
        Плюс потолок ${r.maxPerMonth} приглашений в месяц и окно квалификации ${r.qualifyWindowDays} дней.
      </div></div>
    </div>
  </div>`;
}

function panelSimulation() {
  const runs = SIMULATION.runs;
  const max = 500;
  const bars = runs.map(r => {
    const w = Math.min(100, Math.abs(r.netCm) / max * 100);
    const pos = r.netCm >= 0;
    return `<div class="bar">
      <div class="bl"><span>n = ${r.n.toLocaleString('ru-RU')} · ${r.test.toLocaleString('ru-RU')} test / ${r.control.toLocaleString('ru-RU')} control</span>
        <b style="color:${pos ? 'var(--ok)' : 'var(--bad)'}">${fmt.rub(r.netCm)}</b></div>
      <div class="tr"><div class="zero" style="left:50%"></div>
        <div class="fl" style="width:${w/2}%; margin-left:${pos ? 50 : 50 - w/2}%;
          background:${pos ? 'var(--ok)' : 'var(--bad)'}"></div></div>
    </div>`;
  }).join('');

  const sc = SIMULATION.scenarios.map(s => `
    <tr class="${s.verdict === 'NO_CHALLENGE' ? 'dim' : ''}">
      <td style="font-weight:600">${esc(s.name)}</td>
      <td class="num-c">${fmt.rub(s.dCm)}</td>
      <td class="num-c">${s.rMax ? fmt.rub(s.rMax) : '—'}</td>
      <td class="num-c">${s.selected ? s.selected + ' ₽' : '0 ₽'}</td>
      <td class="num-c" style="color:${s.lcb > 0 ? 'var(--ok)' : 'var(--bad)'}">${fmt.rub(s.lcb)}</td>
      <td>${s.verdict === 'LAUNCH'
        ? '<span class="pill ok">запуск со stop-loss</span>'
        : '<span class="pill no">не показывать</span>'}</td>
    </tr>`).join('');

  return `
  <div class="panel">
    <div class="phead"><span class="num">6</span><h2>Проверка на 1 000 и 10 000 покупателей</h2>
      <span class="right">синтетическая популяция</span></div>
    <div class="pbody">
      <div class="lede">Прогнали механику на синтетической популяции. Показываем не только удачный результат, но и неудачный — иначе это самообман.</div>
      <div class="bars">${bars}</div>
      <div class="note warn"><span>🔬</span><div>
        <b>Знаки разошлись — и мы это показываем.</b> На выборке 1 000 чистая маржа отрицательна,
        на 10 000 положительна, хотя истинный эффект в генераторе один и тот же.
        Это ровно та причина, по которой нельзя выбирать удобный прогон и объявлять его результатом.
        Monte-Carlo на 10 000: среднее ${SIMULATION.monteCarlo[1].mean} доп. визита,
        разброс ${SIMULATION.monteCarlo[1].lo}–${SIMULATION.monteCarlo[1].hi}.
      </div></div>
      <div class="scroll" style="margin-top:13px"><table>
        <thead><tr><th>сценарий</th><th style="text-align:right">Δмаржа</th>
          <th style="text-align:right">потолок</th><th style="text-align:right">выбрано</th>
          <th style="text-align:right">нижняя граница</th><th>решение</th></tr></thead>
        <tbody>${sc}</tbody>
      </table></div>
      <div class="note"><span>📉</span><div>
        В консервативном сценарии средняя прибыль положительна (1,40 ₽), но нижняя граница уходит
        в минус — и механика <b>не запускается</b>. Награда назначается от нижней границы, а не от среднего:
        так оптимизм не превращается в убыток.
      </div></div>
    </div>
  </div>`;
}

function panelPilot() {
  return `
  <div class="panel">
    <div class="phead"><span class="num">7</span><h2>Как это проверить в реальности</h2>
      <span class="right">одна страница для продуктовой команды</span></div>
    <div class="pbody">
      <div class="lede">Три группы покупателей. Без контрольной группы, которая ничего не получает, невозможно понять, сработала механика или люди пришли бы сами.</div>
      <div class="scroll"><table>
        <thead><tr><th>группа</th><th>что получает</th><th>что измеряет</th></tr></thead>
        <tbody>
          <tr><td style="font-weight:600">A · контроль</td><td>текущая программа лояльности без изменений</td><td class="num-c" style="text-align:left">базовый уровень</td></tr>
          <tr><td style="font-weight:600">B · соло</td><td>механика и прогресс без лиги и приглашений</td><td class="num-c" style="text-align:left">эффект ядра, B − A</td></tr>
          <tr><td style="font-weight:600">C · полный</td><td>всё из B плюс лига и приглашения</td><td class="num-c" style="text-align:left">вклад социального слоя, C − B</td></tr>
        </tbody>
      </table></div>
      <div class="kpis" style="margin-top:13px">
        <div class="kpi"><div class="k">главная метрика</div><div class="v" style="font-size:14px">дни с покупкой</div><div class="s">из 42, на всех назначенных</div></div>
        <div class="kpi"><div class="k">рандомизация</div><div class="v" style="font-size:14px">по магазинам</div><div class="s">не по людям — лига создаёт переток</div></div>
        <div class="kpi"><div class="k">окно</div><div class="v" style="font-size:14px">56+42+28</div><div class="s">дней: база, тест, дозревание</div></div>
        <div class="kpi"><div class="k">защитная метрика</div><div class="v" style="font-size:14px">маржа корзины</div><div class="s">не должна упасть</div></div>
      </div>
      <div class="note"><span>🚦</span><div>
        <b>Останавливаем, если:</b> маржа корзины падает; растёт доля алкоголя и табака;
        антифрод систематически блокирует честных; прироста нет после набора достаточной выборки;
        экономика не выходит в плюс даже после снижения награды.
      </div></div>
    </div>
  </div>`;
}

/* ================= симулятор чеков ================= */
const SCENARIOS = {
  valid: { title: 'Чек №8841 · 640 ₽', signals: [], icon: '🧾' },
  dup:   { title: 'Чек №8841 · повторная отправка', signals: ['DUPLICATE_TRANSACTION'], icon: '🔁' },
  split: { title: '5 чеков за 8 минут · один магазин', signals: ['SPLIT_BASKET_SUSPECTED','VELOCITY_ANOMALY'], icon: '✂️' },
  ref:   { title: '14 приглашений, 1 покупка', signals: ['REFERRAL_NO_PURCHASE','DEVICE_CLUSTER'], icon: '👥' },
};

function wireReceipts() {
  document.querySelectorAll('[data-rc]').forEach(b => {
    b.onclick = () => {
      const sc = SCENARIOS[b.dataset.rc];
      const res = scoreFraud(sc.signals);
      const rec = recommend(profile(), chain());
      const pts = rec.winner ? rec.winner.cand.reward : 0;

      state.receipts.unshift({
        icon: sc.icon,
        title: sc.title,
        ok: res.decision === 'APPROVE',
        pts,
        status: res.decision === 'APPROVE' ? 'начислено' : res.hits.map(h => h.code).join(' · '),
      });
      renderLedger();
      renderPhone(rec);
    };
  });
  renderLedger();
}

function renderLedger() {
  const box = el('#ledger'); if (!box) return;
  if (!state.receipts.length) return;

  box.innerHTML = state.receipts.map(r => {
    const sc = Object.values(SCENARIOS).find(s => s.title === r.title);
    const res = scoreFraud(sc ? sc.signals : []);
    const map = {
      APPROVE: ['ok', 'начислено'], HOLD: ['wa', 'задержано'],
      REVIEW:  ['wa', 'на проверку'], DENY: ['no', 'отклонено'],
    };
    const [cls, lbl] = map[res.decision];
    return `<div class="lev">
      <span class="st pill ${cls}">${lbl}</span>
      <div class="ds">
        <b>${esc(r.title)}</b>
        <span>${esc(res.reason)}</span>
        ${res.hits.length ? `<div class="codes" style="margin-top:4px">${res.hits.map(h => `<span class="code neg">${esc(h.code)}</span>`).join('')}</div>` : ''}
      </div>
      <span class="sc" style="color:${r.ok ? 'var(--ok)' : 'var(--ink-3)'}">${r.ok ? '+' + r.pts : 'риск ' + res.score}</span>
    </div>`;
  }).join('');
}

/* ================= запуск ================= */
function render() {
  const rec = recommend(profile(), chain());
  renderPickers();
  renderPhone(rec);
  renderConsole(rec);
}
render();
