FROM python:3.12-alpine

ENV POETRY_VERSION=1.8.3

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY pyproject.toml poetry.lock ./


RUN poetry config virtualenvs.create false


RUN poetry install --no-interaction --no-ansi

COPY . .

RUN poetry install
