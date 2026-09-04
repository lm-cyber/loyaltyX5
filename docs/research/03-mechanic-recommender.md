# Рекомендатель игровой механики для proof of concept X5

**Причинно корректная архитектура, utility-функция, инженерный контракт и дорожная карта до пилота**

*Исследование и инженерная спецификация · 4 сентября 2026 года*

## Содержание

- [План исследования](#план-исследования)
- [1. Executive decision](#1-executive-decision)
- [2. Карта доказательств](#2-карта-доказательств)
- [3. Матрица подходов](#3-матрица-подходов)
- [4. Action catalog](#4-action-catalog)
- [5. Feature specification](#5-feature-specification)
- [6. Utility function](#6-utility-function)
- [7. Алгоритм PoC](#7-алгоритм-poc)
- [8. Контракт решения](#8-контракт-решения)
- [9. Объяснения](#9-объяснения)
- [10. Синтетические примеры решений](#10-синтетические-примеры-решений)
- [11. Оценка](#11-оценка)
- [12. План эволюции](#12-план-эволюции)
- [13. Аудит «Двора»](#13-аудит-двора)
- [14. Fairness и privacy](#14-fairness-и-privacy)
- [15. Реестр параметров](#15-реестр-параметров)
- [16. Источники](#16-источники)
- [Контроль качества перед реализацией](#контроль-качества-перед-реализацией)

**Аудитория:** продуктовая команда, data science, ML engineering, аналитика экспериментов, экономика лояльности, antifraud, privacy и safety
**Область:** персональный челлендж, личный прогресс/аватар, кооперативный «Двор», анонимная лига, реферальное приглашение и `NO_INTERVENTION`

> Этот документ проектирует систему, а не утверждает наличие причинного эффекта у X5. История новых механик и реальные randomized treatment logs не предоставлены; поэтому численные эффекты PoC являются только сценариями. Ни одно число из рабочего концепта «Двора» не считается правилом X5 без отдельного источника или пилота.

# План исследования

1.  Зафиксировать границу доказательности: что можно честно решить на синтетических данных, а что требует рандомизированных показов и зрелых бизнес-исходов.
2.  Сопоставить rules/scorecard, supervised ranking, uplift/CATE, contextual bandit и гибрид по causal validity, объяснимости, cold start, данным и операционному риску.
3.  Спроектировать action catalog, feature contract, utility в рублях, hard gates, `NO_INTERVENTION`, псевдокод и immutable decision log.
4.  Отдельно разобрать «Двор» как систему с interference, групповыми внешними эффектами, opt-in, приватностью и устойчивостью состава.
5.  Определить offline sanity checks, shadow mode, randomized pilot, off-policy evaluation и безопасный переход к causal policy learning/bandit.
6.  Проверить единицы, availability-at-decision-time, leakage, fairness, privacy, antifraud и согласованность с экономикой.

# 1. Executive decision

## 1.1 Рекомендуемое решение

**\[INFERENCE\] Рекомендация для текущего PoC:** использовать гибридную политику `hard eligibility and safety rules → прозрачный robust utility scorecard → явный порог воздержания → NO_INTERVENTION`, а LLM допускать только к формулировке текста из проверенных reason codes.

**\[FACT\]** В пакете проекта прямо указано, что PoC работает на синтетике и не имеет исторических рандомизированных показов новых механик. Следовательно, synthetic response labels нельзя выдавать за наблюдённый causal uplift.

**\[INFERENCE\]** Политика PoC должна оптимизировать не `CTR`, не вероятность принятия и не completion rate, а нижнюю сценарную оценку чистой дополнительной вкладной маржи в рублях за заранее определённый горизонт. Completion-модель разрешена как вспомогательная: оценивать релевантность, вероятность возникновения reward liability и fatigue, но не служить доказательством инкрементальности.

**\[INFERENCE\] Рекомендация после пилота:** собирать multi-arm randomized logs, включая `NO_INTERVENTION`, затем строить doubly robust reward scores, multi-arm CATE и ограниченную интерпретируемую policy. Contextual bandit добавлять только после независимой offline/shadow-проверки, с ограниченным exploration, baseline fallback, бюджетными ограничениями и задержкой обучения до созревания маржинального outcome.

## 1.2 Архитектура в одной строке

```text
feature snapshot as-of decision time
→ versioned action candidates
→ hard eligibility / safety / privacy / antifraud / budget gates
→ component-wise utility estimate in RUB
→ uncertainty penalty and abstention threshold
→ chosen action or NO_INTERVENTION
→ faithful reason codes and customer-safe template
→ immutable log with propensity, policy version and delayed outcomes
```

## 1.3 Почему это решение честно

- **\[FACT\]** Causal policy learning оценивает различия между потенциальными исходами действий, а наблюдаемая вероятность покупки или выполнения описывает только один фактически увиденный исход. Работы по policy learning и CATE требуют рандомизации либо сильных предположений об отсутствии неизмеренного confounding, overlap/positivity и корректной фиксации контекста ([Athey & Wager, 2021](https://doi.org/10.3982/ECTA15732); [Hernán & Robins, 2020](https://miguelhernan.org/whatifbook)).
- **\[FACT\]** Multi-action policy learning может учитывать бюджеты и ограниченные классы политик, но опирается на propensity и doubly robust/AIPW reward estimates; это не способ создать causal labels из сценарной симуляции ([Zhou, Athey & Wager, 2023](https://doi.org/10.1287/opre.2022.2271)).
- **\[INFERENCE\]** Поэтому в PoC численные `expected_incremental_margin` должны иметь статус `ASSUMPTION` или `TO_VALIDATE`, храниться как low/base/high, а интерфейс не должен называть их «доказанным uplift».
- **\[INFERENCE\]** `NO_INTERVENTION` — не fallback из-за ошибки, а полноценное действие с utility, равной нулю по определению. Оно выигрывает, когда все другие действия запрещены, убыточны или слишком неопределённы.

## 1.4 Версии политики

| **Стадия**  | **Политика**                                                      | **Допустимые данные**                                                          | **Что можно утверждать**                                                        | **Критерий перехода**                                                                                   |
|-------------|-------------------------------------------------------------------|--------------------------------------------------------------------------------|---------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| PoC v0      | Rules + robust scorecard + no-action                              | Синтетические чеки, синтетические события, проектные low/base/high             | Связность логики, соблюдение ограничений, сценарная экономика; не causal uplift | Все invariants проходят; shadow-ready contract; согласованы owner-ы параметров                          |
| Pilot v1    | Randomized multi-arm policy; для «Двора» cluster/two-stage design | Реальные decision logs, eligible set, assignment probability, matured outcomes | Intention-to-treat эффект и policy value в экспериментальной популяции          | Overlap, достаточный effective sample size, положительная нижняя граница net margin, guardrails в норме |
| Learning v2 | DR/AIPW + multi-arm CATE + shallow policy tree                    | Randomized или обоснованно ignorable logs, holdout, nuisance models            | Гетерогенность и ценность ограниченной политики с uncertainty                   | Стабильность на новых временных/географических holdout; safe policy improvement                         |
| Online v3   | Conservative contextual bandit with budget/resource constraints   | Онлайн propensity, delayed rewards, baseline policy, monitoring                | Контролируемое exploration при сохранении safety и бюджета                      | Положительный high-confidence lower bound; rollback проверен; mature outcome feedback                   |

## 1.5 Решение по каждому классу методов

- **\[INFERENCE\] Rules/scorecard — использовать сейчас.** Они не становятся causal от прозрачности, но честно выражают допущения и позволяют гарантировать hard constraints.
- **\[INFERENCE\] Propensity/completion model — использовать только как компонент.** Он помогает не показывать заведомо нерелевантное и оценить reward liability; ранжировать только по completion нельзя.
- **\[INFERENCE\] Uplift/CATE — отложить до пилота.** Наилучший первый кандидат после пилота — doubly robust multi-arm estimation с интерпретируемой policy, а не необъяснимый индивидуальный «uplift score».
- **\[INFERENCE\] Contextual bandit — не нужен для хакатонного PoC.** Его ценность появляется при повторяющихся решениях, достаточном трафике, наблюдаемом delayed reward и возможности безопасной рандомизации.
- **\[INFERENCE\] LLM — renderer, не decision maker.** Он не меняет action, числа, reason codes, eligibility, budget или fraud status.

## 1.6 Условия остановки или упрощения

**\[TO_VALIDATE\]** «Двор» следует упростить до добровольного non-monetary social progress или остановить, если пилот показывает хотя бы одно из следующего: отрицательную нижнюю границу group-level net margin; рост opt-out/complaints; нестабильность состава; систематическое исключение малых магазинов; невозможность обеспечить приватность; или spillover, делающий индивидуальную рандомизацию неинтерпретируемой.

# 2. Карта доказательств

## 2.1 Causal treatment selection и policy learning

| **Метод**                            | **Проблема**                                                             | **Требования к данным**                                                         | **Ограничения**                                                                                                     | **Источник / выборка**                                      | **Статус** |
|--------------------------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|------------|
| Propensity score                     | Баланс наблюдаемых ковариат при observational treatment assignment       | Action, outcome, pre-treatment X; overlap; измерены все confounders             | Не устраняет hidden confounding; не создаёт overlap; бинарная исходная постановка                                   | Rosenbaum & Rubin, 1983; методологическая теория            | FACT       |
| DML / orthogonal scores              | Снижает bias от гибких nuisance models                                   | Корректный causal design, pre-treatment X, cross-fitting                        | Не исправляет неправильный estimand, hidden confounding или leakage                                                 | Chernozhukov et al., 2018; теория + 3 эмпирических примера  | FACT       |
| R-learner                            | Оценка heterogeneous treatment effect через residualization              | Outcome и propensity nuisance models; observational ignorability или experiment | В статье основная эмпирика — simulations; не multi-arm business policy «из коробки»                                 | Nie & Wager, 2021; simulation setups                        | FACT       |
| Causal forest / GRF                  | Нелинейная гетерогенность CATE и честное разделение estimation/splitting | Treatment, outcome, pre-treatment covariates; overlap; honesty/cross-fitting    | CATE не равен оптимальной policy; индивидуальная ground truth ненаблюдаема; чувствителен к support                  | Wager & Athey, 2018; Athey, Tibshirani & Wager, 2019        | FACT       |
| S/T/X meta-learners                  | Гибкие CATE-оценки, в том числе при дисбалансе arms                      | Эксперимент или ignorable observational data                                    | Ни один meta-learner не лучший всегда; демонстрации включали simulations и 2 political field experiments, не retail | Künzel et al., 2019                                         | FACT       |
| Empirical welfare maximization       | Прямой выбор treatment rule под welfare и capacity constraints           | Known/estimated propensity; policy class; utility outcome                       | Требует валидной causal reward; компромисс между богатством policy class и variance                                 | Kitagawa & Tetenov, 2018; теория + National JTPA experiment | FACT       |
| Observational policy learning        | Оптимизация ограниченной policy на observational data                    | Unconfoundedness, overlap, doubly robust scores, фиксированный policy class     | Название «observational» не отменяет сильных assumptions; hidden confounding остаётся                               | Athey & Wager, 2021                                         | FACT       |
| Offline multi-action policy learning | Выбор из нескольких действий при budget/restricted tree policy           | Multi-arm propensities, outcomes, covariates, AIPW rewards                      | Нужны поддержка каждого действия и стабильные treatment definitions; вычислительная сложность деревьев              | Zhou, Athey & Wager, 2023                                   | FACT       |

**\[INFERENCE\] Вывод для X5 PoC:** перечисленные методы определяют правильную архитектуру логирования и будущего анализа, но не дают оснований обучать causal recommender на вымышленных treatment labels.

## 2.2 Logged bandit feedback, OPE и exploration

| **Метод**                           | **Проблема**                                                                 | **Требования**                                                                       | **Ограничения**                                                                                                | **Источник / выборка**                                                        | **Статус** |
|-------------------------------------|------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|------------|
| Replay                              | Оценка новой contextual-bandit policy по randomized logs                     | Известная random logging policy, доступные actions, совпадение выбранного action     | Отбрасывает несовпавшие события; при низком overlap effective sample size падает; обычные CRM logs не подходят | Li et al., WSDM 2011; около 40 млн Yahoo! events, примерно 20 articles в pool | FACT       |
| Doubly robust OPE                   | Комбинирует reward model и behavior-policy model                             | Action propensity и outcome model                                                    | «Doubly robust» не означает неуязвимость: плохие обе модели или lack of overlap дают bias/variance             | Dudík, Langford & Li, ICML 2011; empirical comparisons                        | FACT       |
| Counterfactual risk minimization    | Batch policy learning с variance-aware propensity weighting                  | Logged bandit data и propensities                                                    | Тяжёлые importance weights; результаты на multi-label benchmarks, не grocery margin                            | Swaminathan & Joachims, ICML 2015                                             | FACT       |
| Contextual bandit oracle reductions | Exploration/exploitation для большого action space                           | Онлайн контекст, выбранный action, probability, быстрый reward                       | Теоретические regret guarantees не являются бизнес safety guarantee                                            | Agarwal et al., ICML 2014; Foster & Rakhlin, ICML 2020                        | FACT       |
| Conservative bandit                 | Сохранение performance выше доли baseline во времени                         | Надёжная baseline policy, confidence bounds, линейная reward model в исходной работе | Model assumptions; baseline itself может быть плохим; требуется online monitoring                              | Kazerouni et al., NeurIPS 2017                                                | FACT       |
| Bandits with knapsacks              | Exploration при нескольких бюджетах/ресурсах                                 | Reward и resource consumption по action                                              | Абстрактная stochastic model; не заменяет финансовый ledger и hard safety checks                               | Badanidiyuru, Kleinberg & Slivkins, FOCS 2013 / revised 2017                  | FACT       |
| Delayed feedback                    | Обучение, когда reward приходит позже действия                               | Decision timestamp, outcome maturity, censoring/lag tracking                         | Нельзя обновляться на незрелом outcome без bias; задержки ухудшают learning rate                               | Joulani, György & Szepesvári, ICML 2013                                       | FACT       |
| High-confidence policy improvement  | Деплой только при положительной lower confidence bound относительно baseline | Независимый evaluation set, bounded/controlled variance                              | Консервативность может замедлить улучшение; гарантия зависит от assumptions                                    | Thomas et al., ICML 2015; SPIBB family                                        | FACT       |

**\[INFERENCE\] Вывод для X5:** PoC должен уже сейчас логировать `eligible_actions`, `chosen_action`, `assignment_probability` и `policy_version`. Без propensity будущая OPE будет либо невозможна, либо зависеть от ненадёжной реконструкции behavior policy.

## 2.3 Interference, fairness, privacy и faithful explanation

| **Метод/принцип**            | **Что решает**                                                           | **Данные/условия**                                               | **Ограничения**                                                                                  | **Источник**                                                   | **Статус** |
|------------------------------|--------------------------------------------------------------------------|------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|----------------------------------------------------------------|------------|
| Partial/general interference | Исход одного участника зависит от treatment других                       | Group/network membership, exposure mapping, design probabilities | Неправильная exposure model меняет estimand; обычный user-level A/B может быть biased            | Hudgens & Halloran, JASA 2008; Aronow & Samii, AOAS 2017       | FACT       |
| Graph-cluster randomization  | Снижает contamination при network spillovers                             | Граф/кластеры и вероятность network exposure                     | Unbiasedness зависит от корректной exposure model; variance может быть высокой                   | Ugander et al., KDD 2013                                       | FACT       |
| Randomized saturation        | Разделяет direct и spillover effects                                     | Clusters и несколько случайных saturation levels                 | Сложнее operationally и по power; требует predeclared estimands                                  | Baird et al., Review of Economics and Statistics, 2018         | FACT       |
| Feedback-loop analysis       | Показывает, как обучение на собственных рекомендациях искажает поведение | Repeated recommendation logs; exposure-aware evaluation          | Работа демонстрирует механизм в simulations, не оценивает X5                                     | Chaney, Stewart & Engelhardt, RecSys 2018                      | FACT       |
| Interpretable policy         | Faithful auditability вместо post-hoc истории                            | Shallow tree/rules or explicit scorecard                         | Интерпретируемость не гарантирует causal validity или fairness                                   | Rudin, Nature Machine Intelligence 2019; policytree docs       | FACT       |
| k-anonymity                  | Снижает риск re-identification по quasi-identifiers в релизе данных      | Определённые quasi-identifiers и equivalence classes             | Не защищает от attribute disclosure и background knowledge; не является полной privacy guarantee | Sweeney, 2002; Machanavajjhala et al., 2006/2007               | FACT       |
| Group fairness metrics       | Измеряет различия ошибок/доступа между группами                          | Audit attributes и ground truth/outcome                          | Метрики могут конфликтовать; статистическое равенство не заменяет socio-technical анализ         | Hardt, Price & Srebro, NeurIPS 2016; Selbst et al., FAccT 2019 | FACT       |
| AI risk management           | Govern-map-measure-manage lifecycle и документирование рисков            | Roles, controls, measurements, incident process                  | Voluntary general framework; не специфичен для российского retail                                | NIST AI RMF 1.0, 2023; revision underway in 2026               | FACT       |

## 2.4 Публичные retail cases: что они доказывают и чего не доказывают

| **Кейс/линия**                 | **Что поддерживает**                                                        | **Дата/масштаб**                                                                                             | **Ограничение переноса**                                                                                                         | **Источник**                                                        | **Статус**  |
|--------------------------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|-------------|
| Tesco Clubcard Challenges      | Operational feasibility персонализированных challenge campaigns             | Официально запущено 20 мая 2024; кампания 6 недель; пользователю предлагались персонализированные challenges | Официальные материалы не раскрывают randomized control, net incremental margin или causal methodology                            | Tesco, 29.04.2024; последующие trading/results statements 2025–2026 | FACT        |
| Tesco / Eagle Eye case         | Масштаб и engagement funnel                                                 | Поставщик сообщает 10 млн targeted; 76% visitors→players; 62% players→first reward; 4 кампании по 6 недель   | Vendor case; denominators начинаются с посетителей страницы/игроков; это не uplift и не net margin; selection bias возможен      | Eagle Eye case study, доступ 2026                                   | FACT        |
| Morrisons My Points Boosters   | Operational feasibility AI-personalized brand challenges и supplier funding | Официальный анонс trial 16.04.2024; выбор до 10 брендов, spend milestones                                    | Нет опубликованного causal effect, sample size или business-margin methodology                                                   | Morrisons corporate release, 16.04.2024                             | FACT        |
| Carrefour                      | В рабочем концепте упомянут как аналог                                      | Публичного первичного источника с достаточной методикой в этом исследовании не найдено                       | Не использовать как доказательство величины эффекта или sales-to-reward                                                          | Evidence gap                                                        | TO_VALIDATE |
| Köhler effect / social loafing | Гипотеза о мотивации слабого участника и риске снижения усилий              | Meta-analysis motivation gains: 17 studies, N=2,240; social loafing meta-analysis: 78 studies                | Задачи, лабораторные/организационные контексты и moderators не совпадают с grocery loyalty; нельзя переносить фиксированные +25% | Weber & Hertel, 2007; Karau & Williams, 1993                        | FACT        |

**\[INFERENCE\] Итог:** retail cases поддерживают реализуемость персонализированных, supplier-funded и прогресс-ориентированных механик, но не дают X5 переносимого коэффициента uplift. Коэффициенты response, margin, cannibalization и group spillover должны пройти собственный randomized pilot.

# 3. Матрица подходов

| **Подход**                                  | **Causal validity**                                                  | **Cold start**                                     | **Explainability**                               | **Sample need**                                      | **Operational risk**                                                  | **Решение**                                              |
|---------------------------------------------|----------------------------------------------------------------------|----------------------------------------------------|--------------------------------------------------|------------------------------------------------------|-----------------------------------------------------------------------|----------------------------------------------------------|
| Eligibility rules + scorecard               | Низкая как estimator; высокая честность при явных assumptions        | Да: может дать non-monetary fallback               | Очень высокая                                    | Нет causal sample; нужны domain parameters           | Rule explosion, ручные веса, ложная точность                          | Использовать в PoC как policy skeleton и hard-gate layer |
| Supervised propensity/completion ranking    | Нет: прогнозирует observed outcome, не counterfactual difference     | Средняя; можно обучать на старых engagement labels | Средняя/высокая при calibrated model             | Нужны зрелые labels принятия/выполнения              | Sure-thing targeting, reward cannibalization, feedback loops          | Только вспомогательный nuisance/component model          |
| Uplift/CATE                                 | Высокая при randomized/ignorable data, overlap и корректном estimand | Слабая без pooled/hierarchical priors              | Средняя; лучше с shallow policy поверх DR scores | Высокая; особенно для many arms и rare outcomes      | Noisy individual effects, support gaps, hidden confounding            | После пилота; начинать с DR multi-arm + policy tree      |
| Contextual bandit                           | Онлайн causal learning при корректном randomized exploration         | Средняя через priors/baseline                      | Средняя; policy log обязателен                   | Постоянный трафик и быстрый/правильно delayed reward | Exploration loss, budget overspend, nonstationarity, delayed feedback | Только поздняя стадия, conservative и constrained        |
| Hybrid: gates + utility/CATE + LLM renderer | Соответствует causal maturity данных                                 | Высокая                                            | Высокая при component ledger и reason codes      | Постепенно растёт от PoC к pilot                     | Сложность контракта и governance                                      | Рекомендуемая целевая архитектура                        |

## 3.1 Почему completion ranking выбирает «того, кто и так купил бы»

Пусть `P(C=1 | X, A=a)` — вероятность completion при показе действия `a`. Высокое значение может возникнуть у очень активного покупателя, чья вероятность покупки без вмешательства также высока. Для решения нужен контраст:

```text
CATE_a(x) = E[Y(a) - Y(NO_INTERVENTION) | X=x]
```

**\[FACT\]** Наблюдаемая покупка после показа не раскрывает ненаблюдаемый исход того же человека без показа. Это фундаментальная проблема causal inference.

**\[INFERENCE\]** Поэтому high-baseline user может иметь `completion=0.9`, но отрицательную net utility: награда выплачивается за поведение, которое почти наверняка случилось бы и так. В PoC это отражается консервативным cannibalization scenario и reason code `HIGH_BASELINE_PURCHASE_PROPENSITY`; после пилота — randomized no-action contrast.

## 3.2 Роль supervised models в целевой системе

- **\[INFERENCE\] Baseline purchase model:** оценивает вероятный outcome без нового воздействия; используется как nuisance и индикатор sure-thing risk, но не как causal truth.
- **\[INFERENCE\] Acceptance/completion model:** помогает прогнозировать reward settlement и UX relevance.
- **\[INFERENCE\] Fraud model:** оценивает вероятность и ожидаемый loss; blocking threshold остаётся precision-first и отдельно управляется antifraud.
- **\[INFERENCE\] Churn/fatigue model:** только guardrail; не использовать для манипулятивного давления.
- **\[INFERENCE\] CATE/policy model:** появляется после pilot logs и оптимизирует causal utility, а не клики.

# 4. Action catalog

## 4.1 Принцип определения action

**\[INFERENCE\]** Action должен быть версионированным treatment, а не свободным текстом. Любое изменение длительности, reward rule, social visibility или qualification event создаёт новую `action_version` либо заранее объявленный parameter bucket. Иначе несколько разных воздействий смешиваются в один label и причинная интерпретация разрушается.

**\[INFERENCE\]** За один decision epoch пользователю назначается максимум одно incentivized primary action. Аватар может быть пассивным non-monetary overlay только внутри явно заданной комбинации. Скрытая динамическая сборка «челлендж + реферал + лига» запрещена.

## 4.2 Каталог

| **Action ID**                | **Смысл**                                                                 | **Eligibility**                                                                                        | **Экономика**                                                      | **Cooldown/cap**                             | **Fallback**                             |
|------------------------------|---------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|----------------------------------------------|------------------------------------------|
| A0 `NO_INTERVENTION`         | Не показывать новую механику; сохранить обычный продуктовый опыт          | Всегда                                                                                                 | Нет                                                                | Cooldown не создаёт                          | Fallback по умолчанию; control arm       |
| A1 `PERSONAL_CHALLENGE`      | Один достижимый challenge с безопасной категорией/поведением              | Есть history либо безопасный cold-start template; consent; положительный robust utility                | Опционально monetary; max liability известна до показа             | После завершения/истечения + policy cooldown | Если category unsafe/unknown → A2 или A0 |
| A2 `AVATAR_PROGRESS_ONLY`    | Неденежный личный progress/XP без покупки чувствительной категории        | App user; визуальная механика доступна; нет UX fatigue                                                 | Нет денежной liability                                             | Frequency cap на prompts                     | Cold-start и fraud-safe fallback         |
| A3 `CHALLENGE_PLUS_AVATAR`   | Явно заданная комбинация A1 с визуальным progress                         | Оба компонента eligible; одна общая цель и один reward contract                                        | Как у A1                                                           | Единый cooldown                              | Не добавлять другие primary actions      |
| A4 `YARD_JOIN_OFFER`         | Добровольное приглашение в подходящую анонимную группу                    | Explicit social opt-in; достаточный pool; slot; начало/граница цикла; privacy checks                   | Обычно non-monetary на этапе join                                  | Не повторять после отказа до cooldown        | A1/A2/A0; никакого автозачисления        |
| A5 `YARD_MEMBER_CHALLENGE`   | Персональный challenge, вклад которого агрегируется в существующий «Двор» | Активное membership; стабильный состав; group cycle не закрывается; group-level utility неотрицательна | Reward liability на user и yard budget                             | Не более одного challenge на цикл            | A2 или A0; не ломать group state         |
| A6 `ANONYMOUS_LEAGUE_OPT_IN` | Приглашение в крупную анонимную лигу без ФИО/адреса                       | Explicit opt-in; minimum cohort; pseudonym; no public sensitive contribution                           | По умолчанию non-monetary в PoC                                    | Cooldown после decline/exit                  | A2/A0                                    |
| A7 `REFERRAL_INVITE`         | Приглашение с наградой после квалифицирующего поведения invitee           | Consent; cap; low fraud risk; no active referral cooldown; qualification defined                       | Committed max liability; settlement after anti-fraud/return window | Invite and reward caps                       | A1/A2/A0; high fraud → A0/A2             |

## 4.3 Hard constraints

**\[INFERENCE\]** Ни одна модель и ни один LLM не могут переопределить следующие gates:

1.  consent/opt-in и communication permissions;
2.  запрещённые или чувствительные категории и harmful-consumption policy;
3.  reward budget, per-user/per-action caps и максимальная обещанная liability;
4.  antifraud block/review status и возвратное окно;
5.  cooldown, frequency cap, active-action conflict;
6.  privacy: no exact address/name, minimum anonymity cohort, suppression rules;
7.  «Двор»: slot, cycle boundary, membership freeze, group stability и group-level harm gate;
8.  experiment assignment и holdout integrity.

## 4.4 Конфликт одновременно доступных механик

**\[INFERENCE\] Порядок:**

```text
hard constraints
→ existing contractual/group commitments
→ positive robust utility
→ uncertainty
→ lower customer burden
→ lower reward liability
→ deterministic tie-breaker by action_id
```

- Активный незавершённый challenge блокирует новый incentivized action.
- `YARD_MEMBER_CHALLENGE` не получает безусловный приоритет: если group externality или pressure risk отрицательны, выбирается A2/A0.
- Отказ от social format запрещает A4/A5/A6/A7 независимо от predicted response.
- При равной нижней utility выбирается действие с меньшей liability и меньшей нагрузкой.
- При ошибке feature service, model service, budget service или explanation validator — `NO_INTERVENTION`, а не «следующий рискованный кандидат».

# 5. Feature specification

## 5.1 Общие правила

- **\[INFERENCE\]** Все признаки вычисляются `as_of(decision_ts)` и хранятся в immutable feature snapshot.
- **\[INFERENCE\]** Каждая агрегация использует закрытое слева временное окно: событие в момент или после решения не входит.
- **\[INFERENCE\]** Missingness является явным состоянием; `0` и `unknown` не смешиваются.
- **\[INFERENCE\]** Возраст, пол, тип поселения и регион по умолчанию не входят в decision score. Они могут использоваться только для агрегированного fairness audit при наличии правового основания и минимизации данных.
- **\[INFERENCE\]** `store_id` нужен для operational eligibility «Двора», но не выводится пользователю и не используется как proxy ценности человека.

## 5.2 Поведение и экономика

| **Feature**                     | **Источник / окно / формула**                                   | **Availability и missing**               | **Назначение / риск**                                           |
|---------------------------------|-----------------------------------------------------------------|------------------------------------------|-----------------------------------------------------------------|
| `visits_28d`                    | receipts; count distinct receipt_id in \[t-28d,t)               | Да; 0 допустим                           | Активность, достижимость; не causal                             |
| `visits_84d`                    | receipts; 84d count                                             | Да; 0 допустим                           | Стабильность baseline                                           |
| `recency_days`                  | t - max(matured purchase ts)                                    | Unknown при no history                   | Reactivation/uncertainty                                        |
| `median_interpurchase_days_84d` | median gap между matured receipts                               | Unknown при \<2 visits                   | Achievability, cooldown                                         |
| `visit_daypart_entropy_84d`     | entropy по daypart; coarse bins                                 | Unknown при малой истории                | Необязательная устойчивость паттерна; не объяснять пользователю |
| `contribution_margin_84d_rub`   | sum item/category margin proxy after discounts, returns matured | Unknown → conservative                   | Baseline economics; PUBLIC_PROXY/TO_VALIDATE                    |
| `margin_per_visit_84d_rub`      | margin / max(visits,1)                                          | Unknown при 0 visits                     | Reward affordability                                            |
| `promo_share_84d`               | promo item spend / total spend                                  | Unknown при no spend                     | Cannibalization scenario; не использовать для harmful targeting |
| `category_entropy_84d`          | entropy по broad safe categories                                | Unknown при no items                     | Challenge diversity; sensitive categories excluded              |
| `baseline_purchase_prob_H`      | time-split calibrated model for no-new-action outcome           | Unknown/model failure → high uncertainty | Sure-thing guardrail; не uplift                                 |

## 5.3 Engagement, fatigue и history of treatment

| **Feature**                         | **Источник / окно**                 | **Availability и missing**     | **Назначение / риск**                         |
|-------------------------------------|-------------------------------------|--------------------------------|-----------------------------------------------|
| `app_sessions_28d`                  | app events before t                 | 0 или unknown раздельно        | Канал доступен; не proxy «любви к игре»       |
| `mechanic_exposures_28d[action]`    | decision/show logs by action family | Обязательно                    | Frequency cap, feedback-loop control          |
| `mechanic_accepts_84d[action]`      | prior matured accepts               | Unknown при no exposure        | Auxiliary relevance model                     |
| `mechanic_completions_180d[action]` | prior matured completion only       | Unknown при no exposure        | Reward liability; не causal uplift            |
| `days_since_last_action[action]`    | t - last eligible show/assignment   | ∞ при never                    | Cooldown                                      |
| `active_action_id`                  | contract state at t                 | Null допустим                  | Conflict gate                                 |
| `opt_out_gameplay`                  | explicit preference                 | Unknown treated conservatively | Hard exclusion                                |
| `social_opt_in`                     | explicit separate consent           | False/unknown blocks social    | Hard eligibility                              |
| `complaint_or_hide_90d`             | user feedback before t              | False/unknown                  | Fatigue/harm gate; no sensitive text features |

## 5.4 Reward, fraud и operational state

| **Feature**                           | **Источник / формула**                              | **Availability и missing**                 | **Назначение**                             |
|---------------------------------------|-----------------------------------------------------|--------------------------------------------|--------------------------------------------|
| `reward_liability_open_rub`           | ledger of promised but unsettled rewards at t       | Обязательно; fail-closed                   | Hard user/budget cap                       |
| `reward_cost_expected_rub[action]`    | settlement probability × economic unit cost         | Scenario/model + uncertainty               | Utility component; не вместо max liability |
| `reward_liability_max_rub[action]`    | maximum promised face-value/economic liability      | Known deterministically                    | Hard budget gate                           |
| `returns_matured_84d`                 | returns whose observation window closed before t    | Unknown → conservative                     | Economics/fraud; no future returns         |
| `fraud_risk_score`                    | pre-decision graph/device/payment/velocity features | Service failure → monetary actions blocked | Expected loss and block/review             |
| `fraud_reason_codes`                  | precision-first rule/model output                   | Required when score nonzero                | Audit and appeal                           |
| `budget_remaining_rub[action/cohort]` | real-time committed-liability ledger                | Service failure → action unavailable       | Hard gate                                  |
| `experiment_cell`                     | preassigned immutable cell                          | Required in pilot                          | Holdout integrity                          |
| `assignment_probability`              | probability under logging policy                    | 1.0 deterministic PoC; known \>0 pilot     | OPE/causal learning                        |

## 5.5 Состояние «Двора»

| **Feature**                             | **Источник / формула**                                  | **Availability**                    | **Назначение / риск**                      |
|-----------------------------------------|---------------------------------------------------------|-------------------------------------|--------------------------------------------|
| `home_store_id_token`                   | dominant store from prior receipts; internal token      | Unknown blocks auto-match           | Pool lookup only; not displayed            |
| `yard_pool_size_eligible`               | count opted-in eligible users in privacy-safe pool at t | Exact current value                 | Minimum-pool gate; not a privacy guarantee |
| `yard_membership_status`                | none/invited/active/exiting                             | Required                            | Conflict and stability                     |
| `yard_open_slots`                       | capacity - active committed members                     | Required                            | Join eligibility                           |
| `yard_cycle_day` / `days_remaining`     | versioned cycle clock                                   | Required                            | No late join / treatment definition        |
| `yard_goal_remaining_rub`               | group aggregate; no individual public contribution      | Required for active yard            | Group state; customer-safe aggregate       |
| `yard_frequency_ratio_max`              | max frequency bin / min frequency bin                   | Unknown blocks auto-match           | Balance assumption; broad bins only        |
| `yard_membership_changes_last_2_cycles` | join/leave count                                        | Required                            | Stability/harm gate                        |
| `yard_group_fraud_risk`                 | aggregated graph/receipt risk                           | Unknown blocks monetary yard reward | Group loss                                 |
| `yard_externality_scenario_rub`         | low/base/high effect on other members                   | ASSUMPTION before cluster pilot     | Group-level utility                        |

## 5.6 Запрещённые и leakage-признаки

| **Признак/поле**                                            | **Почему недопустим**               | **Риск**                                                 |
|-------------------------------------------------------------|-------------------------------------|----------------------------------------------------------|
| Покупки, клики, progress или completion после `decision_ts` | Будущее относительно решения        | Target leakage; завышенная offline quality               |
| Возврат/отмена, решение fraud review после `decision_ts`    | Post-treatment outcome              | Treatment leakage; использовать только как delayed label |
| Текст, сгенерированный LLM после выбора                     | Следствие action                    | Circular explanation/prediction                          |
| Индивидуальный вклад других членов «Двора» после решения    | Post-treatment + interference       | Неверное приписывание эффекта                            |
| ФИО, точный адрес, контакты, точный геотрек                 | Не нужны для решения                | Privacy и дисквалифицирующее ограничение кейса           |
| Чувствительные категории как причина таргетинга/объяснения  | Риск вреда и раскрытия              | Proxy discrimination, harmful consumption                |
| Возраст/пол/село-город в production score по умолчанию      | Audit-only                          | Стереотипизация и proxy discrimination                   |
| Synthetic `is_fraud` ground truth                           | Генератор знает label, политика нет | Прямой leakage                                           |

# 6. Utility function

## 6.1 Causal estimand целевой стадии

Для пользователя `u`, действия `a` и горизонта `H`:

```text
τ_a(x; H) = E[NetContributionMargin^a_H - NetContributionMargin^A0_H | X=x]
```

**\[FACT\]** Это counterfactual contrast, а не вероятность покупки. В PoC `τ_a` не идентифицирован; допустима только сценарная proxy `τ̃_a` со статусом `ASSUMPTION/TO_VALIDATE`.

## 6.2 Компонентная формула

Определим все компоненты в **рублях на одного eligible пользователя за один decision horizon H**:

```text
U(u,a;H) =
    CM_added_visits
  + CM_added_basket
  - CM_cannibalized_or_shifted
  - Reward_cost_expected
  - Variable_delivery_cost
  - Fraud_loss_expected
  - Fatigue_or_optout_cost
  + Group_externality
  - Uncertainty_penalty
```

где:

- `CM_added_visits` — вкладная маржа дополнительных визитов;
- `CM_added_basket` — дополнительная вкладная маржа внутри визитов;
- `CM_cannibalized_or_shifted` — потеря маржи из-за награждения baseline-покупок, перехода на менее маржинальный mix или переноса покупки между периодами;
- `Reward_cost_expected` — ожидаемая экономическая стоимость реально settled reward;
- `Variable_delivery_cost` — переменные расходы канала/операции;
- `Fraud_loss_expected = P(successful abuse | pre-decision data) × Loss_if_success`;
- `Fatigue_or_optout_cost` — ожидаемая будущая потеря от лишнего контакта, жалобы или отказа;
- `Group_externality` — сумма изменения outcomes других затронутых участников; может быть отрицательной;
- `Uncertainty_penalty` — консервативная надбавка за неопределённость.

**\[INFERENCE\] Правило против double counting:** если causal outcome уже определён как realized contribution margin после промо и product mix, cannibalization не вычитается второй раз. В PoC рекомендуется хранить ledger-компоненты отдельно и собирать `U` только одной утверждённой формулой.

## 6.3 Uncertainty и abstention

До пилота:

```text
U_robust = min(U_low, U_base, U_high)     # recommended PoC default
```

или, при наличии статистически интерпретируемой ошибки после пилота:

```text
U_LCB = E[U] - κ × SE(U)
```

**\[ASSUMPTION\]** `κ` и минимальный safety margin `δ` — governance parameters, а не научные константы.

```text
choose a only if U_robust(a) ≥ δ; otherwise choose A0
```

**\[INFERENCE\]** На ранней стадии предпочтителен worst-case/low scenario, потому что synthetic standard error не имеет частотной causal интерпретации.

## 6.4 Hard budget gate

Utility не может «купить» нарушение бюджета:

```text
reward_liability_max(u,a) ≤ user_cap(a)
committed_liability(cohort,a) + reward_liability_max(u,a) ≤ budget_remaining(a)
reward terms are immutable after display unless customer-favorable
```

**\[INFERENCE\]** Для gate используется максимальная обещанная liability, а для expected utility — ожидаемая settled cost. Эти величины нельзя смешивать.

## 6.5 Group utility для «Двора»

```text
U_yard(g,a;H) = Σ_i U_direct(i,a_i;H)
              + Σ_i Σ_{j≠i} Spillover(i→j;H)
              - Group_churn_and_pressure_cost(g;H)
```

Дополнительные constraints:

```text
LCB[U_yard] ≥ δ_group
LCB[U_direct(i)] ≥ -harm_floor  for every member i
membership and individual contributions remain private
```

**\[INFERENCE\]** Это предотвращает оптимизацию общей суммы за счёт систематического ущерба одному участнику.

## 6.6 Иллюстративный расчёт, не прогноз

**\[ASSUMPTION\]** Для одного challenge на горизонте 28 дней сценарии могут выглядеть так:

| **Сценарий** | **Added visit CM** | **Added basket CM** | **Cannibalization** | **Ops** | **Reward** | **Fraud** | **Group ext.** | **Uncertainty** | **U, ₽** |
|--------------|--------------------|---------------------|---------------------|---------|------------|-----------|----------------|-----------------|----------|
| Low          | 35                 | 15                  | 35                  | 5       | 12         | 10        | 0              | 20              | -62      |
| Base         | 80                 | 25                  | 30                  | 5       | 8          | 8         | 0              | 15              | -11      |
| High         | 145                | 35                  | 25                  | 5       | 5          | 5         | 0              | 10              | 60       |

**\[INFERENCE\]** При выборе `min(low,base,high)` действие отклоняется и назначается `NO_INTERVENTION`, несмотря на положительный high scenario. Этот пример демонстрирует механику abstention, а не ожидаемые значения X5.

# 7. Алгоритм PoC

## 7.1 Детерминированный псевдокод

```python
def decide_mechanic(request, policy, services):
    decision_id = uuid4()
    ts = request.decision_ts

    # 1. Only information available before the decision.
    x = services.features.snapshot_as_of(request.user_id, ts)
    assert x.max_event_ts < ts

    # 2. Candidate generation is versioned and deterministic.
    candidates = [Action.no_intervention()]
    candidates += generate_versioned_candidates(x, policy.action_catalog)

    evaluated = []
    rejected = []

    for candidate in candidates:
        params = parameterize_from_approved_buckets(candidate, x, policy)

        violations = check_hard_constraints(
            user=x,
            action=candidate,
            params=params,
            consent=services.consent,
            safety=services.safety,
            privacy=services.privacy,
            fraud=services.fraud,
            budget=services.budget,
            experiment=services.experiment,
        )

        if violations:
            rejected.append(rejection_record(candidate, violations))
            continue

        components = estimate_utility_components(
            action=candidate,
            params=params,
            features=x,
            scenario_registry=policy.parameters,
            predictive_models=services.models,  # not causal in PoC
        )
        utility = compute_low_base_high_utility(components)

        # Monetary actions also require worst-case committed liability.
        if not hard_budget_gate(candidate, params, services.budget):
            rejected.append(rejection_record(candidate, ["BUDGET_GATE_FAILED"]))
            continue

        evaluated.append(evaluation_record(candidate, params, components, utility))

    # A0 must survive; otherwise fail closed and create an incident.
    assert any(e.action_id == "A0" for e in evaluated)

    feasible = [
        e for e in evaluated
        if e.action_id == "A0" or e.utility.robust_rub >= policy.min_utility_rub
    ]

    chosen = sorted(
        feasible,
        key=lambda e: (
            -e.utility.robust_rub,
            e.reward_liability_max_rub,
            e.customer_burden_rank,
            e.action_id,
        ),
    )[0]

    reason_codes = derive_reason_codes(chosen, evaluated, rejected, x, policy)
    customer_text = render_customer_template(chosen, reason_codes, policy)
    validate_faithfulness_and_safety(customer_text, chosen, reason_codes)

    log = build_immutable_decision_log(
        decision_id=decision_id,
        request=request,
        feature_snapshot=x,
        evaluated=evaluated,
        rejected=rejected,
        chosen=chosen,
        reason_codes=reason_codes,
        assignment_probability=services.experiment.probability_or_one(),
        policy_version=policy.version,
    )
    services.decision_log.append(log)
    return customer_response(log)
```

## 7.2 Инварианты, проверяемые тестами

1.  `A0` всегда присутствует и имеет `utility=0`, `reward_liability=0`.
2.  Ни один action с hard violation не может попасть в `chosen_action`.
3.  Все feature timestamps строго меньше `decision_ts`.
4.  Customer explanation содержит только разрешённые reason codes и значения из decision record.
5.  Денежный action не выбирается при недоступном budget/fraud service.
6.  Сумма committed liability не превышает budget после атомарного reserve.
7.  В pilot assignment probability известна и положительна для назначенного action.
8.  `social_opt_in=false/unknown` исключает A4–A7.
9.  Membership «Двора» не меняется внутри freeze window, кроме добровольного выхода/safety removal.
10. Повторный запуск на том же snapshot и policy version даёт идентичный результат, кроме заранее логируемой экспериментальной рандомизации.

## 7.3 Scorecard PoC

**\[ASSUMPTION\]** Scorecard не должен суммировать произвольные «баллы привлекательности». Он формирует денежные компоненты low/base/high из параметров реестра. Неденежные reason features могут влиять только через явно оценённые cost/value components либо hard rules.

**\[INFERENCE\]** Predictive models должны быть calibrated и time-split validated. Даже идеальная calibration completion не превращает score в uplift.

# 8. Контракт решения

## 8.1 Обязательные поля

| **Поле**                      | **Тип**             | **Назначение**                                                        |
|-------------------------------|---------------------|-----------------------------------------------------------------------|
| `decision_id`                 | UUID/string         | Уникальный id решения; связывает показ, outcome и audit               |
| `decision_ts`                 | ISO-8601            | Момент, относительно которого проверяется availability                |
| `user_id`                     | Internal token/hash | Без ФИО и контактов                                                   |
| `eligible_actions`            | Array               | Все прошедшие hard gates кандидаты с параметрами и utility components |
| `rejected_actions`            | Array               | Action + machine-readable constraint reasons                          |
| `chosen_action`               | Object              | Ровно один action, включая A0                                         |
| `expected_incremental_margin` | Money range         | Low/base/high; status `ASSUMPTION` before pilot                       |
| `expected_reward_cost`        | Money range         | Expected settled cost                                                 |
| `reward_liability_max`        | Money               | Hard budget commitment                                                |
| `uncertainty`                 | Object              | Method, penalty, support flags, maturity                              |
| `reason_codes`                | Array               | Только причины, реально участвовавшие в решении                       |
| `constraints_applied`         | Array               | Rule id, version, pass/fail                                           |
| `explanation`                 | Object              | Customer-safe text + product audit                                    |
| `policy_version`              | String              | Версия catalog, parameters, models, templates                         |
| `fallback`                    | Object              | Был ли fail-closed, причина, исход A0                                 |
| `assignment_probability`      | 0\<p≤1              | Нужна для OPE; 1.0 в детерминированном PoC                            |
| `experiment_unit_id`          | String/null         | User, yard/cohort или cluster                                         |
| `feature_snapshot_id`         | String              | Reproducibility and leakage audit                                     |

## 8.2 Точная JSON-структура: пример

```json
{
  "schema_version": "1.0.0",
  "decision_id": "7cb6633e-1f13-4f65-9db8-2f35fb31a9a4",
  "decision_ts": "2026-09-04T09:00:00+05:00",
  "user_id": "usr_8f26b1",
  "feature_snapshot_id": "fs_20260904_090000_usr_8f26b1",
  "policy_version": "poc-scorecard-0.4.0",
  "action_catalog_version": "catalog-1.0.0",
  "experiment": {
    "experiment_id": null,
    "experiment_unit": "user",
    "experiment_unit_id": "usr_8f26b1",
    "assigned_arm": null,
    "assignment_probability": 1.0
  },
  "eligible_actions": [
    {
      "action_id": "A0",
      "action_type": "NO_INTERVENTION",
      "action_version": "1.0",
      "parameters": {},
      "utility_rub": {"low": 0, "base": 0, "high": 0, "robust": 0},
      "expected_incremental_margin_rub": {"low": 0, "base": 0, "high": 0},
      "expected_reward_cost_rub": {"low": 0, "base": 0, "high": 0},
      "reward_liability_max_rub": 0,
      "uncertainty": {"level": "none", "penalty_rub": 0, "status": "DEFINED_BASELINE"}
    },
    {
      "action_id": "A3",
      "action_type": "CHALLENGE_PLUS_AVATAR",
      "action_version": "1.1",
      "parameters": {
        "horizon_days": 28,
        "target_bucket": "ACHIEVABLE_LOW",
        "reward_bucket": "R1",
        "category_policy": "SAFE_BROAD_CATEGORY_ONLY"
      },
      "utility_rub": {"low": 14, "base": 43, "high": 79, "robust": 14},
      "expected_incremental_margin_rub": {"low": 42, "base": 78, "high": 124},
      "expected_reward_cost_rub": {"low": 8, "base": 12, "high": 16},
      "reward_liability_max_rub": 20,
      "uncertainty": {
        "level": "high",
        "method": "LOW_BASE_HIGH_SCENARIO",
        "penalty_rub": 12,
        "causal_status": "TO_VALIDATE"
      }
    }
  ],
  "rejected_actions": [
    {
      "action_id": "A4",
      "constraint_codes": ["SOCIAL_OPT_IN_REQUIRED"]
    },
    {
      "action_id": "A7",
      "constraint_codes": ["SOCIAL_OPT_IN_REQUIRED", "REFERRAL_COOLDOWN_ACTIVE"]
    }
  ],
  "chosen_action": {
    "action_id": "A3",
    "action_type": "CHALLENGE_PLUS_AVATAR",
    "action_version": "1.1",
    "parameters_ref": "eligible_actions[1].parameters"
  },
  "expected_incremental_margin": {
    "currency": "RUB",
    "horizon_days": 28,
    "low": 42,
    "base": 78,
    "high": 124,
    "evidence_status": "ASSUMPTION"
  },
  "expected_reward_cost": {
    "currency": "RUB",
    "low": 8,
    "base": 12,
    "high": 16,
    "settlement_status": "ESTIMATED"
  },
  "uncertainty": {
    "decision_rule": "MAXIMIZE_ROBUST_UTILITY",
    "robust_utility_rub": 14,
    "min_utility_rub": 10,
    "support_flags": ["NO_RANDOMIZED_TREATMENT_LABELS"],
    "causal_claim_allowed": false
  },
  "reason_codes": [
    "CHALLENGE_ACHIEVABLE",
    "POSITIVE_ROBUST_NET_VALUE",
    "RECENT_APP_ENGAGEMENT",
    "SOCIAL_ACTIONS_EXCLUDED_BY_PREFERENCE"
  ],
  "constraints_applied": [
    {"rule_id": "SAFE_CATEGORY_ONLY", "version": "2.0", "result": "PASS"},
    {"rule_id": "USER_REWARD_CAP", "version": "1.3", "result": "PASS"},
    {"rule_id": "FREQUENCY_CAP_28D", "version": "1.1", "result": "PASS"},
    {"rule_id": "SOCIAL_OPT_IN", "version": "1.0", "result": "FAIL_FOR_SOCIAL_ACTIONS"}
  ],
  "explanation": {
    "customer": "Мы подобрали короткое личное задание по вашей обычной активности. Цель ограничена сроком, а прогресс видите только вы.",
    "product_audit": {
      "summary": "A3 won on low-scenario net value; social actions were not eligible.",
      "feature_values_used": [
        {"feature": "visits_84d", "value": 9},
        {"feature": "days_since_last_action[A3]", "value": 41},
        {"feature": "social_opt_in", "value": false}
      ],
      "forbidden_feature_used": false
    }
  },
  "fallback": {
    "used": false,
    "reason": null,
    "would_choose": "A0"
  },
  "outcome_contract": {
    "maturity_days": 42,
    "primary_outcome": "NET_INCREMENTAL_CONTRIBUTION_MARGIN_RUB",
    "secondary_outcomes": ["PURCHASE_FREQUENCY", "CHALLENGE_COMPLETION"],
    "group_exposure_mapping_version": null
  }
}
```

## 8.3 Contract invariants

- Money fields always include currency and horizon; no unitless «score» is exposed as margin.
- Before causal data, `causal_claim_allowed=false` and evidence status is `ASSUMPTION`/`TO_VALIDATE`.
- `assignment_probability` is the probability of the **actually selected action** under the logging policy, after eligibility filtering.
- Eligible set and rule versions are logged before outcome.
- Outcome updates append to a separate event stream; historical decision record is immutable.
- For «Двор», `experiment_unit` and `exposure_mapping_version` are required.

# 9. Объяснения

## 9.1 Faithful-by-construction pipeline

```text
used features + passed/failed constraints + utility ledger
→ deterministic reason codes
→ allowlisted customer template
→ optional LLM paraphrase under semantic validator
```

**\[INFERENCE\]** LLM получает только выбранный action, допустимые безопасные числа и reason codes. Он не видит raw purchase history, sensitive categories или альтернативные персональные гипотезы. Если paraphrase не проходит exact fact check, используется deterministic template.

## 9.2 Reason code catalog

| **Code**                            | **Trigger**                             | **Product audit**                                                | **Customer-safe rule**                               |
|-------------------------------------|-----------------------------------------|------------------------------------------------------------------|------------------------------------------------------|
| `POSITIVE_ROBUST_NET_VALUE`         | Low/LCB utility выше порога             | «Ожидаемая ценность положительна даже в консервативном сценарии» | Не показывать рублёвую модельную оценку без продукта |
| `NO_POSITIVE_ROBUST_VALUE`          | Все actions ниже порога                 | «Сейчас новых заданий нет»                                       | Не говорить «вы невыгодны»                           |
| `HIGH_BASELINE_PURCHASE_PROPENSITY` | Высокий no-action baseline              | Обычно не выводить; audit only                                   | Не говорить «вы и так купите»                        |
| `CHALLENGE_ACHIEVABLE`              | Target bucket соответствует history     | «Цель подобрана по вашей обычной активности»                     | Не раскрывать конкретные чувствительные покупки      |
| `INSUFFICIENT_HISTORY`              | Недостаточно зрелых событий             | «Пока предложим только личный прогресс»                          | Не делать выводы о человеке                          |
| `MECHANIC_FATIGUE`                  | Exposure/click-hide cap                 | «Сделаем паузу в заданиях»                                       | Без давления и guilt                                 |
| `COOLDOWN_ACTIVE`                   | Последнее действие слишком недавно      | «Новое задание появится позже»                                   | Не указывать скрытые risk scores                     |
| `LOW_EXPECTED_NET_MARGIN`           | Reward/cost превосходит scenario margin | Audit only                                                       | Не раскрывать экономическую ценность пользователя    |
| `FRAUD_REVIEW_PENDING`              | Операция требует проверки               | «Награда ожидает проверки условий»                               | Не обвинять в мошенничестве                          |
| `FRAUD_RISK_ABOVE_THRESHOLD`        | Precision-first block/review            | Audit only / нейтральный service text                            | Не раскрывать detection logic злоумышленнику         |
| `SOCIAL_OPT_IN_REQUIRED`            | Нет explicit consent                    | Не показывать social offer                                       | Не подталкивать к согласию                           |
| `YARD_POOL_TOO_SMALL`               | Privacy/operational minimum не выполнен | «Командный формат пока недоступен»                               | Не раскрывать размер локальной группы                |
| `YARD_CYCLE_NEAR_END`               | Late join blocked                       | «Следующий командный цикл начнётся позже»                        | Не менять состав ради score                          |
| `YARD_STABILITY_PROTECTED`          | Freeze/stability gate                   | Audit only                                                       | Не называть ушедших участников                       |
| `ANONYMOUS_COHORT_AVAILABLE`        | Opt-in + cohort size pass               | «Можно добровольно вступить в анонимную лигу»                    | Никаких адресов/ФИО                                  |
| `REFERRAL_QUALIFICATION_REQUIRED`   | Reward only after qualified outcome     | «Награда появится после выполнения условий приглашённым»         | Не обещать reward за регистрацию                     |
| `UNCERTAINTY_TOO_HIGH`              | Support/variance insufficient           | «Сейчас предложение не показываем»                               | Audit has diagnostics                                |
| `BUDGET_GATE_FAILED`                | Max liability не помещается в budget    | Audit only                                                       | Не показывать пользователю внутренний бюджет         |

## 9.3 Customer templates

**Личный challenge**
«Мы подобрали короткое личное задание по вашей обычной активности. Цель ограничена сроком, а условия и награда показаны заранее.»

**Аватар без денежного воздействия**
«Продолжайте личный прогресс в удобном темпе. Покупать больше для сохранения уровня не требуется.»

**Добровольный «Двор»**
«Можно присоединиться к анонимной команде покупателей этого магазина. Участие добровольное; личный вклад видите только вы.»

**Анонимная лига**
«Можно добровольно участвовать под никнеймом и аватаром. Точный адрес и имя не показываются.»

**Реферал**
«Приглашение не создаёт награду само по себе: она появится только после выполнения заранее указанных условий приглашённым.»

**No intervention**
«Сейчас новых игровых заданий нет. Основные функции и предложения приложения остаются доступны.»

## 9.4 Запрещённые формулировки

- «Не подведите соседей», «без вас двор проиграет», «остальные ждут только вас» — social pressure.
- «Мы знаем, что у вас маленький ребёнок / вредная привычка / заболевание» — sensitive inference disclosure.
- «Потратьте ещё X рублей» без контекста ценности и safety — манипулятивное стимулирование трат.
- «Вы подозреваетесь в мошенничестве» до подтверждённой процедуры — обвинение и раскрытие antifraud logic.
- «AI решил, что вам это понравится» — нефальсифицируемая post-hoc история.
- Публичный индивидуальный вклад, missed target или rank, позволяющий идентифицировать человека.

# 10. Синтетические примеры решений

Все суммы ниже — **\[ASSUMPTION\]** для демонстрации логики, не прогноз X5. `U` указан как low/base/high в рублях за 28 дней; выбор основан на low/robust при illustrative `δ=10 ₽`.

## 10.1 Примеры 1–8

| **Профиль**            | **Состояние**                                                 | **Eligible**   | **Выбор**      | **U low/base/high** | **Reason codes**                                                | **Почему**                                              |
|------------------------|---------------------------------------------------------------|----------------|----------------|---------------------|-----------------------------------------------------------------|---------------------------------------------------------|
| 1\. Cold start         | Новый app user; 0 receipts; social opt-in unknown             | A0, A2         | A2 Avatar only | 0 / 4 / 9           | `INSUFFICIENT_HISTORY`; non-monetary fallback                   | Нет causal/экономической основы для денежного challenge |
| 2\. Sure thing         | 12 visits/28d; высокий calibrated baseline; recent exposure   | A0, A1, A3     | A0             | -22 / 3 / 31        | `HIGH_BASELINE_PURCHASE_PROPENSITY`; `NO_POSITIVE_ROBUST_VALUE` | Не платить за вероятную baseline-покупку                |
| 3\. Fatigue            | 3 игровых показа/28d; hide/complaint                          | A0             | A0             | 0 / 0 / 0           | `MECHANIC_FATIGUE`; `FREQUENCY_CAP_REACHED`                     | Пауза важнее predicted response                         |
| 4\. Низкая экономика   | Challenge релевантен; max reward 80 ₽; margin scenario слабый | A0, A1         | A0             | -55 / -18 / 12      | `LOW_EXPECTED_NET_MARGIN`                                       | High scenario не компенсирует отрицательный low         |
| 5\. High fraud risk    | Velocity/graph rules above monetary threshold; app active     | A0, A2         | A2             | 0 / 3 / 7           | `FRAUD_RISK_ABOVE_THRESHOLD`; non-monetary fallback             | Денежные actions blocked, пользователь не обвиняется    |
| 6\. Social opt-out     | Хорошая history; explicit social_opt_in=false                 | A0, A1, A2, A3 | A3             | 16 / 39 / 71        | `SOCIAL_ACTIONS_EXCLUDED_BY_PREFERENCE`; `CHALLENGE_ACHIEVABLE` | A4–A7 не кандидаты, даже если predicted response высок  |
| 7\. Stable yard member | Active yard; day 3/14; no churn; group scenario positive      | A0, A2, A5     | A5             | 18 / 54 / 92        | `YARD_STABLE`; `POSITIVE_GROUP_UTILITY`                         | Личный вклад приватен; action совместим с общей целью   |
| 8\. Late yard join     | Opt-in=true; slot есть; до конца цикла 2 дня                  | A0, A1, A2     | A1             | 12 / 31 / 56        | `YARD_CYCLE_NEAR_END`; `CHALLENGE_ACHIEVABLE`                   | Не ломать стабильность; выбрать независимую механику    |

## 10.2 Примеры 9–16

| **Профиль**                      | **Состояние**                                                  | **Eligible**   | **Выбор** | **U low/base/high** | **Reason codes**                                    | **Почему**                                                          |
|----------------------------------|----------------------------------------------------------------|----------------|-----------|---------------------|-----------------------------------------------------|---------------------------------------------------------------------|
| 9\. Rural/small pool             | Сельский магазин; opted-in pool ниже privacy threshold         | A0, A1, A2     | A1        | 14 / 33 / 58        | `YARD_POOL_TOO_SMALL`; `POSITIVE_ROBUST_NET_VALUE`  | Тип поселения не снижает личный score; ограничение относится к pool |
| 10\. Старший городской           | 65+; app active; достаточная history; no fatigue               | A0, A1, A2, A3 | A3        | 15 / 37 / 63        | `CHALLENGE_ACHIEVABLE`                              | Возраст не использован; решение совпало бы при иной age group       |
| 11\. Старший rural, inactive app | 65+; 0 app sessions/90d; нет consent на игровые prompts        | A0             | A0        | 0 / 0 / 0           | `CHANNEL_UNAVAILABLE`                               | Причина — канал/consent, не возраст или село                        |
| 12\. Safe referral               | Opt-in; 1 прошлый qualified invite; low fraud; cap available   | A0, A2, A7     | A7        | 13 / 42 / 78        | `REFERRAL_QUALIFICATION_REQUIRED`; `LOW_FRAUD_RISK` | Reward after qualified behavior only                                |
| 13\. Referral star               | 15 invites/2d; invitees without purchases; review pending      | A0, A2         | A0        | 0 / 0 / 0           | `FRAUD_REVIEW_PENDING`; `REFERRAL_CAP_REACHED`      | Fail closed; no accusatory customer text                            |
| 14\. Anonymous league            | Opt-in; large cohort; pseudonym; no leaderboard fatigue        | A0, A2, A6     | A6        | 11 / 25 / 44        | `ANONYMOUS_COHORT_AVAILABLE`                        | Никакой точной географии/ФИО                                        |
| 15\. Reactivation                | Recency 39d; prior frequency low; achievable low-stakes target | A0, A1, A2     | A1        | 10 / 29 / 61        | `REACTIVATION_WINDOW`; `CHALLENGE_ACHIEVABLE`       | Target не требует резкого роста потребления                         |
| 16\. Unstable yard               | 2 exits last cycle; goal risk; pressure indicators             | A0, A2         | A2        | 0 / 5 / 10          | `YARD_STABILITY_PROTECTED`; `GROUP_PRESSURE_RISK`   | Не использовать участника как средство спасения группы              |

## 10.3 Контрфактуальная проверка fairness на примерах

**\[INFERENCE\]** Для профилей 9–11 выполняется тест: изменить только audit-атрибут `age_band` или `urban_rural`, сохранив behavioral, consent, budget и store-pool state. Личный action не должен измениться. Исключение «Двора» может измениться только при изменении operational pool state, а не из-за принадлежности человека к демографической группе.

# 11. Оценка

## 11.1 Четыре разных вопроса качества

| **Уровень**             | **Вопрос**                                      | **Метрики**                                                             | **Не доказывает**                  |
|-------------------------|-------------------------------------------------|-------------------------------------------------------------------------|------------------------------------|
| Data/invariant quality  | Корректно ли воспроизводится решение?           | Leakage tests, schema completeness, timestamp checks, budget invariants | Causal effect                      |
| Prediction quality      | Хорошо ли модели прогнозируют observed labels?  | Calibration, Brier/log loss, MAE, time-split drift                      | Policy value и uplift              |
| Policy value            | Какой expected utility у policy?                | IPS/SNIPS/DR/OPE, effective sample size, lower confidence bound         | Business causal effect вне support |
| Causal business outcome | Изменило ли вмешательство net margin/frequency? | Randomized ITT, confidence intervals, cluster/spillover estimands       | Механизм для каждого индивида      |

## 11.2 Offline sanity checks для PoC

**\[INFERENCE\]** Допустимы:

- unit/property tests всех hard gates и fallback;
- time-travel test: перестановка будущих outcomes не меняет прошлые decisions;
- synthetic scenario analysis low/base/high и tornado sensitivity;
- budget stress: максимум liability при одновременном выборе actions;
- deterministic replay собственной rule policy для reproducibility, не для causal value;
- distribution checks: no-action rate, reasons, action concentration, reward liability, group formation stability;
- time-split validation predictive models;
- fairness slices и counterfactual invariance tests;
- red-team explanation: sensitive leakage, manipulative language, false causal claims.

**\[FACT\]** Replay для unbiased evaluation допустим только при соответствующем randomized logging и известных action probabilities; обычный observational log или synthetic simulator не создаёт это свойство ([Li et al., 2011](https://doi.org/10.1145/1935826.1935878)).

## 11.3 Shadow mode

В shadow policy ничего не показывает и не резервирует reward. Она логирует:

- candidate/eligible/rejected distributions;
- `NO_INTERVENTION` rate и причины;
- projected expected и max liability;
- missing-feature/fail-closed rate;
- score/feature drift;
- disagreement с текущей baseline policy;
- fairness slices;
- для «Двора» — pool size, slot, stability и simulated group-exposure mapping.

**\[INFERENCE\]** Shadow mode проверяет operational behavior, но не causal effect, потому что action не исполняется.

## 11.4 Randomized pilot: индивидуальные механики

**\[INFERENCE\] Рекомендуемый дизайн:** eligibility-first randomized experiment. Сначала hard rules формируют общий допустимый набор; затем эксперимент случайно назначает один из actions, включая A0, с известной probability. Нельзя сравнивать людей, которым разные actions были доступны по разным скрытым правилам, без явного estimand.

- Unit: user для A1/A2/A3/A6/A7, если отсутствуют spillovers.
- Stratification: pre-period purchase frequency/margin, store/format и prior app engagement; не по post-treatment behavior.
- Primary business outcome: net incremental contribution margin per randomized eligible user за matured horizon.
- Key product outcome: purchase frequency и доля с ≥N purchases; N и horizon заранее фиксируются.
- Secondary: acceptance/completion, app engagement, reward settlement.
- Guardrails: margin non-inferiority, reward liability, fraud loss, returns, complaints, opt-out, contact fatigue, fairness gaps.
- Analysis: intention-to-treat first; treatment-on-treated только с predeclared identification strategy.
- Multiple actions: control multiplicity or declare one primary comparison/policy-value estimand.

**\[TO_VALIDATE\]** Sample size вычисляется из baseline variance, intracluster correlation, expected take-up, minimum detectable effect и desired power. Универсальное `N` без этих величин — ложная точность.

## 11.5 Randomized pilot: «Двор»

**\[INFERENCE\]** User-level Bernoulli A/B некорректен, если один treatment меняет цель/опыт других. Рекомендуются два варианта:

1.  **Cluster randomization:** заранее сформированный eligible cohort/yard целиком получает `Dvor enabled` или control.
2.  **Two-stage saturation:** store/cohort случайно получает уровень насыщения приглашениями, затем отдельные пользователи рандомизируются внутри. Это позволяет оценивать direct и spillover effects, но сложнее по power и implementation.

Требуется predeclared exposure mapping: `not exposed`, `invited only`, `active member in treated yard`, `untreated member exposed to treated peers` — только если такие состояния реально возможны.

## 11.6 OPE после пилота

**\[INFERENCE\] Минимальный набор диагностик:**

- overlap plots и доля zero/near-zero propensities;
- maximum/percentile importance weights;
- effective sample size overall и по action;
- IPS, self-normalized IPS и doubly robust estimates;
- bootstrap/cluster-robust confidence intervals по experiment unit;
- policy value lower bound против A0/baseline;
- sensitivity к propensity clipping и nuisance models;
- evaluation на независимом temporal holdout;
- maturity/censoring diagnostics для delayed reward.

**\[INFERENCE\]** Policy не деплоится, если gain существует только после aggressive clipping, в одном model specification или вне overlap support.

## 11.7 Метрики

| **Слой**       | **Метрика**                                                                     | **Единица**                | **Примечание**                                                 |
|----------------|---------------------------------------------------------------------------------|----------------------------|----------------------------------------------------------------|
| Primary causal | Net incremental contribution margin / eligible randomized unit                  | RUB per user or yard per H | ITT difference; rewards, variable costs, returns/fraud matured |
| Product causal | Purchases per user; share with ≥N purchases                                     | count / percentage points  | N and H predeclared                                            |
| Policy value   | Estimated value and lower confidence bound                                      | RUB per unit               | OPE on logged randomized data                                  |
| Prediction     | Calibration/Brier/log loss of acceptance/completion                             | probability quality        | Not called uplift                                              |
| Economics      | Reward liability, settled reward, cannibalization, fraud loss                   | RUB and ratios             | Separate promised vs expected cost                             |
| Safety         | Complaints, opt-out, harmful-category violations                                | rate                       | Hard zero tolerance for prohibited categories                  |
| Antifraud      | Precision, false-positive rate, manual review rate                              | rate                       | Threshold precision-first                                      |
| Fairness       | Eligibility/action/no-action/value/error gaps by audit slice                    | pp/RUB                     | Confidence intervals and small-cell suppression                |
| Dvor           | Group completion, membership churn, direct/spillover value, pressure complaints | group/user rate and RUB    | Cluster-aware inference                                        |

# 12. План эволюции

| **Стадия**                       | **Вход**                                             | **Метод**                                            | **Критерий перехода**                                                               | **Rollback**                                        | **Monitoring**                                           |
|----------------------------------|------------------------------------------------------|------------------------------------------------------|-------------------------------------------------------------------------------------|-----------------------------------------------------|----------------------------------------------------------|
| 0\. PoC scorecard                | Synthetic feature snapshots; parameter registry      | Rules + component utility + A0 + reason codes        | 100% invariants; no false causal claims; scenario economy coherent                  | Feature/model failure → A0; policy version rollback | Decision distribution, liability, reasons, leakage tests |
| 1\. Shadow                       | Real pre-decision features, no treatment             | Run candidate/gates/scoring silently                 | Stable latency/data quality; acceptable no-action and fail-closed rates             | Disable shadow writes/models                        | Missingness, drift, budget projection, fairness          |
| 2\. Randomized pilot             | Known action probabilities, A0, matured outcomes     | Fixed arms; cluster/two-stage for Dvor               | Positive ITT net margin lower bound or explicit learning objective; guardrails pass | Stop assignment; settle promises; revert baseline   | Sequential safety only; final predeclared inference      |
| 3\. Offline causal policy        | Pilot logs + holdout                                 | AIPW/DR scores; multi-arm CATE; shallow policy tree  | Holdout policy LCB \> baseline; overlap/ESS adequate                                | Retain randomized baseline; deploy to small cohort  | Value, support, drift, subgroup gaps                     |
| 4\. Conservative online learning | Continuous randomized logs; delayed outcome pipeline | Constrained contextual bandit with baseline fallback | High-confidence safe improvement, budget and latency SLO                            | One-click baseline policy; exploration off          | Cumulative LCB, regret proxy, liability, mature feedback |

## 12.1 Рекомендуемый first causal learner

**\[INFERENCE\]** После пилота не начинать сразу с online bandit. Сначала:

1.  построить action-specific outcome and propensity nuisance models с cross-fitting;
2.  получить doubly robust reward estimates;
3.  оценить A0-relative multi-arm contrasts;
4.  обучить depth-2/3 policy tree с budget constraints;
5.  проверить policy value на untouched temporal/experimental holdout;
6.  сохранить randomized exploration slice для будущей OPE.

Официальные `grf`/`policytree` инструменты поддерживают multi-arm causal forest и shallow interpretable policies на doubly robust scores ([GRF documentation](https://grf-labs.github.io/grf/reference/multi_arm_causal_forest.html); [policytree](https://grf-labs.github.io/policytree/)). Это инженерный ориентир, не обязательство использовать R в production.

## 12.2 Когда bandit действительно нужен

**\[TO_VALIDATE\]** Bandit оправдан, когда:

- decisions повторяются часто, а preferences/nonstationarity меняются;
- есть достаточно большой eligible traffic для каждого action;
- reward maturity и delayed attribution устойчиво работают;
- exploration может быть ограничено без нарушения customer trust;
- policy canary и rollback автоматизированы;
- бюджет учитывается как ресурс, а не post-hoc отчёт.

До выполнения этих условий static randomized policy + periodic retraining безопаснее и проще.

# 13. Аудит «Двора»

## 13.1 Нужен ли отдельный recommender для вступления/матчинга

**\[INFERENCE\] Да.** Это не обычный user→action ranking, а constrained group-formation/allocation problem, где одно решение меняет feasible set и outcome нескольких людей. Рекомендуется разделить:

1.  `yard_eligibility_service` — opt-in, store pool, privacy, safety;
2.  `yard_matcher` — stable epoch-based matching в broad frequency/RFM bins;
3.  `yard_join_policy` — кому и когда показать добровольное приглашение;
4.  `member_action_policy` — персональный challenge внутри уже зафиксированного yard;
5.  `yard_economics` — group utility, liability и externalities;
6.  `yard_experiment_service` — cluster assignment и exposure mapping.

## 13.2 Store ID и приватность

- **\[FACT\]** В проектном пакете запрещены точные адреса и ФИО; `store_id` предложен как operational anchor.
- **\[INFERENCE\]** `store_id` остаётся quasi-identifier и не должен выводиться вместе с точным временем/индивидуальным вкладом.
- **\[FACT\]** k-anonymity защищает только определённую модель indistinguishability; subsequent privacy research показало attribute/background-knowledge attacks. Поэтому «pool ≥20» — operational assumption, не privacy proof ([Sweeney, 2002](https://dataprivacylab.org/projects/kanonymity/index.html); [Machanavajjhala et al., 2006/2007](https://doi.org/10.1145/1217299.1217302)).
- **\[INFERENCE\]** Нужны data minimization, coarse cohort display, small-cell suppression, separate consent, no exact activity timestamps, no public contribution and privacy review.

## 13.3 Matching и RFM balance

**\[ASSUMPTION\]** Matching по похожей frequency может уменьшить ощущение несправедливости, но границы 3–7 участников, pool 20 и ratio 2.5× из черновика не подтверждены.

Рекомендуемый PoC matcher:

```text
eligible opted-in users by store token
→ broad frequency bands using pre-period data
→ random matching within adjacent allowed bands
→ group-level privacy/stability checks
→ freeze membership for a cycle
```

**\[INFERENCE\]** Не использовать age, family status, sensitive basket or exact location. Randomization within compatible bins снижает popularity bias и делает pilot analyzable.

## 13.4 Stability

- Вступление только до старта или в короткое predeclared join window.
- Выход всегда доступен; removal из safety/fraud причин не раскрывается другим.
- Refill только между циклами, если иначе не нарушается обещанная goal definition.
- Group goal пересчитывается только по заранее описанному customer-favorable rule.
- Нельзя персональным action повышать чью-то норму, чтобы «спасти» group KPI.

## 13.5 Group externalities и interference

**\[FACT\]** При общей цели outcome пользователя зависит от поведения других; стандартное no-interference assumption нарушено. Методы causal inference under interference требуют group/exposure-aware design ([Hudgens & Halloran, 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2600548/); [Aronow & Samii, 2017](https://arxiv.org/abs/1305.6156)).

**\[INFERENCE\]** Экспериментальная единица — yard/cohort или store-level cluster. User-level result можно анализировать внутри cluster-aware estimand, но нельзя считать пользователей независимыми.

## 13.6 Социальная мотивация: решение по утверждению «слабое звено +25%»

**\[FACT\]** Исследования Köhler effect показывают motivation gains у менее способных участников в определённых conjunctive tasks; meta-analysis 17 studies, N=2,240 сообщал moderate effect и сильные moderators. Отдельный meta-analysis 78 studies показал устойчивый social loafing с moderators.

**\[INFERENCE\]** Фиксированный коэффициент `+25% effort` для grocery loyalty отклоняется. В симуляции допустим широкий group-externality range с отрицательным low scenario; causal coefficient измеряется cluster pilot. Customer design запрещает shame, public deficit and «не подведите» messaging.

## 13.7 Falsification criteria

**\[TO_VALIDATE\]** Отказаться от auto-match или monetary group reward, если:

- group-level lower-bound net margin ≤0;
- direct benefit концентрируется у frequent shoppers, а low-frequency members получают pressure/cost;
- membership churn/complaints превышают predeclared guardrail;
- eligible pool систематически исключает small/rural stores;
- privacy review не подтверждает безопасное отображение;
- intrusion of group treatment contaminates control beyond analyzable exposure mapping;
- sponsor funding является единственным способом сделать base scenario положительным, но funding contract не подтверждён.

# 14. Fairness и privacy

## 14.1 Что не использовать для выбора

**\[INFERENCE\]** По умолчанию исключить из decision score: возраст, пол, exact geography, household/child status, sensitive category behavior, disability/health proxies, ethnicity/nationality proxies, income proxies и exact device/location trails. Исключение возможно только для обязательного safety/legal rule после отдельного review, а не для коммерческого uplift.

## 14.2 Audit slices

**\[TO_VALIDATE\]** При наличии законного и минимизированного audit dataset измерять по возрастным группам, urban/rural, region/store format, digital readiness, history length и app activity:

- eligibility rate;
- action mix и `NO_INTERVENTION` rate;
- reward liability and realized net margin;
- acceptance/completion conditional on randomized assignment;
- model calibration/error;
- fraud false-positive/review rate;
- opt-out, complaints and harm indicators;
- «Двор»: pool availability, join rate, churn and group outcome.

Показывать confidence intervals, minimum cell sizes и suppress small cells.

## 14.3 Метрики и ограничения

**\[INFERENCE\]** Не выбирать одну абстрактную fairness metric. Для этой системы полезны:

1.  **Access parity:** различия eligibility/action/no-action после учёта объективных channel/consent constraints.
2.  **Error parity:** calibration и false-positive fraud rate по audit slices.
3.  **Benefit parity:** randomized incremental margin или user benefit, когда sample позволяет.
4.  **Burden parity:** contacts, reward hurdles, pressure complaints, cooldown blocks.
5.  **Counterfactual invariance test:** decision не меняется при изменении audit-only attribute при фиксированных operational features.

**\[FACT\]** Statistical criteria могут конфликтовать и не заменяют анализ процесса, context и распределения harms ([Hardt, Price & Srebro, 2016](https://arxiv.org/abs/1610.02413); [Selbst et al., 2019](https://doi.org/10.1145/3287560.3287598)).

## 14.4 Feedback loops и popularity bias

- Логировать exposures, а не обучаться только на accepted/completed users.
- Сохранять randomized exploration/holdout.
- Не увеличивать показ action только потому, что он уже чаще показывался.
- Контролировать action concentration и coverage.
- Для cold start использовать neutral/non-monetary fallback, а не постоянное исключение.
- Переобучение только на matured outcomes и с temporal holdout.

**\[FACT\]** Simulation research показывает, что обучение на данных, уже изменённых recommender exposure, может усиливать гомогенизацию без роста utility ([Chaney et al., 2018](https://arxiv.org/abs/1710.11214)).

## 14.5 Privacy-by-design

- User ID токенизирован; exact address/name/contact не входят в policy log.
- Raw receipts и reason-code store разделены; explanation service получает минимальный safe payload.
- Store/group aggregates имеют small-cell suppression.
- Membership, social opt-in и individual contribution — отдельные protected fields.
- Retention period и access roles задаются для feature snapshot, decision log и outcome log отдельно.
- Product audit показывает использованные features, но customer text не раскрывает sensitive purchasing.
- Любой экспорт для исследования проходит aggregation/de-identification review; k-anonymity не считается достаточным единственным control.

## 14.6 Действия при fairness gap

1.  остановить expansion затронутой policy/arm;
2.  проверить denominator, missingness, overlap, latency и experiment imbalance;
3.  локализовать gap: eligibility, model, reward design, channel или group formation;
4.  удалить/ограничить proxy, улучшить data coverage или добавить cold-start fallback;
5.  повторить randomized/shadow validation;
6.  задокументировать residual risk и owner;
7.  не «чинить» disparity скрытым повышением social pressure или reward cost.

# 15. Реестр параметров

Значения ниже — проектные диапазоны для scenario analysis. Они не являются правилами X5.

| **Параметр**                                   | **Low** | **Base** | **High** | **Статус**  | **Источник/владелец** | **Как валидировать**                            |
|------------------------------------------------|---------|----------|----------|-------------|-----------------------|-------------------------------------------------|
| Decision horizon H, days                       | 14      | 28       | 42       | ASSUMPTION  | Product/analytics     | Pilot maturity and purchase-cycle sensitivity   |
| Minimum robust utility δ, ₽/user/H             | 0       | 10       | 30       | ASSUMPTION  | Finance/product       | Profit-risk appetite; randomized LCB            |
| Uncertainty multiplier κ                       | 0.5     | 1.0      | 2.0      | ASSUMPTION  | DS/governance         | Coverage calibration on holdout                 |
| Game frequency cap / 28d                       | 1       | 2        | 3        | ASSUMPTION  | Product/safety        | Complaint/opt-out experiment                    |
| Cooldown after incentivized action, days       | 7       | 14       | 28       | ASSUMPTION  | Product               | Fatigue randomized test                         |
| Cold-start history minimum, matured visits     | 1       | 3        | 5        | ASSUMPTION  | DS/product            | Relevance/hit-rate rubric                       |
| Reward max liability per action, ₽             | 10      | 30       | 80       | ASSUMPTION  | Finance               | Incremental margin pilot and budget stress      |
| Reward cost settlement rate                    | 0.6     | 0.8      | 1.0      | TO_VALIDATE | Loyalty finance       | Actual redemption/settlement ledger             |
| Cannibalization share of rewarded margin       | 0.2     | 0.5      | 0.8      | TO_VALIDATE | Causal analytics      | A0 contrast and purchase decomposition          |
| Fraud precision target                         | 0.85    | 0.95     | 0.99     | ASSUMPTION  | Antifraud             | Labeled review sample; cost-sensitive threshold |
| Fraud review maturity, days                    | 7       | 14       | 28       | ASSUMPTION  | Antifraud/ops         | Return/fraud lag distribution                   |
| Exploration share after readiness              | 0.01    | 0.05     | 0.10     | ASSUMPTION  | Experiment owner      | Safe exposure budget and power                  |
| Minimum action propensity in supported stratum | 0.01    | 0.05     | 0.10     | ASSUMPTION  | Experiment/DS         | OPE ESS and variance                            |
| Policy tree depth                              | 2       | 3        | 4        | ASSUMPTION  | DS/product            | Holdout value vs interpretability               |
| Temporal holdout, weeks                        | 2       | 4        | 8        | ASSUMPTION  | DS                    | Seasonality and drift                           |
| Dvor team size                                 | 3       | 5        | 7        | ASSUMPTION  | Product/research      | Cluster pilot; churn/pressure                   |
| Dvor eligible pool minimum                     | 20      | 50       | 100      | ASSUMPTION  | Privacy/product       | Re-identification review and availability       |
| Dvor cycle, days                               | 7       | 14       | 28       | ASSUMPTION  | Product               | Completion, churn, delayed margin               |
| Max frequency ratio in Dvor                    | 1.5×    | 2.0×     | 2.5×     | ASSUMPTION  | Matcher/product       | Perceived fairness and completion               |
| Dvor membership freeze                         | 1       | 2        | 3 cycles | ASSUMPTION  | Product/ops           | Stability vs wait time                          |
| No-late-join window, days before end           | 2       | 4        | 7        | ASSUMPTION  | Product               | Member experience experiment                    |
| Group externality, ₽/member/H                  | -50     | 0        | +50      | TO_VALIDATE | Causal analytics      | Cluster/two-stage pilot                         |
| Group harm floor, ₽/member/H                   | -20     | 0        | +10      | ASSUMPTION  | Safety/finance        | Distributional outcomes and complaints          |
| League minimum visible cohort                  | 50      | 200      | 1000     | ASSUMPTION  | Privacy/product       | Privacy and engagement pilot                    |
| Referral qualification window, days            | 7       | 14       | 30       | ASSUMPTION  | Product/antifraud     | Conversion and fraud lag                        |
| Referral invite cap / 28d                      | 1       | 3        | 5        | ASSUMPTION  | Antifraud/product     | Precision/FP and customer burden                |
| Pilot N purchases threshold                    | 3       | 4        | 6        | ASSUMPTION  | Product/analytics     | Pre-period distribution and business meaning    |
| Pilot MDE in purchase share                    | 1 pp    | 2 pp     | 3 pp     | ASSUMPTION  | Experiment owner      | Power calculation; not success claim            |
| Supplier-funded share                          | 0       | 0.5      | 0.8      | TO_VALIDATE | Commercial/finance    | Signed funding terms and attribution            |

**\[INFERENCE\]** Реестр должен жить в versioned configuration, а не в prompt LLM. Decision log хранит фактически использованные значения и owner/version.

# 16. Источники

## 16.1 Causal inference, policy learning и bandits

1.  [Rosenbaum, P. R.; Rubin, D. B. (1983). The Central Role of the Propensity Score in Observational Studies for Causal Effects. Biometrika.](https://doi.org/10.1093/biomet/70.1.41)
2.  [Hernán, M. A.; Robins, J. M. (2020). Causal Inference: What If.](https://miguelhernan.org/whatifbook)
3.  [Chernozhukov, V. et al. (2018). Double/Debiased Machine Learning for Treatment and Structural Parameters. The Econometrics Journal.](https://doi.org/10.1111/ectj.12097)
4.  [Athey, S.; Imbens, G. (2016). Recursive Partitioning for Heterogeneous Causal Effects. PNAS.](https://doi.org/10.1073/pnas.1510489113)
5.  [Wager, S.; Athey, S. (2018). Estimation and Inference of Heterogeneous Treatment Effects using Random Forests. JASA.](https://doi.org/10.1080/01621459.2017.1319839)
6.  [Athey, S.; Tibshirani, J.; Wager, S. (2019). Generalized Random Forests. Annals of Statistics.](https://doi.org/10.1214/18-AOS1709)
7.  [Künzel, S. R. et al. (2019). Metalearners for Estimating Heterogeneous Treatment Effects using Machine Learning. PNAS.](https://doi.org/10.1073/pnas.1804597116)
8.  [Nie, X.; Wager, S. (2021). Quasi-Oracle Estimation of Heterogeneous Treatment Effects. Biometrika.](https://arxiv.org/abs/1712.04912)
9.  [Kitagawa, T.; Tetenov, A. (2018). Who Should Be Treated? Empirical Welfare Maximization Methods for Treatment Choice. Econometrica.](https://doi.org/10.3982/ECTA13288)
10. [Athey, S.; Wager, S. (2021). Policy Learning With Observational Data. Econometrica.](https://doi.org/10.3982/ECTA15732)
11. [Zhou, Z.; Athey, S.; Wager, S. (2023). Offline Multi-Action Policy Learning: Generalization and Optimization. Operations Research.](https://doi.org/10.1287/opre.2022.2271)
12. [Dudík, M.; Langford, J.; Li, L. (2011). Doubly Robust Policy Evaluation and Learning. ICML.](https://arxiv.org/abs/1103.4601)
13. [Li, L. et al. (2011). Unbiased Offline Evaluation of Contextual-bandit-based News Article Recommendation Algorithms. WSDM.](https://doi.org/10.1145/1935826.1935878)
14. [Swaminathan, A.; Joachims, T. (2015). Counterfactual Risk Minimization: Learning from Logged Bandit Feedback. ICML.](https://proceedings.mlr.press/v37/swaminathan15.html)
15. [Agarwal, A. et al. (2014). Taming the Monster: A Fast and Simple Algorithm for Contextual Bandits. ICML.](https://proceedings.mlr.press/v32/agarwalb14.html)
16. [Foster, D.; Rakhlin, A. (2020). Beyond UCB: Optimal and Efficient Contextual Bandits with Regression Oracles. ICML.](https://proceedings.mlr.press/v119/foster20a.html)
17. [Kazerouni, A. et al. (2017). Conservative Contextual Linear Bandits. NeurIPS.](https://proceedings.neurips.cc/paper/2017/hash/bdc4626aa1d1df8e14d80d345b2a442d-Abstract.html)
18. [Badanidiyuru, A.; Kleinberg, R.; Slivkins, A. (2013/2017). Bandits with Knapsacks.](https://arxiv.org/abs/1305.2545)
19. [Joulani, P.; György, A.; Szepesvári, C. (2013). Online Learning under Delayed Feedback. ICML.](https://proceedings.mlr.press/v28/joulani13.html)
20. [Thomas, P. S.; Theocharous, G.; Ghavamzadeh, M. (2015). High Confidence Policy Improvement. ICML.](https://proceedings.mlr.press/v37/thomas15.html)
21. [GRF: multi_arm_causal_forest documentation.](https://grf-labs.github.io/grf/reference/multi_arm_causal_forest.html)
22. [policytree: interpretable policy learning documentation.](https://grf-labs.github.io/policytree/)
23. [Vowpal Wabbit 9.6.0 contextual bandit options and probability-aware labels.](https://vowpalwabbit.org/docs/vowpal_wabbit/python/9.6.0/command_line_args.html)

## 16.2 Interference, fairness, privacy и recommender risks

24. [Hudgens, M. G.; Halloran, M. E. (2008). Toward Causal Inference With Interference. JASA.](https://pmc.ncbi.nlm.nih.gov/articles/PMC2600548/)
25. [Aronow, P. M.; Samii, C. (2017). Estimating Average Causal Effects Under General Interference. Annals of Applied Statistics.](https://arxiv.org/abs/1305.6156)
26. [Ugander, J. et al. (2013). Graph Cluster Randomization: Network Exposure to Multiple Universes. KDD.](https://arxiv.org/abs/1305.6979)
27. [Baird, S.; Bohren, J. A.; McIntosh, C.; Özler, B. (2018). Optimal Design of Experiments in the Presence of Interference. The Review of Economics and Statistics.](https://doi.org/10.1162/rest_a_00716)
28. [Chaney, A. J. B.; Stewart, B. M.; Engelhardt, B. E. (2018). How Algorithmic Confounding in Recommendation Systems Increases Homogeneity and Decreases Utility. RecSys.](https://arxiv.org/abs/1710.11214)
29. [Rudin, C. (2019). Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. Nature Machine Intelligence.](https://doi.org/10.1038/s42256-019-0048-x)
30. [Kaufman, S. et al. (2012). Leakage in Data Mining: Formulation, Detection, and Avoidance. ACM TKDD.](https://doi.org/10.1145/2382577.2382579)
31. [Sweeney, L. (2002). k-Anonymity: A Model for Protecting Privacy.](https://dataprivacylab.org/projects/kanonymity/index.html)
32. [Machanavajjhala, A. et al. (2006/2007). l-Diversity: Privacy Beyond k-Anonymity.](https://doi.org/10.1145/1217299.1217302)
33. [Hardt, M.; Price, E.; Srebro, N. (2016). Equality of Opportunity in Supervised Learning. NeurIPS.](https://arxiv.org/abs/1610.02413)
34. [Suresh, H.; Guttag, J. (2021). A Framework for Understanding Sources of Harm throughout the Machine Learning Life Cycle.](https://doi.org/10.1145/3465416.3483302)
35. [Selbst, A. D. et al. (2019). Fairness and Abstraction in Sociotechnical Systems. FAccT.](https://doi.org/10.1145/3287560.3287598)
36. [NIST AI Risk Management Framework 1.0, released 26 January 2023; current revision status noted by NIST in 2026.](https://www.nist.gov/itl/ai-risk-management-framework)
37. [Weber, B.; Hertel, G. (2007). Motivation Gains of Inferior Group Members: A Meta-Analytical Review.](https://pubmed.ncbi.nlm.nih.gov/18072849/)
38. [Karau, S. J.; Williams, K. D. (1993). Social Loafing: A Meta-Analytic Review and Theoretical Integration.](https://doi.org/10.1037/0022-3514.65.4.681)

## 16.3 Retail cases

39. [Tesco (29 April 2024). Tesco brings its AI game to new Clubcard Challenges.](https://www.tescoplc.com/tesco-brings-its-ai-game-to-new-clubcard-challenges/)
40. [Tesco Preliminary Results 2024/25 (10 April 2025).](https://www.tescoplc.com/preliminary-results-202425/)
41. [Tesco Interim Results 2025/26 (2 October 2025).](https://www.tescoplc.com/interim-results-trading-statement-202526/)
42. [Tesco Preliminary Results 2025/26 (16 April 2026).](https://www.tescoplc.com/preliminary-results-202526/)
43. [Eagle Eye. Tesco Clubcard Challenges case study.](https://eagleeye.com/case-studies/tesco-clubcard-challenges)
44. [Morrisons (16 April 2024). My Points Boosters trial announcement.](https://www.morrisons-corporate.com/media-centre/corporate-news/morrisons-media-group-mmg-launches-innovative-channels-for-brands-to-connect-with-customers/)

## 16.4 Ограничение источников

**\[FACT\]** Ни один внешний источник не раскрывает внутренние данные X5, causal effect конкретных предлагаемых механик, вкладную маржу, fraud loss или reward economics X5. Поэтому все такие величины остаются `TO_VALIDATE`.

# Контроль качества перед реализацией

## Единицы utility

- Все маржинальные и cost-компоненты — RUB per randomized eligible unit per declared horizon.
- Reward `expected cost` и `max liability` разделены.
- Group utility использует yard/cluster unit либо явно агрегируется из member units.
- Completion, probability и score не складываются с рублями без monetary mapping.

## Availability at decision time

- Все окна заканчиваются строго до `decision_ts`.
- Returns/fraud outcomes после решения — delayed labels, не features.
- Group progress после решения не входит в score этого решения.
- Policy, parameter, template и model versions зафиксированы.

## Label leakage

- Synthetic truth (`is_fraud`, simulated response type) недоступна policy.
- No-action baseline model обучается time-split и не использует treatment-generated events как pre-treatment.
- Outcome maturity и censoring логируются.

## Причинная корректность

- PoC outputs помечены `ASSUMPTION/TO_VALIDATE`; слово uplift не применяется к completion.
- Pilot содержит A0, known propensities и stable treatment definitions.
- OPE выполняется только внутри support; DR не используется как оправдание hidden confounding.
- «Двор» анализируется с interference-aware unit/design.

## Экономика, antifraud и pilot

- Hard budget gate работает на max liability до выбора action.
- Fraud service failure блокирует monetary actions.
- Pending settlement не отменяет мгновенный non-monetary progress, но финансовое обещание неизменно и прозрачно.
- Primary business result — net incremental contribution margin; frequency/completion не могут компенсировать отрицательную маржу.
- Rollback сохраняет уже обещанные пользователю условия.

## Финальная рекомендация

**\[INFERENCE\]** Для защиты PoC показывать не «AI нашёл лучший uplift», а воспроизводимый decision trace: какие actions были допустимы, какие hard constraints сработали, из каких рублёвых компонентов сложилась low/base/high utility, почему победило действие или `NO_INTERVENTION`, и какие randomized logs потребуются, чтобы заменить assumptions causal estimates.
