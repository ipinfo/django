from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import ipinfo_wrapper

class IPinfo(MiddlewareMixin):

    def __init__(self, get_response=None):
        self.get_response = get_response
        self.filter = getattr(settings, 'IPINFO_FILTER', self.is_bot)
        ipinfo_token = getattr(settings, 'IPINFO_TOKEN', None)
        ipinfo_settings = getattr(settings, 'IPINFO_SETTINGS', {})
        self.ipinfo_wrapper = ipinfo_wrapper.getHandler(ipinfo_token, **ipinfo_settings)

    def process_request(self, request):
        if self.filter and self.filter(request):
            request.ipinfo = None
        else:
            request.ipinfo = self.ipinfo_wrapper.getDetails()

    def is_bot(self, request):
        lowercase_user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        return 'bot' in lowercase_user_agent or 'spider' in lowercase_user_agent
