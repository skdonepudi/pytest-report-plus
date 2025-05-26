# Use official Python base
FROM python:3.10-slim

# Set environment
ENV POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH" \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set work directory
WORKDIR /app

# Copy project
COPY pyproject.toml poetry.lock* /app/

# Copy the actual source code BEFORE installing
COPY pytest_json_reporter /app/pytest_json_reporter

RUN poetry install --with dev

# Copy rest of the code
COPY . .

# Default command to run tests
CMD ["poetry", "run", "pytest"]
