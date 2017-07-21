web: gunicorn test_proj.wsgi
worker: celery -A test_proj worker
beat: celery -A test_proj beat -S django