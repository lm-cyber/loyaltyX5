/* ============================================================
   X5 ДВОР — синтетические данные демонстрации
   ВСЕ ЧИСЛА СИНТЕТИЧЕСКИЕ. Это сценарий, а не результат пилота.
   Источники калибровки: docs/research/04-reward-economics.md
   ============================================================ */

/* ---------- Бренды сетей: точные цвета из брендхаба X5 ---------- */
export const CHAINS = {
  ts5: {
    id: 'ts5',
    name: 'Пятёрочка',
    short: '5',
    tag: 'Магазин у дома',
    primary: '#00923A',
    accent: '#E52322',
    lime: '#98C21F',
    promo: '#FFAD26',
    ink: '#0E2A18',
    surface: '#F2FBF4',
    card: '#FFFFFF',
    onPrimary: '#FFFFFF',
    lead: 'challenge',
    leadWhy: 'Высокая частота визитов — есть надёжный baseline, по которому честно считается «N покупок».',
  },
  tsch: {
    id: 'tsch',
    name: 'Чижик',
    short: '🐦',
    tag: 'Жёсткий дискаунтер',
    primary: '#FFDF00',
    accent: '#000000',
    lime: '#6FB644',
    promo: '#E8348B',
    ink: '#111111',
    surface: '#FFFBE6',
    card: '#FFFFFF',
    onPrimary: '#000000',
    lead: 'hotchance',
    leadWhy: 'EDLP-дискаунтер: скидка уже в цене и не работает как стимул. Остаётся эмоция — и самый острый вопрос списаний.',
  },
  tsx: {
    id: 'tsx',
    name: 'Перекрёсток',
    short: '✚',
    tag: 'Супермаркет',
    primary: '#1B3D24',
    accent: '#FEA9C6',
    lime: '#C2F483',
    promo: '#E4784E',
    ink: '#16261B',
    surface: '#F6FBEF',
    card: '#FFFFFF',
    onPrimary: '#FFFFFF',
    lead: 'stm',
    leadWhy: 'Широкий ассортимент и развитая СТМ «Маркет» — есть реальная база для выгодной замены.',
  },
};

/* ---------- Экономические константы (base-сценарий) ---------- */
export const ECON = {
  cmRate: 0.12,          // маржинальность, % от выручки
  avgCheck: 600,         // ₽ средний чек
  cmPerVisit: 72,        // ₽ маржа с визита = 600 × 12%
  pullForward: 0.25,     // доля «покупок, которые всё равно были бы, просто раньше»
  riskBuffer: 0.20,      // запас на неопределённость
  contactCost: 1.5,      // ₽ стоимость коммуникации
  opsCost: 0.30,         // ₽ операционные на пользователя
  fraudRate: 0.015,      // ожидаемые потери от накрутки
  rMaxBase: 22.19,       // ₽ расчётный потолок награды
  safetyBuffer: 0.5,     // ₽ минимальный запас, ниже которого не показываем
};

/* ---------- «Горячие товары»: остаток + срок годности ---------- */
export const HOT_ITEMS = [
  { sku: 'HOT-041', name: 'Сырники «Бабушкина крынка»', cat: 'Готовая еда', price: 189, cm: 34,
    stock: 14, hoursLeft: 20, pWriteOff: 0.72, emoji: '🥞', stm: false },
  { sku: 'HOT-118', name: 'Молоко «Красная цена» 3.2%', cat: 'Молочное', price: 79, cm: 21,
    stock: 31, hoursLeft: 34, pWriteOff: 0.64, emoji: '🥛', stm: true },
  { sku: 'HOT-207', name: 'Салат «Цезарь» готовый', cat: 'Готовая еда', price: 229, cm: 51,
    stock: 8, hoursLeft: 11, pWriteOff: 0.83, emoji: '🥗', stm: false },
  { sku: 'HOT-315', name: 'Хлеб бездрожжевой', cat: 'Хлеб', price: 65, cm: 17,
    stock: 22, hoursLeft: 16, pWriteOff: 0.69, emoji: '🍞', stm: true },
  { sku: 'HOT-402', name: 'Творог 5% «Global Village»', cat: 'Молочное', price: 112, cm: 29,
    stock: 19, hoursLeft: 28, pWriteOff: 0.58, emoji: '🧀', stm: true },
];

/* ---------- Каталог замен на СТМ ----------
   Механика «Сохрани рубли»: баллы ТОЛЬКО если товар
   и дешевле для покупателя, и маржинальнее для сети.   */
export const STM_SWAPS = [
  { from: 'Молоко «Простоквашино» 3.2% 930 мл', fromPrice: 119, fromCm: 14, fromUnit: 930,
    to: 'Молоко «Красная цена» 3.2% 900 мл',    toPrice: 79,  toCm: 21, toUnit: 900,
    cat: 'Молочное', emoji: '🥛' },
  { from: 'Овсянка «Ясно Солнышко» 500 г',      fromPrice: 98,  fromCm: 11, fromUnit: 500,
    to: 'Овсянка «Global Village» 500 г',        toPrice: 69,  toCm: 19, toUnit: 500,
    cat: 'Бакалея', emoji: '🥣' },
  { from: 'Кофе «Jacobs Monarch» 190 г',        fromPrice: 549, fromCm: 62, fromUnit: 190,
    to: 'Кофе «Маркет» молотый 200 г',           toPrice: 399, toCm: 96, toUnit: 200,
    cat: 'Кофе и чай', emoji: '☕' },
  { from: 'Пельмени «Мириталь» 800 г',           fromPrice: 429, fromCm: 48, fromUnit: 800,
    to: 'Пельмени «Красная цена» 900 г',         toPrice: 319, toCm: 71, toUnit: 900,
    cat: 'Заморозка', emoji: '🥟' },
  /* Ловушка: дешевле, но маржа НИЖЕ — механика обязана отказать */
  { from: 'Масло сливочное «Экомилк» 180 г',     fromPrice: 229, fromCm: 41, fromUnit: 180,
    to: 'Масло спред «Эконом» 180 г',            toPrice: 149, toCm: 22, toUnit: 180,
    cat: 'Молочное', emoji: '🧈', trap: true },
];

/* ---------- Демо-профили ----------
   p0 / p1 — НЕ ML-модель, а прозрачные входные вероятности.
   Подставьте реальные данные X5 — контур не изменится.   */
export const PROFILES = [
  {
    id: 'P5_ROUTINE',
    name: 'Ирина',
    avatarEmoji: '🌿',
    chain: 'ts5',
    label: 'Регулярный покупатель',
    story: '8 покупок за 28 дней, ходит раз в 3–4 дня. Хлеб и молочное — почти в каждом чеке.',
    visits28: 8,
    medianGap: 4,
    avgCheck: 620,
    promoShare: 0.31,
    stmShare: 0.22,
    safetyFlag: false,
    fraudRisk: 0.04,
    league: { size: 24, place: 7, score: 340, nextPlace: 380, leader: 610 },
    referral: { invited: 3, qualified: 2, pending: 1 },
    stats: { streak: 4, saved: 1240, level: 3, xp: 62 },
    // Вероятности целевого действия: без механики / с механикой
    candidates: {
      challenge:  { p0: 0.40, p1: 0.52, reward: 20, cmEvent: 240 },
      hotchance:  { p0: 0.40, p1: 0.47, reward: 0,  cmEvent: 180 },
      league:     { p0: 0.40, p1: 0.51, reward: 18, cmEvent: 260 },
      stm:        { p0: 0.30, p1: 0.38, reward: 15, cmEvent: 160 },
    },
  },
  {
    id: 'CH_VALUE',
    name: 'Пётр',
    avatarEmoji: '🐦',
    chain: 'tsch',
    label: 'Чувствителен к выгоде',
    story: 'Ходит в дискаунтер за базовой корзиной. Скидками не удивить — они уже в цене.',
    visits28: 6,
    medianGap: 5,
    avgCheck: 430,
    promoShare: 0.58,
    stmShare: 0.61,
    safetyFlag: false,
    fraudRisk: 0.07,
    league: { size: 18, place: 11, score: 180, nextPlace: 215, leader: 400 },
    referral: { invited: 1, qualified: 0, pending: 1 },
    stats: { streak: 2, saved: 860, level: 2, xp: 35 },
    candidates: {
      challenge:  { p0: 0.34, p1: 0.39, reward: 20, cmEvent: 150 },
      hotchance:  { p0: 0.34, p1: 0.48, reward: 0, cmEvent: 195 },
      league:     { p0: 0.34, p1: 0.38, reward: 25, cmEvent: 140 },
      stm:        { p0: 0.34, p1: 0.37, reward: 15, cmEvent: 110 },
    },
  },
  {
    id: 'X_DISCOVERY',
    name: 'Марина',
    avatarEmoji: '✚',
    chain: 'tsx',
    label: 'Покупает бренды',
    story: 'Большая корзина, много брендовых позиций. Доля СТМ низкая — есть куда расти.',
    visits28: 7,
    medianGap: 4,
    avgCheck: 1180,
    promoShare: 0.24,
    stmShare: 0.09,
    safetyFlag: false,
    fraudRisk: 0.03,
    league: { size: 21, place: 5, score: 470, nextPlace: 505, leader: 720 },
    referral: { invited: 5, qualified: 4, pending: 0 },
    stats: { streak: 6, saved: 2380, level: 5, xp: 88 },
    candidates: {
      challenge:  { p0: 0.44, p1: 0.49, reward: 20, cmEvent: 260 },
      hotchance:  { p0: 0.44, p1: 0.48, reward: 0, cmEvent: 220 },
      league:     { p0: 0.44, p1: 0.50, reward: 25, cmEvent: 240 },
      stm:        { p0: 0.28, p1: 0.44, reward: 18, cmEvent: 310 },
    },
  },
  {
    id: 'SAFE_MODE',
    name: 'Сергей',
    avatarEmoji: '🛡️',
    chain: 'ts5',
    label: 'Safety-ограничение',
    story: 'В чеках регулярно алкоголь и табак. Эти категории — только guardrail, никогда не цель задания.',
    visits28: 9,
    medianGap: 3,
    avgCheck: 740,
    promoShare: 0.29,
    stmShare: 0.18,
    safetyFlag: true,
    fraudRisk: 0.05,
    league: { size: 24, place: 9, score: 290, nextPlace: 325, leader: 610 },
    referral: { invited: 0, qualified: 0, pending: 0 },
    stats: { streak: 3, saved: 940, level: 3, xp: 44 },
    candidates: {
      challenge:  { p0: 0.46, p1: 0.55, reward: 20, cmEvent: 230 },
      hotchance:  { p0: 0.46, p1: 0.51, reward: 0, cmEvent: 170 },
      league:     { p0: 0.46, p1: 0.50, reward: 25, cmEvent: 190 },
      stm:        { p0: 0.32, p1: 0.39, reward: 15, cmEvent: 150 },
    },
  },
  {
    id: 'NO_OFFER',
    name: 'Анна',
    avatarEmoji: '⛔',
    chain: 'ts5',
    label: 'Механика не окупается',
    story: 'Уже ходит очень часто и почти всегда покупает одно и то же. Награда оплатила бы покупку, которая случилась бы сама.',
    visits28: 14,
    medianGap: 2,
    avgCheck: 520,
    promoShare: 0.12,
    stmShare: 0.31,
    safetyFlag: false,
    fraudRisk: 0.02,
    league: { size: 24, place: 3, score: 520, nextPlace: 545, leader: 610 },
    referral: { invited: 1, qualified: 1, pending: 0 },
    stats: { streak: 9, saved: 1810, level: 4, xp: 71 },
    candidates: {
      challenge:  { p0: 0.86, p1: 0.88, reward: 20, cmEvent: 190 },
      hotchance:  { p0: 0.86, p1: 0.87, reward: 0, cmEvent: 160 },
      league:     { p0: 0.86, p1: 0.88, reward: 25, cmEvent: 175 },
      stm:        { p0: 0.74, p1: 0.76, reward: 15, cmEvent: 140 },
    },
  },
  {
    id: 'FRAUD_CASE',
    name: 'Дмитрий',
    avatarEmoji: '🚩',
    chain: 'tsch',
    label: 'Подозрительная активность',
    story: 'Пять чеков за восемь минут в одном магазине и всплеск приглашений с одного устройства.',
    visits28: 22,
    medianGap: 1,
    avgCheck: 210,
    promoShare: 0.44,
    stmShare: 0.25,
    safetyFlag: false,
    fraudRisk: 0.81,
    league: { size: 18, place: 2, score: 380, nextPlace: 395, leader: 400 },
    referral: { invited: 14, qualified: 1, pending: 13 },
    stats: { streak: 11, saved: 320, level: 2, xp: 29 },
    candidates: {
      challenge:  { p0: 0.42, p1: 0.56, reward: 20, cmEvent: 230 },
      hotchance:  { p0: 0.42, p1: 0.60, reward: 0,  cmEvent: 240 },
      league:     { p0: 0.42, p1: 0.52, reward: 18, cmEvent: 200 },
      stm:        { p0: 0.36, p1: 0.42, reward: 15, cmEvent: 150 },
    },
  },
];

/* ---------- Предгенерированные тексты механик ----------
   Роль LLM: только формулировка. Награду, категорию и
   экономику определяет движок, не языковая модель.        */
export const COPY = {
  challenge: {
    ts5:  { title: 'Три покупки за неделю', body: 'Три покупки до воскресенья — и баллы ваши. Подойдёт любая, даже за хлебом.', goal: 3 },
    tsch: { title: 'Две покупки до пятницы', body: 'Две покупки до пятницы — и забираете бонус. Как обычно ходите, так и ходите.', goal: 2 },
    tsx:  { title: 'Соберите ужин', body: 'Возьмите два продукта из подборки за одну покупку — соберётся целый ужин.', goal: 2 },
  },
  hotchance: {
    ts5:  { title: 'Горячий шанс', body: 'После покупки откроется подарок. Внутри — свежий продукт из вашего магазина, который надо забрать сегодня.' },
    tsch: { title: 'Улётная находка', body: 'Каждая покупка — бесплатная попытка выиграть продукт. Ничего доплачивать не нужно.' },
    tsx:  { title: 'Находка дня', body: 'Свежий продукт из вашего магазина — забрать нужно сегодня. Попытка бесплатная.' },
  },
  league: {
    ts5:  { title: 'Ваша лига', body: 'Небольшая группа соседей, которые ходят в магазин примерно как вы. Призы — лучшим за неделю.' },
    tsch: { title: 'Лига выгоды', body: 'Соревнуетесь с теми, у кого похожая корзина. Большой чек преимущества не даёт.' },
    tsx:  { title: 'Лига вкусов', body: 'Небольшая группа с похожим ритмом покупок. Призы — лучшим за неделю.' },
  },
  stm: {
    ts5:  { title: 'Сохрани рубли', body: 'Нашли вариант дешевле того, что вы обычно берёте. Попробуете?' },
    tsch: { title: 'Чистая выгода', body: 'То же самое, но дешевле. Разницу считаем честно — по цене за литр.' },
    tsx:  { title: 'Сохрани рубли', body: 'Сравнили с тем, что вы берёте обычно. Разница остаётся у вас.' },
  },
};

/* ---------- Симуляция (из docs/research/simulation) ---------- */
export const SIMULATION = {
  runs: [
    { n: 1000,  appUsers: 532,  expUsers: 446,  test: 221,  control: 225,
      visitsTest: 16.94, visitsControl: 18.40, upliftRel: -0.0793, netCm: -394.61 },
    { n: 10000, appUsers: 5501, expUsers: 5062, test: 2498, control: 2564,
      visitsTest: 19.15, visitsControl: 18.23, upliftRel: 0.0504, netCm: 142.15 },
  ],
  monteCarlo: [
    { n: 1000,  mean: 1.139, sd: 0.620, lo: 0.085, hi: 2.071 },
    { n: 10000, mean: 1.017, sd: 0.182, lo: 0.603, hi: 1.330 },
  ],
  scenarios: [
    { name: 'Conservative', dCm: 2.50,  rMax: 0,      selected: 0,   profit: 1.40,  lcb: -0.16, verdict: 'NO_CHALLENGE' },
    { name: 'Base',         dCm: 13.50, rMax: 22.19,  selected: 20,  profit: 6.44,  lcb: 0.50,  verdict: 'LAUNCH' },
    { name: 'Upside',       dCm: 44.10, rMax: 147.46, selected: 140, profit: 13.64, lcb: 1.41,  verdict: 'LAUNCH' },
  ],
};

/* ---------- Реферальная программа ---------- */
export const REFERRAL = {
  rewardInviter: 150,     // ₽ номинал приглашающему
  rewardInvitee: 100,     // ₽ номинал приглашённому
  qualifyMinCheck: 400,   // ₽ минимальный чек для квалификации
  qualifyWindowDays: 14,
  maxPerMonth: 5,
  // Экономика одного успешного приглашения
  newUserCm90d: 780,      // ₽ ожидаемая маржа нового покупателя за 90 дней
  pRetain: 0.42,          // доля приглашённых, которые остаются
};
