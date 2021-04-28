FROM python:3.8-slim


RUN pip install poetry \
    && poetry config virtualenvs.create false

WORKDIR /workspaces/hrsl-up
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

