<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Прямой ответ</strong></p>
<p>Нельзя назначать награду из выручки или валового оборота участников. Денежный номинал допускается только из положительной односторонней нижней границы инкрементальной contribution margin на всех randomized eligible users, после pull-forward, каннибализации, возвратов, переменных затрат и реально не профинансированной партнёром части награды.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**Дата:** 4 сентября 2026

**Аудитория:** product, loyalty, finance, experimentation, risk, commercial и data команды

**Статус чисел: ASSUMPTION** / **TO_VALIDATE** — если прямо не указано иное.

**Комплект:** этот отчёт + редактируемая модель X5_reward_economics_model.xlsx.

**Ограничение заключения.** Документ не является бухгалтерским, налоговым или юридическим заключением. Российские вопросы учёта, ККТ, рекламы, персональных данных и договоров с брендами сформулированы как checklist для профильных специалистов.

# Короткий план исследования

- Зафиксировать словарь и единый ledger: contribution margin до игровой награды, causal incrementality, reward economic cost, liability и funding.

- Собрать первичные доказательства и не переносить чужие effect sizes на X5.

- Вывести однозначные формулы с единицами, окном, знаменателем и zero handling.

- Просчитать одинаково определённые conservative/base/upside и stress cases.

- Собрать gate, систему лимитов, правила «Двора», brand contract/data contour, simulation API и pilot dashboard.

- Перепроверить арифметику, treatment/control, pull-forward, двойной учёт и соответствие selected reward динамическому cap.

# Содержание

> 1\. Executive decision
>
> 2\. Словарь экономики
>
> 3\. Evidence review
>
> 4\. Unit-economics model
>
> 5\. Parameter registry
>
> 6\. Три сценария и stress cases
>
> 7\. Reward gate
>
> 8\. Система лимитов
>
> 9\. Экономика «Двора»
>
> 10\. Brand funding
>
> 11\. Интерфейс с симуляцией
>
> 12\. Пилотный dashboard
>
> 13\. Что запросить у X5 и вопросы специалистам
>
> 14\. Источники

## Метки доказательности

| **Метка**        | **Значение**                                                                                                 |
|------------------|--------------------------------------------------------------------------------------------------------------|
| **FACT**         | Прямо подтверждено указанным источником.                                                                     |
| **DERIVED**      | Рассчитано из явно показанных входов и формулы.                                                              |
| **INFERENCE**    | Вывод исследователя из нескольких фактов/ограничений.                                                        |
| **PUBLIC_PROXY** | Публичный показатель используется только как приближение; в этой модели числовые proxy почти не применяются. |
| **ASSUMPTION**   | Сценарное число без достаточного эмпирического подтверждения.                                                |
| **TO_VALIDATE**  | Нужно измерить на данных X5, в пилоте или подтвердить договором/профильным специалистом.                     |

# 1. Executive decision

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Рекомендуемое правило назначения</strong></p>
<p>Для каждого rule/segment/user-challenge сначала резервируется не номинал баллов, а безопасный economic budget. Безопасный бюджет равен positive one-sided LCB инкрементальной contribution margin после risk buffer минус все non-reward costs. Номинал reward получается делением этого бюджета на консервативный cost coefficient и затем ограничивается всеми hard caps.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**DERIVED** Главный guardrail:

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>R_selected ≤ R_max AND LCB[Profit per eligible] &gt; 0</p>
<p><em>Окно: treatment + заранее заданный lag. Знаменатель primary metric: все randomized eligible users (ITT).</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

- Не использовать оборот участников, sales-to-reward или «экономию покупателя» как доказательство прибыльности X5.

- Вести shadow ledger contribution margin до игровой награды; затем вычитать economic reward cost ровно один раз.

- Partner funding учитывать только в части зарезервированного, договорно возмещаемого и ожидаемо собираемого финансирования.

- Любой денежный reward держать в pending до разумного anti-fraud/return settlement; XP и визуальный progress можно показать сразу, но их marginal cost также не равна нулю.

- В runtime использовать budget burn + p95 forecast и автоматический stop new enrollments до исчерпания фонда.

| **Scenario** | **Sustained ΔCM / eligible** | **Prudent CM** | **K non-reward** | **R_max / completer** | **Selected** | **Mean profit / eligible** | **LCB profit / eligible** | **Decision**          |
|--------------|------------------------------|----------------|------------------|-----------------------|--------------|----------------------------|---------------------------|-----------------------|
| Conservative | 2.50 ₽                       | 0.94 ₽         | 1.10 ₽           | 0.00 ₽                | 0.00 ₽       | 1.40 ₽                     | -0.16 ₽                   | NO CHALLENGE          |
| Base         | 13.50 ₽                      | 7.56 ₽         | 2.54 ₽           | 22.19 ₽               | 20.00 ₽      | 6.44 ₽                     | 0.50 ₽                    | LAUNCH WITH STOP-LOSS |
| Upside       | 44.10 ₽                      | 31.86 ₽        | 4.08 ₽           | 147.46 ₽              | 140.00 ₽     | 13.64 ₽                    | 1.41 ₽                    | LAUNCH WITH STOP-LOSS |

**ASSUMPTION** Все три строки — scenario analysis. Conservative point estimate положителен, но запуск отклоняется: prudent LCB profit отрицателен. Это демонстрирует, почему expected value без uncertainty gate недостаточен.

# 2. Словарь экономики

| **Термин**                     | **Определение / формула**                                                                                     | **Единица**               | **Момент**                           | **Типичная ошибка**                                                   |
|--------------------------------|---------------------------------------------------------------------------------------------------------------|---------------------------|--------------------------------------|-----------------------------------------------------------------------|
| Eligible user                  | Пользователь, попавший в заранее заданные eligibility rules до рандомизации.                                  | user                      | До assignment                        | Считать только participants/completers.                               |
| Treated / delivered            | Eligible user, которому фактически доставлено назначение; диагностический denominator.                        | user                      | После delivery                       | Заменять им ITT primary denominator.                                  |
| Baseline CM                    | Средняя contribution margin control на eligible user за окно W.                                               | ₽/eligible/W              | После закрытия W                     | Использовать revenue или gross margin без единого bridge.             |
| Test CM                        | Средняя contribution margin test до вычета game reward за то же окно W.                                       | ₽/eligible/W              | После закрытия W                     | Вычесть reward в Test CM и затем повторно в P&L.                      |
| Gross incremental CM           | CM_test − CM_control.                                                                                         | ₽/eligible/W              | После закрытия W                     | Приписать весь CM участников программе.                               |
| Net behavioural incremental CM | Gross ΔCM после не встроенных в окно pull-forward, substitution, promo interaction и late returns.            | ₽/eligible/W              | После treatment+lag                  | Вычесть те же эффекты второй раз, если они уже попали в длинное окно. |
| Nominal reward                 | Обещанный пользователю номинал баллов/скидки.                                                                 | ₽ nominal                 | Offer/earn state                     | Считать номинал равным economic cost без проверки.                    |
| Issued/earned points           | Номинал, начисленный или заработанный по правилам.                                                            | points / ₽ nominal        | Issue/earn                           | Смешивать с redeemed и accounting liability.                          |
| Redeemed points                | Фактически погашенный номинал.                                                                                | points / ₽ nominal        | Redemption                           | Применять зрелый redemption rate к незрелой когорте без aging.        |
| Breakage                       | Ожидаемо непогашенная доля зрелой issued/earned когорты.                                                      | % issued                  | После maturity/expiry estimate       | Считать всю неактивную когорту окончательным breakage.                |
| Accounting liability           | Отложенное обязательство/выручка по применимому учётному стандарту.                                           | ₽ balance                 | По accounting policy                 | Использовать balance как economic campaign cost.                      |
| Economic reward cost           | Marginal cost valid redemption + settlement/admin + unrecovered losses − collectible partner funding.         | ₽/eligible или ₽ campaign | Expected ex ante; actual ex post     | Обнулить стоимость из-за обещанного brand funding.                    |
| Cannibalized reward cost       | Часть total reward cost, выплаченная за baseline behaviour, которое квалифицировалось бы без treatment.       | ₽ и % reward cost         | Ghost-rule/control estimate          | Вычесть как дополнительный cost сверх total reward cost.              |
| Non-monetary reward cost       | Разработка/амортизация, artwork/licence, serving/storage, moderation/support, fraud/abuse и opportunity cost. | ₽/user/event              | Budget/actual                        | Присвоить косметике нулевую стоимость.                                |
| Partner-funded share           | Фактически ожидаемо собираемая договорная компенсация по reimbursable events в пределах reserve.              | ₽ или % valid cost        | Upon eligibility/collection estimate | Использовать headline share без p_collect и reserve.                  |
| Profit per eligible            | Net campaign profit / randomized eligible users.                                                              | ₽/eligible                | Treatment+lag                        | Скрыть отрицательный эффект за completion rate.                       |
| ROI_X5                         | Campaign net profit / controllable X5 investment.                                                             | x                         | Campaign close                       | Incremental revenue / reward; деление на ноль → бесконечность.        |

**FACT** В опубликованной отчётности X5 loyalty points описаны как отдельная performance obligation/material right; распределение transaction price учитывает ожидаемое непогашение, а contract liability сохраняется до redemption. [<u>X5 FY2025 IFRS statements</u>](https://www.x5.ru/wp-content/uploads/2026/05/auditorskoe-zaklyuchenie-i-finansovaya-otchetnost_pao-kcz-iks-5_2025_format_dop_no-links_eng.pdf) Это подтверждает необходимость отделять accounting liability от causal economic cost. Общая рамка признания выручки приведена в [<u>IFRS 15</u>](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-15-revenue-from-contracts-with-customers/). Конкретное применение должно проверить Finance/Accounting.

# 3. Evidence review

## 3.1. Что подтверждено

| **Тезис**                                                     | **Доказательство**                                                                                                                       | **Применимость к X5**                                                           | **Статус**                  |
|---------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|-----------------------------|
| Loyalty accounting ≠ reward economics                         | X5 раскрывает allocation к points, expected non-redemption и contract liability; IFRS 15 задаёт performance-obligation framework.        | Применимо к словарю и reconciliation; не даёт X5-specific marginal reward cost. | FACT                        |
| Нужен randomized control                                      | Field experiments измеряют exposed/recipient против случайного control; redemption и demand effect могут расходиться.                    | Применим дизайн, не magnitude.                                                  | FACT                        |
| Короткий promotion bump может быть не sustained               | Scanner-data work разделяет brand switching, category expansion и intertemporal substitution; forward-looking behavior влияет на оценку. | Нужен lag/event-study; публичные доли не переносить.                            | FACT                        |
| Лояльные/тяжёлые покупатели могут просто чаще забирать reward | Loyalty research показывает heterogeneity и self-selection risk.                                                                         | Не сравнивать members/participants с nonmembers; ITT + strata.                  | FACT                        |
| Социальная механика создаёт interference                      | При взаимном влиянии individual randomization может быть biased; cluster randomization — стандартный remedy.                             | Для «Двора» рандомизировать целые группы/store pools.                           | INFERENCE supported by FACT |
| 7:1 не является подтверждённым параметром                     | Найден vendor wording “up to 7:1 ROI”, но нет сопоставимого denominator/methodology.                                                     | Не использовать в cap, business case или обещании.                              | TO_VALIDATE                 |

**FACT** В 70 randomized field experiments targeted offer сравнивался со случайно не получившими его пользователями; авторы отдельно анализировали redemption, expenditure и carryover. [<u>Sahni et al.</u>](https://pubsonline.informs.org/doi/10.1287/mnsc.2016.2450) Дизайн переносим, величины эффекта — нет.

**FACT** Promotion bump может включать substitution и purchase acceleration. [<u>Van Heerde et al.</u>](https://pubsonline.informs.org/doi/abs/10.1287/mksc.1040.0061) и [<u>Sun et al.</u>](https://journals.sagepub.com/doi/10.1509/jmkr.40.4.389.19392) поддерживают treatment+lag и decomposition, но не дают валидных X5 коэффициентов.

**FACT** Наблюдаемая высокая активность участников loyalty programme не равна causal uplift: heavy buyers могут забирать rewards без заметного изменения, а membership self-selection искажает простые сравнения. [<u>Liu</u>](https://journals.sagepub.com/doi/10.1509/jmkg.71.4.019); [<u>Leenheer et al.</u>](https://doi.org/10.1016/j.ijresmar.2006.10.005).

## 3.2. Что нельзя переносить на X5

- Effect sizes из online tickets, US department store, Dutch grocery panel или marketplace experiments.

- Tesco vendor-reported engagement как доказательство incremental contribution margin X5.

- “7:1 ROI” как sales-to-reward, как маржинальный ROI или как гарантированный brand-funded outcome.

- Публичную gross margin как замену item/category contribution margin после обычных промо и переменных затрат.

- Публичный/бухгалтерский breakage как ставку для новой игровой механики без когортной redemption curve.

**PUBLIC_PROXY** Числовые public proxies в расчёте сознательно не использованы: их сопоставимость недостаточна. Публичные материалы Tesco/Eagle Eye служат только подтверждением существования механики; [<u>Tesco Clubcard Challenges case</u>](https://eagleeye.com/case-studies/tesco-clubcard-challenges) — vendor evidence, а [<u>Eagle Eye 7:1 claim</u>](https://eagleeye.com/personalized-promotions) остаётся непроверенным marketing claim.

# 4. Unit-economics model

## 4.1. Окно, знаменатель и shadow ledger

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Единица анализа</strong></p>
<p>Основной результат считается за фиксированное W = treatment window + lag window на всех randomized eligible users. Вкладная маржа в test/control считается до game reward. Затем game reward и programme costs вычитаются отдельными строками.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**Рекомендуемый transaction-level bridge:** net sales after returns and ordinary discounts − COGS − ordinary attributable transaction costs ± ordinary supplier funding по единому Finance rule. Game reward исключён из этого bridge и вычитается отдельно. Если Finance выбирает ledger уже после game discount, отдельное вычитание reward запрещено.

## 4.2. Baseline и test contribution margin

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>CM_g(W) = (1 / N_g) × Σ_{i∈g} Σ_{t∈W} CM_pre-game,it, g∈{T,C}</p>
<p><em>Единица: ₽/randomized eligible user/window. N_g=0 → NA. Control — baseline; Test — test CM до game reward.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 4.3. Gross incremental contribution margin

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>ΔCM_gross(W) = CM_T(W) − CM_C(W)</p>
<p><em>Единица: ₽/eligible/window. Это causal ITT estimate при корректной рандомизации, но ещё не net campaign profit.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 4.4. Net behavioural incremental contribution margin

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>ΔCM_beh = ΔCM_gross − A_pull-forward − A_substitution − A_promo-interaction − A_late-returns</p>
<p><em>Вычитать только компоненты, которые не встроены в достаточно длинное netted outcome window. Иначе показать decomposition отдельно и поставить adjustment=0, чтобы не вычесть дважды.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 4.5. Issued, redeemed и breakage

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>Breakage_mature = 1 − Redeemed_nominal / Issued_or_earned_nominal</p>
<p><em>Когорта должна быть зрелой. Issued=0 → NA. Accounting estimate и economic unit cost хранятся отдельно.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 4.6. Expected valid economic reward cost

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>E[C_valid] = p_complete,valid × R_nom × p_redeem × κ_unit</p>
<p><em>Единица: ₽/eligible/window. R_nom — ₽ nominal/completer; κ_unit — ₽ economic cost per redeemed nominal ₽. Ex ante использовать conservative upper bounds.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 4.7. Cannibalized reward cost

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>C_reward,cannibalized = C_reward,total × q_baseline-qualifier</p>
<p><em>q оценивается ghost challenge: применить rule к control без выплаты. Это диагностическая доля total reward cost, а не дополнительный cost для повторного вычитания.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 4.8. Fraud-adjusted reward loss

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>L_fraud = p_fraud-paid × R_nom × p_redeem,fraud × κ_fraud × (1 − clawback_rate)</p>
<p><em>Единица: ₽/eligible/window. Если fraud loss уже включён в all-in reward row, не вычитать повторно в net profit.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 4.9. Partner-funded и X5-funded части

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>F_partner = min(rate_contract × reimbursable_base, reserve_remaining) × p_collect</p>
<p><em>Единица: ₽. Использовать договорное событие, remaining reserve, collection haircut и правила returns/fraud.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>C_reward,X5-clean = C_valid + C_settlement + C_admin + C_nonrecoverable-tax − F_partner</p>
<p><em>All-in вариант = clean + unrecovered reward-linked fraud/returns. Выберите один ledger и не смешивайте их.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 4.10. Profit per eligible, per treated и campaign profit

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>π_eligible = ΔCM_beh − C_reward,X5 − ΔVC_program − L_fraud/returns − A_other − C_fixed / N_eligible</p>
<p><em>Единица: ₽/eligible/window. N_eligible=0 → NA.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>Π_campaign = N_eligible × π_eligible</p>
<p><em>Единица: ₽/campaign. Для heterogeneous policies допустима сумма individual expected profits.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>π_treated = Π_campaign / N_delivered</p>
<p><em>Диагностическая единица: ₽/delivered treated. N_delivered=0 → NA. Не заменяет ITT.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 4.11. ROI

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>ROI_X5 = Π_campaign / Investment_X5</p>
<p><em>Investment_X5 = X5 reward cost + incremental variable/operations/fixed costs. Denominator≤0 → NA, не ∞. Incremental revenue/reward не является главным profitability KPI.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 4.12. Ex-ante safe reward cap

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>LCB_ΔCM = max(0, μ_ΔCM − z_(1−α) × SE_ΔCM)</p>
<p><em>Окно и α задаются заранее. Для cluster trial SE должен учитывать cluster design.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>B_reward = max(0, (1 − risk_buffer) × LCB_ΔCM − K_nonreward)</p>
<p><em>K_nonreward включает promo/substitution/returns, programme variable cost, operations и другие ещё не включённые потери.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>a_cost = p_complete^U × p_redeem^U × κ^U × unfunded_X5_share^U × (1 + fraud^U)</p>
<p><em>Верхние границы U — policy choice. Если a_cost≤0 из-за “100% funding”, cap не бесконечен: без зарезервированного договора R_economic=0.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>R_economic = B_reward / a_cost</p>
<p><em>Единица: ₽ nominal/completer. B_reward=0 → R_economic=0.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>R_max = floor_d(min(R_economic, event, user, cycle, yard, rule, campaign, category, funder remaining caps))</p>
<p><em>d — технический шаг номинала. Любой missing/expired cap трактуется как блокировка, а не как бесконечность.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 4.13. Break-even по дополнительным визитам

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>Visits_BE,sustained = (C_reward,X5 + C_ops) / [CM_visit × (1 − l_promo − l_return) − VC_visit]</p>
<p><em>Единица: sustained visits/eligible. Denominator≤0 → NA и NO CHALLENGE.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>Visits_BE,observed = Visits_BE,sustained / (1 − pull_forward)</p>
<p><em>1−pull_forward≤0 → NA. Для reward, растущего с visits, нужен solve/optimization, а не эта closed-form approximation.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**DERIVED** Два вида каннибализации нельзя смешивать: behavioural margin cannibalization уменьшает ΔCM, а cannibalized reward cost — подмножество уже учтённой reward cost. Их одновременное полное вычитание создаёт double count.

# 5. Parameter registry

**ASSUMPTION** Low/Base/High соответствуют Conservative/Base/Upside. Они показывают sensitivity, а не оценку X5. Реестр в companion XLSX содержит редактируемые inputs и формулы.

| **Parameter**                     | **Low** | **Base** | **High** | **Unit**            | **Status**  | **Source/owner**      | **Sensitivity** | **How to validate**             |
|-----------------------------------|---------|----------|----------|---------------------|-------------|-----------------------|-----------------|---------------------------------|
| Baseline visits                   | 3.0     | 4.0      | 5.0      | visits/eligible/28d | TO_VALIDATE | X5 analytics          | Medium          | Pre-period by arm/stratum       |
| Average check before game reward  | 500     | 600      | 700      | ₽/visit             | ASSUMPTION  | Scenario/X5           | High            | Test/control by format/category |
| Contribution margin rate          | 10%     | 12%      | 14%      | % revenue           | TO_VALIDATE | X5 Finance            | Very high       | Approved CM bridge              |
| Observed incremental visits       | 0.10    | 0.25     | 0.50     | visits/eligible     | ASSUMPTION  | Pilot                 | Very high       | Randomized ITT                  |
| SE incremental visits             | 0.0304  | 0.0456   | 0.0456   | visits/eligible     | ASSUMPTION  | Power design          | Very high       | Variance, ICC, CUPED            |
| Pull-forward share                | 50%     | 25%      | 10%      | % observed uplift   | ASSUMPTION  | Post-window           | Very high       | Treatment+lag event study       |
| Risk buffer                       | 25%     | 20%      | 15%      | % LCB               | ASSUMPTION  | Policy                | High            | Approve risk appetite           |
| Promo/cannibalization margin loss | 20%     | 10%      | 5%       | % sustained ΔCM     | ASSUMPTION  | Control decomposition | High            | Ghost rule + item/category      |
| Return margin loss                | 2.0%    | 1.0%     | 0.5%     | % sustained ΔCM     | ASSUMPTION  | Returns ledger        | Medium          | Netted return window            |
| Variable cost per sustained visit | 5       | 4        | 3        | ₽/visit             | ASSUMPTION  | Operations/Finance    | Medium          | Payment/communication/service   |
| Ops cost per eligible             | 0.30    | 0.30     | 0.30     | ₽/eligible          | ASSUMPTION  | Product/Tech          | Low–medium      | Vendor/cloud/support actuals    |
| Valid completion probability      | 25%     | 35%      | 50%      | % eligible          | ASSUMPTION  | Pilot                 | High            | ITT; valid state                |
| Redemption probability            | 92%     | 85%      | 75%      | % earned            | TO_VALIDATE | X5 loyalty ledger     | High            | Mature cohort redemption curve  |
| Breakage                          | 8%      | 15%      | 25%      | % earned            | DERIVED     | 1−redemption          | High            | Maturity/expiry reconciliation  |
| Economic unit cost κ              | 1.00    | 1.00     | 1.00     | ₽ cost/₽ nominal    | TO_VALIDATE | X5 Finance            | Very high       | Mechanic-specific marginal cost |
| Partner share collected           | 0%      | 25%      | 50%      | % gross valid cost  | ASSUMPTION  | Contract/collection   | Very high       | Reserve + invoice + p_collect   |
| Unrecovered fraud multiplier      | 3.0%    | 1.5%     | 0.5%     | % X5 valid cost     | ASSUMPTION  | Risk                  | Medium          | Paid/recovered cohort           |
| Always-buyer reward share         | 70%     | 50%      | 30%      | % X5 reward cost    | ASSUMPTION  | Ghost challenge       | Medium          | Control qualification           |
| Selected reward                   | 0       | 20       | 140      | ₽/completer         | ASSUMPTION  | Policy output         | Very high       | Must be ≤ R_max                 |

**TO_VALIDATE** Самые чувствительные неизвестные: contribution margin bridge, causal treatment effect и SE, pull-forward, economic unit cost, mature redemption curve и collectible partner share. Публичная информация не заменяет эти данные.

# 6. Три полностью просчитанных сценария

**ASSUMPTION** Общие определения: 28 дней treatment + 28 дней lag, N=100 000 eligible users, check и CM считаются до game reward. Fixed campaign cost в примере равен нулю и должен быть добавлен X5.

| **Scenario** | **Base visits** | **Check** | **CM %** | **Δ visits** | **Pull** | **Sust. ΔCM** | **Prudent CM** | **K**  | **Complete** | **Redeem** | **Partner** | **R_max** | **Selected** | **X5 reward cost** | **Mean profit** | **LCB profit** | **Decision**          |
|--------------|-----------------|-----------|----------|--------------|----------|---------------|----------------|--------|--------------|------------|-------------|-----------|--------------|--------------------|-----------------|----------------|-----------------------|
| Conservative | 3.0             | 500 ₽     | 10.0%    | 0.100        | 50.0%    | 2.50 ₽        | 0.94 ₽         | 1.10 ₽ | 25.0%        | 92.0%      | 0.0%        | 0.00 ₽    | 0.00 ₽       | 0.00 ₽             | 1.40 ₽          | -0.16 ₽        | NO CHALLENGE          |
| Base         | 4.0             | 600 ₽     | 12.0%    | 0.250        | 25.0%    | 13.50 ₽       | 7.56 ₽         | 2.54 ₽ | 35.0%        | 85.0%      | 25.0%       | 22.19 ₽   | 20.00 ₽      | 4.53 ₽             | 6.44 ₽          | 0.50 ₽         | LAUNCH WITH STOP-LOSS |
| Upside       | 5.0             | 700 ₽     | 14.0%    | 0.500        | 10.0%    | 44.10 ₽       | 31.86 ₽        | 4.08 ₽ | 50.0%        | 75.0%      | 50.0%       | 147.46 ₽  | 140.00 ₽     | 26.38 ₽            | 13.64 ₽         | 1.41 ₽         | LAUNCH WITH STOP-LOSS |

## 6.1. Conservative

- CM/visit = 500 ₽ × 10.0% = 50.00 ₽.

- Gross ΔCM = 0.100 visits × 50.00 ₽ = 5.00 ₽/eligible.

- Sustained visits = 0.100 × (1 − 50.0%) = 0.0500; sustained ΔCM = 2.50 ₽.

- LCB visits = max(0, 0.100 − 1.645 × 0.030395) = 0.0500; after pull-forward LCB CM = 1.25 ₽.

- Prudent CM = 1.25 ₽ × (1 − 25.0%) = 0.94 ₽.

- K = promo 0.50 ₽ + returns 0.05 ₽ + variable 0.25 ₽ + ops 0.30 ₽ = 1.10 ₽.

- Reward budget = max(0, 0.94 ₽ − 1.10 ₽) = 0.00 ₽.

- Cost coefficient = 25.0% × 92.0% × 1.00 × (1 − 0.0%) × (1 + 3.0%) = 0.236900 ₽/eligible per nominal ₽.

- R_max = min(0.00 ₽, event 150.00 ₽, user 250.00 ₽) = 0.00 ₽; selected = 0.00 ₽.

- Gross valid reward cost = 0.00 ₽; collected partner funding = 0.00 ₽; unrecovered fraud = 0.00 ₽; X5 all-in reward cost = 0.00 ₽/eligible.

- Mean profit = 2.50 ₽ − 1.10 ₽ − 0.00 ₽ = 1.40 ₽/eligible; prudent LCB profit = -0.16 ₽/eligible.

- Campaign point estimate = 140 000.00 ₽; ROI_X5 = 2.55x; Decision: NO CHALLENGE.

## 6.2. Base

- CM/visit = 600 ₽ × 12.0% = 72.00 ₽.

- Gross ΔCM = 0.250 visits × 72.00 ₽ = 18.00 ₽/eligible.

- Sustained visits = 0.250 × (1 − 25.0%) = 0.1875; sustained ΔCM = 13.50 ₽.

- LCB visits = max(0, 0.250 − 1.645 × 0.045593) = 0.1750; after pull-forward LCB CM = 9.45 ₽.

- Prudent CM = 9.45 ₽ × (1 − 20.0%) = 7.56 ₽.

- K = promo 1.35 ₽ + returns 0.14 ₽ + variable 0.75 ₽ + ops 0.30 ₽ = 2.54 ₽.

- Reward budget = max(0, 7.56 ₽ − 2.54 ₽) = 5.02 ₽.

- Cost coefficient = 35.0% × 85.0% × 1.00 × (1 − 25.0%) × (1 + 1.5%) = 0.226472 ₽/eligible per nominal ₽.

- R_max = min(22.19 ₽, event 150.00 ₽, user 250.00 ₽) = 22.19 ₽; selected = 20.00 ₽.

- Gross valid reward cost = 5.95 ₽; collected partner funding = 1.49 ₽; unrecovered fraud = 0.07 ₽; X5 all-in reward cost = 4.53 ₽/eligible.

- Mean profit = 13.50 ₽ − 2.54 ₽ − 4.53 ₽ = 6.44 ₽/eligible; prudent LCB profit = 0.50 ₽/eligible.

- Campaign point estimate = 643 556.25 ₽; ROI_X5 = 1.15x; Decision: LAUNCH WITH STOP-LOSS.

## 6.3. Upside

- CM/visit = 700 ₽ × 14.0% = 98.00 ₽.

- Gross ΔCM = 0.500 visits × 98.00 ₽ = 49.00 ₽/eligible.

- Sustained visits = 0.500 × (1 − 10.0%) = 0.4500; sustained ΔCM = 44.10 ₽.

- LCB visits = max(0, 0.500 − 1.645 × 0.045593) = 0.4250; after pull-forward LCB CM = 37.48 ₽.

- Prudent CM = 37.48 ₽ × (1 − 15.0%) = 31.86 ₽.

- K = promo 2.21 ₽ + returns 0.22 ₽ + variable 1.35 ₽ + ops 0.30 ₽ = 4.08 ₽.

- Reward budget = max(0, 31.86 ₽ − 4.08 ₽) = 27.79 ₽.

- Cost coefficient = 50.0% × 75.0% × 1.00 × (1 − 50.0%) × (1 + 0.5%) = 0.188437 ₽/eligible per nominal ₽.

- R_max = min(147.46 ₽, event 150.00 ₽, user 250.00 ₽) = 147.46 ₽; selected = 140.00 ₽.

- Gross valid reward cost = 52.50 ₽; collected partner funding = 26.25 ₽; unrecovered fraud = 0.13 ₽; X5 all-in reward cost = 26.38 ₽/eligible.

- Mean profit = 44.10 ₽ − 4.08 ₽ − 26.38 ₽ = 13.64 ₽/eligible; prudent LCB profit = 1.41 ₽/eligible.

- Campaign point estimate = 1 364 325.00 ₽; ROI_X5 = 0.49x; Decision: LAUNCH WITH STOP-LOSS.

## 6.4. Stress cases

| **Stress**                         | **Sustained ΔCM** | **Non-reward cost** | **X5 reward cost** | **Extra loss** | **Profit/eligible** | **Action**                                |
|------------------------------------|-------------------|---------------------|--------------------|----------------|---------------------|-------------------------------------------|
| Zero uplift                        | 0.00 ₽            | 0.30 ₽              | 4.53 ₽             | 0.00 ₽         | -4.83 ₽             | STOP / do not launch                      |
| All observed uplift = pull-forward | 0.00 ₽            | 0.30 ₽              | 4.53 ₽             | 0.00 ₽         | -4.83 ₽             | STOP; extend lag                          |
| High returns + failed clawback     | 13.50 ₽           | 3.75 ₽              | 4.53 ₽             | 0.22 ₽         | 5.00 ₽              | Continue only if return gate and LCB pass |
| Partner budget exhausted (Upside)  | 44.10 ₽           | 4.08 ₽              | 52.76 ₽            | 0.00 ₽         | -12.74 ₽            | STOP new enrollments / rescale            |

**DERIVED** Проверка арифметики: Base zero-uplift и full-pull-forward дают -4.83 ₽/eligible; Upside при полном исчерпании partner budget даёт -12.74 ₽/eligible. Следовательно, reserve coverage должен быть runtime gate, а не постфактум variance.

# 7. Reward gate

| **Step** | **Gate**           | **Question**                                                                    | **Fail action**            | **Pass action**  |
|----------|--------------------|---------------------------------------------------------------------------------|----------------------------|------------------|
| 1        | Core data          | Есть CM bridge, randomized control, window, SE, redemption/cost/funding inputs? | Нет → NO CHALLENGE         | Да → compute ITT |
| 2        | Causal effect      | Outcome на eligible ITT и treatment+lag; SRM/interference acceptable?           | Нет → NO CHALLENGE         | Да → LCB         |
| 3        | Prudent CM         | One-sided LCB после pull-forward и buffer \> 0?                                 | Нет → NO CHALLENGE         | Да → subtract K  |
| 4        | Reward budget      | B_reward = prudent CM − K \> 0?                                                 | Нет → NO MONETARY REWARD   | Да → coefficient |
| 5        | Funding            | Reserve, reimbursable event, p_collect, returns/fraud rules valid?              | Нет → haircut/reprice      | Да → R_economic  |
| 6        | Caps               | Selected ≤ economic + event/user/group/rule/campaign/category/funder caps?      | Нет → REJECT/RESCALE       | Да → risk checks |
| 7        | Operational safety | Fraud/returns/stock/promo/budget signals below stop levels?                     | Нет → PENDING/STOP         | Да → LAUNCH      |
| 8        | Runtime            | Actual + commitments + p95 claims within budget and LCB not below tolerance?    | Нет → STOP NEW ENROLLMENTS | Да → continue    |

## Псевдокод

| if core_data_missing or control_missing: return NO_CHALLENGE |
|--------------------------------------------------------------|

| lcb_cm = max(0, mean_delta_cm - z \* se_delta_cm) |
|---------------------------------------------------|

| prudent_cm = lcb_cm \* (1 - risk_buffer) |
|------------------------------------------|

| reward_budget = max(0, prudent_cm - nonreward_costs) |
|------------------------------------------------------|

| if reward_budget == 0: return NO_MONETARY_REWARD or NO_CHALLENGE |
|------------------------------------------------------------------|

| coef = p_complete_U \* p_redeem_U \* unit_cost_U \* unfunded_share_U \* (1 + fraud_U) |
|---------------------------------------------------------------------------------------|

| r_econ = 0 if coef \<= 0 else reward_budget / coef |
|----------------------------------------------------|

| r_max = floor_to_denomination(min(r_econ, all_remaining_hard_caps)) |
|---------------------------------------------------------------------|

| if selected_reward \> r_max: return REJECT_OR_RESCALE |
|-------------------------------------------------------|

| if runtime_stop_flag: return STOP_NEW_ENROLLMENTS |
|---------------------------------------------------|

| return LAUNCH_WITH_STOP_LOSS |
|------------------------------|

# 8. Система лимитов

**ASSUMPTION** Диапазоны ниже — стартовые PoC constraints, а не правила X5. Динамический economic cap всегда имеет приоритет над статическим диапазоном.

| **Level**        | **PoC range**             | **Rule**                                    | **Soft gate**   | **Hard gate**              |
|------------------|---------------------------|---------------------------------------------|-----------------|----------------------------|
| Event/completion | 5–150 ₽ nominal           | ≤ individual R_max                          | 80% warning     | 100% block                 |
| User/day         | 0–1 monetary settlement   | XP может быть чаще; money cooldown          | 1 pending       | No second settlement       |
| User/28d         | 50–250 ₽ nominal          | Все mechanics/funding pools суммарно        | 80% cap         | 100% block                 |
| Dvor/cycle       | 200–800 ₽ for 3–7 members | ≤ Σ individual R_max                        | 80% group cap   | Σ individual/campaign caps |
| Rule/day         | 1–2% of rule budget       | Expected + commitments + p95 claims         | 80% burn review | 95% freeze / 100% stop     |
| Campaign         | Pre-funded envelope       | No uncapped exposure                        | 80% review      | 95% pause / 100% stop      |
| Category/SKU     | Dynamic                   | No negative-CM, stock-out or promo conflict | Alert           | Block offer                |
| Funder           | Reserve ≥ p95 claims      | Collection-adjusted                         | \<1.1x review   | \<1.0x stop                |
| Referral         | Qualified behavior only   | Never registration-only payout              | Pending         | Deny/clawback              |

**Окна settlement.** Рекомендуется instant XP/visual success + delayed monetary settlement. Конкретная задержка зависит от возвратов, fraud SLA и UX; «14 дней» из черновика не подтверждено как универсальное правило.

# 9. Экономика «Двора»

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Рекомендуемая версия «Двор Lite»</strong></p>
<p>Общий прогресс и равный group XP сохраняются. Денежная выплата требует минимального verified personal action и не может превысить individual R_max. Это сохраняет кооперацию, но ограничивает free-rider subsidy и групповую бюджетную экспозицию.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Element**              | **Verdict**            | **Rule**                                                                                            | **Validation metric**                                |
|--------------------------|------------------------|-----------------------------------------------------------------------------------------------------|------------------------------------------------------|
| Равная награда всем      | ИЗМЕНИТЬ               | Равный XP/косметика; деньги только active member с verified action.                                 | Free-rider payout share; payout to zero contributors |
| Личный multiplier до 20% | УБРАТЬ из денег на PoC | XP-only; money only from residual individual cap.                                                   | Cap breach, payout concentration                     |
| Backup β=0.7             | ПРОВЕРИТЬ              | XP-only first; β∈\[0.5,1.0\], cap на замещение.                                                     | Completion, CM, pressure/complaints, free-riding     |
| Общая цель               | ИЗМЕНИТЬ               | Σ personalized incremental targets/qualified progress, не buyer savings как P&L.                    | Incremental CM and attainability                     |
| Membership changes       | ОСТАВИТЬ с rules       | Snapshot at cycle start; join after cutoff ineligible; leaver proration; zero contributor no money. | Budget predictability, churn                         |
| Randomization            | ИЗМЕНИТЬ               | Assign whole Dvor/store pool to one arm.                                                            | Cross-arm spillover/interference                     |

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>R_i,nom = 1{yard_success} × 1{active_i} × min(R_equal_base + R_personal_i, R_i,max)</p>
<p><em>R_equal_base должен быть малой частью денежного pool или нулём на первом PoC; equal social reward может быть XP.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>Σ_i R_i,nom ≤ min(Σ_i R_i,max, yard_cap, rule_cap, campaign_cap, funder_remaining_cap)</p>
<p><em>Group cap никогда не создаёт дополнительный бюджет поверх individual safe caps.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>backup_required_j = deficit_i / β, 0 &lt; β ≤ 1</p>
<p><em>β=0.7 из черновика — ASSUMPTION. Backup contribution нужно cap-ить и не превращать автоматически в денежный multiplier.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**Partial completion.** Для денег рекомендуется binary verified minimum + proportional personal residual reward; для общего XP возможен плавный progress. При изменении состава финансовый denominator фиксируется snapshot-ом цикла; выход участника не должен ретроспективно увеличивать выплаты другим без повторного gate.

**Falsification criteria.** Упростить или остановить «Двор», если cluster-ITT profit не положителен, free-rider payout превышает pre-specified tolerance, complaints/group churn растут, либо interference/selection не позволяет получить интерпретируемый causal estimate. Альтернатива — индивидуальный challenge + shared non-monetary community progress.

**INFERENCE** Социальная механика требует cluster randomization из-за возможного взаимного влияния участников. Общий methodological support: [<u>Athey & Imbens</u>](https://arxiv.org/abs/1607.00698) и [<u>Airbnb interference</u>](https://pubsonline.informs.org/doi/10.1287/mnsc.2020.01157); empirical effect sizes Airbnb не переносятся.

# 10. Brand funding

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Принцип</strong></p>
<p>Brand funding меняет распределение cost/risk, но не превращает sponsored sales в incremental sales и не обнуляет X5 cost. В gate входит только reserve-backed, contract-eligible и collection-adjusted funding.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Contract/data block** | **Minimum requirement**                                                                          | **Failure mode**                                  |
|-------------------------|--------------------------------------------------------------------------------------------------|---------------------------------------------------|
| Causal attribution      | Randomized holdout; eligible population; treatment+lag; SKU/category and cross-category outcomes | Sponsored sales counted as incremental            |
| Funding event           | Одно определение: issued / earned / redeemed / qualified purchase                                | Issued and redeemed bases mixed                   |
| Rate/tax/fees           | Rate, VAT/tax treatment, service/media/admin fees                                                | Headline share treated as collected cash          |
| Budget                  | Reserved amount, real-time remaining, commitments, p95 claims                                    | Exhaustion silently shifts cost to X5             |
| Returns/fraud           | Reimbursement/clawback matrix, rejected claims, liability owner                                  | Partner refuses returned/fraud claims post-launch |
| Settlement              | Invoice cadence, evidence, disputes, collection probability/bad debt                             | Theoretical receivable used as funding            |
| Promo stacking          | Exclusivity, ordinary promo calendar, stock-outs                                                 | Double subsidy or promo conflict                  |
| Data/privacy            | Permitted aggregate fields, retention, audit rights, advertising disclosure                      | Unnecessary personal data or unusable attribution |

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>F_partner = min(rate_contract × reimbursable_base, reserve_remaining) × p_collect</p>
<p><em>Returns/fraud/clawback and nonrecoverable tax/admin should be applied according to the contract, not assumed away.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Ledger**                | **Required reporting**                                                                                                                                     |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| X5 ledger                 | Total incremental basket CM; X5 reward cost net of collected funding; ordinary promo interaction; programme VC; fraud/returns; campaign profit and ROI_X5. |
| Brand ledger              | Incremental brand units/revenue and brand CM if provided; funded rewards; service/media fees; brand campaign profit/ROI.                                   |
| Shared attribution report | Eligible/control counts, assignment, offer delivery, qualifying event, returns, funding claim status, confidence intervals and caveats.                    |

**TO_VALIDATE** Claim “7:1”. Найденная vendor page использует wording “up to 7:1 ROI” / “7:1 ROI”, тогда как проектный черновик называет это sales-to-reward. Методика, denominator, revenue/margin basis, randomization, time window и all-in cost не раскрыты. [<u>Eagle Eye 7:1 claim</u>](https://eagleeye.com/personalized-promotions) Поэтому показатель нельзя повторять как факт или параметр X5; он допустим только как вопрос поставщику с запросом первичного measurement protocol.

# 11. Интерфейс с симуляцией

## 11.1. Входы по grain

| **Grain**          | **Keys**                                              | **Inputs**                                                                         | **Control**                 |
|--------------------|-------------------------------------------------------|------------------------------------------------------------------------------------|-----------------------------|
| Eligible user      | campaign_id, user_id_hash, arm, strata, store_cluster | eligibility, assignment, delivery, pre-period visits/CM/covariates                 | No name/address/contact     |
| Action/challenge   | challenge_id, user_id_hash                            | shown, accepted, progress, completed, valid, timestamps, reward_nominal, funded_by | State machine/idempotency   |
| Receipt            | receipt_id, user_id_hash, timestamp                   | net paid before game reward, ordinary promo, returns/void, store/format            | Netted return window        |
| Item/category      | receipt_id, category/SKU                              | qty, net sales, CM proxy, promo, supplier funding, stock-out                       | Approved CM bridge          |
| Reward transaction | reward_txn_id, challenge_id                           | issued/earned/pending/redeemed/expired/reversed, unit cost, funding collected      | Cohort aging/reconciliation |
| Dvor cycle         | yard_id, cycle_id, member_hash                        | membership snapshot, personal target, contribution, backup, eligibility, payout    | Cluster assignment          |
| Partner campaign   | funder_id, campaign_id                                | event basis, rate, reserve, remaining, p_collect, returns/fraud rules              | Real-time burn              |

## 11.2. Выходы

| **Grain**    | **Outputs**                                                                     | **Unit**             | **Use**              |
|--------------|---------------------------------------------------------------------------------|----------------------|----------------------|
| User/window  | CM_pre-game, visits, net sales, returns                                         | ₽/eligible; counts   | Input to ITT         |
| Rule/segment | mean ΔCM, SE, LCB, completion, redemption, q_baseline-qualifier                 | ₽/eligible; rates    | Cap inputs           |
| Reward       | R_economic, R_max, selected, valid cost, fraud loss, partner collected, X5 cost | ₽/eligible and total | Reward API / Finance |
| Dvor/cycle   | group success, active payout, free-rider share, backup, group cap               | rates/₽              | Mechanic diagnostics |
| Campaign     | profit/eligible, profit/treated, campaign profit, ROI, burn and p95 forecast    | ₽, x                 | Primary dashboard    |

## 11.3. Рекомендуемые таблицы

- \`experiment_assignment\`: immutable eligibility, strata, cluster, arm, assignment_time, delivery_time.

- \`user_window_outcomes\`: one row per user × analysis window with visits, net sales, CM_pre_game, returns.

- \`challenge_states\`: complete event-state history; monetary settlement separate from XP.

- \`reward_ledger\`: nominal states, economic unit cost, funding claim/collection, reversal/clawback.

- \`rule_economics\`: mean effect, SE/LCB, conservative cost inputs, R_max, selected reward, decision.

- \`campaign_budget\`: approved budget, actual, commitments, p50/p95 expected claims, remaining reserve, stop flag.

**Simulation logic.** Scenario analysis may simulate behavioral response, but it must label assumed uplift explicitly and preserve a holdout. The simulator is not evidence of real uplift; it validates formulas, state transitions, caps, budget burn and failure behavior.

# 12. Пилотный dashboard

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Primary metric</strong></p>
<p>ITT Net Incremental Profit per Eligible User over treatment + lag, with two-sided confidence interval and one-sided lower confidence bound. Frequency growth and completion are diagnostics, not substitutes for profit.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Metric**                        | **Formula**                                                     | **Unit/denominator**  | **Role**     | **Uncertainty**            | **Stop-loss**                             |
|-----------------------------------|-----------------------------------------------------------------|-----------------------|--------------|----------------------------|-------------------------------------------|
| Net Incremental Profit / Eligible | ΔCM_beh − X5 reward − programme VC − losses − fixed/N           | ₽/randomized eligible | Primary      | 95% CI + one-sided LCB     | LCB \< −tolerance or p95 loss \> envelope |
| Campaign Profit                   | N eligible × primary metric                                     | ₽/campaign            | Primary      | Cluster/bootstrap interval | Forecast loss \> budget                   |
| Purchases / User                  | Receipts / randomized eligible                                  | visits/eligible       | Diagnostic   | 95% CI                     | Never sufficient alone                    |
| Share ≥ N purchases               | Pre-specified threshold                                         | % eligible            | Product      | Difference CI              | N fixed before test                       |
| Gross vs sustained ΔCM            | Short window vs treatment+lag                                   | ₽/eligible            | Pull-forward | Weekly/event study CI      | Sustained effect collapses                |
| Reward cost split                 | valid / cannibalized diagnostic / fraud; X5 / partner collected | ₽/eligible and total  | Budget       | p95 claims                 | 80% review; 95% freeze; 100% stop         |
| Partner reserve coverage          | remaining reserve / p95 claims                                  | x                     | Budget       | Forecast band              | \<1.1x review; \<1.0x stop                |
| Returns/clawback                  | returned qualifiers and unrecovered rewards                     | % and ₽               | Safety       | Control limits             | Pre-specified threshold                   |
| Fraud paid/recovered              | paid suspected fraud, recovery, precision/FPR                   | ₽ and rates           | Safety       | Review-sample CI           | Hard fraud-loss envelope                  |
| Dvor free-riding/interference     | zero-contributor payout, cross-arm spillover, group churn       | %/₽                   | Mechanism    | Cluster CI                 | Modify/stop mechanic                      |

## Экспериментальный дизайн

- Personal challenge: individual randomization, stratified by pre-period frequency/CM/store format; immutable assignment.

- Dvor: whole Dvor or store-level pool cluster randomization; prevent members from crossing arms during a cycle.

- Primary analysis: ITT; offer delivered/per-treated and completer analyses are secondary diagnostics.

- Treatment and lag windows fixed before launch. Four + four weeks in scenarios is an ASSUMPTION, not a prescribed duration.

- Use pre-period covariates/CUPED when pre-specified; estimate actual variance reduction on X5 data. Source: [<u>CUPED</u>](https://dl.acm.org/doi/10.1145/2433396.2433413).

- No continuous peeking for efficacy; efficacy looks and alpha spending pre-specified. Budget/fraud safety may stop continuously.

- Sample size computed from MDE in profit/eligible, variance, pre-period correlation, expected attrition/non-delivery and cluster ICC.

- Check sample-ratio mismatch, delivery failures, contamination, stock-outs and metric logging before reading uplift.

# 13. Что запросить у X5

| **Priority** | **Request**                                                                                                      | **Minimum grain**                                   | **Uncertainty reduced**                    |
|--------------|------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|--------------------------------------------|
| 1            | Contribution-margin bridge before game reward after ordinary promo, supplier funding and approved variable costs | category × format × week; arm if available          | CM rate / CM per visit                     |
| 2            | Randomized pre/test/post visits, net sales and CM by arm/stratum                                                 | user_hash × week or sufficient aggregate statistics | Treatment effect, SE, pull-forward         |
| 3            | Reward issue→redeem→expire→reverse cohort curves and mechanic-specific economic unit cost                        | reward cohort × age × mechanic                      | Redemption, breakage, κ                    |
| 4            | Ghost-challenge qualification in control                                                                         | rule × arm × week                                   | Baseline qualification/cannibalized reward |
| 5            | Ordinary promo calendar, stacking, supplier funding and stock-outs                                               | category/SKU × store cluster × day                  | Promo interaction/substitution             |
| 6            | Returns/voids, clawbacks, fraud paid and recovered                                                               | mechanic × cohort × age                             | Return/fraud losses                        |
| 7            | Partner contracts, reserves, burn, claim rejection and collection                                                | campaign/funder/day                                 | Collectible funding                        |
| 8            | Payment, messaging, cloud/vendor, support and settlement variable costs                                          | campaign/week                                       | All-in profit / break-even                 |
| 9            | Cluster sizes, ICC, pre-period variance/correlation                                                              | store/Dvor pool                                     | Power and valid CI                         |

**Privacy-minimized form.** Hashed/pseudonymous user identifiers or aggregate sufficient statistics are enough for the pilot design; names, exact addresses, contacts and detailed geotracks are unnecessary.

## 13.1. Вопросы Accounting/Tax/KKT — не заключение

- Какова approved accounting policy для allocation к loyalty points, standalone selling price, expected redemption и contract liability по конкретной mechanic?

- Как reconciliation between nominal points, accounting liability, revenue recognition and economic marginal cost должен выглядеть в management reporting?

- Как квалифицируется каждое reward state: discount, bonus payment, separate performance obligation, marketing service, supplier reimbursement?

- Какие значения и теги должны попадать в кассовый чек при скидке/списании/начислении и как обрабатывать возврат?

- Как учитывать VAT/tax and nonrecoverable costs в X5/brand split?

Официальные отправные точки: [<u>X5 FY2025 IFRS statements</u>](https://www.x5.ru/wp-content/uploads/2026/05/auditorskoe-zaklyuchenie-i-finansovaya-otchetnost_pao-kcz-iks-5_2025_format_dop_no-links_eng.pdf), [<u>IFRS 15</u>](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-15-revenue-from-contracts-with-customers/), contextual/archived [<u>FNS receipt guidance</u>](https://www.nalog.gov.ru/rn77/news/activities_fts/15175966/) и [<u>FNS bonus details</u>](https://www.nalog.gov.ru/rn43/news/activities_fts/15194625/). Последние не заменяют профильную проверку.

## 13.2. Вопросы Legal/Privacy/Advertising — не заключение

- Lawful basis, transparency and retention for challenge personalization, pseudonymous store-linked cohorts and Dvor membership.

- Whether store-level auto-matching can create re-identification or unwanted social inference; required minimum pool and opt-in/opt-out.

- What claims, material terms, expiry, funding disclosure and stimulating-event rules must be shown to the user.

- How online advertising/brand sponsorship disclosures and data sharing should be implemented.

- How to exclude sensitive/vulnerable targeting and harmful consumption categories from objectives and recommendation features.

Отправные тексты для юристов: [<u>152-FZ</u>](https://pravo.gov.ru/proxy/ips/?docbody=&nd=102108261) и [<u>Advertising law</u>](https://www.consultant.ru/document/cons_doc_LAW_58968/). Использовать актуальные consolidated texts на дату запуска.

# 14. Источники

**Дата доступа к web-источникам: 4 сентября 2026.** Приоритет: первичные/официальные источники; vendor materials отмечены отдельно. Исследование остановлено, когда определения и методология получили достаточную опору, а X5-specific параметры были честно оставлены TO_VALIDATE вместо подстановки несопоставимых proxy.

**1.** [<u>X5 Corporate Center — Audited IFRS Financial Statements for FY2025</u>](https://www.x5.ru/wp-content/uploads/2026/05/auditorskoe-zaklyuchenie-i-finansovaya-otchetnost_pao-kcz-iks-5_2025_format_dop_no-links_eng.pdf). X5 Corporate Center; 2026; geography: Russia / X5. **Применение:** Loyalty points as a separate performance obligation/material right; transaction-price allocation; expected non-redemption; contract liability until redemption; disclosed liability movements. **Ограничение:** Accounting recognition, not a causal estimate of reward profitability or an X5 redemption rate for the proposed mechanic.

**2.** [<u>IFRS 15 Revenue from Contracts with Customers</u>](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-15-revenue-from-contracts-with-customers/). IFRS Foundation; current official page; standard effective 2018; geography: International. **Применение:** Five-step revenue model and allocation of transaction price to performance obligations. **Ограничение:** Application to X5 facts and Russian statutory reporting requires professional accounting review.

**3.** [<u>Do Targeted Discount Offers Serve as Advertising? Evidence from 70 Field Experiments</u>](https://pubsonline.informs.org/doi/10.1287/mnsc.2016.2450). Sahni, Zou & Chintagunta; Management Science; 2017; geography: United States, online ticket resale. **Применение:** Randomized recipient/control measurement; reward redemption and causal demand effects are not the same; carryover can matter. **Ограничение:** Channel, category and effect sizes are not transferable to Russian grocery retail.

**4.** [<u>Decomposing the Sales Promotion Bump with Store Data</u>](https://pubsonline.informs.org/doi/abs/10.1287/mksc.1040.0061). Van Heerde, Leeflang & Wittink; Marketing Science; 2004; geography: Retail scanner datasets. **Применение:** Promotion response can contain cross-brand substitution, category expansion and cross-period purchase acceleration. **Ограничение:** Historical datasets and reported shares are mechanisms, not X5 parameter proxies.

**5.** [<u>Measuring the Impact of Promotions on Brand Switching When Consumers Are Forward Looking</u>](https://journals.sagepub.com/doi/10.1509/jmkr.40.4.389.19392). Sun, Neslin & Srinivasan; Journal of Marketing Research; 2003; geography: Consumer packaged goods. **Применение:** Purchase timing and forward-looking behavior can bias reduced-form promotion response estimates. **Ограничение:** Methodological evidence, not a direct parameter for X5.

**6.** [<u>The Long-Term Impact of Loyalty Programs on Consumer Purchase Behavior and Loyalty</u>](https://journals.sagepub.com/doi/10.1509/jmkg.71.4.019). Yuping Liu; Journal of Marketing; 2007; geography: United States, convenience-store franchise. **Применение:** Heavy buyers can be most likely to claim rewards yet change behavior less; treatment heterogeneity matters. **Ограничение:** Legacy observational setting; not an X5 causal estimate.

**7.** [<u>Do Loyalty Programs Really Enhance Behavioral Loyalty? An Empirical Analysis Accounting for Self-Selecting Members</u>](https://doi.org/10.1016/j.ijresmar.2006.10.005). Leenheer et al.; International Journal of Research in Marketing; 2007; geography: Netherlands grocery panel. **Применение:** Member/non-member comparisons can be biased by endogenous self-selection. **Ограничение:** Country, period and programme design differ; use as design caution only.

**8.** [<u>The Dual Value of Delayed Incentives: Evidence from a Gift Card Promotion</u>](https://pubsonline.informs.org/doi/10.1287/msom.2022.0218). Kadiyala, Özer & Şimşek; Manufacturing & Service Operations Management; 2024; geography: United States, online department store. **Применение:** Issuance and later redemption can create distinct behavioral effects and should be measured separately. **Ограничение:** Fuzzy regression discontinuity; not grocery and not an RCT.

**9.** [<u>Latent Stratification for Incrementality Experiments</u>](https://pubsonline.informs.org/doi/10.1287/mksc.2022.0297). Berman & Feit; Marketing Science; 2024; geography: Catalog experiments. **Применение:** Precision and heterogeneous effects in incrementality experiments. **Ограничение:** Optional analytical method; does not provide X5 effect magnitudes.

**10.** [<u>The Econometrics of Randomized Experiments</u>](https://arxiv.org/abs/1607.00698). Athey & Imbens; 2016/2017; geography: General methodology. **Применение:** Intent-to-treat, stratification, clustering, noncompliance and confidence intervals. **Ограничение:** General method reference.

**11.** [<u>Reducing Interference Bias in Online Marketplace Experiments Using Cluster Randomization</u>](https://pubsonline.informs.org/doi/10.1287/mnsc.2020.01157). Airbnb researchers; Management Science; 2021; geography: Online marketplace. **Применение:** Individual randomization can be biased when subjects affect each other; cluster assignment is a standard remedy. **Ограничение:** Marketplace-specific empirical magnitude; only the design principle transfers.

**12.** [<u>Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data</u>](https://dl.acm.org/doi/10.1145/2433396.2433413). Deng, Xu, Koh & Walker; WSDM; 2013; geography: Microsoft online experiments. **Применение:** Pre-period covariates can reduce variance when specified correctly. **Ограничение:** No guaranteed precision gain for X5; must be estimated from X5 pre-period data.

**13.** [<u>Tesco Clubcard Challenges Case Study</u>](https://eagleeye.com/case-studies/tesco-clubcard-challenges). Eagle Eye (vendor); current vendor page, accessed 2026-09-04; geography: United Kingdom / Tesco. **Применение:** Evidence that large-scale personalized challenge campaigns have been implemented and vendor-reported engagement is available. **Ограничение:** Vendor case; no randomized incremental contribution-margin evidence for transfer to X5.

**14.** [<u>Personalized Promotions</u>](https://eagleeye.com/personalized-promotions). Eagle Eye (vendor marketing); current page, accessed 2026-09-04; geography: Retail/brands, unspecified. **Применение:** Origin of the wording “up to 7:1 ROI” / “7:1 ROI”. **Ограничение:** No disclosed randomized control, denominator, revenue-versus-margin definition, time window, all-in costs or directly comparable “sales-to-reward” definition.

**15.** [<u>FNS guidance on receipt price after discounts and bonus use</u>](https://www.nalog.gov.ru/rn77/news/activities_fts/15175966/). Federal Tax Service of Russia; 2024-08-28 (archived guidance); geography: Russia. **Применение:** Raises questions for receipt representation of discounts/bonus consideration. **Ограничение:** Archived and contextual; not a complete tax/KKT conclusion.

**16.** [<u>FNS guidance on optional receipt details for bonus points</u>](https://www.nalog.gov.ru/rn43/news/activities_fts/15194625/). Federal Tax Service of Russia; 2024; geography: Russia. **Применение:** Possible receipt disclosure fields for bonus points and monetary equivalent. **Ограничение:** Not a full accounting, tax or KKT opinion.

**17.** [<u>Federal Law No. 152-FZ On Personal Data</u>](https://pravo.gov.ru/proxy/ips/?docbody=&nd=102108261). Official legal information portal; current consolidated text to verify; geography: Russia. **Применение:** Checklist source for privacy, lawful basis, minimization and group mechanics. **Ограничение:** Professional legal review required.

**18.** [<u>Federal Law On Advertising</u>](https://www.consultant.ru/document/cons_doc_LAW_58968/). Current law index / text to verify; current consolidated text to verify; geography: Russia. **Применение:** Checklist for stimulating events and digital promotion communications. **Ограничение:** Professional legal review required; this report is not a legal opinion.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Финальный arithmetic / double-count audit</strong></p>
<p>Проверено: одинаковые units/window/denominator во всех сценариях; ITT test–control; reward исключён из CM ledger и вычтен один раз; cannibalized reward — subset, не дополнительное вычитание; fraud subcomponent не дублируется; partner funding collection-adjusted; Base selected 20 ₽ ≤ R_max 22.19 ₽; Upside 140 ₽ ≤ 147.46 ₽; Conservative rejected because LCB profit &lt; 0.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


---

## Файлы модели

- Расчётная модель: `X5_reward_economics_model.xlsx`
- Нормализованная сценарная таблица: [`04-reward-scenarios.csv`](04-reward-scenarios.csv)
- Все рублёвые сценарные значения в модели являются `ASSUMPTION` / scenario analysis, если явно не указано иное.
