FROM python:3.10-slim

ENV POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH" \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y curl build-essential

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set workdir
WORKDIR /app

COPY . .

RUN ls -R /app

RUN poetry lock

RUN poetry install --with dev

RUN poetry run playwright install --with-deps



