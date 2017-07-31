web: gunicorn tipsyapp.wsgi
worker: celery -A tipsyapp worker
beat: celery -A tipsyapp beat -S django