#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-oscar-stores',
    version="0.0.1a",
    url='https://github.com/tangentlabs/django-oscar-stores',
    author="Sebastian Vetter",
    author_email="sebastian.vetter@tangentsnowball.com.au",
    description="An extension for Oscar to include store locations",
    long_description=open('README.rst').read(),
    keywords="django, oscar, e-commerce",
    license='BSD',
    platforms=['linux'],
    packages=find_packages(exclude=["sandbox*", "tests*"]),
    include_package_data=True,
    install_requires=[
        'Django>=1.4.1',
        'django-oscar>=0.3.3',
        'django-model-utils>=1.1.0',
    ],
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Operating System :: Unix',
      'Programming Language :: Python'
    ]
)
