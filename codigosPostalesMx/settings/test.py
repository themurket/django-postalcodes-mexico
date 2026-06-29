from .base import *  # noqa: F401,F403

SECRET_KEY = "test-secret-key-not-for-production"

DEBUG = True

INSTALLED_APPS += [
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django_postalcodes_mexico.test_utils.test_app",
]

ROOT_URLCONF = "tests.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
