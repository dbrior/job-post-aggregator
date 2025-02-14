FROM python:3-slim

WORKDIR /app

RUN apt-get -y update; apt-get -y install curl

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./site_scrapers ./site_scrapers
COPY ./ ./