from django.http import HttpResponse
from django.urls import path


async def test_view(request):
    ipinfo = getattr(request, "ipinfo", None)

    if ipinfo:
        return HttpResponse(f"For testing: {ipinfo.ip}", status=200)

    return HttpResponse("Request filtered.", status=200)


urlpatterns = [path("test_view/", test_view)]
