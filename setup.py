from setuptools import setup

long_description = """
The official Django library for IPinfo.

IPinfo prides itself on being the most reliable, accurate, and in-depth source of IP address data available anywhere.
We process terabytes of data to produce our custom IP geolocation, company, carrier and IP type data sets.
You can visit our developer docs at https://ipinfo.io/developers.
"""

setup(
    name="ipinfo_django",
    version="1.0.0",
    description="Official Django library for IPinfo",
    long_description=long_description,
    url="https://github.com/ipinfo/django",
    author="IPinfo",
    author_email="support@ipinfo.io",
    license="Apache License 2.0",
    packages=["ipinfo_django"],
    install_requires=["django", "ipinfo==2.0.0"],
    zip_safe=False,
)
