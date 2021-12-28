DEBUG = False
SECRET_KEY = "FOR-TESTING-ONLY"

ROOT_URLCONF = "tests.urls"

MIDDLEWARE = [
    "ipinfo_django.middleware.IPinfoAsyncMiddleware",
]

USE_TZ = False
