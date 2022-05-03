FROM python:3.10.4-slim-bullseye

LABEL maintainers="m.drozdetskiy@gmail.com"

ENV HOME='/home/httpd'

RUN mkdir -p $HOME/app \
    $HOME/app/src/.meta

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    libxml2-dev \
    postgresql-client && \
    apt-get autoremove && \
    apt-get clean

WORKDIR $HOME/app/src
