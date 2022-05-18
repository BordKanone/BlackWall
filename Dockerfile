FROM python:3.9-slim-buster

WORKDIR /blackwall/back

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -U pip
COPY . .
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile


