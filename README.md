# Zipcode API (Códigos Postales MX)

Django service that serves Mexican postal-code data from the SEPOMEX catalog.
Given a postal code it returns `{ codigoPostal, municipio, estado, colonias[] }`.
Consumed by the events API as the provider behind `/api/v1/zip-code`.

## Stack

- Python 3.12 · Django 5.2 LTS · Gunicorn
- PostgreSQL 15
- Docker (multi-stage build)

## Layout

```
codigosPostalesMx/        # Django project shell (settings package, urls, wsgi)
  settings/{base,prod,test}.py
django_postalcodes_mexico/  # reusable app: models, views, the SEPOMEX importer
tests/                    # service test suite (sqlite, settings.test)
requirements/{base,dev}.txt
Dockerfile                # multi-stage: base / builder / production / test
Dockerfile.dev            # dev image: bind-mount + autoreload
start.sh / start.dev.sh   # entrypoints (migrate + seed + serve)
```

## Local development

The service runs as part of the `murket-infrastructure` stack:

```bash
cd ../murket-infrastructure
docker compose up -d zipcode-api
```

Direct request (port 8009):

```bash
curl -sL http://localhost:8009/03103/ | python3 -m json.tool
```

## Tests

```bash
docker build --target test -t zipcode-test . && docker run --rm zipcode-test
```

CI runs the same test target on every pull request.

## Seeding

`importpostalcodesmx` downloads the SEPOMEX catalog from Correos de México and
seeds the database once (idempotent). Force a refresh with:

```bash
python manage.py importpostalcodesmx --force
```

## Environment

See `.env.example`. Required: `SECRET_KEY`, `POSTGRES_DB`, `POSTGRES_USER`,
`POSTGRES_PASSWORD` (and optionally `POSTGRES_HOST`, `POSTGRES_PORT`, `ALLOWED_HOSTS`).

## Upstream

Forked from [`EduardoZepeda/django-postalcodes-mexico`](https://github.com/EduardoZepeda/django-postalcodes-mexico).
The `django_postalcodes_mexico/` app is kept as a mirror of the upstream package
so fixes can be cherry-picked; the surrounding service scaffolding is ours.
