FROM python:3.7-buster

RUN apt-get update
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash
RUN apt-get -y install nodejs
RUN npm install

COPY . /app
WORKDIR /app
RUN pip install -U pip
RUN pip install -r requirements.txt
WORKDIR /app/static
RUN npm install
RUN mv node_modules/reveal.js-plugins/chart node_modules/reveal.js/plugins/
WORKDIR /app
ENV SECRET_KEY=${SECRET_KEY}

CMD gunicorn --bind=0.0.0.0:8000 wsgi:app

