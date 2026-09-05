/* ============================================================
   X5 ДВОР — движок выбора механики
   Никакого ML: прозрачная арифметика, которую можно проверить
   на бумаге. Подставьте реальные данные X5 — контур не изменится.
   ============================================================ */

import { ECON, HOT_ITEMS, STM_SWAPS, COPY, REFERRAL } from './data.js';

export const MECHANICS = {
  hotchance: { key: 'hotchance', name: 'Горячий шанс',  icon: '🎁', internal: 'казино' },
  league:    { key: 'league',    name: 'Личная лига',   icon: '🏆', internal: 'leaderboard' },
  challenge: { key: 'challenge', name: 'Челлендж',      icon: '🎯', internal: 'цели' },
  stm:       { key: 'stm',       name: 'Сохрани рубли', icon: '💚', internal: 'СТМ' },
};

/* ---------- Ожидаемая чистая дополнительная маржа ----------

   ENIM = (p1 − p0) × CM_событие          дополнительная маржа
        − p1 × стоимость_награды          награду получают ВСЕ, кто выполнил,
                                          включая тех, кто купил бы и так
        − стоимость_коммуникации
        − ожидаемые потери от накрутки

   Ключевой момент: награда вычитается через p1, а не через uplift.
   Иначе экономика систематически завышается.                        */
export function computeEnim(cand, profile, opts = {}) {
  const uplift = cand.p1 - cand.p0;
  const grossCm = uplift * cand.cmEvent;
  const sustainedCm = grossCm * (1 - ECON.pullForward);
  const rewardCost = cand.p1 * cand.reward;
  const fraudCost = cand.reward * cand.p1 * profile.fraudRisk;

  /* Предотвращённое списание засчитывается только тогда, когда приз
     реально выдан. Приз получает не каждый: механику надо выполнить
     (p1) и выиграть в розыгрыше (pWin). Прибавлять всю экономию к
     каждому показу — та же ошибка, что считать награду без p1.      */
  const pWin = opts.pWin || 0;
  const writeOffSaving = (opts.writeOffSaving || 0) * cand.p1 * pWin;
  /* Сам приз — тоже расход: товар уходит бесплатно. */
  const prizeCost = (opts.prizeCost || 0) * cand.p1 * pWin;

  const enim = sustainedCm + writeOffSaving
             - rewardCost - prizeCost - ECON.contactCost - fraudCost - ECON.opsCost;

  return {
    uplift,
    grossCm,
    sustainedCm,
    writeOffSaving,
    prizeCost,
    pWin,
    rewardCost,
    contactCost: ECON.contactCost,
    fraudCost,
    opsCost: ECON.opsCost,
    enim,
  };
}

/* ---------- Параметры «Горячего шанса» ----------
   Шанс выигрыша объявляется пользователю заранее и не меняется
   задним числом. Без ставок, без пополнения баланса, без cash-out. */
export const HOT_CHANCE = {
  pWin: 0.25,                 // объявленный шанс выигрыша
  consolation: 'Баллы X5 Клуба',
};

/* ---------- «Горячий товар» не бесплатный ----------

   Соблазн сказать «его всё равно спишут, значит приз даром».
   Это неверно: часть таких товаров продалась бы сама.

   Выгода = P(списание) × стоимость_списания
          − P(продажа)  × маржа_которую_потеряли                */
export function hotItemEconomics(item) {
  const pSell = 1 - item.pWriteOff;
  const writeOffCost = item.price - item.cm;      // себестоимость, которую потеряем
  const savedLoss = item.pWriteOff * writeOffCost;
  const lostMargin = pSell * item.cm;
  const handling = 4;                              // ₽ комплектация и выдача
  const net = savedLoss - lostMargin - handling;
  return { pSell, writeOffCost, savedLoss, lostMargin, handling, net, eligible: net > 0 };
}

/* ---------- «Сохрани рубли»: два условия одновременно ----------

   Баллы начисляются ТОЛЬКО если:
     1) новая покупка ДЕШЕВЛЕ исторического аналога — выгода покупателю
     2) её маржа ВЫШЕ — выгода сети

   Дешёвый, но менее маржинальный товар не квалифицируется.
   Сравнение — по цене за единицу (за литр/кг), а не за упаковку,
   иначе разный объём даст ложную экономию.                        */
export function stmSwapEconomics(swap) {
  const fromUnitPrice = swap.fromPrice / swap.fromUnit;
  const toUnitPrice = swap.toPrice / swap.toUnit;
  const savingPerUnit = fromUnitPrice - toUnitPrice;
  const savingRubles = Math.max(0, swap.fromPrice - swap.toPrice * (swap.fromUnit / swap.toUnit));
  const marginDelta = swap.toCm - swap.fromCm;

  const cheaper = savingPerUnit > 0;
  const moreMargin = marginDelta > 0;
  const eligible = cheaper && moreMargin;

  return {
    fromUnitPrice, toUnitPrice, savingPerUnit,
    savingRubles: Math.round(savingRubles),
    marginDelta, cheaper, moreMargin, eligible,
    reason: eligible ? 'STM_SWAP_QUALIFIED'
          : !cheaper ? 'NOT_CHEAPER_FOR_CUSTOMER'
          : 'MARGIN_LOWER_THAN_BASELINE',
  };
}

/* ---------- Персональная лига ----------

   Ключевое отличие от обычного leaderboard: очки начисляются
   НЕ за сумму трат, а за прирост к собственной норме.

   Иначе рейтинг всегда выигрывают крупные семьи и перекупщики,
   мелкий покупатель видит, что шансов нет, и уходит — механика
   демотивирует ровно тех, кого должна была растормошить.
   Плюс мы платили бы за поведение, которое уже было.             */
export function leagueScore(profile) {
  const baseline = profile.visits28 / 4;                  // обычная норма в неделю
  const dailyCap = 40;                                    // потолок очков в день
  const weeklyCap = dailyCap * 7;
  return {
    baseline: Math.round(baseline * 10) / 10,
    dailyCap, weeklyCap,
    rule: 'Очки за прирост к собственной норме, а не за размер чека',
    fair: true,
  };
}

/* ---------- Реферальная награда ----------

   Награда — только за КВАЛИФИЦИРОВАННУЮ покупку приглашённого,
   никогда за регистрацию. Это и есть основная защита от накрутки:
   создать пустой аккаунт бесплатно, а совершить реальную покупку
   на 400 ₽ — уже нет.                                            */
export function referralEconomics(profile) {
  const r = REFERRAL;
  const qualified = profile.referral.qualified;
  const pending = profile.referral.pending;

  const costPerQualified = r.rewardInviter + r.rewardInvitee;
  const expectedCm = r.newUserCm90d * r.pRetain;
  const netPerQualified = expectedCm - costPerQualified;

  const earned = qualified * r.rewardInviter;
  const totalCost = qualified * costPerQualified;
  const totalCm = qualified * expectedCm;

  return {
    ...r,
    qualified, pending,
    costPerQualified,
    expectedCm: Math.round(expectedCm),
    netPerQualified: Math.round(netPerQualified),
    earned,
    totalCost,
    totalCm: Math.round(totalCm),
    net: Math.round(totalCm - totalCost),
    profitable: netPerQualified > 0,
    remaining: Math.max(0, r.maxPerMonth - qualified - pending),
  };
}

/* ---------- Антифрод: три правила, не система ----------

   Полноценный антифрод-контур прямо вне скоупа кейса.
   Здесь минимум, закрывающий критерий: простой скоринг
   с объяснимым порогом, Precision важнее Recall.

   Порог блокировки объясним: автоматически блокируем только
   при двух независимых семействах сигналов. Один сигнал —
   максимум задержка выплаты, потому что ошибочно заблокировать
   честного покупателя дороже, чем пропустить мошенника.          */
export const FRAUD_RULES = [
  { code: 'DUPLICATE_TRANSACTION', family: 'ledger', weight: 100,
    label: 'Тот же чек отправлен повторно',
    explain: 'Номер чека уже засчитан в системе' },
  { code: 'SPLIT_BASKET_SUSPECTED', family: 'velocity', weight: 45,
    label: 'Несколько чеков за минуты в одном магазине',
    explain: 'Похоже на дробление одной корзины ради нескольких наград' },
  { code: 'VELOCITY_ANOMALY', family: 'velocity', weight: 40,
    label: 'Нереальная скорость выполнения заданий',
    explain: 'Задания закрываются быстрее, чем физически возможно' },
  { code: 'REFERRAL_NO_PURCHASE', family: 'referral', weight: 50,
    label: 'Приглашения без покупок',
    explain: 'Аккаунты созданы, но ни одной квалифицированной покупки' },
  { code: 'DEVICE_CLUSTER', family: 'device', weight: 35,
    label: 'Много аккаунтов с одного устройства',
    explain: 'Приглашения приходят с того же устройства' },
];

export const FRAUD_THRESHOLDS = { pending: 25, review: 50, block: 75 };

export function scoreFraud(signals) {
  const hits = FRAUD_RULES.filter(r => signals.includes(r.code));
  const hard = hits.find(h => h.weight >= 100);
  const score = hard ? 100 : Math.min(99, hits.reduce((s, h) => s + h.weight, 0));
  const families = new Set(hits.map(h => h.family));

  let decision, reason;
  if (hard) {
    decision = 'DENY';
    reason = 'Жёсткое правило: чек уже был засчитан';
  } else if (score >= FRAUD_THRESHOLDS.block && families.size >= 2) {
    decision = 'DENY';
    reason = `Два независимых семейства сигналов (${[...families].join(', ')})`;
  } else if (score >= FRAUD_THRESHOLDS.review) {
    decision = 'REVIEW';
    reason = 'Один сигнал высокого веса — отправлено на ручную проверку, не заблокировано';
  } else if (score >= FRAUD_THRESHOLDS.pending) {
    decision = 'HOLD';
    reason = 'Выплата задержана до окончания окна возвратов';
  } else {
    decision = 'APPROVE';
    reason = 'Сигналов риска не обнаружено';
  }
  return { score, hits, decision, reason, families: [...families] };
}

/* ---------- Safety-фильтр ----------
   Работает ДО экономики и не может быть отменён.
   Алкоголь и табак — только guardrail, никогда не цель задания. */
export const BLOCKED_CATEGORIES = ['Алкоголь', 'Табак'];

export function safetyCheck(profile, mechanicKey) {
  if (!profile.safetyFlag) return { blocked: false };
  // Категорийные механики подменяются на нейтральные
  if (mechanicKey === 'stm') {
    return {
      blocked: true,
      code: 'SAFETY_CATEGORY_BLOCKED',
      note: 'Категорийная замена может задеть исключённые категории — переключаем на нейтральную механику',
    };
  }
  return { blocked: false, note: 'Исключённые категории убраны из подбора товаров' };
}

/* ---------- Главный вход: выбор механики ---------- */
export function recommend(profile, chain) {
  const rows = [];

  for (const key of Object.keys(MECHANICS)) {
    const cand = profile.candidates[key];
    const safety = safetyCheck(profile, key);
    const reasons = [];
    let blocked = safety.blocked;
    let blockCode = safety.code;
    let extra = {};
    let econOpts = {};

    // «Горячий шанс» требует подходящего остатка в магазине
    if (key === 'hotchance') {
      const items = HOT_ITEMS.map(i => ({ item: i, econ: hotItemEconomics(i) }))
                             .filter(x => x.econ.eligible);
      if (!items.length) {
        blocked = true; blockCode = 'NO_ELIGIBLE_HOT_STOCK';
      } else {
        const best = items.sort((a, b) => b.econ.net - a.econ.net)[0];
        extra = { hotItem: best.item, hotEcon: best.econ, pWin: HOT_CHANCE.pWin };
        econOpts = {
          pWin: HOT_CHANCE.pWin,                  // шанс выигрыша объявлен заранее
          writeOffSaving: best.econ.savedLoss,    // предотвращённая потеря
          prizeCost: best.econ.writeOffCost + best.econ.handling, // товар уходит бесплатно
        };
        reasons.push('HOT_STOCK_AVAILABLE');
      }
    }

    // «Сохрани рубли» требует пары «дешевле И маржинальнее»
    if (key === 'stm') {
      const swaps = STM_SWAPS.map(s => ({ swap: s, econ: stmSwapEconomics(s) }))
                             .filter(x => x.econ.eligible);
      if (!swaps.length) {
        blocked = true; blockCode = 'NO_QUALIFIED_STM_SWAP';
      } else {
        const best = swaps.sort((a, b) => b.econ.marginDelta - a.econ.marginDelta)[0];
        extra = { swap: best.swap, swapEcon: best.econ };
        reasons.push('STM_SWAP_QUALIFIED');
      }
    }

    if (key === 'league') {
      extra = { league: leagueScore(profile) };
      reasons.push('FAIR_COHORT_SCORING');
    }

    const econ = computeEnim(cand, profile, econOpts);

    // Экономический gate
    let verdict;
    if (blocked) verdict = 'BLOCKED';
    else if (econ.enim <= ECON.safetyBuffer) verdict = 'NEGATIVE';
    else verdict = 'ELIGIBLE';

    if (verdict === 'NEGATIVE') reasons.push('NEGATIVE_EXPECTED_NIM');
    if (verdict === 'ELIGIBLE') reasons.push('POSITIVE_EXPECTED_NIM');
    if (cand.reward > ECON.rMaxBase && key !== 'hotchance') reasons.push('REWARD_ABOVE_RMAX');
    if (profile.fraudRisk > 0.5) reasons.push('HIGH_FRAUD_RISK');

    rows.push({
      key, mechanic: MECHANICS[key], cand, econ, verdict, blocked, blockCode,
      reasons, extra, safetyNote: safety.note,
      chainLead: chain.lead === key,
    });
  }

  // Сортируем по ENIM; при равенстве приоритет ведущей механике сети
  const eligible = rows.filter(r => r.verdict === 'ELIGIBLE')
                       .sort((a, b) => {
                         const d = b.econ.enim - a.econ.enim;
                         if (Math.abs(d) < 1.5) return (b.chainLead ? 1 : 0) - (a.chainLead ? 1 : 0);
                         return d;
                       });

  const winner = eligible[0] || null;

  return {
    rows: rows.sort((a, b) => b.econ.enim - a.econ.enim),
    winner,
    noOffer: !winner,
    noOfferReason: !winner
      ? (rows.every(r => r.verdict === 'NEGATIVE')
          ? 'Ни одна механика не окупается: награда оплатила бы покупку, которая случилась бы и так'
          : 'Все кандидаты заблокированы правилами безопасности или доступностью товара')
      : null,
  };
}

/* ---------- Текст механики под сеть ---------- */
export function copyFor(mechanicKey, chainId) {
  return COPY[mechanicKey]?.[chainId] || COPY[mechanicKey]?.ts5 || { title: '', body: '' };
}

export const fmt = {
  rub: n => `${n < 0 ? '−' : ''}${Math.abs(n).toLocaleString('ru-RU', { maximumFractionDigits: 2 })} ₽`,
  pct: n => `${(n * 100).toFixed(1).replace('.', ',')}%`,
  pp:  n => `${n >= 0 ? '+' : '−'}${Math.abs(n * 100).toFixed(0)} п.п.`,
  num: n => n.toLocaleString('ru-RU', { maximumFractionDigits: 2 }),
};
