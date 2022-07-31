# [<img src="https://ipinfo.io/static/ipinfo-small.svg" alt="IPinfo" width="24"/>](https://ipinfo.io/) IPinfo Django Client Library

This is the official Django client library for the [IPinfo.io](https://ipinfo.io) IP address API, allowing you to lookup your own IP address, or get any of the following details for an IP:

- [IP to geolocation](https://ipinfo.io/ip-geolocation-api) (city, region, country, postal code, latitude and longitude)
- [IP to ASN](https://ipinfo.io/asn-api) (ISP or network operator, associated domain name, and type, such as business, hosting or company)
- [IP to Company](https://ipinfo.io/ip-company-api) (the name and domain of the business that uses the IP address)
- [IP to Carrier](https://ipinfo.io/ip-carrier-api) (the name of the mobile carrier and MNC and MCC for that carrier if the IP is used exclusively for mobile traffic)

Check all the data we have for your IP address [here](https://ipinfo.io/what-is-my-ip).

### Getting Started

You'll need an IPinfo API access token, which you can get by signing up for a free account at [https://ipinfo.io/signup](https://ipinfo.io/signup).

The free plan is limited to 50,000 requests per month, and doesn't include some of the data fields such as IP type and company data. To enable all the data fields and additional request volumes see [https://ipinfo.io/pricing](https://ipinfo.io/pricing)

#### Installation

```bash
pip install ipinfo_django
```

#### Quickstart

Once configured, `ipinfo_django` will make IP address data accessible within Django's `HttpRequest` object. The following view from the `view.py` file:

```python
from django.http import HttpResponse

def location(request):
    response_string = 'The IP address {} is located at the coordinates {}, which is in the city {}.'.format(
        request.ipinfo.ip,
        request.ipinfo.loc,
        request.ipinfo.city
    )

    return HttpResponse(response_string)
```

will return the following as an `HttpResponse` object:

```python
'The IP address 216.239.36.21 is located at the coordinates 37.8342,-122.2900, which is in the city Emeryville.'
```

To get the details of user defined IP, we will import ipinfo package directly to the `view.py` file:
```python
from django.shortcuts import render
from django.http import HttpResponse 
from django.conf import settings
import ipinfo



def get_ip_details(ip_address=None):
	ipinfo_token = getattr(settings, "IPINFO_TOKEN", None)
	ipinfo_settings = getattr(settings, "IPINFO_SETTINGS", {})
	ip_data = ipinfo.getHandler(ipinfo_token, **ipinfo_settings)
	ip_data = ip_data.getDetails(ip_address)
	return ip_data

def location(request): 

	ip_data = get_ip_details('168.156.54.5')

	response_string = 'The IP address {} is located at the coordinates {}, which is in the city {}.'.format(ip_data.ip,ip_data.loc,ip_data.city)

	return HttpResponse(response_string)

```

The above code will print the IP details provide. We can use GET and POST methods to get the details of user defined IP
```python
'The IP address 168.156.54.5 is located at the coordinates 47.6104,-122.2007, which is in the city Bellevue.'
```

### Setup

Setup can be accomplished in three steps:

1. Install with `pip`

```bash
pip install ipinfo_django
```

2. Add `'ipinfo_django.middleware.ipinfo'` to `settings.MIDDLEWARE` in `settings.py`:

```python
MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  ...
  'ipinfo_django.middleware.IPinfo',
]
```

3. Optionally, configure with custom settings in `settings.py`:

```python
IPINFO_TOKEN = '123456789abc'
IPINFO_SETTINGS = {
  'cache_options': {
      'ttl':30,
      'maxsize': 128
  },
  'countries_file': 'custom_countries.json'
}
IPINFO_FILTER = lambda request: request.scheme == 'http'
IPINFO_IP_SELECTOR = my_custom_ip_selector_implementation
```
   
### Async support

`'ipinfo_django.middleware.IPinfoAsyncMiddleware'` can be used under ASGI. This is an async-only middleware which works only when placed in an async middleware chain, that is, a chain of Django middleware which are both async and async capable. For example:

```python
MIDDLEWARE = [
  'package_b.middleware.ExampleSyncAndAsyncMiddleware',
  'ipinfo_django.middleware.IPinfoAsyncMiddleware',
  'package_a.middleware.ExampleAsyncMiddleware',
]
```

See [asynchronous-support](https://docs.djangoproject.com/en/4.0/topics/http/middleware/#asynchronous-support) for more.

### Details Data

`HttpRequest.ipinfo` is a `Details` object that contains all fields listed [IPinfo developer docs](https://ipinfo.io/developers/responses#full-response) with a few minor additions. Properties can be accessed directly.

```python
>>> request.ipinfo.hostname
cpe-104-175-221-247.socal.res.rr.com
```

#### Country Name

`HttpRequest.ipinfo.country_name` will return the country name, as supplied by the `countries.json` file. See below for instructions on changing that file for use with non-English languages. `HttpRequest.ipinfo.country` will still return country code.

```python
>>> request.ipinfo.country
US
>>> request.ipinfo.country_name
United States
```

#### IP Address

`HttpRequest.ipinfo.ip` will return an IP string.

```python
>>> request.ipinfo.ip
104.175.221.247
>>> type(request.ipinfo.ip)
<class 'str'>
```

#### Longitude and Latitude

`HttpRequest.ipinfo.latitude` and `HttpRequest.ipinfo.longitude` will return latitude and longitude, respectively, as strings. `HttpRequest.ipinfo.loc` will still return a composite string of both values.

```python
>>> request.ipinfo.loc
34.0293,-118.3570
>>> request.ipinfo.latitude
34.0293
>>> request.ipinfo.longitude
-118.3570
```

#### Accessing all properties

`HttpRequest.ipinfo.all` will return all details data as a dictionary.

```python
>>> request.ipinfo.all
{
'asn': {  'asn': 'AS20001',
           'domain': 'twcable.com',
           'name': 'Time Warner Cable Internet LLC',
           'route': '104.172.0.0/14',
           'type': 'isp'},
'city': 'Los Angeles',
'company': {   'domain': 'twcable.com',
               'name': 'Time Warner Cable Internet LLC',
               'type': 'isp'},
'country': 'US',
'country_name': 'United States',
'hostname': 'cpe-104-175-221-247.socal.res.rr.com',
'ip': '104.175.221.247',
'loc': '34.0293,-118.3570',
'latitude': '34.0293',
'longitude': '-118.3570',
'phone': '323',
'postal': '90016',
'region': 'California'
}
```

### Authentication

The IPinfo library can be authenticated with your IPinfo API token, which is set in the `settings.py` file. It also works without an authentication token, but in a more limited capacity. From `settings.py`:

```python
IPINFO_TOKEN = '123456789abc'
```

### Caching

In-memory caching of `details` data is provided by default via the `cachetools <https://cachetools.readthedocs.io/en/latest/>`_ library. This uses an LRU (least recently used) cache with a TTL (time to live) by default. This means that values will be cached for the specified duration; if the cache's max size is reached, cache values will be invalidated as necessary, starting with the oldest cached value.

#### Modifying cache options

Cache behavior can be modified by setting the `cache_options` key in `settings.IPINFO_SETTINGS`. `cache_options` is a dictionary in which the keys are keyword arguments specified in the `cachetools` library. The nesting of keyword arguments is to prevent name collisions between this library and its dependencies.

- Default maximum cache size: 4096 (multiples of 2 are recommended to increase efficiency)
- Default TTL: 24 hours (in seconds)

From `settings.py`:

```python
IPINFO_SETTINGS = {
    'cache_options': {
        'ttl': 30,
        'maxsize': 128
    }
}
```

#### Using a different cache

It's possible to use a custom cache by creating a child class of the [CacheInterface](https://github.com/ipinfo/python/blob/master/ipinfo/cache/interface.py) class and setting the `cache` value in `settings.IPINFO_SETTINGS`. FYI this is known as [the Strategy Pattern](https://sourcemaking.com/design_patterns/strategy).

From `settings.py`:

```python
IPINFO_SETTINGS = {'cache': my_fancy_custom_cache_object}
```

### Internationalization

When looking up an IP address, the response object includes a `details.country_name` attribute which includes the country name based on American English. It is possible to return the country name in other languages by setting the `countries_file` keyword argument in `settings.py`.

The file must be a `.json` file with the following structure:

```js
{
    "BD": "Bangladesh",
    "BE": "Belgium",
    "BF": "Burkina Faso",
    "BG": "Bulgaria"
    // …
}
```

From `settings.py`:

```python
IPINFO_SETTINGS = {'countries_file': 'custom_countries.json'}
```

### Filtering

By default, `ipinfo_django` filters out requests that have `bot` or `spider` in the user-agent. Instead of looking up IP address data for these requests, the `HttpRequest.ipinfo` attribute is set to `None`. This is to prevent you from unnecessarily using up requests on non-user traffic. This behavior can be switched off by modifying the `settings.IPINFO_FILTER` object in `settings.py`.

To turn off filtering:

```python
IPINFO_FILTER = None
```

To set your own filtering rules, *thereby replacing the default filter*, you can set `settings.IPINFO_FILTER` to your own, custom callable function which satisfies the following rules:

- Accepts one request.
- Returns *True to filter out, False to allow lookup*

To use your own filter rules:

```python
IPINFO_FILTER = lambda request: request.scheme == 'http'
```

### IP Selection Mechanism

By default, the IP is used by ignoring the reverse proxies depending on whether we are behind a reverse proxy or not.

Since the desired IP by your system may be in other locations, the IP selection mechanism is configurable and some alternative built-in options are available.

#### Using built-in IP selectors

- Default IP Selector
- Client IP Selector

##### Default IP selector

A [DefaultIPSelector](https://github.com/ipinfo/django/blob/master/ipinfo_django/ip_selector/default.py) object is used by default if no IP selection mechanism is provided. It selects an IP address by trying to extract it from the `X-Forwarded-For` header. It will default to the source IP on the request if the header doesn't exist.

This selector can be set explicitly by setting the `IPINFO_IP_SELECTOR` in `settings.py` file.

```python
from ipinfo_django.ip_selector.default import DefaultIPSelector

IPINFO_IP_SELECTOR = DefaultIPSelector()
```

##### Client IP selector

A [ClientIPSelector](https://github.com/ipinfo/django/blob/master/ipinfo_django/ip_selector/remote_client.py) returns the client IP address from the incoming request.

This selector can be set by setting the `IPINFO_IP_SELECTOR` in `settings.py`file.

```python
from ipinfo_django.ip_selector.remote_client import ClientIPSelector

IPINFO_IP_SELECTOR = ClientIPSelector()
```

#### Using a custom IP selector

In case a custom IP selector is required, you may implement the [IPSelectorInterface](https://github.com/ipinfo/django/blob/master/ipinfo_django/ip_selector/interface.py) and pass the instance to `IPINFO_IP_SELECTOR` in `settings.py` file.

For example:

```python
IPINFO_IP_SELECTOR = my_custom_ip_selector_implementation
```

### Errors

If there's an error while making a request to IPinfo (e.g. your token was rate
limited, there was a network issue, etc.), then the traceback will be logged
using the built-in Python logger, and `HttpRequest.ipinfo` will be `None`.

### Local development and testing

To test the project locally, install Tox in your Python virtual environment:

```bash
pip install tox
```

Then, run Tox:

```bash
PYTHONPATH=. tox
```

### Other Libraries

There are official IPinfo client libraries available for many languages including PHP, Go, Java, Ruby, and many popular frameworks such as Django, Rails and Laravel. There are also many third party libraries and integrations available for our API.

### About IPinfo

Founded in 2013, IPinfo prides itself on being the most reliable, accurate, and in-depth source of IP address data available anywhere. We process terabytes of data to produce our custom IP geolocation, company, carrier, VPN detection, hosted domains, and IP type data sets. Our API handles over 40 billion requests a month for 100,000 businesses and developers.

[![image](https://avatars3.githubusercontent.com/u/15721521?s=128&u=7bb7dde5c4991335fb234e68a30971944abc6bf3&v=4)](https://ipinfo.io/)
