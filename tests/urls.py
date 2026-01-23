from django.http import HttpResponse
from django.urls import path


async def test_view(request):
    ipinfo = getattr(request, "ipinfo", None)

    if ipinfo:
        return HttpResponse(f"For testing: {ipinfo.ip}", status=200)

    return HttpResponse("Request filtered.", status=200)


async def test_resproxy_view(request):
    ipinfo_resproxy = getattr(request, "ipinfo_resproxy", None)

    if ipinfo_resproxy:
        ip = getattr(ipinfo_resproxy, "ip", None)
        if ip:
            return HttpResponse(f"Resproxy for: {ip}", status=200)
        return HttpResponse("Empty resproxy response.", status=200)

    return HttpResponse("Request filtered.", status=200)


urlpatterns = [
    path("test_view/", test_view),
    path("test_resproxy_view/", test_resproxy_view),
]
