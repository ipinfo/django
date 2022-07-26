"""
Abstract interface for selecting IP from incoming request.
"""

import abc


class IPSelectorInterface(metaclass=abc.ABCMeta):
    """Interface for selecting IP."""

    @abc.abstractmethod
    def get_ip(self, request):
        pass
