# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app

FROM base AS builder
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements/base.txt requirements/base.txt
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements/base.txt

FROM base AS production
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
COPY . .
RUN chmod +x start.sh
EXPOSE 8000
ENTRYPOINT ["./start.sh"]

FROM builder AS test
COPY requirements/dev.txt requirements/dev.txt
RUN pip install --no-cache-dir -r requirements/dev.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE=codigosPostalesMx.settings.test
CMD ["python", "manage.py", "test", "tests", "-v", "2"]
