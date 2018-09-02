from setuptools import setup

setup(name='ipinfo_django',
      version='0.1.0',
      description='Official Django library for IPinfo',
      url='https://github.com/ipinfo/django',
      author='James Timmins',
      author_email='jameshtimmins@gmail.com',
      license='Apache License 2.0',
      packages=['ipinfo_django'],
      install_requires=[
        'django',
      ],
      zip_safe=False)