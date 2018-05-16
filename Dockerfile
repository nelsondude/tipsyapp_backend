# Use an official Python runtime as a parent image
FROM python:3.6.5-slim-jessie
ENV PYTHONUNBUFFERED 1

ENV BACKEND_DIR /app/
RUN mkdir -p $BACKEND_DIR
WORKDIR $BACKEND_DIR

ADD requirements.txt $BACKEND_DIR
RUN pip install -r requirements.txt

RUN python -m nltk.downloader book
RUN pkill -f "beat"
RUN pkill -f "worker"
RUN apt-get update
RUN apt-get install nano


ADD . $BACKEND_DIR

CMD python manage.py runserver 0.0.0.0:8000