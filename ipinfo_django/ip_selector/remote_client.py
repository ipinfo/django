"""
An IP selector implementation returning client IP from REMOTE_ADDR.
"""

from .interface import IPSelectorInterface
from ipinfo_django.helpers import REMOTE_ADDR


class ClientIPSelector(IPSelectorInterface):
    """Use client IP address from REMOTE_ADDR."""

    def get_ip(self, request):
        return request.META.get(REMOTE_ADDR)
