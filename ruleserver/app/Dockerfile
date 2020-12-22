FROM python:3.8-slim-buster

# LABEL maintainer="fabeirojorge.secondwindow@gmail.com"

RUN apt-get update -y && \
    apt-get install -y netcat-openbsd

COPY ./requirements.txt /app/requirements.txt

# If rebuilt, must be downloaded first from Prometheus website
COPY ./promtool /bin/promtool

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY ./app.py /app

CMD [ "sh", "-c", "gunicorn -w ${GUNICORN_WORKERS} -b :9092 app:app" ]
