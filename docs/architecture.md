# Архитектура ScriptBot (боевой baseline)

## Модули

- `app/adapters/base.py` — единый контракт парсеров.
- `app/adapters/http_adapter.py` — общий HTTP/HTML-движок парсинга.
- `app/adapters/sources/*.py` — подключаемые парсеры сайтов.
- `app/adapters/registry.py` — регистрация адаптеров и управление через `ENABLED_SOURCES`.
- `app/services/aggregator.py` — fan-out поиска и агрегация результатов.
- `app/services/search.py` — нормализация, translit и fuzzy score.
- `app/api/routes.py` — API для источников, поиска, карточек и глав.

## Поддерживаемые источники на текущем этапе

1. mangalib
2. mangabuff
3. remanga
4. senkuro
5. dezu
6. mangachan

## Логика выбора источника

- В aggregated result сохраняются все кандидаты.
- `best_source` выбирается по максимальному `chapter_count`.
- При равенстве первее идет источник с более высоким fuzzy score в выдаче.

## Масштабирование

- API stateless, горизонтальное масштабирование через несколько инстансов.
- Очереди Celery для тяжелых задач экспорта/обхода anti-bot.
- Redis для кэширования выдачи поиска.

## Что дальше до fully production

- Реальные API/селекторы под каждый сайт и regression-тесты парсеров.
- Экспорт PDF/CBZ/EPUB как задачи Celery.
- Схема PostgreSQL + Alembic миграции.
- Подписки на новые главы и webhook/polling-уведомления.
- Anti-bot fallback (Playwright session pool per-domain).
