# Исследование 7. План реального пилота

## Игровая лояльность X5: кооперативный «Двор»

*Preregistration-ready дизайн причинного эксперимента с защитой вкладной маржи, пользователей и бюджета*

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Рекомендация в одном абзаце</strong></p>
<p><strong>Основной дизайн:</strong> matched/blocked parallel cluster RCT по магазинам с тремя рукавами: A - BAU control; B - solo-parity active control; C - «Двор». <strong>Primary estimand:</strong> ITT-эффект C против A на числе квалифицированных покупочных дней за 42 дня. <strong>Ключевой guardrail:</strong> non-inferiority вкладной маржи на заранее eligible user, нижняя граница 95% CI выше -delta_M. <strong>Fallback при нехватке магазинов:</strong> убрать B и провести двухрукавный store-cluster RCT; если независимых магазинов все равно недостаточно - рандомизировать заранее сформированные непересекающиеся proto-yards с жестким контролем cross-yard contamination и явно более слабой внешней валидностью.</p>
<p><strong>Основание:</strong> [S0] Временный пакет GPT Pro: План реального пилота; <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC2600548/"><u>[S1] Hudgens, M. G.; Halloran, M. E., 2008</u></a>; <a href="https://openknowledge.worldbank.org/bitstreams/c12c79f1-5fcd-51e7-a6f7-fc908f506846/download"><u>[S2] Baird, S.; Bohren, J. A.; McIntosh, C.; Özler, B., 2018</u></a>; <a href="https://projecteuclid.org/journals/statistical-science/volume-24/issue-1/The-Essential-Role-of-Pair-Matching-in-Cluster-Randomized-Experiments/10.1214/08-STS274.full"><u>[S5] Imai, K.; King, G.; Nall, C., 2009</u></a>; <a href="https://www.fda.gov/media/78504/download"><u>[S14] U.S. Food and Drug Administration, 2016</u></a></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**Короткий план исследования**

> **1.** Зафиксировать причинный вопрос, interference structure и единицу назначения.
>
> **2.** Сопоставить индивидуальный RCT, cluster RCT, randomized saturation, encouragement и phased rollout.
>
> **3.** Определить estimands, одну primary metric, margin non-inferiority и intercurrent events.
>
> **4.** Задать формулы мощности, low/base/high сценарии и data request для точной симуляции.
>
> **5.** Собрать SAP, instrumentation, preflight, monitoring, stop rules и joint decision matrix.

**Статус чисел**

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>FACT</strong></p>
<p>Прямо подтверждено источником или нормативным текстом.</p></th>
<th><p><strong>INFERENCE</strong></p>
<p>Вывод из источников и ограничений проекта.</p></th>
<th><p><strong>ASSUMPTION</strong></p>
<p>Сценарное проектное значение, не факт X5.</p></th>
<th><p><strong>TO_VALIDATE</strong></p>
<p>Нужно измерить или утвердить до preregistration/launch.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

Версия 1.0 \| Дата: 04.09.2026 \| Язык: русский \| География: пилот X5 в заранее выбранных магазинах РФ

*Важно: кейс не задает N, период, MDE, baseline variance, ICC и delta_M. В отчете они не выдаются за факты X5; сценарные значения помечены ASSUMPTION, финальные параметры - TO_VALIDATE.*

# 1. Одностраничный pilot charter
| **Решение**            | **Рекомендуется** three-arm store-cluster RCT; primary contrast C «Двор» vs A BAU. B solo-parity нужен для оценки добавочной ценности social layer.                                                                              | **Primary estimand** | User-weighted ITT difference E\[Y\|C\]-E\[Y\|A\] с adjustment по block/pair и pre-period outcome; 95% CI с uncertainty на уровне магазина.                                                                                                 |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Аудитория**          | Закрытая pre-eligible когорта пользователей карты лояльности и приложения, определенная до assignment по 56-дневному lookback. Все пороги eligibility - ASSUMPTION/TO_VALIDATE.                                                  | **Margin guardrail** | theta_M = E\[CM\|C\]-E\[CM\|A\]. Pass NI, если нижняя граница 95% CI \> -delta_M; delta_M утверждает finance до просмотра outcomes.                                                                                                        |
| **Intervention C**     | Персональный челлендж + индивидуальный прогресс/аватар + кооперативная цель двора + общий progress bar + квалифицированные приглашения + заранее зафиксированные reward/fraud rules.                                             | **Safety gates**     | Privacy/security incident; severe harmful challenge; false-positive fraud block; Dvor-attributable complaints/social pressure; opt-out; reward/budget overrun; unreconciled data failure.                                                  |
| **Control A**          | Обычное приложение/программа лояльности без нового игрового слоя, новых reward rules и Dvor-коммуникаций.                                                                                                                        | **Основной анализ**  | ITT ANCOVA/OLS с centered pre-period covariates, treatment interactions и store-cluster uncertainty; randomization inference/CR2 при малом числе clusters.                                                                                 |
| **Active control B**   | Тот же personal challenge, cadence, UI и сопоставимая reward opportunity, но без group goal, peer rescue, group progress и Dvor referral. Не считать чистым психологическим эффектом, если фактические reward costs различаются. | **Launch gate**      | Offline hit rate \>=70% на 30-50 synthetic profiles + no critical safety failure; economics stress pass; fraud shadow pass; A/A, SRM и reconciliation pass; legal/privacy/product sign-off.                                                |
| **Unit of assignment** | **Магазин**. Пользователь закрепляется за pre-period home_store и сохраняет исходный arm независимо от последующих переходов.                                                                                                    | **Joint success**    | Primary superiority + margin NI + safety/data-quality gates. Нельзя принять решение по одному p-value.                                                                                                                                     |
| **Срок**               | **ASSUMPTION:** 56 дней pre-period; 42 дня treatment/outcome; 28 дней maturation для возвратов, pending reward и fraud settlement.                                                                                               | **Decision**         | **GO:** joint success и бизнес-эффект достаточен. **ITERATE:** margin/safety safe, но effect or take-up inconclusive/remediable. **STOP:** harm, powered null against business threshold, privacy/social incident или убыточная экономика. |
| **Primary metric**     | Число дней из 42, в которые у пользователя есть \>=1 квалифицированная loyalty-linked покупка после возвратов/отмен. Denominator - все eligible users на T0, независимо от opt-in.                                               | **Fallback**         | При недостатке stores - C vs A two-arm bundle test. При еще меньшем числе stores - pre-formed proto-yard randomization. Randomized saturation - отдельный следующий эксперимент.                                                           |

**Методологические источники:** \[S0\] Встроенный проектный пакет пользователя (03.09.2026); [<u>\[S1\] Hudgens, M. G.; Halloran, M. E. (2008)</u>](https://pmc.ncbi.nlm.nih.gov/articles/PMC2600548/); [<u>\[S5\] Imai, K.; King, G.; Nall, C. (2009)</u>](https://projecteuclid.org/journals/statistical-science/volume-24/issue-1/The-Essential-Role-of-Pair-Matching-in-Cluster-Randomized-Experiments/10.1214/08-STS274.full); [<u>\[S6\] Campbell, M. K. et al. (2012)</u>](https://www.bmj.com/content/345/bmj.e5661); [<u>\[S13\] International Council for Harmonisation (2019/2020)</u>](https://www.ema.europa.eu/en/ich-e9-statistical-principles-clinical-trials-scientific-guideline); [<u>\[S14\] U.S. Food and Drug Administration (2016)</u>](https://www.fda.gov/media/78504/download)

# 2. Design decision: что рандомизировать и почему
<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Ключевой causal constraint</strong></p>
<p>В «Дворе» участники воздействуют друг на друга, а приглашения и общий прогресс создают spillover. Индивидуальная рандомизация пользователей внутри реально взаимодействующей группы нарушает no-interference assumption. Поэтому первая проверка должна назначать политику на уровне, который максимально покрывает фактическую сеть взаимодействий; для PoC это магазин, а не участник.</p>
<p><strong>Основание:</strong> [S0] Временный пакет GPT Pro: План реального пилота; <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC2600548/"><u>[S1] Hudgens, M. G.; Halloran, M. E., 2008</u></a>; <a href="https://projecteuclid.org/journals/annals-of-applied-statistics/volume-11/issue-4/Estimating-average-causal-effects-under-general-interference-with-application-to/10.1214/16-AOAS1005.full"><u>[S3] Aronow, P. M.; Samii, C., 2017</u></a></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Дизайн**                                   | **Unit**                                   | **Сильная сторона**                                                                               | **Критический риск**                                                                                                                   | **Решение**                                                         |
|----------------------------------------------|--------------------------------------------|---------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| **Индивидуальный RCT для solo**              | Пользователь                               | Высокая мощность; чистый personal-mechanic effect                                                 | Непригоден для Dvor внутри общей сети: spillover и contamination                                                                       | **Да** для отдельной solo-механики; **нет** для Dvor                |
| **Randomize фактически сформированный Dvor** | Dvor                                       | Ближе к социальной единице                                                                        | Dvor формируется после opt-in; randomize только formed groups = post-treatment selection; связи между дворами одного магазина остаются | Не основной. Допустим только как **pre-formed proto-yard fallback** |
| **Store-cluster RCT**                        | Магазин / pre-period home_store            | Оценивает политику предложения; минимизирует внутри-магазинную contamination; операционно понятно | Нужны многие независимые stores; возможны cross-store users и referrals                                                                | **Рекомендуется для первого PoC**                                   |
| **Two-stage randomized saturation**          | Store saturation -\> user/proto-yard offer | Идентифицирует direct, spillover, total/overall effects при корректной exposure mapping           | Больше arms/cells, сложнее group formation и power; много clusters                                                                     | Следующий causal experiment, не первый PoC                          |
| **Encouragement design**                     | Store/user offer как encouragement         | Сохраняет voluntary opt-in; ITT оценивает offer policy                                            | CACE/TOT требует сильных assumptions; interference усложняет IV                                                                        | Использовать как **интерпретацию assignment**, не замену RCT        |
| **Phased/stepped rollout**                   | Randomized rollout order                   | Операционно возможен при невозможности одновременного holdout                                     | Calendar trends, seasonality, anticipation, carryover; сложнее анализ                                                                  | Last resort: randomized order + persistent holdout                  |

**Методологические источники:** [<u>\[S1\] Hudgens, M. G.; Halloran, M. E. (2008)</u>](https://pmc.ncbi.nlm.nih.gov/articles/PMC2600548/); [<u>\[S2\] Baird, S.; Bohren, J. A.; McIntosh, C.; Özler, B. (2018)</u>](https://openknowledge.worldbank.org/bitstreams/c12c79f1-5fcd-51e7-a6f7-fc908f506846/download); [<u>\[S3\] Aronow, P. M.; Samii, C. (2017)</u>](https://projecteuclid.org/journals/annals-of-applied-statistics/volume-11/issue-4/Estimating-average-causal-effects-under-general-interference-with-application-to/10.1214/16-AOAS1005.full); [<u>\[S4\] Imai, K.; Jiang, Z.; Malani, A. (2021)</u>](https://imai.fas.harvard.edu/research/spillover.html); [<u>\[S5\] Imai, K.; King, G.; Nall, C. (2009)</u>](https://projecteuclid.org/journals/statistical-science/volume-24/issue-1/The-Essential-Role-of-Pair-Matching-in-Cluster-Randomized-Experiments/10.1214/08-STS274.full)

## 2.1 Рекомендуемый three-arm store-cluster RCT
<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Assignment -&gt; exposure -&gt; analysis</strong></p>
<p>Pre-period eligible snapshot + home_store freeze</p>
<p>-&gt; matched/blocked stores</p>
<p>-&gt; random assignment A / B / C</p>
<p>-&gt; immutable user policy by original store arm</p>
<p>-&gt; voluntary opt-in and Dvor formation only inside C</p>
<p>-&gt; purchase, margin, reward, fraud, complaint outcomes for ALL T0 eligible users</p>
<p>-&gt; ITT analysis by original store assignment</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**Primary confirmatory contrast:** C vs A. Это общий causal effect политики «предложить Двор» по сравнению с BAU, включая take-up, неучастие, churn и фактическое формирование групп.

**Key mechanistic contrast:** C vs B, только по заранее заданной gatekeeping-процедуре. Он показывает добавочную ценность social layer при сопоставимых персональных компонентах, но не является чистым психологическим эффектом, если фактическая стоимость/получение наград различаются между B и C.

**Secondary contrast:** B vs A. Он проверяет solo bundle и помогает интерпретировать ситуацию, когда Dvor не добавляет эффекта.

**Multiplicity:** joint pass primary superiority + margin NI является intersection-union решением; дополнительный penalty между этими двумя обязательными условиями не нужен. Для C vs B и B vs A применить fixed gatekeeping либо Dunnett/Holm.

**Методологические источники:** [<u>\[S14\] U.S. Food and Drug Administration (2016)</u>](https://www.fda.gov/media/78504/download); [<u>\[S16\] Holm, S. (1979)</u>](https://www.jstor.org/stable/4615733); [<u>\[S17\] Dunnett, C. W. (1955)</u>](https://www.tandfonline.com/doi/abs/10.1080/01621459.1955.10501294)

## 2.2 Fallback hierarchy при недостатке кластеров
> **1. Сначала убрать arm B** и сохранить two-arm store-cluster RCT C vs A. Это честный bundle test: результат нельзя приписывать только кооперации.
>
> **2.** Если stores все равно мало, до assignment сформировать **непересекающиеся proto-yards** по pre-period данным, затем randomize proto-yards внутри stores. Запретить cross-yard invitations/discovery, заморозить membership eligibility и логировать contamination. Это усиливает partial-interference assumption и снижает внешнюю валидность.
>
> **3.** Если параллельный holdout невозможен, использовать **randomized phased rollout** с постоянным holdout и calendar fixed effects. Не заменять его простым before-after.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Не использовать как fallback</strong></p>
<p>Не рандомизировать отдельных пользователей внутри уже взаимодействующего двора и не анализировать только тех, кто вступил. Оба решения создают соответственно interference bias и post-treatment selection.</p>
<p><strong>Основание:</strong> <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC2600548/"><u>[S1] Hudgens, M. G.; Halloran, M. E., 2008</u></a>; <a href="https://projecteuclid.org/journals/annals-of-applied-statistics/volume-11/issue-4/Estimating-average-causal-effects-under-general-interference-with-application-to/10.1214/16-AOAS1005.full"><u>[S3] Aronow, P. M.; Samii, C., 2017</u></a></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 3. Estimand table
*Термины population, treatment strategies, outcome, intercurrent events и summary measure используются как дисциплина постановки вопроса. ICH E9(R1) здесь - методологическая рамка, а не применимое к retail юридическое требование.*

| **Estimand**                                     | **Population**                                                | **Treatment strategies**                               | **Outcome**                                         | **Intercurrent events**                                                                                                     | **Summary measure**                                              |
|--------------------------------------------------|---------------------------------------------------------------|--------------------------------------------------------|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| **Primary overall policy ITT**                   | Все T0 eligible users в stores A и C                          | Offer Dvor policy C vs BAU A                           | 42-day qualifying purchase days                     | No opt-in, no exposure, group exit, app uninstall, store migration, delayed reward, refunds: treatment-policy; не исключать | User-weighted adjusted mean difference C-A; 95% CI               |
| **Margin NI ITT**                                | Тот же closed cohort                                          | C vs A                                                 | Finalized net contribution margin per eligible user | Refunds/reversals attach to originating events; pending liability accrued; fraud and non-take-up remain                     | Mean difference theta_M; lower 95% CI vs -delta_M                |
| **Social increment**                             | T0 eligible users в B и C                                     | Dvor social layer C vs solo-parity B                   | Primary count + margin                              | Как выше                                                                                                                    | Adjusted mean difference C-B; confirmatory only after gate       |
| **Solo bundle**                                  | T0 eligible users в A и B                                     | Solo B vs BAU A                                        | Primary count + margin                              | Как выше                                                                                                                    | Adjusted mean difference B-A; secondary/gated                    |
| **Direct effect in future saturation design**    | Predefined users/proto-yards within partial-saturation stores | Offered vs not offered at same saturation              | Purchase days / margin                              | Take-up retained under assignment policy                                                                                    | ADE at fixed saturation; requires two-stage design               |
| **Spillover effect in future saturation design** | Unoffered users                                               | Positive-saturation cluster vs zero-saturation cluster | Purchase days / margin / complaints                 | Exposure mapping fixed before outcome review                                                                                | AIE/spillover difference                                         |
| **Complier/TOT supplement**                      | Latent compliers under instrument assumptions                 | Receipt of Dvor participation induced by offer         | Purchase days / margin                              | Interference and take-up explicitly modeled                                                                                 | IV/CACE only supplementary; assumptions reported, no GO decision |

**Методологические источники:** [<u>\[S1\] Hudgens, M. G.; Halloran, M. E. (2008)</u>](https://pmc.ncbi.nlm.nih.gov/articles/PMC2600548/); [<u>\[S2\] Baird, S.; Bohren, J. A.; McIntosh, C.; Özler, B. (2018)</u>](https://openknowledge.worldbank.org/bitstreams/c12c79f1-5fcd-51e7-a6f7-fc908f506846/download); [<u>\[S3\] Aronow, P. M.; Samii, C. (2017)</u>](https://projecteuclid.org/journals/annals-of-applied-statistics/volume-11/issue-4/Estimating-average-causal-effects-under-general-interference-with-application-to/10.1214/16-AOAS1005.full); [<u>\[S4\] Imai, K.; Jiang, Z.; Malani, A. (2021)</u>](https://imai.fas.harvard.edu/research/spillover.html); [<u>\[S13\] International Council for Harmonisation (2019/2020)</u>](https://www.ema.europa.eu/en/ich-e9-statistical-principles-clinical-trials-scientific-guideline); [<u>\[S18\] Angrist, J. D.; Imbens, G. W.; Rubin, D. B. (1996)</u>](https://www.jstor.org/stable/2291629)

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Primary interpretation</strong></p>
<p>The primary effect is the effect of <strong>assigning the offer policy</strong>, not the effect among joiners. A low opt-in rate is part of product performance, not a reason to redefine the denominator.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 4. Eligibility, recruitment, consent и assignment timing
<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Freeze before assignment</strong></p>
<p>Eligible cohort, home_store, blocking variables and any proto-yard fallback must be computed from pre-period data and frozen before randomization. Consent/opt-in occurs only after assignment; membership, challenge completion and post-launch activity never determine primary eligibility.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Элемент**                    | **Правило preregistration**                                                                                                                                                                                                   |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Lookback**                   | **ASSUMPTION:** 56 календарных дней до T0; выбрать так, чтобы измерить baseline frequency, margin, app activity и home_store stability.                                                                                       |
| **Loyalty/app**                | Активный loyalty account + установленное/аутентифицированное приложение в lookback. Push permission не обязателен для eligibility; использовать как blocking/diagnostic, иначе ухудшается generalizability.                   |
| **Purchase activity**          | **ASSUMPTION:** минимум 2 qualifying purchase days в 56 дней и \>=1 в последние 28 дней. Финальный порог выбрать на blinded pre-period data и заморозить.                                                                     |
| **Home store**                 | Магазин с максимальным числом qualifying purchase days в lookback; tie-breaker - более поздняя покупка. Stability share threshold - TO_VALIDATE. Outcomes считать по всем заранее in-scope X5 channels, не только home_store. |
| **Exclusions**                 | Employee/test/service accounts; pre-existing hard fraud blocks; deletion/closure request до T0; технически неэкспонируемые accounts; возраст/условия участия - только по решению legal. Все правила pre-treatment.            |
| **Shared accounts/households** | Account остается unit of analysis. Не исключать post hoc. До запуска определить proxy shared-account flag и провести sensitivity, не раскрывая household identity.                                                            |
| **Consent/opt-in**             | После store assignment показать понятные правила, reward settlement, privacy, group visibility, exit и complaint channel. Opt-in добровольный и легко обратимый.                                                              |
| **New users**                  | Пользователи после T0 получают arm по текущему store-policy, но не входят в primary closed cohort. Отдельный entrant cohort - secondary.                                                                                      |
| **Store movers**               | Сохраняют original arm по home_store (ITT). Exposure и purchases in other stores логируются; arm switching запрещен.                                                                                                          |
| **Dvor formation**             | Алгоритм matching, minimum pool, goal calculation, backup rules и copy version фиксируются до randomization. Фактическое формирование после opt-in не меняет ITT denominator.                                                 |

**Методологические источники:** \[S0\] Встроенный проектный пакет пользователя (03.09.2026); [<u>\[S13\] International Council for Harmonisation (2019/2020)</u>](https://www.ema.europa.eu/en/ich-e9-statistical-principles-clinical-trials-scientific-guideline); [<u>\[S19\] Российская Федерация; актуальная консолидированная редакция (ред. от 26.07.2026)</u>](https://www.consultant.ru/document/cons_doc_LAW_61801/96fbc469f91f57235cc842a85e0516a99f23dc85/); [<u>\[S20\] ГИС ЗПП Роспотребнадзора (04.09.2024)</u>](https://zpp.rospotrebnadzor.ru/news/regional/506273)

## 4.1 Recruitment flow
<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Closed cohort flow</strong></p>
<p>All loyalty accounts in candidate stores</p>
<p>-&gt; apply PRE-TREATMENT eligibility and exclusions</p>
<p>-&gt; assign immutable home_store</p>
<p>-&gt; freeze eligible_user_id_hash + covariates</p>
<p>-&gt; randomize stores</p>
<p>-&gt; send arm-specific offer / no offer</p>
<p>-&gt; voluntary opt-in</p>
<p>-&gt; retain everyone in primary ITT denominator</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**Post-treatment selection audit:** нельзя исключать no-show, no-opt-in, group failure, fraud review, group exit, uninstall или отсутствие покупок. Исключение допустимо только при заранее документированной ошибочной eligibility (например, тестовый аккаунт), выявленной слепо к outcome и по одинаковому правилу во всех arms.

# 5. Arms и component control
| **Arm**                            | **Компоненты**                                                                                                                                                                                             | **Контроль смешения**                                                                                                             |
|------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| **A - BAU control**                | Текущая программа лояльности и приложение без новых Dvor/solo screens, Dvor pushes, Dvor rewards и qualified referral rules.                                                                               | Не менять BAU cadence специально для эксперимента. Логировать concurrent campaigns.                                               |
| **B - Solo-parity active control** | Personal challenge; индивидуальный progress/avatar; та же cadence; максимально сопоставимые reward cap, settlement и copy quality; нет group goal, shared progress, peer rescue, group invitation.         | Component parity фиксируется до запуска. Фактическая earned reward может отличаться и является частью механизма.                  |
| **C - Dvor**                       | Все компоненты B + small voluntary same-store group; group target as sum of personal targets; shared progress without public individual contribution; qualified invite; exit and anti-pressure safeguards. | Размер группы, cycle length, backup coefficient, reward multiplier и minimum pool из draft spec - ASSUMPTION, подлежат preflight. |

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Почему bundle test допустим</strong></p>
<p>Для первой бизнес-проверки допустимо спросить, работает ли целостная политика Dvor. Но если arm B исключен ради мощности, отчет обязан прямо сказать: эффект нельзя разложить на UI, reward, challenge и social layer. Любое component attribution потребует следующего дизайна.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 5.1 Component freeze
> **•** Reward cap, qualifying action, cycle length, push cadence, visibility, group exit, referral qualification, fraud pending и refund handling фиксируются в versioned policy manifest.
>
> **•** LLM не рассчитывает target/reward. Детерминированный policy engine создает числа; LLM только формулирует текст в пределах validated slots.
>
> **•** Все промты, rule hashes, model version и content safety filters замораживаются. Изменение после T0 = protocol deviation; emergency safety patch логируется отдельно.

# 6. Метрики: одна primary, один margin guardrail
<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Primary outcome</strong></p>
<p><strong>Рекомендация:</strong> число квалифицированных покупочных дней на pre-eligible user за 42 дня. Это count outcome, использующий всю информацию, менее чувствительный к дроблению одного визита на несколько чеков и не требующий произвольного N. Доля пользователей с &gt;=N покупочными днями остается key secondary.</p></th>
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
<th><p><strong>Primary metric definition</strong></p>
<p>Y_i = sum_{d=1}^{42} I(user i has &gt;=1 qualifying purchase on calendar day d)</p>
<p>qualifying purchase = loyalty-linked, in-scope X5 transaction with positive net sales</p>
<p>remaining valid after cancellation / return maturation</p>
<p>denominator = every T0 eligible user assigned by original home_store</p>
<p>no purchase = 0, not missing</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Role**          | **Metric**                                                             | **Formula**                                                                                                | **Unit/denominator**                                        | **Source/direction**                      | **Returns/zeros/notes**                                                                                        |
|-------------------|------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|-------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| **Primary**       | Qualifying purchase days                                               | sum day-indicators over days 1-42                                                                          | Eligible user; all T0 eligible                              | Receipt/loyalty ledger; direction up      | Full refund removes day only if no other valid purchase remains; partial refund keeps day if positive net sale |
| **Guardrail**     | Net contribution margin                                                | sales - COGS - X5-funded discounts - variable costs - X5 reward economic cost - fraud loss - refund impact | Eligible user; same cohort/window; finalized through day 70 | Finance ledger; direction non-inferior/up | Accrue pending/unredeemed liability using finance-approved rule; subtract supplier funding separately          |
| **Key secondary** | Share \>= N                                                            | I(Y_i \>= N); one frozen N                                                                                 | Eligible user                                               | Derived from primary; up                  | N chosen only from blinded pre-period; N+/-1 sensitivity descriptive                                           |
| **Secondary**     | Valid receipt count and net sales                                      | Count/sum over 42 days                                                                                     | Eligible user                                               | Receipt ledger; contextual                | Deduplicate idempotently; returns/reversals attached to origin                                                 |
| **Secondary**     | Basket and item/category mix                                           | Net sales / valid purchase day; category shares                                                            | Eligible user/day                                           | Item ledger; no directional success rule  | Detect stock-up, cannibalization and harmful category shift                                                    |
| **Diagnostic**    | Offer -\> exposure -\> opt-in -\> formed Dvor -\> active -\> completed | Stage-specific rates with fixed denominators                                                               | Offered eligible users / formed groups                      | App events                                | Never replace ITT denominator with triggered users                                                             |
| **Diagnostic**    | Contamination                                                          | Control users with Dvor exposure/invite; treatment users lacking policy; cross-store exposure              | Eligible user/store                                         | Exposure/referral logs; down              | Report by source and week                                                                                      |
| **Safety**        | Complaints/social harm                                                 | Dvor-attributable complaints per 10,000 eligible; severity                                                 | Eligible users                                              | CRM/moderation; down                      | Independent severity review; no public blame                                                                   |
| **Safety**        | Fraud false positives                                                  | Confirmed legitimate blocked/reversed cases / reviewed legitimate cases; severe count                      | Reviewed cases and per 10,000 eligible                      | Fraud review ledger; down                 | Precision-first; manual review; shadow where possible                                                          |
| **Safety**        | Privacy/security incident                                              | Count by severity                                                                                          | Experiment/system                                           | Incident management                       | Any severe incident triggers immediate pause/stop                                                              |

## 6.1 Formal margin non-inferiority
<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Margin estimand and hypotheses</strong></p>
<p>theta_M = E[CM_i | arm C] - E[CM_i | arm A]</p>
<p>H0: theta_M &lt;= -delta_M</p>
<p>H1: theta_M &gt; -delta_M</p>
<p>PASS NI if lower bound of two-sided 95% CI for theta_M &gt; -delta_M</p>
<p>equivalently: one-sided alpha = 0.025</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

delta_M - максимальная допустимая потеря вкладной маржи на eligible user. Ее утверждают finance и business **до** просмотра pilot outcomes, в рублях на пользователя за 42 дня либо как заранее переведенную абсолютную величину. Нельзя выбирать delta_M из данных пилота.

Формула contribution margin должна быть согласована с X5 Finance: какие скидки уже отражены в net sales, как оценивать экономическую стоимость баллов, breakage, supplier funding, acquiring/fulfilment cost, возвраты и fraud loss. Иначе возникает double counting или искусственная выгода от отложенного reward settlement.

**Методологические источники:** [<u>\[S13\] International Council for Harmonisation (2019/2020)</u>](https://www.ema.europa.eu/en/ich-e9-statistical-principles-clinical-trials-scientific-guideline); [<u>\[S14\] U.S. Food and Drug Administration (2016)</u>](https://www.fda.gov/media/78504/download)

## 6.2 Почему не использовать ROI как primary
ROI - нелинейное отношение с нестабильным знаменателем и сложной интерпретацией при малой/нулевой reward cost. Для решения лучше отдельно оценивать causal purchase effect и causal net contribution margin per eligible user. ROI, incremental margin / X5-funded reward cost и sales-to-reward показывать как economics diagnostics с доверительными интервалами/bootstrapping, но не как единственную success metric.

# 7. Выбор N и окна без подглядывания
| **Шаг**                  | **Правило**                                                                                                                                                                        |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1. Freeze window**     | **ASSUMPTION:** 42 days. Проверить на pre-period, что окно покрывает несколько естественных циклов покупок и не пересекает аномальные праздники/массовые кампании без блокировки.  |
| **2. Define candidates** | До randomization сформировать небольшой набор бизнес-осмысленных N на основе pre-period distribution и привычного purchase cadence. Не использовать treatment outcomes.            |
| **3. Choose one N**      | Выбрать N с понятной бизнес-интерпретацией и не экстремальной control prevalence; решение подписывают product + analytics до outcome access.                                       |
| **4. Freeze status**     | Доля \>=N - key secondary при count primary. Если business требует binary primary, сменить primary **до preregistration**, пересчитать power и отказаться от count как co-primary. |
| **5. Sensitivity**       | N-1 и N+1, 28/42/56-day standardized rates - только sensitivity/descriptive. Не выбирать лучший после факта.                                                                       |

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>ASSUMPTION по срокам</strong></p>
<p>56-day pre-period + 42-day outcome + 28-day maturation - проектный стартовый вариант. Он выбран, чтобы иметь pre-period adjustment, несколько игровых циклов и время на refunds/reward settlement. Это не правило X5 и должно быть проверено на фактическом return-delay curve, seasonality и cadence.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 8. Power, MDE и sample size
<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Главный принцип</strong></p>
<p>В store-cluster RCT мощность определяется прежде всего числом независимых магазинов, ICC, неравномерностью store sizes и ITT-эффектом после dilution из-за take-up. Большое число пользователей внутри нескольких stores не заменяет независимые clusters.</p>
<p><strong>Основание:</strong> <a href="https://pubmed.ncbi.nlm.nih.gov/16943232/"><u>[S8] Eldridge, S. M.; Ashby, D.; Kerry, S., 2006</u></a>; <a href="https://arxiv.org/abs/1601.01981"><u>[S9] Pustejovsky, J. E.; Tipton, E., 2018</u></a></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 8.1 Формулы для первичного приближения
<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Count outcome, equal-size individual approximation</strong></p>
<p>n_ind_per_arm = 2 * (z_(1-alpha/2) + z_(1-beta))^2 * Var(Y) / Delta_ITT^2</p></th>
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
<th><p><strong>Binary outcome</strong></p>
<p>n_ind_per_arm = [z_a*sqrt(2*pbar*(1-pbar)) + z_b*sqrt(p0*(1-p0)+p1*(1-p1))]^2</p>
<p>/ (p1-p0)^2</p></th>
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
<th><p><strong>Unequal cluster-size inflation</strong></p>
<p>DE ~= 1 + ( ((1 + CV_m^2) * m_bar) - 1 ) * ICC</p>
<p>n_cluster_adjusted = n_ind * DE / (1 - individual_attrition)</p>
<p>clusters_per_arm = ceil(n_cluster_adjusted / m_bar)</p></th>
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
<th><p><strong>Take-up dilution</strong></p>
<p>If Delta_participant is a receipt-of-treatment effect and q is take-up:</p>
<p>Delta_ITT ~= q * Delta_participant =&gt; n scales roughly as 1 / q^2</p>
<p>Do not apply this again when the target MDE is already defined on ITT.</p></th>
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
<th><p><strong>Margin NI approximation, true difference planned at 0</strong></p>
<p>n_ind_per_arm = 2 * (z_(1-alpha_NI) + z_(1-beta))^2 * sigma_M^2 / delta_M^2</p>
<p>Use one-sided alpha_NI = 0.025 and then apply cluster inflation.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

CUPED/pre-period adjustment can reduce variance approximately by a factor related to 1-R^2, but final gain must be estimated from the actual pre/post relationship and exact planned model. Do not simply assume a variance reduction.

**Методологические источники:** [<u>\[S8\] Eldridge, S. M.; Ashby, D.; Kerry, S. (2006)</u>](https://pubmed.ncbi.nlm.nih.gov/16943232/); [<u>\[S10\] Deng, A.; Xu, Y.; Kohavi, R.; Walker, T. (2013)</u>](https://dl.acm.org/doi/10.1145/2433396.2433413); [<u>\[S11\] Lin, W. (2013)</u>](https://projecteuclid.org/journals/annals-of-applied-statistics/volume-7/issue-1/Agnostic-notes-on-regression-adjustments-to-experimental-data--Reexamining/10.1214/12-AOAS583.full)

## 8.2 Сценарии count primary: только illustration
| **Scenario**            | **Outcome/take-up assumptions**                                          | **Cluster assumptions**                             | **Design effect** | **Approximate requirement**                                     |
|-------------------------|--------------------------------------------------------------------------|-----------------------------------------------------|-------------------|-----------------------------------------------------------------|
| **Low / optimistic**    | Var(Y)=4.5; participant effect=0.50 day; take-up q=0.60 -\> ITT MDE=0.30 | m=400; CV=0.25; ICC=0.005; attrition=5%; power=80%  | DE=3.12           | n_ind=785; adjusted users=2,578; **formula floor 7 stores/arm** |
| **Base**                | Var(Y)=8.0; participant effect=0.50; q=0.40 -\> ITT MDE=0.20             | m=600; CV=0.50; ICC=0.010; attrition=10%; power=90% | DE=8.49           | n_ind=4,203; adjusted users=39,648; **67 stores/arm**           |
| **High / conservative** | Var(Y)=15.0; participant effect=0.60; q=0.25 -\> ITT MDE=0.15            | m=800; CV=0.75; ICC=0.020; attrition=15%; power=90% | DE=25.98          | n_ind=14,010; adjusted users=428,208; **536 stores/arm**        |

*Все значения в таблице - ASSUMPTION и не являются ожиданием эффекта X5. Low scenario показывает математический floor, а не разрешение запускать trial с 7 stores/arm: при малом числе clusters asymptotic SE ненадежны, и exact randomization simulation может потребовать существенно больше.*

## 8.3 Binary key secondary и margin NI sensitivity
| **Scenario**    | **Assumptions**                | **DE**   | **Approximate requirement**                    |
|-----------------|--------------------------------|----------|------------------------------------------------|
| **Binary low**  | p0=0.30 -\> p1=0.34; power=80% | DE=3.12  | n_ind=2,134; adjusted=7,008; 18 stores/arm     |
| **Binary base** | p0=0.40 -\> p1=0.43; power=90% | DE=8.49  | n_ind=5,667; adjusted=53,456; 90 stores/arm    |
| **Binary high** | p0=0.50 -\> p1=0.52; power=90% | DE=25.98 | n_ind=13,127; adjusted=401,221; 502 stores/arm |

| **Scenario** | **Standardized NI margin**          | **DE**   | **Approximate requirement**                   |
|--------------|-------------------------------------|----------|-----------------------------------------------|
| **NI low**   | delta_M / sigma_M = 0.15; power=80% | DE=3.12  | n_ind=698; adjusted=2,291; 6 stores/arm       |
| **NI base**  | delta_M / sigma_M = 0.10; power=90% | DE=8.49  | n_ind=2,101; adjusted=19,824; 34 stores/arm   |
| **NI high**  | delta_M / sigma_M = 0.05; power=90% | DE=25.98 | n_ind=8,406; adjusted=256,925; 322 stores/arm |

Финальный sample size = максимум требований для primary superiority, margin NI, запланированных confirmatory contrasts и точности safety estimates, с учетом store attrition. Для three-arm equal allocation base count example дает примерно 201 store total; для two-arm - 134. Это illustration, а не рекомендация.

## 8.4 Обязательный финальный power calculation
> **1.** Получить real pre-period store/user distributions, ICC, CV, covariance pre/post, margin variance, take-up proxy и attrition.
>
> **2.** Воспроизводить **точную** blocking/matching/randomization scheme, включая unequal store sizes и multiple arms.
>
> **3.** Многократно randomize historical/resampled data under null и under candidate ITT effects; запускать тот же estimator, CR2/RI и decision gates.
>
> **4.** Проверить type-I error, power primary, power margin NI, CI coverage, cluster loss, contamination и take-up sensitivity.
>
> **5.** Выбрать число stores до randomization; не пересчитывать effect assumptions по unblinded outcomes. Blind variance re-estimation допустима только по заранее описанной процедуре.

**Методологические источники:** [<u>\[S5\] Imai, K.; King, G.; Nall, C. (2009)</u>](https://projecteuclid.org/journals/statistical-science/volume-24/issue-1/The-Essential-Role-of-Pair-Matching-in-Cluster-Randomized-Experiments/10.1214/08-STS274.full); [<u>\[S8\] Eldridge, S. M.; Ashby, D.; Kerry, S. (2006)</u>](https://pubmed.ncbi.nlm.nih.gov/16943232/); [<u>\[S9\] Pustejovsky, J. E.; Tipton, E. (2018)</u>](https://arxiv.org/abs/1601.01981)

# 9. Randomization, concealment и contamination prevention
| **Элемент**                | **Спецификация**                                                                                                                                                                                                                     |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Candidate store freeze** | Список stores, eligible counts, block covariates и exclusions фиксируются до randomization. No replacement after assignment.                                                                                                         |
| **Blocking/matching**      | Region, format, eligible volume, baseline primary, baseline CM, app engagement, promo intensity/seasonality. Pair matching допустим, если pairs действительно сопоставимы и анализ сохраняет pair structure.                         |
| **Assignment**             | Reproducible RNG/cryptographic hash from experiment_id \| store_id \| secret_salt; seed/salt escrowed; code committed. Для constrained randomization хранить полный допустимый allocation set и выбранный draw.                      |
| **Allocation concealment** | Product/ops не видят allocation до freeze cohort/config; analysts без outcome access готовят code. Immutable assignment table.                                                                                                       |
| **User arm**               | Original pre-period home_store -\> store arm. Arm не меняется при visit migration, app reinstall, Dvor exit или new device.                                                                                                          |
| **Invitations**            | В первом PoC разрешать qualified Dvor invites только внутри того же eligible store/arm; cross-arm invite блокируется нейтральной copy и логируется. Иначе primary contrast contaminated.                                             |
| **New users**              | Policy по current store arm, но отдельный secondary entrant cohort; не добавлять в closed primary denominator.                                                                                                                       |
| **Concurrent campaigns**   | Freeze/exclude or balance major store promotions; log campaign exposure. Emergency operations documented as deviations.                                                                                                              |
| **SRM**                    | Проверять store counts against exact scheme. User-level 1:1/1:1:1 binomial SRM **невалиден** при unequal store sizes; использовать randomization distribution conditional on frozen store sizes. Отдельно проверять exposure funnel. |

**Методологические источники:** [<u>\[S5\] Imai, K.; King, G.; Nall, C. (2009)</u>](https://projecteuclid.org/journals/statistical-science/volume-24/issue-1/The-Essential-Role-of-Pair-Matching-in-Cluster-Randomized-Experiments/10.1214/08-STS274.full); [<u>\[S6\] Campbell, M. K. et al. (2012)</u>](https://www.bmj.com/content/345/bmj.e5661); [<u>\[S12\] Fabijan, A. et al. (2019)</u>](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/)

## 9.1 Contamination map
| **Path**                          | **Measure**                                  | **Handling**                                           |
|-----------------------------------|----------------------------------------------|--------------------------------------------------------|
| **Control received Dvor UI/push** | wrong-arm exposure rate                      | Immediate incident; pause if systematic                |
| **Treatment not exposed**         | non-exposure among assigned; reasons         | Retain in ITT; product funnel diagnostic               |
| **Cross-store user**              | share of outcome activity outside home_store | Count outcomes across in-scope X5; retain original arm |
| **Cross-arm referral**            | invite/accept/qualified events crossing arms | Block for PoC; report attempted contamination          |
| **Multiple Dvors / switching**    | membership count and switches                | One experiment Dvor at a time; no arm switch           |
| **External social exposure**      | survey/complaint/proxy only                  | Limitation; assess geography/network sensitivity       |

# 10. Statistical Analysis Plan
## 10.1 Primary ITT model
<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Primary ANCOVA / OLS estimand</strong></p>
<p>Y_i = alpha + beta_C * I(C) + beta_B * I(B) + block_FE</p>
<p>+ gamma * centered_preY_i + treatment x centered_preY_i</p>
<p>+ prespecified covariates/interactions + error_i</p>
<p>Primary estimate = beta_C for C vs A (or corresponding contrast)</p>
<p>Uncertainty clustered at randomized store; analysis honors pairs/blocks.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

OLS/ANCOVA on a bounded count is selected for a transparent **absolute mean difference** and randomization-based interpretation. Pre-period adjustment uses only frozen covariates. Poisson/negative-binomial marginal standardized rate ratio is a robustness analysis, not a replacement primary model.

При малом числе stores использовать randomization inference respecting blocks/pairs, CR2 bias-reduced cluster-robust variance with Satterthwaite degrees of freedom и cluster-level sensitivity. Обычный asymptotic cluster-robust Wald test без small-sample adjustment не является достаточным.

**Методологические источники:** [<u>\[S5\] Imai, K.; King, G.; Nall, C. (2009)</u>](https://projecteuclid.org/journals/statistical-science/volume-24/issue-1/The-Essential-Role-of-Pair-Matching-in-Cluster-Randomized-Experiments/10.1214/08-STS274.full); [<u>\[S9\] Pustejovsky, J. E.; Tipton, E. (2018)</u>](https://arxiv.org/abs/1601.01981); [<u>\[S10\] Deng, A.; Xu, Y.; Kohavi, R.; Walker, T. (2013)</u>](https://dl.acm.org/doi/10.1145/2433396.2433413); [<u>\[S11\] Lin, W. (2013)</u>](https://projecteuclid.org/journals/annals-of-applied-statistics/volume-7/issue-1/Agnostic-notes-on-regression-adjustments-to-experimental-data--Reexamining/10.1214/12-AOAS583.full)

## 10.2 Margin model and joint inference
Аналогичный adjusted model применяется к finalized CM_i. Report: mean difference, 95% CI, lower bound relative to -delta_M, raw means, cluster-level distributions and sensitivity to finance accounting. Success requires both primary superiority and margin NI; neither compensирует провал другого.

## 10.3 Missing data, refunds, outliers и intercurrent events
| **Issue**                            | **Primary handling**                                                                                                                                                                               |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **No purchase**                      | Y_i=0 and purchase margin=0; user remains in denominator.                                                                                                                                          |
| **App telemetry missing**            | Не влияет на receipt-based primary if transaction ledger complete; exposure diagnostics marked missing. Source outage may trigger pause.                                                           |
| **Account deletion / legal erasure** | Privacy obligation prevails. Do not exclude. Report differential rate; perform bounds/tipping-point sensitivity on unavailable outcomes under pre-approved lawful retention policy.                |
| **Full refund**                      | Attach to originating transaction. After maturation, remove qualifying day only when no valid positive-net transaction remains that day; reverse margin/reward.                                    |
| **Partial refund**                   | Update net sales, COGS, margin and reward; purchase day remains if positive net transaction persists.                                                                                              |
| **Late refund beyond day 70**        | Primary uses pre-specified maturation cutoff plus provision/expected-loss sensitivity from historical delay curve.                                                                                 |
| **Delayed reward**                   | Accrue economic liability for earned pending/unredeemed rewards; do not make margin appear better by delaying settlement.                                                                          |
| **Margin outliers**                  | No post-hoc deletion. Primary raw accounting; pre-specified winsorized/Huber/cluster-level sensitivity. Negative margins retained.                                                                 |
| **Fraud**                            | Confirmed fraud loss and reward reversals remain in business estimand. Fraud-screened “clean user” analysis is supplementary only.                                                                 |
| **Store closure/outage**             | No replacement after randomization. Retain cluster when outcomes available; document operational exposure. Supplementary open-day analysis and matched-pair sensitivity, not primary redefinition. |

## 10.4 Multiplicity and heterogeneity
> **• One primary outcome, one primary contrast.** No co-primary frequency/share\>=N pair.
>
> **•** C vs B and B vs A: fixed gatekeeping after C vs A or Dunnett/Holm familywise control. Exact plan frozen before outcome access.
>
> **•** Secondary outcomes: effect estimates and CIs; label confirmatory only where multiplicity controlled.
>
> **•** Heterogeneity is exploratory unless separately powered: baseline frequency, store format, region, prior app engagement, lawful age bands/accessibility. Report interaction estimates/CIs, not subgroup p-value fishing.
>
> **•** No causal statements from small cells; suppress/recombine cells under privacy thresholds.

**Методологические источники:** [<u>\[S16\] Holm, S. (1979)</u>](https://www.jstor.org/stable/4615733); [<u>\[S17\] Dunnett, C. W. (1955)</u>](https://www.tandfonline.com/doi/abs/10.1080/01621459.1955.10501294)

## 10.5 Robustness checks
| **Dimension**     | **Check**                                                                                                        |
|-------------------|------------------------------------------------------------------------------------------------------------------|
| **Estimator**     | Unadjusted difference; adjusted OLS; cluster-level means; count GLM standardized contrast                        |
| **Inference**     | CR2/Satterthwaite; block-respecting randomization inference; wild cluster bootstrap if validated                 |
| **Weights**       | User-weighted primary; store-weighted supplementary to diagnose size-effect relationship                         |
| **Window**        | 42-day primary; 28/56-day standardized diagnostic only                                                           |
| **Contamination** | As-assigned primary; exclude high-contamination stores only in labeled sensitivity; exposure mapping sensitivity |
| **Finance**       | Accrual vs realized reward cost; alternative return provision; supplier-funded and X5-funded split               |
| **Missing**       | Bounds/tipping point for legal deletion/source loss; no complete-case convenience analysis                       |

# 11. Instrumentation и reconciliation
Event model должен позволять восстановить causal chain **assignment -\> offer -\> exposure -\> action -\> purchase -\> margin -\> reward -\> fraud/refund -\> complaint/opt-out**. Primary outcome строится из transaction/finance ledgers, а не только из app events.

| **Domain**     | **Required events/fields**                                                                                                |
|----------------|---------------------------------------------------------------------------------------------------------------------------|
| **Experiment** | experiment_definition, eligibility_snapshot, home_store_assignment, cluster_randomization, arm_assignment, policy_version |
| **Exposure**   | offer_created, impression, screen_open, push_sent/delivered/opened, opt_in, opt_out                                       |
| **Dvor**       | yard_create/join/leave, membership_state, group_progress, goal_recalculation, peer_backup, cycle_complete/fail            |
| **Challenge**  | challenge_offer/accept/progress/complete, target/reward slots, model/rule version, safety flags                           |
| **Referral**   | invite_created/sent/accepted, invitee_eligible, qualified_purchase, referral_reward_pending/settled/reversed              |
| **Commerce**   | receipt, item, payment, cancel, return, refund, net_sales, COGS_proxy/actual, store/channel                               |
| **Reward**     | reward_reserved, pending, settled, redeemed, expired, reversed, funded_by, economic_cost                                  |
| **Fraud**      | score, rule hits, version, review, final label, block/release, false_positive_severity, fraud_loss                        |
| **Safety**     | complaint, social_harm, prohibited_content, privacy_incident, security_incident, uninstall/deletion_request               |

## 11.1 Common fields
event_id, idempotency key, hashed account/user id, store_id, yard_id, experiment_id, arm, assignment timestamp, event timestamp UTC + local timezone, source system, schema version, app/policy/model version, amount/currency, reason code, original event reference, ingestion timestamp.

## 11.2 Daily and final reconciliation
| **Layer**                | **Gate**                                                                                                                            |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| **Assignment integrity** | Every eligible hash has one immutable arm; every store belongs to one arm; no post-T0 reassignment.                                 |
| **Exposure**             | Assigned C/B eligible -\> expected policy availability; control -\> zero Dvor availability. Investigate gaps by app version/device. |
| **Commerce**             | Receipt header = sum(items/payments/discounts); duplicate and orphan checks; store calendar completeness.                           |
| **Finance**              | Net sales/COGS/discount/variable cost/reward/funding/refund components reconcile to finance ledger.                                 |
| **Reward**               | Earned -\> pending -\> settled/reversed/expired states balance; no negative/duplicate liability; supplier funding documented.       |
| **Fraud**                | Every block/reversal has score/rule/version/review trail; gold-label sample for precision/FP estimation.                            |
| **Safety**               | CRM/moderation incidents link to experiment where lawful; severity adjudication blinded to outcome when feasible.                   |

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>SRM nuance for clusters</strong></p>
<p>At user level, equal arm proportions are not expected when stores have unequal eligible counts. The correct SRM check compares observed allocation with the exact cluster randomization distribution conditional on frozen store sizes; naive binomial testing can misdiagnose a healthy cluster trial.</p>
<p><strong>Основание:</strong> <a href="https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/"><u>[S12] Fabijan, A. et al., 2019</u></a></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 12. Preflight и launch gate
| **Gate**                  | **Pass condition**                                                                                                                                                                                                                       |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Offline AI acceptance** | 30-50 synthetic profiles; one frozen challenge/profile; blinded rubric; \>=70% point hit rate per case requirement; Wilson/exact CI and inter-rater agreement reported; **zero critical harmful/prohibited challenge**. Не заменяет RCT. |
| **Rubric**                | Fit to purchase history; achievable target; no invented numeric basis; no prohibited/harmful category; clear copy; reward within deterministic policy; no sensitive-trait inference.                                                     |
| **Economics stress**      | Low/base/high for incremental visits, margin, redemption/breakage, refund, fraud, supplier funding, cannibalization. Fail if any plausible base path is structurally loss-making without explicit risk acceptance.                       |
| **Fraud validation**      | Synthetic/known fraud patterns + shadow production sample; precision-first threshold; manual review; severe false-positive cap and rollback. XP can be immediate; monetary reward pending.                                               |
| **A/A**                   | Full assignment/logging/analysis pipeline with identical policy; historical re-randomization and live dry run; nominal false-positive behavior, no unexplained imbalance/SRM.                                                            |
| **Data quality**          | Event completeness, deduplication, timestamps, app version coverage, ledger reconciliation, return linkage and reward state machine pass pre-agreed thresholds.                                                                          |
| **Privacy/security**      | Data inventory, purpose/minimization, access, retention/deletion, threat model, incident response, no public individual contribution/name/address/exact geo.                                                                             |
| **Consumer terms**        | Rules available before opt-in: qualification, reward pending/reversal, cycle, exit, complaint and changes; copy avoids coercion/nagging/shame.                                                                                           |
| **Dry run/rollback**      | End-to-end test in shadow/canary stores; kill switch at policy/store/version; preserve assignment and audit logs.                                                                                                                        |

**Методологические источники:** \[S0\] Встроенный проектный пакет пользователя (03.09.2026); [<u>\[S19\] Российская Федерация; актуальная консолидированная редакция (ред. от 26.07.2026)</u>](https://www.consultant.ru/document/cons_doc_LAW_61801/96fbc469f91f57235cc842a85e0516a99f23dc85/); [<u>\[S20\] ГИС ЗПП Роспотребнадзора (04.09.2024)</u>](https://zpp.rospotrebnadzor.ru/news/regional/506273); [<u>\[S21\] OECD (2022)</u>](https://www.oecd.org/en/publications/dark-commercial-patterns_44f5e846-en.html); [<u>\[S22\] National Institute of Standards and Technology (AI RMF 1.0; страница актуальна в 2026)</u>](https://airc.nist.gov/)

## 12.1 Launch decision
<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>LAUNCH only if all gates are green</strong></p>
<p>AI hit-rate criterion, critical content safety, economics stress, fraud false-positive control, A/A/SRM/reconciliation, privacy/security/consumer terms review, budget owner and exact stop-loss thresholds must all be signed off. Any red gate blocks launch even if another dimension looks strong.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 13. Monitoring, peeking и stop rules
<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Preferred monitoring regime</strong></p>
<p>Fixed-horizon confirmatory analysis. Continuously monitor only safety, privacy, technical integrity, budget and data quality. Do not watch primary p-values weekly. If one interim is operationally required, pre-specify information time, alpha-spending and nonbinding futility before launch.</p>
<p><strong>Основание:</strong> <a href="https://academic.oup.com/biomet/article-abstract/70/3/659/247777"><u>[S15] Lan, K. K. G.; DeMets, D. L., 1983</u></a></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Rule**                       | **Operational specification**                                                                                                                                                                                                     |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Immediate pause/stop**       | Severe privacy/security incident; wrong-arm policy exposure at scale; prohibited/harmful challenge with material exposure; public disclosure of individual contribution; uncontrolled reward overissue; severe social-harm event. |
| **Financial stop-loss**        | Cumulative X5-funded reward liability + fraud loss - reversals exceeds pre-approved budget boundary; or conservative projected CM harm crosses pre-approved red line. Exact ruble thresholds - TO_VALIDATE and frozen.            |
| **Margin harm**                | Safety board may stop for clear harm using a conservative pre-specified boundary. Final NI claim still uses planned inference; early “not significant” is not safety.                                                             |
| **Technical pause**            | Assignment corruption, source outage, ledger mismatch, app crash, stale policy/version mismatch. Pause exposure; do not declare scientific futility.                                                                              |
| **Complaints/social pressure** | Severity-weighted complaint rate or cluster of incidents crosses baseline-relative boundary; immediate review of copy, group visibility and exit flow.                                                                            |
| **Fraud false positives**      | Severe legitimate block/reward reversal exceeds cap; switch to shadow/manual review or pause monetary settlement.                                                                                                                 |
| **Efficacy interim**           | None by default. Optional one look at ~50% **cluster-level information** with Lan-DeMets/O’Brien-Fleming-like spending; independent unblinded reviewer; product team remains blinded.                                             |
| **Futility**                   | Nonbinding only, based on predictive/conditional power under pre-specified assumptions; never stop merely because early p\>0.05.                                                                                                  |

## 13.1 Sequential design details if interim is used
> **•** Define information fraction from independent clusters and matured outcomes, not raw event volume.
>
> **•** Allocate alpha separately for primary superiority; margin NI and safety boundaries must also be specified. Additional looks are forbidden.
>
> **•** Use an independent monitoring group with access only to coded arms until action is required.
>
> **•** Document every pause, restart and protocol deviation; calendar time continues unless rules explicitly define otherwise.

# 14. Decision matrix: go \| iterate and retest \| stop
| **Decision**           | **Primary evidence**                                                                                                                               | **Margin**                                                                        | **Safety/quality**                                                                    | **Action**                                                                      |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| **GO**                 | Primary C-A: lower 95% CI \> 0 and point estimate reaches pre-frozen business minimum Delta_business (or stricter lower-bound criterion if chosen) | Margin lower 95% CI \> -delta_M                                                   | All safety/data/contamination gates pass; budget within limit                         | Scale only through randomized expansion with persistent holdout                 |
| **ITERATE AND RETEST** | Effect direction promising but CI includes 0/Delta_business; or C-A works but C-B does not; or take-up/funnel low                                  | NI passes and no material harm                                                    | Issues remediable; no severe privacy/social incident                                  | Change one bounded component, update protocol, run new test. Do not call it GO. |
| **STOP**               | Adequately powered result rules out business-relevant effect, shows harm, or no stable effect after retest                                         | NI fails, projected/observed stop-loss, or reward economics structurally negative | Severe privacy/security/social harm; uncontrolled contamination/instrumentation/fraud | Do not roll out. Archive learnings and kill/replace concept.                    |

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Interpretation of arm B</strong></p>
<p>If B vs A works but C vs B does not, the evidence supports the solo layer, not the social layer. Ship/iterate solo only; do not roll out Dvor for storytelling reasons. If C vs A works and C vs B adds value while margin/safety pass, Dvor earns a scale test.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 15. Rollout: shadow -\> limited pilot -\> expansion
| **Stage**                         | **Requirement**                                                                                                                                                       |
|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **0. Shadow**                     | No user-visible Dvor and no monetary reward. Generate challenges/groups/logs; validate relevance, economics, privacy, fraud and instrumentation.                      |
| **1. Canary**                     | Very small operational canary outside confirmatory sample or before T0; test kill switch, copy, pending/reversal, complaint routing. No causal claims.                |
| **2. Limited confirmatory pilot** | Three-arm or two-arm store-cluster RCT; 42-day primary + 28-day closeout; fixed cohort and policy version.                                                            |
| **3. Randomized expansion**       | Add stores by randomized waves; preserve a long-term holdout sized by separate power calculation; keep same assignment history.                                       |
| **4. Long-term follow-up**        | Weekly effect trajectory, novelty decay, 8-12 week retention/margin, complaints, fraud, group survival. Long-term outcomes secondary unless separately preregistered. |
| **5. Rollback**                   | Store/arm/policy-version kill switch; stop new offers; settle/reverse rewards according to rules; preserve audit trail and user communication.                        |

Novelty decay: report week-specific effects descriptively and pre-specify a trend interaction as exploratory. Do not redefine the primary window after seeing a strong first-week spike.

# 16. Privacy, fairness и consumer safety reporting
<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Legal scope</strong></p>
<p>Этот раздел - продуктово-аналитический контрольный план, не юридическое заключение. 152-ФЗ требует законной/справедливой обработки, конкретных целей, соответствия объема данных целям, минимизации и ограниченного хранения. Финальные lawful basis, consent wording, localization, retention и user rights утверждает X5 Legal/Privacy.</p>
<p><strong>Основание:</strong> <a href="https://www.consultant.ru/document/cons_doc_LAW_61801/96fbc469f91f57235cc842a85e0516a99f23dc85/"><u>[S19] Российская Федерация; актуальная консолидированная редакция, ред. от 26.07.2026</u></a></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Area**                | **Rule**                                                                                                                                                                                                         |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Identity/visibility** | Nickname/avatar; no full name, address, exact geotrack or public individual contribution. Shared group progress only.                                                                                            |
| **Location**            | Use internal store_id for assignment/access-controlled operations; do not expose exact residence or infer neighborhood identity.                                                                                 |
| **Data minimization**   | Only fields needed for eligibility, assignment, outcomes, fraud and safety; retention schedule; role-based access; hashed experiment IDs.                                                                        |
| **Opt-in/exit**         | Clear voluntary opt-in, equally visible exit, no penalty/shaming, no pre-checked social sharing, no nagging cadence.                                                                                             |
| **Challenge safety**    | Block alcohol, tobacco/nicotine, gambling, harmful/compulsive purchase patterns and sensitive-trait inference. Avoid “buy more than normal to save the group” framing.                                           |
| **Fairness slices**     | When lawfully available and sufficiently powered: region, settlement type, store format, baseline frequency, app/accessibility, prior digital engagement, broad age bands. Pre-specify and suppress small cells. |
| **Fairness metrics**    | Exposure, take-up, completion, reward, fraud review/false positive, complaints, opt-out and effect estimates by slice.                                                                                           |
| **Interpretation**      | No causal claims from underpowered subgroups; no claim that pilot sample represents Russia. National demographics are not X5 customer weights.                                                                   |

**Методологические источники:** \[S0\] Встроенный проектный пакет пользователя (03.09.2026); [<u>\[S19\] Российская Федерация; актуальная консолидированная редакция (ред. от 26.07.2026)</u>](https://www.consultant.ru/document/cons_doc_LAW_61801/96fbc469f91f57235cc842a85e0516a99f23dc85/); [<u>\[S20\] ГИС ЗПП Роспотребнадзора (04.09.2024)</u>](https://zpp.rospotrebnadzor.ru/news/regional/506273); [<u>\[S21\] OECD (2022)</u>](https://www.oecd.org/en/publications/dark-commercial-patterns_44f5e846-en.html)

## 16.1 Demography and simulation
Official demographic priors can make a **synthetic scenario population** plausible, but they do not identify X5 app users, eligible customers or pilot-store traffic. The real pilot reports the observed eligible population and, if intentionally oversampled, separate segment and reweighted estimates using actual sampling probabilities. Do not use Russia-wide weights to “correct” an unknown X5 customer mix.

# 17. Риски «Двора»: measurement и mitigation
| **Risk**                       | **Failure mode**                                  | **Measure**                                                               | **Mitigation**                                                                         |
|--------------------------------|---------------------------------------------------|---------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| **Interference beyond store**  | Cross-store users, external friends               | Cross-store purchase share; attempted cross-arm invites; exposure proxies | Home_store assignment; in-scope outcomes across X5; invitation constraint; sensitivity |
| **Free-riding/social loafing** | Few members carry group                           | Contribution concentration/Gini; peer-backup share; inactive members      | Private contribution, bounded backup, goal recalculation, no blame copy                |
| **Group failure**              | Repeated failure causes churn/frustration         | Cycle failure, group exit, app opt-out, complaints                        | Achievability calibration, soft reset/exit, no sunk-cost pressure                      |
| **Matching harm/privacy**      | Re-identification or uncomfortable grouping       | Pool size, uniqueness risk, complaint/decline reason                      | No address; minimum pool chosen by privacy review; pseudonyms; opt-in                  |
| **Invite abuse**               | Fake accounts/rings/empty users                   | Qualified conversion, graph rules, fraud precision/loss                   | Reward only after qualifying behavior; pending settlement; manual review               |
| **Multiple stores/Dvors**      | Arm switching and network overlap                 | Home-store stability, membership switches, exposure graph                 | Immutable arm; one experiment Dvor; log migrations                                     |
| **Shared accounts**            | Household behavior attributed to one user         | Pre-period shared-account proxy; device/payment patterns                  | Account-level estimand; sensitivity; no household identity inference                   |
| **Social pressure**            | Shame, nagging, harmful extra trips               | Complaints, opt-out, copy flags, late-cycle activity spikes               | No public deficit attribution; easy exit; cadence cap; safety stop                     |
| **Harmful consumption**        | Challenge steers prohibited/compulsive categories | Prohibited-content rate; item mix; expert review                          | Deterministic category blocklist/policy; zero-tolerance critical gate                  |
| **Reward economics**           | Cannibalization and delayed liability             | Incremental CM, accrued/realized reward, supplier funding                 | Formal margin NI; reward caps; funding ledger; no “savings” proxy                      |
| **Fraud false positives**      | Legitimate users blocked                          | Precision, severe FP, complaints, manual overturn                         | Shadow first; precision-first; pending rather than hard deny; rollback                 |
| **Novelty decay**              | Early spike vanishes                              | Week effects, post-window retention/margin                                | Long-term randomized holdout; no launch on week-1 alone                                |

# 18. Что запросить у X5 для окончательного расчета
<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Минимизация данных</strong></p>
<p>Для первичного power calculation достаточно store-level aggregates и cross-products; для окончательной exact simulation предпочтителен pseudonymized user panel внутри защищенной среды X5, без экспорта ФИО, адресов, контактов и точных геотреков.</p>
<p><strong>Основание:</strong> <a href="https://www.consultant.ru/document/cons_doc_LAW_61801/96fbc469f91f57235cc842a85e0516a99f23dc85/"><u>[S19] Российская Федерация; актуальная консолидированная редакция, ред. от 26.07.2026</u></a></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Request**                | **Minimum aggregate/schema**                                                                                                                                   |
|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Store universe**         | Candidate store_id (pseudonymous), region/format, open days, eligible n; distribution mean/SD/CV/min/max; expected closures.                                   |
| **Primary baseline**       | Per store: n, sum(Y_pre), sum(Y_pre^2), zero count, quantiles; weekly series; between/within-store variance and ICC.                                           |
| **Margin baseline**        | Per store/user aggregate: n, sum(CM_pre), sum(CM_pre^2), quantiles/negative share, ICC; finance-approved component dictionary.                                 |
| **Pre/post covariance**    | Historical adjacent-window cross-products for Y and CM (sum pre, sum post, sum pre^2, sum post^2, sum pre\*post) to estimate CUPED gain.                       |
| **Cluster sizes**          | Eligible user count by store under candidate eligibility thresholds; sensitivity grid; CV and tail.                                                            |
| **Take-up proxies**        | Historical app offer impression/open/opt-in/completion by store and baseline activity; push/app-version coverage.                                              |
| **Mobility/contamination** | Home-store share distribution; aggregated store-to-store transition matrix; multi-store user rate; referral geography/network overlap proxy.                   |
| **Returns**                | Return/cancel delay curve by category/channel; partial/full return rates; reward reversal timing.                                                              |
| **Rewards**                | Issued/pending/settled/redeemed/expired/reversed states; economic cost, breakage method, supplier reimbursements, tax/accounting treatment.                    |
| **Fraud**                  | Baseline confirmed fraud loss, review volume, precision/false-positive sample, appeal/overturn rates; no raw sensitive device data outside secure environment. |
| **Complaints/safety**      | Baseline complaint/opt-out/deletion rates and severity taxonomy; app crash/uninstall baseline if available.                                                    |
| **Campaign calendar**      | Store/region promotions, assortment changes, price campaigns, holidays, closures and concurrent product tests.                                                 |
| **Schemas/quality**        | Receipt/item/event/reward/fraud/CRM schema, source ownership, latency, completeness, duplicate/orphan rates, reconciliation rules.                             |

## 18.1 Owners and freeze dates
| **Owner**                     | **Decision/data**                                                               |
|-------------------------------|---------------------------------------------------------------------------------|
| **Analytics/Experimentation** | Eligibility, ICC/CV, power simulation, randomization, SAP, SRM/A/A              |
| **Finance**                   | CM formula, delta_M, reward economic cost, supplier funding, stop-loss          |
| **Product/Growth**            | Arms, component parity, Delta_business, cadence, take-up funnel                 |
| **Engineering/Data**          | Assignment service, event schemas, reconciliation, kill switch, versioning      |
| **Fraud/Risk**                | Pending rules, review, gold labels, severe FP threshold, fraud loss             |
| **Legal/Privacy/Consumer**    | Opt-in/terms, lawful basis, minimization, retention, rights, complaint handling |
| **Operations**                | Store universe, closures, concurrent campaigns, rollout feasibility             |

# 19. Preregistration checklist
> **1.** Protocol title, version, timestamp, decision owner, analysis owner and immutable repository hash.
>
> **2.** Scientific/business question and explicit falsification conditions for Dvor.
>
> **3.** Target population, 56-day lookback, closed cohort, eligibility/exclusions, home_store rule.
>
> **4.** Arms A/B/C and exact component manifest; control of reward/UI/cadence differences.
>
> **5.** Randomization unit, store list, block/pair variables, allocation ratio, seed/salt/constrained set and concealment.
>
> **6.** Interference assumption, exposure mapping, invitation constraints and contamination metrics.
>
> **7.** Primary outcome formula, unit, denominator, data source, 42-day window and maturation cutoff.
>
> **8.** Single N and status of share\>=N; no second primary.
>
> **9.** Contribution margin component dictionary, delta_M, accrual policy and supplier-funding treatment.
>
> **10.** Primary and margin estimands, intercurrent-event strategies and summary measures.
>
> **11.** MDE/Delta_business, alpha, power, ICC, cluster size/CV, take-up, attrition and simulation code.
>
> **12.** Primary model, covariates, interactions, pair/block handling, CR2/RI and CI construction.
>
> **13.** Missing/deletion, refunds, late returns, delayed rewards, fraud, store closure and outlier rules.
>
> **14.** Multiplicity/gatekeeping for C-A, C-B, B-A; secondary and heterogeneity status.
>
> **15.** A/A, SRM/randomization-distribution checks, balance, event completeness and reconciliation thresholds.
>
> **16.** AI offline hit-rate rubric, reviewers, critical safety rules and exact pass criterion.
>
> **17.** Fraud shadow/manual review, severe false-positive threshold and reward pending behavior.
>
> **18.** Privacy/security/consumer terms, data inventory, retention, access and incident response sign-off.
>
> **19.** Safety metrics, financial stop-loss, technical pause, complaint/social-harm and privacy stop rules.
>
> **20.** Any interim analysis: information time, alpha spending, monitoring group and futility rule; otherwise explicit no-peeking.
>
> **21.** Joint GO/ITERATE/STOP matrix, including action when solo works but Dvor increment does not.
>
> **22.** Rollout/rollback, persistent holdout and novelty-decay follow-up.
>
> **23.** Protocol deviation taxonomy; emergency safety patch procedure; analysis blind and data freeze.
>
> **24.** Final reporting template: CONSORT-style flow at store and user levels, effect estimates/CIs, harms, deviations and limitations.

**Методологические источники:** [<u>\[S6\] Campbell, M. K. et al. (2012)</u>](https://www.bmj.com/content/345/bmj.e5661); [<u>\[S7\] Hopewell, S. et al. (2025)</u>](https://www.bmj.com/content/389/bmj-2024-081123); [<u>\[S13\] International Council for Harmonisation (2019/2020)</u>](https://www.ema.europa.eu/en/ich-e9-statistical-principles-clinical-trials-scientific-guideline)

# 20. Методологическая самопроверка и ограничения
| **Risk**                     | **Resolution**                                                                                                                       | **Status**         |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|--------------------|
| **Post-treatment selection** | Исправлено: closed pre-eligible cohort; opt-in/group membership не меняют denominator.                                               | PASS               |
| **Contamination**            | Store assignment, invitation constraint, home_store freeze и explicit metrics. Cross-store social exposure полностью не исключается. | PASS + limitation  |
| **Peeking**                  | Fixed horizon; optional one interim only with alpha spending.                                                                        | PASS               |
| **Multiple primary metrics** | Одна primary count metric; share\>=N secondary.                                                                                      | PASS               |
| **Unit of analysis**         | Assignment/store uncertainty honored; user-level outcomes with store-cluster inference.                                              | PASS               |
| **ICC/unequal sizes**        | DE/CV scenarios + exact randomization simulation requested.                                                                          | PASS               |
| **Take-up/attrition**        | ITT dilution included; no joiner-only primary; closed cohort and sensitivity.                                                        | PASS               |
| **Margin harm**              | Formal NI with prespecified delta_M and CI; reward/fraud/refunds included.                                                           | PASS               |
| **Direct/spillover claims**  | Primary store RCT estimates overall policy effect, not separate spillover. Saturation design reserved for follow-up.                 | PASS               |
| **AI hit rate**              | Explicitly separate offline acceptance, not proof of purchase uplift.                                                                | PASS               |
| **Demographic validity**     | No Russia-demography substitution for X5 customers.                                                                                  | PASS               |
| **Legal certainty**          | No legal conclusion; final review required.                                                                                          | OPEN / TO_VALIDATE |

## 20.1 Material limitations
> **•** Final sample size cannot be stated without X5 baseline variance, ICC, store-size distribution, pre/post correlation, take-up and delta_M. The scenario table is deliberately broad.
>
> **•** Store-level partial interference may fail because users shop across stores and invite external contacts. The pilot reduces and measures this risk but cannot prove zero cross-cluster influence.
>
> **•** A three-arm design can isolate the social increment only to the extent that personal challenge, cadence, UI and reward opportunity are truly comparable; actual earned reward remains a mediator.
>
> **•** Voluntary opt-in dilutes ITT. CACE/TOT estimates are supplementary and especially assumption-sensitive under interference.
>
> **•** Six weeks may be insufficient for durable habit formation or novelty decay; long-term holdout is needed before full rollout.
>
> **•** Finance accounting and legal/privacy obligations require internal X5 decisions; external methodological sources do not replace them.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Final recommendation</strong></p>
<p>Proceed to preregistration only after X5 supplies the minimum aggregates and Finance approves delta_M. The causal default is a store-cluster ITT trial, not a joiner analysis. If the store count cannot support the primary and margin questions, simplify the number of arms or the product concept rather than lowering evidentiary standards.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 21. Источники и ограничения применимости
*Приоритет: original research, official guidance/law and official consumer-protection sources. Медицинские trial standards используются как общая статистическая методология; они не являются обязательным правовым режимом retail-эксперимента. Доступ к источникам проверен 04.09.2026.*

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S0</strong></th>
<th><p><strong>Встроенный проектный пакет пользователя.</strong> Временный пакет GPT Pro: План реального пилота. 03.09.2026.</p>
<p><em>Главный промт и встроенные материалы проекта X5. Проектные числа коллеги не считаются подтвержденными фактами.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S1</strong></th>
<th><p><strong>Hudgens, M. G.; Halloran, M. E..</strong> Toward Causal Inference With Interference. 2008. <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC2600548/"><u>Открыть источник</u></a></p>
<p><em>Формализует direct, indirect/spillover, total и overall effects при partial interference и двухступенчатой рандомизации.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S2</strong></th>
<th><p><strong>Baird, S.; Bohren, J. A.; McIntosh, C.; Özler, B..</strong> Optimal Design of Experiments in the Presence of Interference. 2018. <a href="https://openknowledge.worldbank.org/bitstreams/c12c79f1-5fcd-51e7-a6f7-fc908f506846/download"><u>Открыть источник</u></a></p>
<p><em>Randomized saturation design: сначала насыщенность кластера, затем индивидуальное назначение.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S3</strong></th>
<th><p><strong>Aronow, P. M.; Samii, C..</strong> Estimating Average Causal Effects Under General Interference. 2017. <a href="https://projecteuclid.org/journals/annals-of-applied-statistics/volume-11/issue-4/Estimating-average-causal-effects-under-general-interference-with-application-to/10.1214/16-AOAS1005.full"><u>Открыть источник</u></a></p>
<p><em>Связывает design, exposure mapping и estimands при интерференции.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S4</strong></th>
<th><p><strong>Imai, K.; Jiang, Z.; Malani, A..</strong> Causal Inference With Interference and Noncompliance in Two-Stage Randomized Experiments. 2021. <a href="https://imai.fas.harvard.edu/research/spillover.html"><u>Открыть источник</u></a></p>
<p><em>Complier direct/spillover effects требуют дополнительных идентифицирующих допущений.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S5</strong></th>
<th><p><strong>Imai, K.; King, G.; Nall, C..</strong> The Essential Role of Pair Matching in Cluster-Randomized Experiments. 2009. <a href="https://projecteuclid.org/journals/statistical-science/volume-24/issue-1/The-Essential-Role-of-Pair-Matching-in-Cluster-Randomized-Experiments/10.1214/08-STS274.full"><u>Открыть источник</u></a></p>
<p><em>Обосновывает matched-pair cluster randomization и анализ, учитывающий matching.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S6</strong></th>
<th><p><strong>Campbell, M. K. et al..</strong> CONSORT 2010 statement: extension to cluster randomised trials. 2012. <a href="https://www.bmj.com/content/345/bmj.e5661"><u>Открыть источник</u></a></p>
<p><em>Специфические требования к планированию и отчетности cluster trials.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S7</strong></th>
<th><p><strong>Hopewell, S. et al..</strong> CONSORT 2025 statement: updated guideline for reporting randomised trials. 2025. <a href="https://www.bmj.com/content/389/bmj-2024-081123"><u>Открыть источник</u></a></p>
<p><em>Актуальная общая рамка прозрачной отчетности; использовать вместе с cluster extension.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S8</strong></th>
<th><p><strong>Eldridge, S. M.; Ashby, D.; Kerry, S..</strong> Sample size for cluster randomized trials: effect of coefficient of variation of cluster size and analysis method. 2006. <a href="https://pubmed.ncbi.nlm.nih.gov/16943232/"><u>Открыть источник</u></a></p>
<p><em>Показывает влияние неравных размеров кластеров и CV на мощность.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S9</strong></th>
<th><p><strong>Pustejovsky, J. E.; Tipton, E..</strong> Small-Sample Methods for Cluster-Robust Variance Estimation and Hypothesis Testing. 2018. <a href="https://arxiv.org/abs/1601.01981"><u>Открыть источник</u></a></p>
<p><em>CR2/BRL и Satterthwaite-коррекция для малого числа независимых кластеров.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S10</strong></th>
<th><p><strong>Deng, A.; Xu, Y.; Kohavi, R.; Walker, T..</strong> Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data. 2013. <a href="https://dl.acm.org/doi/10.1145/2433396.2433413"><u>Открыть источник</u></a></p>
<p><em>CUPED: снижение дисперсии за счет pre-period covariates.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S11</strong></th>
<th><p><strong>Lin, W..</strong> Agnostic Notes on Regression Adjustments to Experimental Data. 2013. <a href="https://projecteuclid.org/journals/annals-of-applied-statistics/volume-7/issue-1/Agnostic-notes-on-regression-adjustments-to-experimental-data--Reexamining/10.1214/12-AOAS583.full"><u>Открыть источник</u></a></p>
<p><em>Регрессионная корректировка с centered covariates, interactions и robust uncertainty.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S12</strong></th>
<th><p><strong>Fabijan, A. et al..</strong> Diagnosing Sample Ratio Mismatch in Online Controlled Experiments. 2019. <a href="https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/"><u>Открыть источник</u></a></p>
<p><em>SRM как сигнал системной ошибки назначения, логирования или отбора.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S13</strong></th>
<th><p><strong>International Council for Harmonisation.</strong> ICH E9(R1): Addendum on Estimands and Sensitivity Analysis. 2019/2020. <a href="https://www.ema.europa.eu/en/ich-e9-statistical-principles-clinical-trials-scientific-guideline"><u>Открыть источник</u></a></p>
<p><em>Структурирует population, treatment conditions, outcomes, intercurrent events и summary measure. Методологическая аналогия, не retail-регулирование.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S14</strong></th>
<th><p><strong>U.S. Food and Drug Administration.</strong> Non-Inferiority Clinical Trials to Establish Effectiveness. 2016. <a href="https://www.fda.gov/media/78504/download"><u>Открыть источник</u></a></p>
<p><em>Предварительная фиксация NI margin и решение по границе доверительного интервала. Используется как статистическая логика, не как обязательное правило для X5.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S15</strong></th>
<th><p><strong>Lan, K. K. G.; DeMets, D. L..</strong> Discrete Sequential Boundaries for Clinical Trials. 1983. <a href="https://academic.oup.com/biomet/article-abstract/70/3/659/247777"><u>Открыть источник</u></a></p>
<p><em>Alpha-spending для заранее спланированного sequential monitoring.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S16</strong></th>
<th><p><strong>Holm, S..</strong> A Simple Sequentially Rejective Multiple Test Procedure. 1979. <a href="https://www.jstor.org/stable/4615733"><u>Открыть источник</u></a></p>
<p><em>Strong FWER control для семейства гипотез.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S17</strong></th>
<th><p><strong>Dunnett, C. W..</strong> A Multiple Comparison Procedure for Comparing Several Treatments with a Control. 1955. <a href="https://www.tandfonline.com/doi/abs/10.1080/01621459.1955.10501294"><u>Открыть источник</u></a></p>
<p><em>Many-to-one comparisons при нескольких treatment arms и общем control.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S18</strong></th>
<th><p><strong>Angrist, J. D.; Imbens, G. W.; Rubin, D. B..</strong> Identification of Causal Effects Using Instrumental Variables. 1996. <a href="https://www.jstor.org/stable/2291629"><u>Открыть источник</u></a></p>
<p><em>LATE/CACE интерпретация IV требует exclusion, monotonicity и других допущений.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S19</strong></th>
<th><p><strong>Российская Федерация; актуальная консолидированная редакция.</strong> Федеральный закон N 152-ФЗ, статья 5: Принципы обработки персональных данных. ред. от 26.07.2026. <a href="https://www.consultant.ru/document/cons_doc_LAW_61801/96fbc469f91f57235cc842a85e0516a99f23dc85/"><u>Открыть источник</u></a></p>
<p><em>Законность, конкретная цель, минимизация объема, точность и ограничение хранения. Не заменяет юридическое заключение.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S20</strong></th>
<th><p><strong>ГИС ЗПП Роспотребнадзора.</strong> Бонусные программы и права потребителей. 04.09.2024. <a href="https://zpp.rospotrebnadzor.ru/news/regional/506273"><u>Открыть источник</u></a></p>
<p><em>Условия начисления, расходования и списания должны быть зафиксированы в доступных правилах программы.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S21</strong></th>
<th><p><strong>OECD.</strong> Dark Commercial Patterns. 2022. <a href="https://www.oecd.org/en/publications/dark-commercial-patterns_44f5e846-en.html"><u>Открыть источник</u></a></p>
<p><em>Рабочая рамка манипулятивных цифровых практик и потребительского вреда.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>S22</strong></th>
<th><p><strong>National Institute of Standards and Technology.</strong> AI Risk Management Framework - Key Resources. AI RMF 1.0; страница актуальна в 2026. <a href="https://airc.nist.gov/"><u>Открыть источник</u></a></p>
<p><em>Добровольная рамка управления AI-рисками; версия 1.0 находится в процессе пересмотра.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>


Конец отчета
