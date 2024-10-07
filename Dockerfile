FROM python:3.12-slim

ENV POETRY_VERSION=1.8.3

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY . .

RUN poetry install --no-root

CMD ["poetry", "run", "fastapi", "run", "src/main.py"]
