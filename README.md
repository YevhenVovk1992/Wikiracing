# BenzinCheck
### Get information about the price of fuel for your region or country. Use for it our websuite or REST API service.
Link - 
___
![Screenshot from 2022-11-23 12-14-28](https://user-images.githubusercontent.com/104986485/203813383-4865c00f-c7e2-4da9-b67b-1cb198fcbbd0.png)
___
### What we do?
Technologies used: Djando, Django Unittest, Django crispy forms, DjangoORM, Celery Worker, Django baet, PostgresDB, Docker, Jinja2, HTML5, CSS, JS, Asyncio, Asyncpg, Beautifulsoup4, Aiohttp,  

Create Djngo project with Celery Worker (used RabbitMQ as broker). Created REST API service and start page. The user can get fuel prices through the form on the site or through a GET request with the appropriate parameters.The Postgres database is used. You can update the data in the database manually or it will update automatically. Only a super user can edit data, which is created by the corresponding command in Django.
The data is received by the asynchronous parser. You can start the parser once a day (it starts automatically at 0-10 every day). Django beat and celery worker is used for automation.
You can edit records in the database through the menu on the start page. You must first log in to the site. Or you can use the django admin panel.
___
### How to start project?
1. pip install -r requerements.txt;
2. Create .env file and write to it enviroment variables:
	- SECRET_KEY
	- POSTGRES_USER
	- POSTGRES_PASSWORD
	- POSTGRES_DB
	- DB_HOST
	- DB_PORT
	- CELERY_BROKER_URL (pyamqp://guest@localhost//)
3. Run 'docker-compose up -d'to make a container for the whole application ('python manage.py migrate' start automaticaly);
4. Run 'python manage.py migrate' (If you are using docker, the migration takes place when the container is started);
5. Create superuser 'python manage.py createsuperuser' and add user's groups: guide and traveler in admin panel;
6. Run Celery Worker - celery -A BenzinCheck worker --beat --scheduler django --loglevel=info;
7. Load fixtures:
	- python manage.py loaddata fixtures/fuel.json --app fuel.fuel
	- python manage.py loaddata fixtures/fueloperator.json --app fuel.fueloperator
	- python manage.py loaddata fixtures/region.json --app fuel.region
