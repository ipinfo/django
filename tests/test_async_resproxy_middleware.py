from http import HTTPStatus
from unittest import mock

import pytest
from ipinfo.details import Details


@pytest.mark.asyncio
async def test_middleware_appends_resproxy_info(
    async_client, ipinfo_async_resproxy_middleware
):
    with mock.patch("ipinfo.AsyncHandler.getResproxy") as mocked_getResproxy:
        mocked_getResproxy.return_value = Details(
            {
                "ip": "127.0.0.1",
                "last_seen": "2026-01-15",
                "percent_days_seen": 100,
                "service": "test_service",
            }
        )
        res = await async_client.get("/test_resproxy_view/")
        assert res.status_code == HTTPStatus.OK
        assert b"Resproxy for: 127.0.0.1" in res.content


@pytest.mark.asyncio
async def test_middleware_filters(async_client, ipinfo_async_resproxy_middleware):
    res = await async_client.get("/test_resproxy_view/", USER_AGENT="some bot")
    assert res.status_code == HTTPStatus.OK
    assert b"Request filtered." in res.content


@pytest.mark.asyncio
async def test_middleware_behind_proxy(async_client, ipinfo_async_resproxy_middleware):
    with mock.patch("ipinfo.AsyncHandler.getResproxy") as mocked_getResproxy:
        mocked_getResproxy.return_value = Details(
            {
                "ip": "93.44.186.197",
                "last_seen": "2026-01-15",
                "percent_days_seen": 100,
                "service": "test_service",
            }
        )
        res = await async_client.get(
            "/test_resproxy_view/", X_FORWARDED_FOR="93.44.186.197"
        )

        mocked_getResproxy.assert_called_once_with("93.44.186.197")
        assert res.status_code == HTTPStatus.OK
        assert b"Resproxy for: 93.44.186.197" in res.content


@pytest.mark.asyncio
async def test_middleware_not_behind_proxy(
    async_client, ipinfo_async_resproxy_middleware
):
    with mock.patch("ipinfo.AsyncHandler.getResproxy") as mocked_getResproxy:
        mocked_getResproxy.return_value = Details(
            {
                "ip": "127.0.0.1",
                "last_seen": "2026-01-15",
                "percent_days_seen": 100,
                "service": "test_service",
            }
        )
        res = await async_client.get("/test_resproxy_view/")

        mocked_getResproxy.assert_called_once_with("127.0.0.1")
        assert res.status_code == HTTPStatus.OK
        assert b"Resproxy for: 127.0.0.1" in res.content


@pytest.mark.asyncio
async def test_middleware_empty_response(
    async_client, ipinfo_async_resproxy_middleware
):
    """Test that empty response from API (IP not in resproxy database) is passed through."""
    with mock.patch("ipinfo.AsyncHandler.getResproxy") as mocked_getResproxy:
        mocked_getResproxy.return_value = Details({})
        res = await async_client.get("/test_resproxy_view/")

        mocked_getResproxy.assert_called_once_with("127.0.0.1")
        assert res.status_code == HTTPStatus.OK
        assert b"Empty resproxy response." in res.content
