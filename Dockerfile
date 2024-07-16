FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev \
    libpq-dev \
    nmap

ADD pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install poetry gunicorn psycopg2-binary

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "k2i.wsgi:application"]
