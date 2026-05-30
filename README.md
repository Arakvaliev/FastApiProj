# Проект HR сервиса на Fast API

## Запуск
Последовательность команд для запуска проекта:

1. docker-compose up -d --build -сборка и запуск
2. docker-compose exec api alembic upgrade head - применяем миграции

После этого можно проводить тестирование с помощью Swagger: "http://localhost:8000/docs"

Для запуска тестов:

1. docker-compose up -d db - поднимаем только БД
2. alembic upgrade head - применяем миграции
3. pytest tests/ -v

Также после запуска БД можно запустить бекенд вне контейнера с помощью команды: "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

## Окружение

Также для запуска в корне проекта необходимо создать .env файл, описать в нем следующие переменные:

PROJECT_NAME=

VERSION=1.0.0

API_V1_STR=/api/v1

POSTGRES_SERVER=

POSTGRES_USER=

POSTGRES_PASSWORD=

POSTGRES_DB=

SECRET_KEY=

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=

REFRESH_TOKEN_EXPIRE_DAYS=

## Примечание

При работе над проектом использовались технологии ИИ:

1. Для генерации тестовых данных
2. Для генерации HTTP-ответов
3. Для генерации некоторых регулярных выражений
4. Для анализа кода и поиска сложных ошибок