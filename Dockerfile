FROM python:3.8

COPY ./requirements.txt /app/
WORKDIR /app

RUN pip install -r requirements.txt
