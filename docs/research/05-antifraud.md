# Explainable precision-first антифрод PoC для игровой лояльности X5

**Чеки, возвраты, рефералы и кооперативная механика «Двор»**
*Исследовательский отчёт*
**Дата:** 4 сентября 2026

**Фокус:** чеки, возвраты, рефералы, кооперативная механика «Двор»
**Аудитория:** продукт, антифрод, аналитика, CRM, безопасность и юристы
**Статус:** исследовательский дизайн и воспроизводимая синтетическая проверка; не production-решение

> **Прямой ответ.** Запускать PoC целесообразно как rule-first и graph-lite контур с приоритетом precision: объективно невалидные reward-события отклоняются на уровне события, денежная награда проходит через `pending`, а необратимая блокировка аккаунта возможна только при высокой сумме риска и не менее чем двух независимых семействах сигналов. Визуальный XP и прогресс можно показывать сразу. Утверждение «фейковый реферал невыгоден, потому что награда только после покупки» верно лишь в узком случае и не выдерживает adversarial-аудит при дешёвой квалификации, финансировании покупки пригласившим, возврате, захвате групповой выгоды или сговоре.

### Как читать маркировку доказательности

- **FACT** - утверждение непосредственно поддержано указанным источником или результатом воспроизводимого прогона.
- **INFERENCE** - инженерный вывод из фактов и механики продукта; он логичен, но не измерен на данных X5.
- **ASSUMPTION** - числовой или продуктовый параметр сценария, введённый для PoC.
- **TO_VALIDATE** - вопрос, который нельзя закрыть без реального data contract, правовой оценки или контролируемого пилота.

## 0. Резюме решения

### 0.1 Рекомендуемая конструкция

1.  **Objective integrity layer.** Точный повтор уже вознаграждённого чека, подтверждённый возврат до расчёта награды и иной детерминированный конфликт приводят к `reject_event` или `reverse_reward`, но сами по себе не объявляют пользователя мошенником.
2.  **Reward state machine.** `observed -> visual_progress -> pending_cash -> confirmed | reversed`. Это отделяет эмоциональную обратную связь от окончательного денежного расчёта.
3.  **Explainable risk score.** Весовые правила формируют score 0-100 и список стабильных reason codes.
4.  **Two-family gate.** `block` разрешён только при высоком score и минимум двух независимых семействах сигналов. Один общий телефон, один Wi-Fi, редкая корзина или массовое приглашение не блокируют.
5.  **Graph-lite.** Для PoC достаточно явных графовых признаков: степени узлов, взаимность, короткие циклы, доля контроля «Двора», общие токены и временные всплески. GNN и большой graph platform нужны только после доказанного прироста.
6.  **Human-in-the-loop.** Пограничные случаи идут в `manual_review`; пользователь получает апелляцию и повторную попытку после исправления данных.
7.  **Monitoring and rollback.** Каждое правило имеет hit rate, precision sample, жалобы, отмены решения, monetary impact, версию и kill switch.

> **FACT.** Публичная система FENCE описывает именно проблему multiple IDs ради referral/promotional bonuses и сочетает графовые связи с human-in-the-loop; это архитектурный аналог, а не источник переносимых порогов ([FENCE, Upreti et al., 2023](https://arxiv.org/abs/2310.05651)).
> **FACT.** PromoGuardian рассматривает promotion abuse как групповое явление со spatial/temporal relations и принят в IEEE S&P 2026; опубликованные показатели относятся к чужой платформе и не являются benchmark X5 ([preprint](https://arxiv.org/abs/2510.12652), [accepted papers](https://sp2026.ieee-security.org/accepted-papers.html)).
> **INFERENCE.** Поэтому PoC должен сначала доказать ценность понятных агрегатов и правил, а не начинаться с непрозрачной GNN.

### 0.2 Условия go / no-go

> **ASSUMPTION.** Для перехода из shadow mode к автоматическому `block` одновременно нужны:

- нижняя 95% граница precision на независимом реальном holdout не ниже согласованного product-risk уровня;
- отсутствие необратимого решения по одной семье сигналов;
- review volume внутри мощности Fraud Ops;
- стабильный pending SLA и приемлемая доля апелляций;
- положительный net benefit при консервативной стоимости false positive;
- юридически утверждённые purpose, retention, доступ и сценарий автоматизированного решения.

**NO-GO:** если эти условия не доказаны, система остаётся в `pending`/`manual_review`; score используется для маршрутизации, а не для санкции.

## 1. Метод, область и границы доказательности

### 1.1 Вопрос и исключения

Исследование отвечает на практический вопрос: как построить объяснимый антифрод-контур для игровой лояльности X5, который ограничивает abuse чеков, возвратов, рефералов и «Двора», но не наказывает обычные домохозяйства и пользователей с нетипичным поведением. Полный юридический аудит, калибровка на production-данных, OCR/forensics изображений чеков, device fingerprinting SDK и промышленная графовая платформа не входят в PoC.

### 1.2 Источники и принцип переноса

Приоритет отдан первичным материалам: research papers, официальные условия reward-программ, нормативные тексты и security guidance. Внешние цифры используются только для архитектурных выводов. В частности, 93.15% precision из PromoGuardian и показатели FENCE нельзя переносить на grocery loyalty: отличаются fraud base rate, стимулы, набор идентификаторов, доступность разметки и цена ошибки.

> **FACT.** Для редкого класса PR-кривая и average precision информативнее одной ROC-кривой; это особенно важно, когда отрицательных событий намного больше ([Saito and Rehmsmeier, 2015](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432)).
> **FACT.** Cost-sensitive decision making требует выбирать действие по ожидаемой стоимости, а не по абстрактной точности; стоимость может быть не только денежной ([Elkan, 2001](https://cseweb.ucsd.edu/~elkan/rescale.pdf)).

### 1.3 Критерий остановки исследования

Поиск остановлен после того, как были закрыты пять consequential-слотов: coordinated abuse, reward settlement, evaluation under imbalance, privacy/security и synthetic-data limitations. Дополнительные источники повторяли уже подтверждённые принципы и не меняли решение: rule-first PoC, graph-lite признаки, staged settlement, two-family gate и статистически честная валидация.

## 2. Threat model

### 2.1 Активы, акторы и ущерб

| **Актив / доверие**          | **Актор и путь**                                          | **Возможный ущерб**                            | **Precision-first контроль**                            | **Остаточный риск**             |
|------------------------------|-----------------------------------------------------------|------------------------------------------------|---------------------------------------------------------|---------------------------------|
| Бюджет наград                | Одиночный пользователь: повтор чека, самореферал, возврат | Прямая выплата, dilution промо                 | event dedupe; pending; return reconciliation            | Новые варианты «почти дублей»   |
| Бюджет и база аккаунтов      | Фермер аккаунтов: звезда, циклинг                         | Массовое получение бонусов                     | mature conversion; lifetime; shared tokens; rate limits | Низкоскоростная ферма           |
| Справедливость «Двора»       | Коалиция участников                                       | Захват групповой награды, вытеснение честных   | доля контроля; циклы; churn/rejoin; contribution caps   | Сговор без технических связей   |
| Аналитика промо              | Brand/merchant abuse или stuffing                         | Ложный uplift, завышенные reimbursement claims | SKU/return reconciliation; counterfactual monitoring    | Легальные промо-всплески        |
| Доверие клиента              | Слишком агрессивный antifraud                             | Жалобы, отток, публичный ущерб                 | one-signal no-block; appeal; reason codes; sampled QA   | Скрытая дискриминация по прокси |
| Безопасность идентификаторов | Внутренний нарушитель или утечка                          | Re-identification, linkability                 | HMAC/tokenization; key separation; RBAC; audit          | Корреляция между системами      |
| Операционная устойчивость    | Ошибка данных/правила                                     | Массовые ложные hold/block                     | shadow, canary, kill switch, versioning                 | Задержка обнаружения инцидента  |

### 2.2 Trust boundaries

1.  POS/receipt source of truth - данные о чеке, строках, оплате и возврате.
2.  Loyalty identity - токен аккаунта, история бонусов, статусы согласий.
3.  Technical linkage service - токены device/payment/network; не выдаёт исходные идентификаторы аналитикам.
4.  Referral/Dvor service - временные ребра приглашений, членство, вклад и цели.
5.  Risk decision service - только агрегированные признаки, score, action, reason codes.
6.  Fraud Ops - минимально необходимый case view с журналом доступа.
7.  Product UI - только безопасный статус; без раскрытия точных порогов и связей.

### 2.3 Preventive и detective controls

**Preventive:** уникальность reward claim; qualification state; pending settlement; caps; inviter cannot fund qualifying transaction where detectable; rejoin cooldown; per-yard concentration guard.
**Detective:** graph features; return-after-reward; clone baskets; temporal bursts; component growth; manual sampling.
**INFERENCE.** Preventive controls обычно дешевле расследования, но слишком жёсткая prevention переносит цену на честных пользователей. Поэтому она допустима только для объективной eligibility, а подозрение должно вести в hold/review.

## 3. Adversarial-аудит утверждения про «Двор»

### 3.1 Экономический тест

Утверждение «фейковый участник невыгоден, потому что бонус появляется лишь после покупки» выполняется, только если:

    PrivateReward + CapturedGroupBenefit + ReversibleSpendBenefit
        <= IrreversibleQualifyingCost + CoordinationCost + ExpectedDetectionLoss

> **INFERENCE.** Квалифицирующая покупка не устраняет атаку, а добавляет цену входа. Если цена входа ниже частной и групповой выгоды или покупка обратима, атака остаётся рациональной.

### 3.2 Минимум 8 стратегий атаки

| **\#** | **Стратегия**                         | **Почему исходное утверждение сужается/ломается**                                | **Prevention**                                                    | **Detection и остаточный риск**                                             |
|--------|---------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------|-----------------------------------------------------------------------------|
| 1      | Самореферал + дешёвая квалификация    | Небольшой чек может разблокировать большую частную/групповую выгоду              | minimum eligible basket; non-transferable reward; pending         | self-link + shared payment + cheap qualifier; семьи могут делить устройство |
| 2      | Пригласивший финансирует покупку      | Экономическая цена остаётся у одного злоумышленника, а аккаунты формально разные | запрет/hold при общем payment token; лимит inviter-funded pattern | shared payment + short lifetime; наличные не видны                          |
| 3      | Возврат после начисления              | Квалифицирующая трата обратима                                                   | confirmation после окна возврата; clawback                        | return-after-reward; поздний возврат остаётся                               |
| 4      | Циклинг аккаунтов                     | Стоимость квалификации повторяется, но бонусный цикл тоже                        | cooldown на повторное устройство/платёж; lifetime qualification   | короткая жизнь + re-registration; новые устройства снижают сигнал           |
| 5      | «Звезда»: один центр, много листьев   | Каждый лист делает минимально допустимое действие                                | progressive cap; maturation by invitee quality                    | fanout burst + low matured conversion; органический инфлюенсер похож        |
| 6      | Кольцо взаимных приглашений           | Выгода циркулирует внутри группы, не требует одного центра                       | запрет reciprocal qualification; component caps                   | короткие циклы + общие токены; длинные циклы труднее                        |
| 7      | Захват большинства «Двора»            | Атакующий контролирует правила/цель и получает externality от честных участников | concentration limit; independent-member quorum                    | control share + linked component; сговор реальных людей                     |
| 8      | Координированный fake progress        | Несколько аккаунтов синхронно создают видимость вклада                           | contribution maturity; diminishing returns                        | временные всплески, похожие корзины; реальные семьи синхронны               |
| 9      | Churn/rejoin для сброса цели          | Повторный вход меняет denominator, статус или цель                               | rejoin cooldown; immutable cycle accounting                       | повторные membership intervals; смена «Двора» может быть легитимной         |
| 10     | Эксплуатация backup-коэффициента      | Недовыполненный вклад переносится/компенсируется выгоднее, чем честный           | cap на перенос; non-linear backup only after quality checks       | abnormal deficit transfer; сложность объяснения пользователю                |
| 11     | Free-rider / низкая персональная цель | Аккаунт почти не тратит, но получает долю групповой награды                      | minimum personal contribution; share proportionality              | low contribution over cycles; риск наказать малобюджетных клиентов          |
| 12     | Brand-funded SKU stuffing + возврат   | Брендовая субсидия и возврат могут сделать net cost нулевой/отрицательной        | settle after returns; per-SKU caps; net sales basis               | SKU spike + rapid return; сезонное промо даёт похожий паттерн               |

### 3.3 Вердикт

> **INFERENCE.** Тезис про невыгодность можно оставить только как product hypothesis: «пустой аккаунт без покупки, возврата, финансирования и контроля группы не получает награду». Нельзя использовать его как antifraud guarantee. «Двор» создаёт дополнительную attack surface, потому что один участник способен присвоить часть выгоды, созданной другими.
>
> **TO_VALIDATE.** Нужны точные правила распределения награды, цели, backup-механики, rejoin, refundable SKUs, источник финансирования и временная связь между purchase, return и settlement.

## 4. Минимальная архитектура PoC

### 4.1 Decision pipeline

| **Стадия**                | **Данные, доступные к моменту решения**                                  | **Выход**                          | **Запрещённое действие**                                         |
|---------------------------|--------------------------------------------------------------------------|------------------------------------|------------------------------------------------------------------|
| T0: submit                | чек, account token, coarse time/store, доступные technical tokens        | validate; visual XP; allow/pending | использовать будущий возврат или matured conversion              |
| T1: maturity              | статус возврата, qualifying purchase, elapsed window, invitee activation | confirm/reverse; review            | переписывать историю признаков задним числом                     |
| T2: periodic graph review | component degree, cycles, control share, churn/rejoin                    | account review/block proposal      | блок по одному proxy-сигналу                                     |
| T3: appeal/ops            | case evidence, rule versions, analyst outcome                            | uphold/release; label feedback     | показывать исходные payment/device identifiers без необходимости |

### 4.2 Reward state machine

    OBSERVED
      -> VISUAL_PROGRESS      # XP, animation, streak; reversible accounting flag
      -> PENDING_CASH         # monetary value not spendable yet
          -> CONFIRMED        # eligibility matured, no disqualifying event
          -> REVERSED         # duplicate/return/failed qualification
          -> MANUAL_REVIEW    # conflicting high-risk evidence

> **FACT.** В официальной reward-практике Rakuten cashback остаётся pending, подтверждение зависит от merchant data, returns/exchanges и иных изменений; referral bonus подтверждается после qualifying purchase и подтверждения cashback ([Rakuten FAQ](https://www.rakuten.com/help/article/bilt-faq), [Terms updated 15 Oct 2025](https://www.rakuten.com/help/article/terms-conditions)).
> **INFERENCE.** Это подтверждает жизнеспособность staged settlement как паттерна, но срок 3-14 недель к grocery X5 не переносится. Для X5 нужен собственный минимальный срок по фактической latency возвратов.

### 4.3 Почему graph-lite, а не GNN

> **FACT.** EnsemFDet показывает применимость dense-subgraph подходов к transaction graphs на JD.com, а Temporal Motifs показывает ценность временных циклов/повторов в финансовых сетях ([EnsemFDet](https://arxiv.org/abs/1912.11113), [Temporal Motifs](https://arxiv.org/abs/2301.07791)).
> **INFERENCE.** Для PoC этого достаточно, чтобы считать степени, взаимность, короткие циклы и компонентные агрегаты. GNN оправдана только если explicit features не дают нужный recall при том же precision и есть инфраструктура для latency, explainability, drift и backfills.

## 5. Data contract

### 5.1 Семантический контракт

| **Поле**                                       | **Тип и гранулярность**                   | **Доступность**            | **Назначение PoC**              | **Leakage guard**                             |
|------------------------------------------------|-------------------------------------------|----------------------------|---------------------------------|-----------------------------------------------|
| `receipt_token`                                | HMAC token; reward event                  | T0                         | exact dedupe                    | не вычислять из label/outcome                 |
| `receipt_canonical_hash`                       | HMAC нормализованного store/time/basket   | T0 после нормализации      | cross-account clone candidate   | хранить версию canonicalizer                  |
| `account_token`                                | токен аккаунта                            | T0                         | node/account aggregation        | `is_fraud` в другом namespace                 |
| `device_token`                                 | rotating keyed token                      | T0 при наличии             | degree/new-account linkage      | missing = unknown, не benign                  |
| `payment_token`                                | processor/network token, не PAN           | T0/T1                      | funding linkage                 | отдельный vault; минимальный доступ           |
| `network_bucket_token`                         | грубый ASN/subnet bucket                  | T0                         | burst/context only              | никогда не использовать один                  |
| `store_id`                                     | магазин, не GPS                           | T0                         | velocity/cohort baseline        | no precise customer location                  |
| `event_ts_bucket`                              | 5-15 min bucket                           | T0                         | velocity/bursts                 | raw timestamp только ограниченному сервису    |
| `receipt_total_rub`                            | decimal; receipt                          | T0                         | qualifier/economics             | нормировать по channel/store                  |
| `sku_token`, `category_id`, `qty`, `net_price` | line item                                 | T0                         | clone, quantity, brand patterns | исключить текстовые персональные поля         |
| `return_status`, `return_ts`                   | receipt/line                              | T1                         | reward reversal; rapid return   | запрещено в T0 model snapshot                 |
| `invite_edge`                                  | inviter, invitee, created_ts              | T0                         | fanout, reciprocity             | temporal edge; не заменять current state      |
| `qualification_state`                          | enum + effective_ts                       | T1                         | matured conversion              | только состояние на decision_ts               |
| `yard_membership_interval`                     | yard, account, from/to                    | T0-T2                      | control, churn/rejoin           | reconstruct point-in-time membership          |
| `yard_contribution`                            | cycle/account/category                    | T1/T2                      | progress quality                | distinguish visual vs settled                 |
| `reward_ledger`                                | reward id, state, amount, funder          | T0-T2                      | exposure/prevented loss         | immutable event sourcing                      |
| `decision_log`                                 | score, action, rule version, reason codes | decision                   | audit/appeal                    | no raw tokens in product logs                 |
| `is_fraud`, `attack_type`                      | evaluator-only                            | after generation/ops label | metrics only                    | schema physically separated from feature view |

### 5.2 Обращение, retention и доступ

| **Группа**        | **Псевдонимизация**                                 | **Retention - ASSUMPTION**                       | **Доступ**                                   | **Комментарий**                                   |
|-------------------|-----------------------------------------------------|--------------------------------------------------|----------------------------------------------|---------------------------------------------------|
| Link tokens       | keyed HMAC/token vault, key separation and rotation | raw link map 30-90 дней; aggregates 180-365 дней | risk service; ограниченный security admin    | сроки **TO_VALIDATE** по 152-ФЗ, цели и возвратам |
| Receipt lines     | SKU/category tokens; без имён/адресов               | 180-365 дней                                     | feature pipeline; case view по необходимости | хранить минимальный набор для апелляции           |
| Graph edges       | токены + effective intervals                        | 180-365 дней                                     | graph feature job                            | удаление должно каскадировать в feature store     |
| Decision/evidence | reason codes, версии, evidence hashes               | срок спора + audit need                          | Fraud Ops/Risk Governance                    | точный срок утверждает legal/records policy       |
| Product telemetry | aggregate status only                               | минимальный operational SLA                      | support/product                              | не логировать payment/device token                |

> **FACT.** GDPR определяет pseudonymisation как обработку, при которой связь с субъектом требует дополнительной информации, и рассматривает такие данные как персональные при возможности обратного связывания; он также закрепляет minimisation и storage limitation ([EUR-Lex, Regulation 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng)).
> **FACT.** Российский 152-ФЗ в актуальной странице содержит определения, принципы обработки, права при исключительно автоматизированных решениях и требования безопасности; страница отражает изменения до 26 июля 2026 года ([152-ФЗ, КонсультантПлюс](https://www.consultant.ru/document/cons_doc_LAW_61801/)).
> **TO_VALIDATE.** Применимость конкретных норм, правовое основание, уведомления, локализация, сроки и схема апелляции требуют отдельного заключения X5 Legal/Privacy. Этот отчёт не является юридической консультацией.

## 6. Каталог признаков

### 6.1 Чеки и возвраты

| **Feature**                         | **Формула / окно**                                             | **Направление риска** | **Missing handling**                 | **Объяснение и FP-риск**                                  |
|-------------------------------------|----------------------------------------------------------------|-----------------------|--------------------------------------|-----------------------------------------------------------|
| `exact_reward_duplicate`            | тот же `receipt_token` уже получил reward                      | резкий рост           | source unavailable -\> pending       | объективная неeligible попытка; возможен retry UX         |
| `canonical_cross_account_duplicate` | одинаковый canonical hash у разных accounts                    | рост                  | no lines -\> не считать              | семейная покупка/ошибка POS возможна; нужен второй сигнал |
| `basket_clone_similarity`           | weighted Jaccard/MinHash по SKU, qty, net price                | рост                  | sparse basket -\> lower confidence   | типовая корзина в одном магазине создаёт FP               |
| `impossible_velocity`               | разные store/channel за физически/операционно невозможное окно | рост                  | coarse store only -\> wide tolerance | часы/таймзоны/POS delay должны быть нормализованы         |
| `qty_price_robust_z`                | robust z внутри store-category-week                            | U-shaped/outlier      | cohort too small -\> global fallback | оптовая семейная покупка легитимна; не hard rule          |
| `rapid_return_ratio`                | returned eligible amount / rewarded amount, 7-60d              | рост                  | open return window -\> pending       | обычные возвраты допустимы; важна повторяемость           |
| `reward_after_return`               | reward confirmed after disqualifying return                    | высокий               | inconsistent ledger -\> ops incident | может быть системная ошибка, не user fraud                |
| `brand_return_stuffing`             | funded SKU spike + high return ratio                           | рост                  | funder missing -\> no feature        | сезонная акция похожа; compare matched stores             |

### 6.2 Идентичность, техника и рефералы

| **Feature**                  | **Формула / окно**                                   | **Направление риска**      | **Missing handling**                  | **Объяснение и FP-риск**                         |
|------------------------------|------------------------------------------------------|----------------------------|---------------------------------------|--------------------------------------------------|
| `device_account_degree`      | distinct new accounts per device, 7/30d              | рост после cohort baseline | missing -\> unknown                   | общий семейный телефон; один не блокирует        |
| `payment_account_degree`     | accounts per payment token, 30/90d                   | рост                       | cash -\> unknown                      | семейная карта; нужен referral/economic signal   |
| `network_registration_burst` | new accounts in coarse network bucket, 1h/24h        | слабый рост                | mobile NAT -\> low weight             | общежитие/офис/магазин; только context           |
| `self_link_strength`         | inviter/invitee share stable technical/payment token | высокий                    | unavailable -\> no penalty            | shared household требует manual semantics        |
| `fanout_burst`               | new invitees per inviter, 48h/7d                     | рост                       | immature edges excluded               | легитимный инфлюенсер; сочетать с conversion     |
| `matured_nonqualify_ratio`   | invitees without eligible purchase after maturity    | рост                       | right-censored -\> exclude            | нельзя считать новые invitees «плохими» заранее  |
| `short_lifetime_share`       | invitees inactive shortly after reward               | рост                       | observation incomplete -\> exclude    | сезонные пользователи могут быть краткосрочными  |
| `reciprocity_cycle_score`    | reciprocal edges / cycles length 2-8, 14-30d         | рост                       | graph incomplete -\> lower confidence | реальные друзья могут приглашать друг друга      |
| `inviter_funded_share`       | qualifying events sharing inviter payment token      | высокий                    | cash/missing -\> unknown              | сильный признак только при надёжном tokenization |
| `cheap_qualifier_share`      | spend near minimum threshold                         | слабый-средний             | threshold version required            | честный price-sensitive user; никогда один       |

### 6.3 «Двор» и компоненты

| **Feature**                      | **Формула / окно**                                      | **Направление риска** | **Missing handling**                  | **Объяснение и FP-риск**                          |
|----------------------------------|---------------------------------------------------------|-----------------------|---------------------------------------|---------------------------------------------------|
| `yard_control_share`             | members/invite paths controlled by one linked component | рост                  | missing links -\> lower bound         | большая семья/ТСЖ может быть реальной             |
| `yard_component_density`         | linked edges / possible edges within yard               | рост                  | small yard -\> shrinkage              | малые группы дают нестабильную оценку             |
| `churn_rejoin_count`             | membership exits/entries in 60-120d                     | рост                  | history truncation -\> unknown        | переезд/ошибка UX легитимны                       |
| `backup_exploit_score`           | repeated gain from deficit transfer/reset               | рост                  | rule version required                 | механизм может сам создавать аномалию             |
| `synchronous_progress`           | correlated contributions within short windows           | рост                  | timezone/POS delays -\> tolerance     | совместные походы семьи похожи на атаку           |
| `component_reward_concentration` | share of yard reward to linked component                | рост                  | reward ledger incomplete -\> no score | различия в spend capacity требуют fairness review |

## 7. Таблица правил PoC

Все числовые пороги ниже - **ASSUMPTION** для синтетического теста, не production-конфигурация и не текст для пользователя.

| **Rule / reason code**      | **Условие PoC**                                | **Тип**               | **Вес / gate** | **Action и защита от FP**                      |
|-----------------------------|------------------------------------------------|-----------------------|----------------|------------------------------------------------|
| R001 `EXACT_DUPLICATE`      | receipt token уже rewarded                     | objective event       | hard event     | `reject_event`; аккаунт не блокировать         |
| R002 `CANONICAL_CLONE`      | одинаковый canonical receipt в разных accounts | heuristic             | +25..35        | pending/review; нужен второй family            |
| R003 `IMPOSSIBLE_VELOCITY`  | 2-5 конфликтующих событий за 10-30 min         | heuristic             | +20..30        | review; учитывать POS latency                  |
| R004 `BASKET_CLONE`         | similarity выше cohort percentile              | heuristic             | +12..22        | не блокирует без identity/graph                |
| R010 `DEVICE_DEGREE`        | 3-6 новых accounts на token за 7d              | weak heuristic        | +5..10         | household negative test обязателен             |
| R011 `PAYMENT_DEGREE`       | 3-5 accounts на payment token                  | medium                | +8..15         | семейная карта + no referral -\> allow/pending |
| R012 `SELF_LINK`            | inviter и invitee устойчиво связаны            | strong                | +25..35        | manual semantics; cash cases unknown           |
| R020 `STAR_LOW_CONVERSION`  | 8-20 invites/48h + low matured conversion      | compound              | +20..35        | maturation required; influencer exception path |
| R021 `RECIPROCAL_RING`      | cycle 2-8 nodes + shared token                 | compound              | +25..40        | graph evidence + second family                 |
| R022 `SHORT_LIFETIME`       | высокий share brief-life invitees              | medium                | +10..20        | censoring guard                                |
| R023 `INVITER_FUNDED`       | inviter payment funds invitee qualifier        | strong                | +20..35        | no raw payment details in UI                   |
| R030 `RETURN_BEFORE_SETTLE` | qualifier returned while cash pending          | objective eligibility | hard event     | reverse/reject reward; не account block        |
| R031 `RETURN_AFTER_REWARD`  | repeated reward then rapid return              | compound              | +25..40        | review; distinguish system error               |
| R040 `YARD_CONTROL`         | linked component controls 40-60% yard          | strong aggregate      | +25..40        | small-yard shrinkage; second family            |
| R041 `CHURN_REJOIN`         | 1-3 repeated cycles / 60-120d                  | medium                | +10..20        | cooldown, not permanent block                  |
| R042 `BACKUP_EXPLOIT`       | repeated disproportionate deficit benefit      | medium                | +10..20        | verify product formula first                   |
| R043 `BRAND_RETURN`         | funded SKU spike + rapid returns               | compound              | +20..35        | matched-store baseline; funder reconciliation  |

### 7.1 Hard rules vs heuristics

**Hard event rule** допустимо применять, когда система доказывает неeligibility события: один и тот же reward claim уже погашен, подтверждённый возврат отменяет условие или ledger state невозможен. Даже тогда action относится к reward-событию, а не к личности.
**Heuristic rule** повышает score и формирует reason code. Необратимый `block` требует второй независимый family.
**Operational anomaly** - конфликт ledger/POS/return pipeline - должен открывать incident, а не автоматически обвинять пользователя.

## 8. Score, policy и explainability

### 8.1 Формула

    risk_score = min(100,
                     sum(active_rule_weight)
                     + sum(interaction_bonus))

    block_allowed = (risk_score >= T_block)
                    and (independent_signal_families >= 2)
                    and (critical_data_quality_ok)

Семейства: receipt integrity, return behavior, technical link, identity link, referral graph, referral economics, yard control. Коррелирующие признаки внутри одной семьи не считаются независимым подтверждением.

### 8.2 Синтетическая policy table

| **Score / условие**   | **Action**      | **Денежный статус**      | **Пользовательский UX**                           | **Internal handling**                   |
|-----------------------|-----------------|--------------------------|---------------------------------------------------|-----------------------------------------|
| 0-24                  | `allow`         | normal                   | прогресс и reward по обычному SLA                 | sample 0.1-1% для quality               |
| 25-49                 | `pending`       | not spendable            | «Награда проверяется; прогресс сохранён»          | дождаться return/maturity/second signal |
| 50-74                 | `manual_review` | pending                  | нейтральный статус + срок                         | case pack с reason codes                |
| \>=75 и \>=2 families | `block`         | hold/reverse по правилам | «Награда временно недоступна; доступна апелляция» | dual control для high-value             |
| exact invalid event   | `reject_event`  | event reversed           | «Это событие уже учтено / покупка возвращена»     | не блокировать account автоматически    |

### 8.3 Псевдокод

    features = point_in_time_features(event, decision_ts)
    assert "is_fraud" not in features

    hard = objective_eligibility_check(event)
    if hard:
        return Decision("reject_event", reason=hard.code, account_block=False)

    score, reasons, families = weighted_rules(features)
    if not data_quality_ok(features):
        return Decision("pending", reason="DATA_INCOMPLETE")
    if score >= T_block and len(families) >= 2:
        return Decision("block", reasons=reasons)
    if score >= T_review:
        return Decision("manual_review", reasons=reasons)
    if score >= T_pending:
        return Decision("pending", reasons=reasons)
    return Decision("allow")

### 8.4 Honest reason codes

Internal reason code сообщает наблюдение, не мотив: `SHARED_PAYMENT_WITH_INVITER`, а не `FRAUDSTER`; `REWARD_EVENT_DUPLICATE`, а не `FAKE_RECEIPT`; `YARD_COMPONENT_CONCENTRATION`, а не `COLLUSION_CONFIRMED`. Customer-facing текст агрегирует причину и не раскрывает пороги, токены или граф соседей.

## 9. Воспроизводимые синтетические сценарии

### 9.1 Население и split

**FACT - synthetic run.** Seed `20260904` создаёт 12 000 аккаунтов и 65 632 reward-события. Компоненты хешируются в development/validation/test 60/20/20; связанные ring/yard accounts остаются в одной части. Итоговый test содержит 2,334 аккаунта, из них 186 fraud, и 12,888 события, из них 625 fraud.
**FACT - leakage guard.** Колонки `is_fraud` и `attack_type/cohort` передаются только evaluator; scoring читает booleans feature families, score и point-in-time state. Скрипт приложен к отчёту.

| **Cohort**              | **N accounts** | **Ground truth** | **Что генерируется**                                 |
|-------------------------|----------------|------------------|------------------------------------------------------|
| benign normal           | 10 300         | 0                | низкие независимые anomaly rates                     |
| shared-device household | 600            | 0                | общий device/payment/network без fraud family        |
| legit mass inviter      | 100            | 0                | высокий fanout, но нормальная matured conversion     |
| star                    | 120            | 1                | fanout burst, low conversion, short lifetime         |
| ring                    | 100            | 1                | reciprocity/cycles, shared tokens, funded qualifiers |
| account cycling         | 150            | 1                | short life, recreation, cheap qualification          |
| self-referral           | 120            | 1                | self links, shared payment/device, funded purchase   |
| clone receipts          | 150            | 1                | duplicate/near-clone/velocity receipt patterns       |
| return after reward     | 150            | 1                | rapid return and reward-return ordering              |
| Dvor capture            | 120            | 1                | majority control, linked component, churn/rejoin     |
| Dvor brand-return       | 90             | 1                | funded SKU stuffing, return, backup exploitation     |

### 9.2 Генератор и ожидаемая метка

- Feature values генерируются фиксированными Bernoulli profiles по cohort; это **ASSUMPTION**, а не оценка распространённости.
- Reward exposure генерируется lognormal distribution с различными synthetic medians по типу атаки.
- Закрытая event-разметка считает reward claims от seeded attack accounts положительными. Это делает denominator однозначным, но не моделирует mixed-intent attacker, который иногда покупает честно.
- Weights и thresholds зафиксированы до test evaluation; validation sweep сохранён отдельно.
- Twenty-seed fast stability check повторяет те же profiles и policy без переобучения.

> **TO_VALIDATE.** Production replay должен генерировать point-in-time snapshots из реального event log и включать delayed labels, partial returns, cash payment, missing technical tokens, household graph, seasonality и campaign changes.

## 10. Оценка PoC

### 10.1 Account-level test

Confusion matrix для `block`:

| **Actual / decision** | **not block** | **block** |
|-----------------------|---------------|-----------|
| benign                | 2148          | 0         |
| fraud                 | 87            | 99        |

- Precision@block: **100.00%**, Wilson 95% CI **96.26%–100.00%**, denominator 99 blocked accounts.
- Recall@block: **53.23%**, 95% CI **46.06%–60.26%**, denominator 186 fraud accounts.
- FPR: **0.00%**, 95% CI **0.00%–0.18%**, denominator 2148 benign accounts.
- PR-AUC: **0.9932**.
- Review-or-block recall: **87.63%** at observed precision **100.00%**.

**Interpretation.** Нулевой FP в 99 auto-blocks не доказывает «100% precision»: нижняя Wilson-граница лишь 96.26%. Для lower bound 98.5% при нуле ошибок нужно не менее 253 независимых positive decisions; для 99% - 381; для 99.5% - 765. Компонентная зависимость увеличивает эффективную потребность.

### 10.2 Event-level test

Confusion matrix для `block or reject_event`:

| **Actual / decision** | **not block/reject** | **block/reject** |
|-----------------------|----------------------|------------------|
| benign                | 12259                | 4                |
| fraud                 | 317                  | 308              |

- Precision: **98.72%**, 95% CI **96.75%–99.50%**, denominator 312 decisions.
- Recall: **49.28%**, 95% CI **45.38%–53.19%**.
- FPR: **0.03%**, 95% CI **0.01%–0.08%**.
- PR-AUC: **0.9937**.
- `manual_review or harder`: precision **99.16%**, recall **75.36%**.
- `any hold`: precision **96.17%**, recall **96.48%**.

**Interpretation.** Precision-first auto-action ловит примерно половину synthetic fraud-events, а `pending` поднимает coverage до 96.48% ценой большей доли честных hold. Это ожидаемый продуктовый trade-off: hold обратим, block нет.

### 10.3 Monetary metrics

- Fraud exposure в test: **202 949 ₽**.
- Заблокировано/отклонено fraud exposure: **110 039 ₽**.
- Monetary precision@block: **99.83%**, component-bootstrap 95% CI **99.61%–99.97%**.
- Monetary recall@block: **54.22%**, 95% CI **44.47%–64.35%**.
- Scenario prevented loss с resolution fractions `pending=45%`, `manual=75%`, `block/reject=100%`: **164 762 ₽**, monetary recall **81.18%**, 95% CI **76.67%–85.61%**.

> **ASSUMPTION.** Resolution fractions - сценарные коэффициенты, а не измеренная эффективность Fraud Ops. Без них доказан только block/reject lower bound.

| **Action**    | **События** | **Fraud-события** | **Доля fraud** | **Экспозиция** | **Предотвращено (сценарий)** |
|---------------|-------------|-------------------|----------------|----------------|------------------------------|
| allow         | 12261       | 22                | 0.2%           | 866 911 ₽      | 0 ₽                          |
| block         | 222         | 222               | 100.0%         | 79 670 ₽       | 79 670 ₽                     |
| manual_review | 163         | 163               | 100.0%         | 49 780 ₽       | 37 335 ₽                     |
| pending       | 152         | 132               | 86.8%          | 39 890 ₽       | 17 389 ₽                     |
| reject_event  | 90          | 86                | 95.6%          | 30 552 ₽       | 30 369 ₽                     |

### 10.4 Разрез по типу атаки

Account-level:

| **Тип атаки**                 | **Fraud-аккаунты в test** | **Recall auto-block** | **Recall review+block** |
|-------------------------------|---------------------------|-----------------------|-------------------------|
| циклинг аккаунтов             | 27                        | 40.7%                 | 81.5%                   |
| клоны чеков                   | 30                        | 23.3%                 | 80.0%                   |
| брендовый stuffing + возвраты | 15                        | 93.3%                 | 100.0%                  |
| захват «Двора»                | 25                        | 96.0%                 | 96.0%                   |
| возврат после награды         | 30                        | 20.0%                 | 86.7%                   |
| реферальное кольцо            | 5                         | 40.0%                 | 80.0%                   |
| самореферал                   | 33                        | 84.8%                 | 93.9%                   |
| реферальная «звезда»          | 21                        | 33.3%                 | 81.0%                   |

Event-level:

| **Тип атаки**                 | **Fraud-события в test** | **Recall block/reject** | **Recall review+** |
|-------------------------------|--------------------------|-------------------------|--------------------|
| циклинг аккаунтов             | 96                       | 27.1%                   | 60.4%              |
| клоны чеков                   | 100                      | 85.0%                   | 93.0%              |
| брендовый stuffing + возвраты | 51                       | 96.1%                   | 100.0%             |
| захват «Двора»                | 85                       | 37.6%                   | 78.8%              |
| возврат после награды         | 97                       | 71.1%                   | 91.8%              |
| реферальное кольцо            | 15                       | 20.0%                   | 53.3%              |
| самореферал                   | 114                      | 37.7%                   | 78.1%              |
| реферальная «звезда»          | 67                       | 1.5%                    | 23.9%              |

**Key findings.**

- Clone receipts имеют высокий event recall (85.0%), но низкий account auto-block recall, потому что receipt-only evidence остаётся в одной семье. Это желательное разделение event eligibility и account accusation.
- Return-after-reward чаще приводит к event action, чем к permanent account block.
- Dvor capture лучше виден на account/component aggregate, чем на отдельном событии.
- Star attack имеет очень низкий event auto-block recall: система намеренно не блокирует за fanout alone. Нужны matured conversion, identity linkage, rate-limits и экономические caps.
- Ring test содержит только 5 fraud accounts; любой процент здесь статистически нестабилен.

### 10.5 Повторные seeds

| **Метрика**                    | **Среднее** | **P05** | **Медиана** | **P95** |
|--------------------------------|-------------|---------|-------------|---------|
| Account recall @ block         | 50.81%      | 46.92%  | 51.52%      | 55.58%  |
| Event precision @ block/reject | 99.33%      | 98.67%  | 99.34%      | 100.00% |
| Event recall @ block/reject    | 46.78%      | 43.04%  | 47.18%      | 49.87%  |
| Event recall @ review+         | 75.49%      | 72.88%  | 75.58%      | 79.36%  |
| Event precision @ any hold     | 96.33%      | 95.20%  | 96.24%      | 97.52%  |
| Event recall @ any hold        | 96.59%      | 95.20%  | 96.67%      | 97.87%  |
| Monetary precision @ block     | 99.87%      | 99.74%  | 99.89%      | 100.00% |
| Monetary recall @ block        | 53.37%      | 48.36%  | 54.19%      | 56.92%  |
| Monetary recall, all actions   | 81.16%      | 78.87%  | 81.70%      | 82.97%  |

**FACT - synthetic stability.** В 20 seeds event precision@block имеет P05 98.67% и P95 100.00%; event recall P05-P95 равен 43.04%-49.87%.
**LIMIT.** Повтор seeds проверяет устойчивость собственного генератора, а не переносимость на реальный мир. J.P. Morgan AI Research описывает synthetic-data process как цикл «metrics on real data -\> generator -\> calibration», что подчёркивает необходимость калибровать генератор по реальным агрегатам ([J.P. Morgan synthetic data process](https://www.jpmorganchase.com/about/technology/research/ai/synthetic-data); [Assefa et al., ICAIF 2020](https://dl.acm.org/doi/10.1145/3383455.3422554)).

## 11. Выбор порога без подглядывания в test

### 11.1 Validation sweep

| **Порог** | **Precision** | **Нижняя 95% граница** | **Recall** | **FPR** | **Auto-blocks** |
|-----------|---------------|------------------------|------------|---------|-----------------|
| 55        | 99.44%        | 96.87%                 | 79.64%     | 0.05%   | 177             |
| 60        | 99.41%        | 96.72%                 | 76.02%     | 0.05%   | 169             |
| 65        | 100.00%       | 97.55%                 | 69.23%     | 0.00%   | 153             |
| 70        | 100.00%       | 97.35%                 | 63.80%     | 0.00%   | 141             |
| 75        | 100.00%       | 97.11%                 | 58.37%     | 0.00%   | 129             |
| 80        | 100.00%       | 96.82%                 | 52.94%     | 0.00%   | 117             |
| 85        | 100.00%       | 96.50%                 | 47.96%     | 0.00%   | 106             |
| 90        | 100.00%       | 95.99%                 | 41.63%     | 0.00%   | 92              |

> **ASSUMPTION.** Выбран `T_block=75`, потому что он сохраняет two-family gate и уменьшает auto-block volume; это не data-derived production optimum. Validation показывает, что observed 100% precision не даёт высокую нижнюю границу CI при малом числе решений.

### 11.2 Cost matrix

    ExpectedCost(t) = C_FP * FP(t)
                    + C_FN(event_amount) * FN(t)
                    + C_review * N_review(t)
                    + C_pending * N_pending(t)
                    + C_appeal * N_appeal(t)

| **Компонент**  | **Сценарный диапазон - ASSUMPTION** | **Что включить в production**                     |
|----------------|-------------------------------------|---------------------------------------------------|
| `C_FP block`   | 3 000-15 000 ₽ / account            | support, goodwill, LTV/churn, legal/escalation    |
| `C_FP pending` | 10-80 ₽ / event                     | contact rate, delay dissatisfaction, breakage     |
| `C_review`     | 80-250 ₽ / case                     | analyst time, tooling, QA, management overhead    |
| `C_FN`         | 1.0-3.0 x reward exposure           | direct loss, network propagation, repeat attempts |
| `C_appeal`     | 150-800 ₽ / case                    | support + ops + compensation                      |

**Decision rule.** На validation выбрать точку с максимальным conservative net benefit при ограничениях на нижнюю CI precision, review capacity, pending SLA и subgroup FPR. Test используется один раз для итоговой оценки. При недостаточном sample size action понижается с `block` до `manual_review`.

> **FACT.** Для time-ordered данных обычное перемешивание может обучать на будущем и оценивать на прошлом; TimeSeriesSplit документирует этот риск. Для связанных объектов нужны non-overlapping groups ([TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html), [GroupKFold family](https://scikit-learn.org/stable/api/sklearn.model_selection.html)).

## 12. Негативные и fairness-тесты

### 12.1 Обязательные benign cohorts

| **Кейс**                           | **Ожидаемое поведение**                                  | **Synthetic block rate** | **Дополнительная проверка**                     |
|------------------------------------|----------------------------------------------------------|--------------------------|-------------------------------------------------|
| Общий семейный телефон/карта/Wi-Fi | allow или pending; не block по technical-only            | 0.00%                    | пары parent/child, multi-generational household |
| Легитимный массовый пригласивший   | allow/pending; review только при low matured conversion  | 0.00%                    | influencer/corporate campaign exception         |
| Обычный пользователь               | низкий score                                             | 0.00%                    | weekly/seasonal drift                           |
| Соседи одного магазина             | no block from store/network proximity                    | **TO_VALIDATE**          | cluster by store and shift                      |
| Bulk family shopping               | quantity anomaly alone no block                          | **TO_VALIDATE**          | holidays, rural trips, wholesale-like basket    |
| Смена телефона                     | temporary missing/link discontinuity -\> pending at most | **TO_VALIDATE**          | restore identity without penalty                |
| Слабая связь / delayed POS         | widen timing tolerance                                   | **TO_VALIDATE**          | offline cash desk backfill                      |
| Cash payment                       | missing payment token != safe/fraud                      | **TO_VALIDATE**          | separate calibration by payment channel         |

### 12.2 Fairness protocol

1.  Считать FPR, pending rate, review overturn и appeal uphold по заранее разрешённым operational cohorts: store format, channel, region bucket, device availability, payment channel, household proxy. Не собирать чувствительные признаки без отдельного правового основания.
2.  Сравнивать не только абсолютный gap, но и причину: missingness и инфраструктурные задержки могут создавать proxy bias.
3.  Требовать minimum denominator и CI; не публиковать рейтинг малых магазинов/групп.
4.  Для rule changes проводить counterfactual replay: сколько прежних benign cases изменили action.
5.  Если subgroup FPR превышает guardrail, отключать rule для auto-block, сохраняя review.

## 13. Продуктовое поведение

### 13.1 Что показывать сразу

- XP, анимацию, streak, вклад в визуальную шкалу - сразу, с флагом `provisional` в ledger.
- Денежный reward, промокод высокой стоимости или переносимый актив - только после `confirmed`.
- При `pending` не обнулять визуальный прогресс и не использовать обвинительный текст.

### 13.2 Customer messages

| **Internal action** | **Безопасный текст**                                                                      | **Что не раскрывать**            |
|---------------------|-------------------------------------------------------------------------------------------|----------------------------------|
| `pending`           | «Покупка учтена. Награда проходит обычную проверку и будет доступна после подтверждения.» | score, thresholds, shared tokens |
| duplicate event     | «Этот чек уже был учтён ранее.»                                                           | другой account, graph component  |
| return reversal     | «Награда отменена, потому что покупка была возвращена.»                                   | fraud suspicion                  |
| manual review       | «Нужно дополнительное подтверждение. Мы сообщим результат до \[SLA\].»                    | internal feature list            |
| block/appeal        | «Награды временно недоступны. Решение можно обжаловать.»                                  | detection evasion details        |

### 13.3 Cooldown и повторная попытка

> **ASSUMPTION.** Pending timeout 24-72h для обычных чеков либо до наступления конкретного maturity event; high-value cases имеют отдельный SLA. Rejoin cooldown 30-90 дней и progressive caps проверяются экспериментально. Ошибка/неполные данные должны приводить к повторной обработке, а не к накоплению штрафа.

## 14. Privacy и security

### 14.1 Hashing не равен anonymization

> **FACT.** Детерминированный hash сохраняет linkability и может быть перебран на малом пространстве идентификаторов. Псевдонимизированные данные остаются персональными, если дополнительная информация позволяет связать их с человеком; дополнительная информация должна храниться отдельно и защищённо ([GDPR Recital 26 and Article 4(5)](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng)).

**Design:**

- keyed HMAC/tokenization вместо plain hash;
- разные keys/domains для account, device, payment, network;
- rotation с контролируемым overlap для расследований;
- raw-to-token mapping только в отдельном vault;
- аналитики получают агрегаты и case-scoped tokens;
- удаление/исправление субъекта распространяется на feature store и graph.

### 14.2 Минимизация

Не собирать имена, адреса, точный GPS, текстовые комментарии кассира, PAN, advertising IDs «на всякий случай». Для velocity достаточно store ID и coarse time; для network - coarse bucket; для корзины - SKU/category token и числовые поля.

### 14.3 Логи и reason codes

> **FACT.** OWASP рекомендует исключать из логов access tokens, authentication passwords, payment data и иные чувствительные данные; доступ к логам следует ограничивать, мониторить и привязывать retention к целям ([OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)).

Каждая запись decision log содержит:

- `decision_id`, `event_id_token`, `decision_ts`;
- action, score band, independent-family count;
- ordered reason codes без raw identifiers;
- rule/config version, data freshness, missingness flags;
- analyst outcome/appeal outcome в append-only форме;
- access audit для case view.

## 15. Мониторинг, drift и rollback

| **Контроль**     | **Метрика**                                         | **Частота**    | **Guardrail / действие**                       |
|------------------|-----------------------------------------------------|----------------|------------------------------------------------|
| Rule health      | hit rate, unique accounts, overlap                  | hourly/daily   | spike -\> shadow/kill switch                   |
| Decision quality | sampled precision, review overturn                  | weekly         | lower CI below target -\> downgrade action     |
| Customer harm    | complaints, appeal rate, compensation               | daily/weekly   | cohort spike -\> freeze rule                   |
| Monetary         | prevented loss, false hold exposure, net benefit    | weekly/monthly | negative conservative value -\> recalibrate    |
| Pending UX       | median/P90/P99 age, abandoned rewards               | hourly/daily   | SLA breach -\> fail-open or manual route       |
| Data quality     | token missingness, POS/return latency, schema drift | real time      | critical missing -\> pending, not block        |
| Graph            | component size, degree distribution, cycle rate     | daily          | campaign/store-level anomaly review            |
| Drift            | PSI/KS/quantile shift by cohort                     | weekly         | diagnostic only; label-based backtest required |
| Delayed labels   | return/refund backfill, confirmed fraud labels      | daily/monthly  | restate prior metrics point-in-time            |
| Release          | canary share, config checksum, rollback time        | each deploy    | one-click rollback and replay                  |

> **INFERENCE.** PSI/KS и hit-rate drift не доказывают ухудшение fraud quality; они только запускают investigation. Главный quality signal - delayed-labeled precision/recall, review outcome и monetary impact на point-in-time replay.

## 16. Реестр параметров и граница PoC/production

### 16.1 Parameter registry

| **Параметр**                | **Synthetic value/range**       | **Владелец**     | **Production calibration**                |
|-----------------------------|---------------------------------|------------------|-------------------------------------------|
| `T_pending`                 | 25                              | Product Risk     | cost + pending SLA                        |
| `T_review`                  | 50                              | Fraud Ops        | queue capacity and precision              |
| `T_block`                   | 75                              | Risk Governance  | lower CI precision + net benefit          |
| independent families        | \>=2                            | Risk Governance  | red-team / FP replay                      |
| fanout window               | 48h/7d                          | Referral Product | campaign-specific baseline                |
| graph cycle length          | 2-8                             | Risk Analytics   | component size/latency                    |
| return window               | 7-60d family                    | Commerce Ops     | actual category/store return distribution |
| link-token retention        | 30-90d raw; 180-365d aggregates | Privacy/Security | legal purpose and incident need           |
| pending resolution fraction | 45%                             | scenario only    | measured backtest                         |
| manual resolution fraction  | 75%                             | scenario only    | analyst outcomes                          |
| monetary loss multiplier    | 1-3x                            | Finance/Risk     | repeat/network externality                |
| rejoin cooldown             | 30-90d                          | Dvor Product     | experiment + fairness                     |

### 16.2 Что PoC доказывает

- rules/score/action plumbing и explainable reason codes;
- separation event reject vs account block;
- point-in-time feature discipline и component split;
- synthetic evaluation with account/event/monetary denominators and CIs;
- negative-test principle for household and legitimate fanout;
- reproducibility through code and fixed seeds.

### 16.3 Что PoC не доказывает

- реальную fraud prevalence, fraud loss или production precision X5;
- переносимость synthetic weights/thresholds;
- юридическую допустимость конкретных токенов и retention;
- эффективность GNN, device fingerprint или OCR;
- review capacity, appeal cost, customer churn;
- устойчивость к adaptive adversary после раскрытия продукта.

### 16.4 План перехода в production

1.  Утвердить data inventory, purpose, retention и access model с Legal/Privacy/Security.
2.  Построить immutable reward ledger и point-in-time feature snapshots.
3.  Запустить 4-8 недель shadow scoring без customer harm.
4.  Создать adjudication guide и double-review sample для ground truth.
5.  Калибровать pending/review; event hard rules включать постепенно.
6.  Auto-block разрешать только после достаточного independent denominator и red-team.
7.  Провести canary по store/channel/campaign с rollback.
8.  Добавлять graph platform/GNN только при измеримом incremental recall при неизменном precision floor.

## 17. Финальный чек качества решения

| **Проверка**                             | **Статус PoC** | **Комментарий**                                   |
|------------------------------------------|----------------|---------------------------------------------------|
| `is_fraud` не попадает в признаки        | PASS           | отдельная evaluator-only колонка                  |
| Нет post-outcome leakage в T0            | PASS by design | return/matured features доступны только T1/T2     |
| Account и event denominators разделены   | PASS           | отдельные confusion matrices                      |
| Monetary metrics и assumptions разделены | PASS           | block lower bound отдельно от resolution scenario |
| Нет block по одной аномалии              | PASS           | two-family gate; exact duplicate = event reject   |
| Shared household negative test           | PASS synthetic | 0% block; real cohort **TO_VALIDATE**             |
| Legit mass inviter negative test         | PASS synthetic | 0% block; campaign exception path needed          |
| CI при малом sample                      | PASS           | Wilson + component bootstrap; limits disclosed    |
| Privacy минимизация                      | DESIGN PASS    | production legal/security review required         |
| Source metrics не перенесены на X5       | PASS           | applicability limits in source register           |

## 18. Реестр источников и ограничения применимости

| **Источник**                                                                                                                                                                                                               | **Дата / тип**                            | **Поддерживаемый вывод**                                              | **Ограничение применимости**                            |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------|-----------------------------------------------------------------------|---------------------------------------------------------|
| [FENCE: Fairplay Ensuring Network Chain Entity](https://arxiv.org/abs/2310.05651), Upreti et al.                                                                                                                           | 9 Oct 2023; paper/system                  | multiple IDs для bonus/referral abuse; graph + human review           | fantasy sports; закрытая разметка; пороги не переносимы |
| [PromoGuardian](https://arxiv.org/abs/2510.12652); [IEEE S&P 2026 acceptance](https://sp2026.ieee-security.org/accepted-papers.html)                                                                                       | 14 Oct 2025; accepted paper               | group-based promotion abuse, spatial/temporal relations               | e-commerce platform and GNN; proprietary data           |
| [EnsemFDet](https://arxiv.org/abs/1912.11113), Ren et al.                                                                                                                                                                  | 23 Dec 2019; paper                        | dense bipartite components and scalability                            | JD.com; not a grocery loyalty benchmark                 |
| [Temporal Motifs for Financial Networks](https://arxiv.org/abs/2301.07791), Liu et al.                                                                                                                                     | 18 Jan 2023; paper                        | temporal cycles and repeated motifs add signal                        | Mercari/JPMC/Venmo domains differ                       |
| [Rakuten Bilt FAQ](https://www.rakuten.com/help/article/bilt-faq)                                                                                                                                                          | accessed 4 Sep 2026; official FAQ         | pending until returns/exchanges/qualification mature                  | 3-14 week timing not transferable                       |
| [Rakuten Terms](https://www.rakuten.com/help/article/terms-conditions)                                                                                                                                                     | updated 15 Oct 2025; official terms       | pending not payable; fraud/anomaly may delay                          | US cashback product, not X5 policy                      |
| [GDPR, Regulation 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng)                                                                                                                                             | 27 Apr 2016; official law                 | pseudonymisation, minimisation, storage limitation                    | EU benchmark; Russian applicability needs counsel       |
| [152-ФЗ «О персональных данных»](https://www.consultant.ru/document/cons_doc_LAW_61801/)                                                                                                                                   | current page incl. 26 Jul 2026 amendments | Russian legal context: principles, automated decisions, security      | Consultant is legal database; full legal audit excluded |
| [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)                                                                                                                       | current; security guidance                | sensitive-data exclusion, access, retention/audit                     | engineering guidance, not legal retention schedule      |
| [Saito and Rehmsmeier](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432)                                                                                                                          | 4 Mar 2015; PLOS ONE                      | PR evaluation for imbalanced datasets                                 | metric guidance; not fraud-specific threshold           |
| [Brown, Cai, DasGupta](https://projecteuclid.org/journals/statistical-science/volume-16/issue-2/Interval-Estimation-for-a-Binomial-Proportion/10.1214/ss/1009213286.full)                                                  | 2001; Statistical Science                 | binomial interval limitations and Wilson family                       | independence assumption; cluster bootstrap also needed  |
| [Elkan, Foundations of Cost-Sensitive Learning](https://cseweb.ucsd.edu/~elkan/rescale.pdf)                                                                                                                                | 2001; IJCAI                               | choose action by expected cost; avoid incoherent cost matrix          | costs must be estimated locally                         |
| [J.P. Morgan Synthetic Data process](https://www.jpmorganchase.com/about/technology/research/ai/synthetic-data); [Assefa et al.](https://dl.acm.org/doi/10.1145/3383455.3422554)                                           | 2020; research                            | synthetic generator must be evaluated/calibrated against real metrics | finance context; does not validate this generator       |
| [scikit-learn TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html) and [model selection API](https://scikit-learn.org/stable/api/sklearn.model_selection.html) | accessed 4 Sep 2026; official docs        | time-aware and group-disjoint evaluation                              | implementation documentation, not a causal guarantee    |

## Приложение A. Артефакты воспроизводимости

Комплект содержит:

- `antifraud_poc_simulation.py` - генератор, score, actions, split, CIs и monetary evaluation;
- `run_antifraud_multiseed_fast.py` - 20-seed stability check;
- `metrics.json` - test metrics;
- `metrics_by_attack.csv` - attack-specific recall;
- `validation_threshold_sweep.csv` - пороговый sweep на validation;
- `events_by_action.csv` - объёмы и monetary scenario по action;
- `multi_seed_summary.csv` и `multi_seed_distribution.csv` - повторные seeds;
- `README.md` - команды запуска и ограничения.

Команда:

    python antifraud_poc_simulation.py
    python run_antifraud_multiseed_fast.py

**Последнее предупреждение.** Высокие synthetic precision и PR-AUC являются свойством заданных profiles. Они показывают, что архитектура способна быть precision-first при заданных разделениях, но не являются прогнозом качества на X5.
