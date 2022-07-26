"""
A default iphandler implementation that returns IP to query for depending on whether we are behind a reverse proxy or not.
"""

from .interface import IPHandlerInterface
from ipinfo_django.helpers import get_ip


class DefaultIPSelector(IPSelectorInterface):
    """Determine what IP to query for depending on whether we are behind a reverse proxy or not."""
    
    def get_ip(self, request):
        return get_ip(request)
