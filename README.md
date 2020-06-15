# NLawP-flask

This repository houses the flask deployment of an interactive view of predictions of US District Court Cases based on NLP analysis of over 100k US District Court Cases over the past 100 years.

## How to Deploy

### Gunicorn

Deployment with [Gunicorn](https://gunicorn.org/) with the following command:

```bash
gunicorn wsgi:app
```

### Docker

There is also an included Dockerfile which can be used to build and run NLPLaw docker container.  The docker container can be built with the following command:
```bash
docker build -t nlawp https://www.github.com/smerz1989/NLawP-flask
```
The docker can then be run with the docker run command:

```bash
docker run -d -p 8000:8000 nlawp:latest
```
