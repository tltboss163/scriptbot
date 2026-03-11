# ScriptBot — боевая версия каркаса агрегатора манги

ScriptBot — backend + Telegram-бот для поиска и агрегации манги по подключаемым модулям источников.

## Что уже реализовано

- FastAPI API с endpoints:
  - `GET /health/live`
  - `GET /health/ready`
  - `GET /api/sources`
  - `GET /api/search?q=<query>`
  - `GET /api/manga/{source}/{source_id}`
  - `GET /api/manga/{source}/{source_id}/chapters`
- Подключаемые модули-парсеры источников:
  - `mangalib`
  - `mangabuff`
  - `remanga`
  - `senkuro`
  - `dezu`
  - `mangachan`
- Единый агрегатор поиска с дедупликацией по fingerprint и ранжированием.
- Телеграм-бот (aiogram 3) с базовыми командами `/start` и `/sources`.
- Docker Compose: API, Celery worker/beat, PostgreSQL, Redis.

## Принцип подключаемости парсеров

Каждый источник — отдельный модуль в `app/adapters/sources/*.py`, реализующий интерфейс `SourceAdapter`.
Регистрация и включение/отключение делается через `app/adapters/registry.py` и переменную `ENABLED_SOURCES`.

## Быстрый запуск

```bash
cp .env.example .env
docker compose up --build
```

Проверка:

```bash
curl 'http://localhost:8000/api/sources'
curl 'http://localhost:8000/api/search?q=naruto'
```

## Важно

Селекторы сайтов могут меняться, поэтому каждый модуль парсера изолирован и может обновляться независимо.
Для сайтов с anti-bot/Cloudflare предусмотрена стратегия fallback (следующий этап — браузерный контекст Playwright в адаптерах).
