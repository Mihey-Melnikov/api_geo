# API Geo

## Цель

Упростить и автоматизировать работу с географическими объектами в Ракете.

## Быстрый запуск

1. Установите PostgreSQL и создайте сервер. Креды подключения к серверу укажите в .env файле
2. Клонируйте репозиторий
3. Установите все необходимые модули

```python
pip install -r requirements.txt
```

3. Создайте локальную БД миграцией

```python
alembic upgrade head
```

4. Запустите скрипты наполнения базы. База заполняется по данным Ракеты

```python
python ./osm/script.py -a=fill -e=all
```

5. Запустите проект

```python
uvicorn src.main:app --reload
```

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

Запуск тестов  
```python
pytest -v -s --disable-warnings  tests/ 
```
