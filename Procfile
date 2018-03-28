web: gunicorn openfruit.wsgi --log-file -
worker: celery worker --app=django_geo_db.tasks
