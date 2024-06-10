FROM python:3-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --update nodejs npm \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/cache/apk/*

COPY . .

ENV THREADS=4

EXPOSE 8080

CMD gunicorn -c config/gunicorn.conf.py -w $THREADS -b :8080 main:app