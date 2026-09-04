# Документация «X5 Двор»

Этот файл задаёт канонический порядок чтения. Если документы расходятся, используйте приоритет: условия кейса и поздние уточнения → safety/privacy/causal constraints → профильное исследование → итоговая концепция → ранний черновик.

## Быстрое погружение — 30–40 минут

1. [01-case.md](01-case.md) — исходная задача, границы и критерии.
2. [08-correspondence-summary.md](08-correspondence-summary.md) — последние уточнения организаторов и команды.
3. [00-final-concept.md](00-final-concept.md) — итоговое решение от пользовательской петли до пилота и питча.
4. [05-team-plan.md](05-team-plan.md) — роли и ближайшие командные задачи.

После этих четырёх документов коллега должен понимать, что строим, почему социальный слой отделён от ядра, как защищается маржа и чем PoC отличается от реального пилота.

## Чтение по ролям

### Product и UX

1. [00-final-concept.md](00-final-concept.md), разделы 1–6 и 16–20.
2. [research/01-game-mechanics.md](research/01-game-mechanics.md) — выбор персональной миссии, приватного прогресса и «Двора-Lite».
3. [research/03-mechanic-recommender.md](research/03-mechanic-recommender.md) — правила выбора механики и объяснения.
4. [dvor-spec.md](dvor-spec.md) — исходная расширенная гипотеза коллеги; читать как исторический дизайн, не как финальные правила.

### AI и backend

1. [00-final-concept.md](00-final-concept.md), разделы 7–10 и 12.
2. [research/02-ai-challenge-generator.md](research/02-ai-challenge-generator.md) — контракт и ограничения генератора миссий.
3. [research/03-mechanic-recommender.md](research/03-mechanic-recommender.md) — policy/ranker и reason codes.
4. [research/05-antifraud.md](research/05-antifraud.md) — event integrity, ledger, graph-lite и tiered actions.

### Analytics, экономика и эксперимент

1. [research/04-reward-economics.md](research/04-reward-economics.md) и [сценарии CSV](research/04-reward-scenarios.csv).
2. [research/06-simulation-summary.md](research/06-simulation-summary.md) — корректная интерпретация 1k/10k и Monte Carlo.
3. [research/simulation/README.md](research/simulation/README.md) — код, конфиг и сохранённые результаты.
4. [research/07-pilot-plan.md](research/07-pilot-plan.md) — preregistration-ready store-cluster RCT.
5. [03-metrics-and-pilot.md](03-metrics-and-pilot.md) — ранняя постановка метрик; при конфликте использовать профильный отчёт 07.

### Сегменты и демография

1. [04-customer-segments.md](04-customer-segments.md) — синтетические клиентские сегменты команды.
2. [07-russia-demography-for-simulation.md](07-russia-demography-for-simulation.md) — официальные ориентиры РФ и правила калибровки.
3. [data/customer-segments.csv](data/customer-segments.csv) и [data/russia-simulation-demographic-priors.csv](data/russia-simulation-demographic-priors.csv) — машиночитаемые данные.

## Справочные и исторические документы

| Файл | Статус и назначение |
| --- | --- |
| [02-solution-concept.md](02-solution-concept.md) | Ранний продуктовый черновик; решения заменены итоговой концепцией там, где расходятся |
| [03-metrics-and-pilot.md](03-metrics-and-pilot.md) | Ранняя схема метрик и A/B-теста |
| [04-customer-segments.md](04-customer-segments.md) | Синтетические X5-сегменты, не статистика клиентской базы |
| [05-team-plan.md](05-team-plan.md) | Историческая переписка и распределение задач |
| [06-risks-and-recommendations.md](06-risks-and-recommendations.md) | Ранний аудит рисков, часть решений учтена в финале |
| [07-russia-demography-for-simulation.md](07-russia-demography-for-simulation.md) | Национальные priors, не профиль клиентов X5 |
| [08-correspondence-summary.md](08-correspondence-summary.md) | Рабочая выжимка; не дословная стенограмма организаторов |
| [dvor-spec.md](dvor-spec.md) | Исходная спецификация коллеги до исследовательского аудита |
| [research/00-intake-audit.md](research/00-intake-audit.md) | Комплектность ответов, конфликты и недостающие приложения |

## Уровни достоверности

- **Условия/уточнения** — требования кейса и рабочая выжимка переписки.
- **FACT** — тезис, подтверждённый указанным внешним источником.
- **Проектное решение** — выбранный командой продуктовый дизайн.
- **ASSUMPTION / scenario** — число для PoC или симуляции, которое нельзя выдавать за результат X5.
- **TO_VALIDATE** — параметр, требующий внутренних данных, правовой проверки или реального пилота.

Национальная демография не заменяет данные клиентов X5. Синтетическая симуляция демонстрирует метод и sampling variation, но не прогнозирует uplift. Размер награды, пилота и допустимое снижение маржи фиксируются только после калибровки и до просмотра результатов эксперимента.

## История материалов

Ранняя выгрузка командного диалога была разложена по файлам `01–06`; исходник не сохранился в Git. Финальный GPT-синтез перенесён в [00-final-concept.md](00-final-concept.md), проверен против семи профильных исследований и отредактирован в местах, где модель не распознала вложения.
