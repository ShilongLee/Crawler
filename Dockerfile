FROM python:3-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    cmake \
    pkg-config \
    libffi-dev \
    nodejs \
    npm \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/cache/apk/* \
    && rm -rf /var/lib/apt/lists/*

COPY . .

ENV FILE=config/docker-config.yaml

EXPOSE 8080

CMD uvicorn --host 0.0.0.0 --port 8080 main:app

