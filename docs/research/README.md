# Исследовательский архив GPT Pro

Здесь лежат семь тематических исследований, использованных для проверки и редактирования [итоговой концепции](../00-final-concept.md). Это подробные материалы для углубления, а не обязательный линейный маршрут для всей команды.

## Порядок чтения

| № | Тема | Документ | Канонический вывод |
| ---: | --- | --- | --- |
| 0 | Приёмка комплекта | [00-intake-audit.md](00-intake-audit.md) | Показывает конфликты, пропуски и статус артефактов |
| 1 | Игровые механики | [01-game-mechanics.md](01-game-mechanics.md) | Миссия + приватный прогресс — ядро; «Двор-Lite» — отдельный arm |
| 2 | AI-генератор | [02-ai-challenge-generator.md](02-ai-challenge-generator.md) | Policy задаёт числа и ограничения; LLM только формулирует текст |
| 3 | Рекомендатель | [03-mechanic-recommender.md](03-mechanic-recommender.md) | Explainable rules/ranker, no-offer и reason codes обязательны |
| 4 | Экономика наград | [04-reward-economics.md](04-reward-economics.md) + [CSV](04-reward-scenarios.csv) | Reward ограничивается conservative LCB дополнительной маржи |
| 5 | Антифрод | [05-antifraud.md](05-antifraud.md) | Event integrity + ledger + tiered policy; synthetic thresholds не production |
| 6 | Симуляция | [06-simulation-summary.md](06-simulation-summary.md) + [артефакты](simulation/README.md) | 1k/10k показывают sampling variation, а не прогноз X5 |
| 7 | Пилот | [07-pilot-plan.md](07-pilot-plan.md) | Three-arm store-cluster RCT; N определяется power analysis |

## Правила использования

- Более поздние уточнения из [`../08-correspondence-summary.md`](../08-correspondence-summary.md) имеют приоритет в вопросах терминологии, вредных категорий и канала MVP.
- Не усреднять несовместимые экономические конфиги: simulation base использует reward `80 ₽`, отдельный economics base — `R_max = 22,19 ₽` и выбранные `20 ₽`.
- Не выбирать лучший одиночный seed симуляции; использовать Monte Carlo, sensitivity и честно показывать разброс.
- Для антифрода использовать профильный отчёт, а не упрощённый score симулятора.
- Покупки алкоголя и сигарет допустимы только как receipt-derived safety-признак и guardrail, но не как цель миссии.

## Комплектность

Получены шесть полных Markdown-отчётов, CSV экономики и ZIP симуляции. Авторы отчётов также ссылались на файлы, которых в ответах не было:

- JSON schemas/examples генератора миссий;
- отдельные code/metrics artifacts антифрода;
- редактируемый XLSX экономики.

Эти позиции считаются `MISSING/TO_BUILD`; ссылки внутри исходных отчётов не означают, что приложения доставлены.

Исходный ZIP симуляции был проверен (`SHA-256: 7ed12380dac3f727ca352080f6cc5f750cf92bc4918223fdeb9c2990909e99aa`). После извлечения кода, конфигов, результатов, графиков и сводок архив и тяжёлые воспроизводимые CSV удалены из рабочего репозитория.
