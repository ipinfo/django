from setuptools import setup

description_long = 'The official Django library for IPinfo. IPinfo prides itself on being the most reliable, accurate, and in-depth source of IP address data available anywhere. We process terabytes of data to produce our custom IP geolocation, company, carrier and IP type data sets. You can visit our developer docs at https://ipinfo.io/developers.'

setup(name='ipinfo_django',
      version='0.1.2',
      description='Official Django library for IPinfo',
      description_long=description_long,
      url='https://github.com/ipinfo/django',
      author='James Timmins',
      author_email='jameshtimmins@gmail.com',
      license='Apache License 2.0',
      packages=['ipinfo_django'],
      install_requires=[
        'django',
        'ipinfo_wrapper',
      ],
      zip_safe=False)
