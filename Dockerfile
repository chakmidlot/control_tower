FROM python:3.7-alpine

COPY requirements.txt /app/requirements.txt

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev && \
  pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app
