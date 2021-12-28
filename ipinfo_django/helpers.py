HTTP_X_FORWARDED_FOR = "HTTP_X_FORWARDED_FOR"
REMOTE_ADDR = "REMOTE_ADDR"


def is_bot(request):
    """Whether or not the request user-agent self-identifies as a bot"""
    lowercase_user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
    return "bot" in lowercase_user_agent or "spider" in lowercase_user_agent


def get_ip(request):
    """Determine what ip address to query for depending on whether we are behind a reverse proxy or not."""
    if request.META.get(HTTP_X_FORWARDED_FOR):
        return request.META.get(HTTP_X_FORWARDED_FOR)
    return request.META.get(REMOTE_ADDR)
