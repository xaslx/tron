FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /src

RUN apt update -y && \
    apt install -y python3-dev gcc musl-dev postgresql-client


COPY pyproject.toml poetry.lock* /src/


RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

COPY src/ /src/