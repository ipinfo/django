HTTP_X_FORWARDED_FOR = "HTTP_X_FORWARDED_FOR"
REMOTE_ADDR = "REMOTE_ADDR"


def is_bot(request):
    """Whether or not the request user-agent self-identifies as a bot"""
    lowercase_user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
    return "bot" in lowercase_user_agent or "spider" in lowercase_user_agent


def get_ip(request):
    """Determine what IP to query for depending on whether we are behind a reverse proxy or not."""
    x_forwarded_for = request.META.get(HTTP_X_FORWARDED_FOR)
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get(REMOTE_ADDR)
