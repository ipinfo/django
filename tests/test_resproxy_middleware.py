from http import HTTPStatus
from unittest import mock

from ipinfo.details import Details


def test_middleware_appends_resproxy_info(client, ipinfo_resproxy_middleware):
    with mock.patch("ipinfo.Handler.getResproxy") as mocked_getResproxy:
        mocked_getResproxy.return_value = Details(
            {
                "ip": "127.0.0.1",
                "last_seen": "2026-01-15",
                "percent_days_seen": 100,
                "service": "test_service",
            }
        )
        res = client.get("/test_resproxy_view/")
        assert res.status_code == HTTPStatus.OK
        assert b"Resproxy for: 127.0.0.1" in res.content


def test_middleware_filters(client, ipinfo_resproxy_middleware):
    res = client.get("/test_resproxy_view/", HTTP_USER_AGENT="some bot")
    assert res.status_code == HTTPStatus.OK
    assert b"Request filtered." in res.content


def test_middleware_behind_proxy(client, ipinfo_resproxy_middleware):
    with mock.patch("ipinfo.Handler.getResproxy") as mocked_getResproxy:
        mocked_getResproxy.return_value = Details(
            {
                "ip": "93.44.186.197",
                "last_seen": "2026-01-15",
                "percent_days_seen": 100,
                "service": "test_service",
            }
        )
        res = client.get("/test_resproxy_view/", HTTP_X_FORWARDED_FOR="93.44.186.197")

        mocked_getResproxy.assert_called_once_with("93.44.186.197")
        assert res.status_code == HTTPStatus.OK
        assert b"Resproxy for: 93.44.186.197" in res.content


def test_middleware_not_behind_proxy(client, ipinfo_resproxy_middleware):
    with mock.patch("ipinfo.Handler.getResproxy") as mocked_getResproxy:
        mocked_getResproxy.return_value = Details(
            {
                "ip": "127.0.0.1",
                "last_seen": "2026-01-15",
                "percent_days_seen": 100,
                "service": "test_service",
            }
        )
        res = client.get("/test_resproxy_view/")

        mocked_getResproxy.assert_called_once_with("127.0.0.1")
        assert res.status_code == HTTPStatus.OK
        assert b"Resproxy for: 127.0.0.1" in res.content


def test_middleware_empty_response(client, ipinfo_resproxy_middleware):
    """Test that empty response from API (IP not in resproxy database) is passed through."""
    with mock.patch("ipinfo.Handler.getResproxy") as mocked_getResproxy:
        mocked_getResproxy.return_value = Details({})
        res = client.get("/test_resproxy_view/")

        mocked_getResproxy.assert_called_once_with("127.0.0.1")
        assert res.status_code == HTTPStatus.OK
        assert b"Empty resproxy response." in res.content
