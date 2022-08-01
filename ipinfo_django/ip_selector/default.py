"""
A default iphandler implementation that returns IP to query for depending on whether we are behind a reverse proxy or not.
"""

from .interface import IPSelectorInterface
from ipinfo_django.helpers import HTTP_X_FORWARDED_FOR, REMOTE_ADDR


class DefaultIPSelector(IPSelectorInterface):
    """Default IP selector which uses IP depending on whether we are behind a reverse proxy or not."""

    def get_ip(self, request):
        """Determine what IP to query for depending on whether we are behind a reverse proxy or not."""
        x_forwarded_for = request.META.get(HTTP_X_FORWARDED_FOR)
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get(REMOTE_ADDR)
