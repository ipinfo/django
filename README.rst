The official Django library for the `IPinfo <https://ipinfo.io/>`_ API.
###########################################################################

`ipinfo_django` is a Django middleware plugin for the IPinfo API, which provides up-to-date IP address data. It intercepts the `HttpRequest` object and adds the attribute `HttpRequest.ipinfo`, which is an `IPinfo.Details` object.

.. contents::

.. section-numbering::

Usage
=====

Once configured, `ipinfo_django` will make IP address data accessible within Django's `HttpRequest` object. The following view from the `view.py` file::

    from django.http import HttpResponse

    def location(request):
        response_string = 'The IP address {} is located at the coordinates {}, which is in the city {}.'.format(
            request.ipinfo.ip,
            request.ipinfo.city,
            request.ipinfo.loc
        )

    return HttpResponse(response_string)

will return the following as an `HttpResponse` object::

    'The IP address 216.239.36.21 is located at the coordinates 37.8342,-122.2900, which is in the city Emeryville.'

Setup
=====

Setup can be accomplished in three steps:

1. Install with `pip`

>>> pip install ipinfo_django

2. Add `'ipinfo_django.middleware.ipinfo'` to `settings.MIDDLEWARE` in `settings.py`::

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        ...
        'ipinfo_django.middleware.IPinfo',
    ]

3. Optionally, configure with custom settings in `settings.py`::

    IPINFO_TOKEN = '123456789abc'
    IPINFO_SETTINGS = {
                        'cache_options': {
                            'ttl':30, 
                            'maxsize': 128
                        }, 
                        'countries_file': 'custom_countries.json'
                    }
    IPINFO_FILTER = lambda request: request.scheme == 'http'

Details Data
=============
`HttpRequest.ipinfo` is a `Details` object that contains all fields listed `IPinfo developer docs <https://ipinfo.io/developers/responses#full-response>`_ with a few minor additions. Properties can be accessed directly.

>>> request.ipinfo.hostname
cpe-104-175-221-247.socal.res.rr.com


Country Name
------------

`HttpRequest.ipinfo.country_name` will return the country name, as supplied by the `countries.json` file. See below for instructions on changing that file for use with non-English languages. `HttpRequest.ipinfo.country` will still return country code.

>>> request.ipinfo.country
US
>>> request.ipinfo.country_name
United States

IP Address
----------

`HttpRequest.ipinfo.ip_address` will return the an `ipaddress` object from the `Python Standard Library <https://docs.python.org/3/library/ipaddress.html>`_. `details.ip` will still return a string.

>>> request.ipinfo.ip
104.175.221.247
>>> type(request.ipinfo.ip)
<class 'str'>
>>> request.ipinfo.ip_address
104.175.221.247
>>> type(request.ipinfo.ip_address)
<class 'ipaddress.IPv4Address'>

Longitude and Latitude
----------------------

`HttpRequest.ipinfo.latitude` and `HttpRequest.ipinfo.longitude` will return latitude and longitude, respectively, as strings. `HttpRequest.ipinfo.loc` will still return a composite string of both values.

>>> request.ipinfo.loc
34.0293,-118.3570
>>> request.ipinfo.latitude
34.0293
>>> request.ipinfo.longitude
-118.3570

Accessing all properties
------------------------

`HttpRequest.ipinfo.all` will return all details data as a dictionary.

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

Authentication
==============
The IPinfo library can be authenticated with your IPinfo API token, which is set in the `settings.py` file. It also works without an authentication token, but in a more limited capacity. From `settings.py`::

    IPINFO_TOKEN = '123456789abc'

Caching
=======
In-memory caching of `details` data is provided by default via the `cachetools <https://cachetools.readthedocs.io/en/latest/>`_ library. This uses an LRU (least recently used) cache with a TTL (time to live) by default. This means that values will be cached for the specified duration; if the cache's max size is reached, cache values will be invalidated as necessary, starting with the oldest cached value.

Modifying cache options
-----------------------

Cache behavior can be modified by setting the `cache_options` key in `settings.IPINFO_SETTINGS`. `cache_options` is a dictionary in which the keys are keyword arguments specified in the `cachetools` library. The nesting of keyword arguments is to prevent name collisions between this library and its dependencies.

* Default maximum cache size: 4096 (multiples of 2 are recommended to increase efficiency)
* Default TTL: 24 hours (in seconds)

From `settings.py`::

    IPINFO_SETTINGS = {
        'cache_options': {'ttl':30, 'maxsize': 128},
    }

Using a different cache
-----------------------

It's possible to use a custom cache by creating a child class of the `CacheInterface <https://github.com/jhtimmins/ipinfo-python/blob/master/cache/interface.py>`_ class and setting the `cache` value in `settings.IPINFO_SETTINGS`. FYI this is known as `the Strategy Pattern <https://sourcemaking.com/design_patterns/strategy>`_.

From `settings.py`::

    IPINFO_SETTINGS = {'cache': my_fancy_custom_cache_object}

Internationalization
====================
When looking up an IP address, the response object includes a `details.country_name` attribute which includes the country name based on American English. It is possible to return the country name in other languages by setting the `countries_file` keyword argument in `settings.py`.

The file must be a `.json` file with the following structure::

    {
     "BD": "Bangladesh",
     "BE": "Belgium",
     "BF": "Burkina Faso",
     "BG": "Bulgaria"
     ...
    }

From `settings.py`::

    IPINFO_SETTINGS = {'countries_file': 'custom_countries.json'}

Filtering
=========

By default, `ipinfo_django` filters out requests that have `bot` or `spider` in the user-agent. Instead of looking up IP address data for these requests, the `HttpRequest.ipinfo` attribute is set to `None`. This is to prevent you from unnecessarily using up requests on non-user traffic. This behavior can be switched off by modifying the `settings.IPINFO_FILTER` object in `settings.py`.

To turn off filtering::
    
    IPINFO_FILTER = None
    
To set your own filtering rules, *thereby replacing the default filter*, you can set `settings.IPINFO_FILTER` to your own, custom callable function which satisfies the following rules:

* Accepts one request.
* Returns *True to filter out, False to allow lookup*

To use your own filter rules::

    IPINFO_FILTER = lambda request: request.scheme == 'http'

