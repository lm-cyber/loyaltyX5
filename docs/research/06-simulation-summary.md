# Компактная выжимка ответа по симуляции

## Статус артефакта

Источник — полученный `x5_all_data.zip`. Архив содержал воспроизводимый synthetic scenario-analysis package, а не прогноз реального поведения X5. ZIP был проверен без ошибок; SHA-256: `7ed12380dac3f727ca352080f6cc5f750cf92bc4918223fdeb9c2990909e99aa`. После приёмки компактные артефакты сохранены в [`simulation/`](simulation/README.md), а тяжёлые воспроизводимые CSV и сам ZIP удалены.

В исходном архиве было 69 файлов:

- исходный контекст и prompt package;
- конфиги и source ledger;
- полные синтетические сущности для `n=1 000`;
- сущности user/yard/challenge/reward/fraud/weekly/receipt для `n=10 000`;
- item-level строки для `n=1 000`, но не для `n=10 000`;
- reference metrics, 45 Monte Carlo повторов для каждого размера, 17 sensitivity runs;
- validation checks, три диагностических графика и код генератора.

Все X5-specific behavioral, economic, app-selection, reward, fraud и treatment-effect значения в архиве имеют статус `ASSUMPTION` или `LATENT_GROUND_TRUTH`, пока не заменены данными X5/пилота.

## Основные сценарные входы

| Сценарий | Causal uplift mean | Награда | Margin rate | Cannibalization | Fraud prevalence | Group-harm probability |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Conservative | 2% | 100 ₽ | 16% | 30% | 1,5% | 15% |
| Base | 6% | 80 ₽ | 20% | 15% | 1,0% | 8% |
| Upside | 10% | 60 ₽ | 24% | 8% | 0,7% | 4% |
| Stress: low completion | 1% | 80 ₽ | 20% | 20% | 1,0% | 12% |
| Stress: high fraud | 6% | 80 ₽ | 20% | 15% | 5,0% | 8% |
| Stress: group harm | 1% | 80 ₽ | 20% | 15% | 1,0% | 30% |

Эти строки нельзя смешивать с independent reward-economics scenarios без повторного расчёта.

## Reference runs

| Метрика | n=1 000 | n=10 000 |
| --- | ---: | ---: |
| App users | 532 | 5 501 |
| Experiment users | 446 | 5 062 |
| «Дворы» | 100 | 1 094 |
| Test / control | 221 / 225 | 2 498 / 2 564 |
| Visits per user test | 16,941 | 19,145 |
| Visits per user control | 18,400 | 18,227 |
| Observed relative frequency uplift | −7,93% | +5,04% |
| Latent true incremental visits, 8 недель | +0,675 | +0,782 |
| Incremental contribution margin per user | −329,96 ₽ | +204,69 ₽ |
| X5 reward cost total | 14 288,20 ₽ | 156 242,84 ₽ |
| Net incremental CM per test user | −394,61 ₽ | +142,15 ₽ |
| Yard-cycle completion | 27,08% | 29,28% |
| Fraud precision / recall at 0,65 | 0 / 0 | 1,000 / 0,0206 |

Одиночные reference runs нельзя использовать как оценку ожидаемого эффекта. Противоположные знаки при положительном latent effect демонстрируют высокую sampling variation и различия конкретных seeds. Для fraud `0/0` при `n=1 000` без event counts недостаточно, чтобы отличить отсутствие положительных решений от иных причин.

## Monte Carlo: 45 повторов на размер

`estimated_itt_visits` измеряется в дополнительных визитах на пользователя за 8 недель.

| n | Mean estimate | SD | 2,5% | 97,5% | RMSE относительно latent ATT |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 000 | 1,139 | 0,620 | 0,085 | 2,071 | 0,607 |
| 10 000 | 1,017 | 0,182 | 0,603 | 1,330 | 0,174 |

Это распределение свойств заданного DGP, а не confidence interval реального пилота и не ожидаемый uplift X5.

## One-factor sensitivity

Base deterministic translation использует `14,4` baseline visits/8 weeks, basket `760 ₽`, completion `48%`, causal uplift `6%`, reward `80 ₽`, margin `20%`, cannibalization `15%`:

- incremental visits: `0,7344` на пользователя;
- incremental CM: `111,63 ₽`;
- reward cost: `38,40 ₽`;
- net incremental CM: `+73,23 ₽`.

Ключевые результаты sensitivity:

- uplift `−2%` → net `−75,61 ₽`;
- uplift `0%` → net `−38,40 ₽`;
- uplift `3%` → net `+17,41 ₽`;
- reward `140 ₽` при прочем base → net `+44,43 ₽`;
- margin `12%` → net `+28,58 ₽`;
- cannibalization `50%` → net `+27,26 ₽`.

Эти результаты механически следуют из сценарной формулы и не учитывают conservative LCB reward gate из отдельного economics report. Финальный синтез должен выбрать единый канонический economics config и пересчитать симуляцию.

## Validation checks

В итоговых result-файлах отмечены как passed:

- уникальность `user_id`;
- возрастные квоты с допустимым отклонением не более одного человека из-за округления;
- assignment раньше treatment;
- fraud ground truth отделён от policy features;
- внешние ключи receipts → users/stores;
- item-to-receipt reconciliation для `n=1 000`;
- reward-ledger reconciliation;
- A/A null check для обоих размеров.

Ограничения проверки:

- A/A для `n=1 000` близок к границе (`z = −1,940`), хотя формально не отвергает null на 5%;
- generated code использует абсолютный путь `/mnt/data`, поэтому для локального повторного запуска нужен параметризованный output root;
- `continue_x5.py` пересобирал 10k run и часть validation output; итоговые result-файлы следует считать финальными артефактами, а два скрипта — совместной процедурой;
- каталог не содержит отдельных alcohol/tobacco категорий, появившихся в более позднем уточнении;
- встроенный fraud score слишком упрощён для канонического антифрода;
- внешняя валидность отсутствует до замены assumptions реальными aggregate/pilot inputs.

## Что использовать в финальном синтезе

Использовать архитектуру сущностей, разделение observed/latent outcomes, seed/reproducibility, source ledger, ledger reconciliation, Monte Carlo и sensitivity framework. Не переносить point estimates, reward `80 ₽`, margin `20%`, fraud threshold `0,65` или causal uplift `6%` как продуктовые решения без сверки с dedicated reports.
