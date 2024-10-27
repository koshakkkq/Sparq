FROM python:3.12-alpine

ENV POETRY_VERSION=1.8.3

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN poetry install
