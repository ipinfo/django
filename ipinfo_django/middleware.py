import logging
import traceback

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import ipinfo

LOGGER = logging.getLogger(__name__)


class IPinfo(MiddlewareMixin):
    def __init__(self, get_response=None):
        """Initializes class while gettings user settings and creating the cache."""
        self.get_response = get_response
        self.filter = getattr(settings, "IPINFO_FILTER", self.is_bot)

        ipinfo_token = getattr(settings, "IPINFO_TOKEN", None)
        ipinfo_settings = getattr(settings, "IPINFO_SETTINGS", {})
        self.ipinfo = ipinfo.getHandler(ipinfo_token, **ipinfo_settings)

    def process_request(self, request):
        """Middleware hook that acts on and modifies request object."""
        try:
            if self.filter and self.filter(request):
                request.ipinfo = None
            else:
                request.ipinfo = self.ipinfo.getDetails()
        except Exception as exc:
            request.ipinfo = None
            LOGGER.error(traceback.format_exc())

    def is_bot(self, request):
        """Whether or not the request user-agent self-identifies as a bot"""
        lowercase_user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
        return "bot" in lowercase_user_agent or "spider" in lowercase_user_agent
