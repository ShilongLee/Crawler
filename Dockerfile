FROM python:3

WORKDIR /app

COPY . .

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs

RUN pip3 install -r requirements.txt

ENV THREADS=4

EXPOSE 8080

CMD gunicorn -c config/gunicorn.conf.py -w $THREADS -b :8080 main:app
