FROM alpine:3.12 as builder

ENV PROMETHEUS_VERSION=2.23.0

# Download promtool from Prometheus site
RUN apk --update add wget tar \
    && wget -c https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VERSION}/prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz \
    && tar -xzf prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz \
    && mv prometheus-${PROMETHEUS_VERSION}.linux-amd64 prometheus

FROM python:3.11.0a7-slim

# LABEL maintainer="fabeirojorge.secondwindow@gmail.com"

RUN apt-get update -y && \
    apt-get install -y netcat-openbsd

COPY ./requirements.txt /app/requirements.txt

COPY --from=builder prometheus/promtool /bin/promtool

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY ./app.py /app

CMD [ "sh", "-c", "gunicorn -w ${GUNICORN_WORKERS} -b :${RULESERVER_PORT} app:app" ]
