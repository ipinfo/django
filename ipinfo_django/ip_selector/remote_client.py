"""
An IP selector implementation returning client IP from REMOTE_ADDR.
"""

from .interface import IPHandlerInterface


class ClientIPSelector(IPSelectorInterface):
    """Returns client IP address from REMOTE_ADDR."""
    return request.META.get(REMOTE_ADDR)
