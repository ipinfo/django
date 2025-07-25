import pytest


@pytest.fixture
def ipinfo_middleware(settings):
    settings.MIDDLEWARE = [
        "ipinfo_django.middleware.IPinfoMiddleware",
    ]


@pytest.fixture
def ipinfo_async_middleware(settings):
    settings.MIDDLEWARE = [
        "ipinfo_django.middleware.IPinfoAsyncMiddleware",
    ]


@pytest.fixture
def ipinfo_lite_middleware(settings):
    settings.MIDDLEWARE = [
        "ipinfo_django.middleware.IPinfoLiteMiddleware",
    ]


@pytest.fixture
def ipinfo_async_lite_middleware(settings):
    settings.MIDDLEWARE = [
        "ipinfo_django.middleware.IPinfoAsyncLiteMiddleware",
    ]
