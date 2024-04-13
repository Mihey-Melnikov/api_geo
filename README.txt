запуск vevn
venv\Scripts\activate.ps1

запуск всего
uvicorn src.main:app --reload

убиваем uvicorn и venv через закрытие терминала

создаем миграцию
alembic revision --autogenerate -m "Database creation"

поднимаем миграцию
alembic upgrade <id миграции>

откатываем миграцию
alembic downgrade <id миграции>

устанавливаем текущее состояние исходным
alembic upgrade head

drop table 
	public.airport, 
	public.railway_station, 
	public.metro, 
	public.city, 
	public.region, 
	public.country, 
	public.user, 
	public.alembic_version,
	public.translation_language