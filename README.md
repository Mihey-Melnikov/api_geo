# API Geo

## Быстрый запуск

0. Установите PostgreSQL и создайте сервер с кредами:

```python
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
```

2. Клонируйте репозиторий
3. Установите все необходимые модули

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

Создание новой миграции:  
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

Починить авторизацию во всех запросах: добавить строки в каждом `router.py` для каждой ручки:  
```python
from src.auth.base_config import current_user
from src.auth.models import User
user: User = Depends(current_user)
```
