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


@pytest.fixture
def ipinfo_core_middleware(settings):
    settings.MIDDLEWARE = [
        "ipinfo_django.middleware.IPinfoCoreMiddleware",
    ]


@pytest.fixture
def ipinfo_async_core_middleware(settings):
    settings.MIDDLEWARE = [
        "ipinfo_django.middleware.IPinfoAsyncCoreMiddleware",
    ]
