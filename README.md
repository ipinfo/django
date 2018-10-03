# <img src="https://ipinfo.io/static/ipinfo-small.svg" alt="IPinfo" width="24"/> IPinfo Django Client Library

This is the official Django client library for the [IPinfo.io](https://ipinfo.io) IP address API, allowing you to lookup your own IP address, or get any of the following details for an IP:
 - IP geolocation (city, region, country, postal code, latitude and longitude)
 - ASN details (ISP or network operator, associated domain name, and type, such as business, hosting or company)
 - Company details (the name and domain of the business that uses the IP address)
 - Carrier details (the name of the mobile carrier and MNC and MCC for that carrier if the IP is used exclusively for mobile traffic)


### Getting Started

You'll need an IPinfo API access token, which you can get by singing up for a free account at [https://ipinfo.io/signup](https://ipinfo.io/signup?ref=lib-Python).

The free plan is limited to 1,000 requests a day, and doesn't include some of the data fields such as IP type and company data. To enable all the data fields and additional request volumes see [https://ipinfo.io/pricing](https://ipinfo.io/pricing?ref=lib-Python)

#### Installation

```
pip install ipinfo_django
```

#### Quickstart

Once configured, `ipinfo_django` will make IP address data accessible within Django's `HttpRequest` object. The following view from the `view.py` file:

```
from django.http import HttpResponse

def location(request):
    response_string = 'The IP address {} is located at the coordinates {}, which is in the city {}.'.format(
        request.ipinfo.ip,
        request.ipinfo.city,
        request.ipinfo.loc
    )

    return HttpResponse(response_string)
```

will return the following as an `HttpResponse` object:

    'The IP address 216.239.36.21 is located at the coordinates 37.8342,-122.2900, which is in the city Emeryville.'

### Setup

Setup can be accomplished in three steps:

1. Install with `pip`

```
>>> pip install ipinfo_django
```

2. Add `'ipinfo_django.middleware.ipinfo'` to `settings.MIDDLEWARE` in `settings.py`:

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
    'ipinfo_django.middleware.IPinfo',
    ]
```

3. Optionally, configure with custom settings in `settings.py`:

```
IPINFO_TOKEN = '123456789abc'
IPINFO_SETTINGS = {
                    'cache_options': {
                        'ttl':30,
                        'maxsize': 128
                    },
                    'countries_file': 'custom_countries.json'
                }
IPINFO_FILTER = lambda request: request.scheme == 'http'
```

### Details Data

`HttpRequest.ipinfo` is a `Details` object that contains all fields listed [IPinfo developer docs](https://ipinfo.io/developers/responses#full-response) with a few minor additions. Properties can be accessed directly.

```
>>> request.ipinfo.hostname
cpe-104-175-221-247.socal.res.rr.com
```

#### Country Name

`HttpRequest.ipinfo.country_name` will return the country name, as supplied by the `countries.json` file. See below for instructions on changing that file for use with non-English languages. `HttpRequest.ipinfo.country` will still return country code.

```
>>> request.ipinfo.country
US
>>> request.ipinfo.country_name
United States
```

#### IP Address

`HttpRequest.ipinfo.ip_address` will return the an `ipaddress` object from the [Python Standard Library](https://docs.python.org/3/library/ipaddress.html). `details.ip` will still return a string.

```
>>> request.ipinfo.ip
104.175.221.247
>>> type(request.ipinfo.ip)
<class 'str'>
>>> request.ipinfo.ip_address
104.175.221.247
>>> type(request.ipinfo.ip_address)
<class 'ipaddress.IPv4Address'>
```

#### Longitude and Latitude

`HttpRequest.ipinfo.latitude` and `HttpRequest.ipinfo.longitude` will return latitude and longitude, respectively, as strings. `HttpRequest.ipinfo.loc` will still return a composite string of both values.

```
>>> request.ipinfo.loc
34.0293,-118.3570
>>> request.ipinfo.latitude
34.0293
>>> request.ipinfo.longitude
-118.3570
```

#### Accessing all properties

`HttpRequest.ipinfo.all` will return all details data as a dictionary.

```
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
'ip_address': IPv4Address('104.175.221.247'),
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

```
IPINFO_TOKEN = '123456789abc'
```

### Caching

In-memory caching of `details` data is provided by default via the `cachetools <https://cachetools.readthedocs.io/en/latest/>`_ library. This uses an LRU (least recently used) cache with a TTL (time to live) by default. This means that values will be cached for the specified duration; if the cache's max size is reached, cache values will be invalidated as necessary, starting with the oldest cached value.

#### Modifying cache options

Cache behavior can be modified by setting the `cache_options` key in `settings.IPINFO_SETTINGS`. `cache_options` is a dictionary in which the keys are keyword arguments specified in the `cachetools` library. The nesting of keyword arguments is to prevent name collisions between this library and its dependencies.

* Default maximum cache size: 4096 (multiples of 2 are recommended to increase efficiency)
* Default TTL: 24 hours (in seconds)

From `settings.py`:

```
IPINFO_SETTINGS = {
    'cache_options': {'ttl':30, 'maxsize': 128},
}
```

#### Using a different cache

It's possible to use a custom cache by creating a child class of the [CacheInterface](https://github.com/ipinfo/python/blob/master/ipinfo/cache/interface.py) class and setting the `cache` value in `settings.IPINFO_SETTINGS`. FYI this is known as [the Strategy Pattern](https://sourcemaking.com/design_patterns/strategy).

From `settings.py`:

```
IPINFO_SETTINGS = {'cache': my_fancy_custom_cache_object}
```

### Internationalization

When looking up an IP address, the response object includes a `details.country_name` attribute which includes the country name based on American English. It is possible to return the country name in other languages by setting the `countries_file` keyword argument in `settings.py`.

The file must be a `.json` file with the following structure:

```
{
 "BD": "Bangladesh",
 "BE": "Belgium",
 "BF": "Burkina Faso",
 "BG": "Bulgaria"
 ...
}
```

From `settings.py`:

```
IPINFO_SETTINGS = {'countries_file': 'custom_countries.json'}
```

### Filtering

By default, `ipinfo_django` filters out requests that have `bot` or `spider` in the user-agent. Instead of looking up IP address data for these requests, the `HttpRequest.ipinfo` attribute is set to `None`. This is to prevent you from unnecessarily using up requests on non-user traffic. This behavior can be switched off by modifying the `settings.IPINFO_FILTER` object in `settings.py`.

To turn off filtering:

```
IPINFO_FILTER = None
```

To set your own filtering rules, *thereby replacing the default filter*, you can set `settings.IPINFO_FILTER` to your own, custom callable function which satisfies the following rules:

* Accepts one request.
* Returns *True to filter out, False to allow lookup*

To use your own filter rules:

```
IPINFO_FILTER = lambda request: request.scheme == 'http'
```

### Other Libraries

There are official IPinfo client libraries available for many languages including PHP, Go, Java, Ruby, and many popular frameworks such as Django, Rails and Laravel. There are also many third party libraries and integrations available for our API.

### About IPinfo

Founded in 2013, IPinfo prides itself on being the most reliable, accurate, and in-depth source of IP address data available anywhere. We process terabytes of data to produce our custom IP geolocation, company, carrier and IP type data sets. Our API handles over 12 billion requests a month for 100,000 businesses and developers.

![image](https://avatars3.githubusercontent.com/u/15721521?s=128&u=7bb7dde5c4991335fb234e68a30971944abc6bf3&v=4)
