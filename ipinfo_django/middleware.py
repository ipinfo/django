import logging
import traceback

import ipinfo
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from ipinfo_django.helpers import is_bot
from ipinfo_django.ip_selector.default import DefaultIPSelector

LOGGER = logging.getLogger(__name__)


class IPinfo(MiddlewareMixin):
    def __init__(self, get_response=None):
        """
        Initializes class while gettings user settings and creating the cache.
        """
        self.get_response = get_response
        self.filter = getattr(settings, "IPINFO_FILTER", self.is_bot)

        ipinfo_token = getattr(settings, "IPINFO_TOKEN", None)
        ipinfo_settings = getattr(settings, "IPINFO_SETTINGS", {})
        self.ip_selector = getattr(
            settings, "IPINFO_IP_SELECTOR", DefaultIPSelector()
        )
        self.ipinfo = ipinfo.getHandler(ipinfo_token, **ipinfo_settings)

    def process_request(self, request):
        """Middleware hook that acts on and modifies request object."""
        try:
            if self.filter and self.filter(request):
                request.ipinfo = None
            else:
                request.ipinfo = self.ipinfo.getDetails(
                    self.ip_selector.get_ip(request)
                )
        except Exception as exc:
            request.ipinfo = None
            LOGGER.error(traceback.format_exc())

    def is_bot(self, request):
        return is_bot(request)


class IPinfoAsyncMiddleware:
    sync_capable = False
    async_capable = True

    def __init__(self, get_response):
        """Initialize class, get settings, and create the cache."""
        self.get_response = get_response

        self.filter = getattr(settings, "IPINFO_FILTER", self.is_bot)

        ipinfo_token = getattr(settings, "IPINFO_TOKEN", None)
        ipinfo_settings = getattr(settings, "IPINFO_SETTINGS", {})
        self.ip_selector = getattr(
            settings, "IPINFO_IP_SELECTOR", DefaultIPSelector()
        )
        self.ipinfo = ipinfo.getHandlerAsync(ipinfo_token, **ipinfo_settings)

    def __call__(self, request):
        return self.__acall__(request)

    async def __acall__(self, request):
        """Middleware hook that acts on and modifies request object."""
        try:
            if self.filter and self.filter(request):
                request.ipinfo = None
            else:
                request.ipinfo = await self.ipinfo.getDetails(
                    self.ip_selector.get_ip(request)
                )
        except Exception:
            request.ipinfo = None
            LOGGER.error(traceback.format_exc())

        response = await self.get_response(request)
        return response

    def is_bot(self, request):
        return is_bot(request)
