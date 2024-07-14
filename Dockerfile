FROM python:3-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --update nodejs npm cmake\
    && pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf /var/cache/apk/*

COPY . .

ENV FILE = config/docker-config.yaml

EXPOSE 8080

CMD uvicorn --host 0.0.0.0 --port $(port) main:app