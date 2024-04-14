# API Geo

## Быстрый запуск

0. Установите PostgreSQL
1. Клонируйте репозиторий
2. Установите все необходимые модули

```python
pip install -r requirements.txt
```

3. Создайте локальную БД миграцией

```python
alembic upgrade head
```

4. Запустите проект

```python
uvicorn src.main:app --reload
```

## Структура проекта

Основная структура:
* `migrations/` - миграции
* `src/` - основной проект
* `.env` - переменные окружения

Вложенные файлы:
* `*/models` - описание моделей БД для миграций
* `*/schemas` - описание схем БД для API
* `*/router` - роутинг и основной код API

## FAQ

Создание новой миграции

```python
alembic revision --autogenerate -m "message"
```

Работа с виртаульным окружением. Запуск:
```python
venv\Scripts\activate.ps1
```
Выход:
```python
deactivate
```