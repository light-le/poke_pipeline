FROM python:3.6-alpine AS package-install
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
            --upgrade \
            --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        alpine-sdk \
        postgresql-dev=9.6.10-r0

RUN python3 -m venv env
ENV PATH="env/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.6-alpine
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache \
            --upgrade \
            --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        libpq \
        postgresql-client \
    && rm -rf /var/cache/apk/*

WORKDIR poke_pipeline
COPY extract/ ./extract/
COPY load/postgres_load.py ./load/
COPY etl_postgres.py .

COPY --from=package-install env env
ENV PATH="env/bin:$PATH"

CMD ["python3", "etl_postgres.py"]
