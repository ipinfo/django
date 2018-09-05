from setuptools import setup

setup(name='ipinfo_django',
      version='0.1.1',
      description='Official Django library for IPInfo',
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
