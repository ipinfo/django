from http import HTTPStatus
from unittest import mock

from ipinfo.details import Details


def test_middleware_appends_ip_info(client, ipinfo_lite_middleware):
    with mock.patch("ipinfo.HandlerLite.getDetails") as mocked_getDetails:
        mocked_getDetails.return_value = Details({"ip": "127.0.0.1"})
        res = client.get("/test_view/")
        assert res.status_code == HTTPStatus.OK
        assert b"For testing: 127.0.0.1" in res.content


def test_middleware_filters(client, ipinfo_lite_middleware):
    res = client.get("/test_view/", HTTP_USER_AGENT="some bot")
    assert res.status_code == HTTPStatus.OK
    assert b"Request filtered." in res.content


def test_middleware_behind_proxy(client, ipinfo_lite_middleware):
    with mock.patch("ipinfo.HandlerLite.getDetails") as mocked_getDetails:
        mocked_getDetails.return_value = Details({"ip": "93.44.186.197"})
        res = client.get("/test_view/", HTTP_X_FORWARDED_FOR="93.44.186.197")

        mocked_getDetails.assert_called_once_with("93.44.186.197")
        assert res.status_code == HTTPStatus.OK
        assert b"For testing: 93.44.186.197" in res.content


def test_middleware_not_behind_proxy(client, ipinfo_lite_middleware):
    with mock.patch("ipinfo.HandlerLite.getDetails") as mocked_getDetails:
        mocked_getDetails.return_value = Details({"ip": "127.0.0.1"})
        res = client.get("/test_view/")

        mocked_getDetails.assert_called_once_with("127.0.0.1")
        assert res.status_code == HTTPStatus.OK
        assert b"For testing: 127.0.0.1" in res.content
