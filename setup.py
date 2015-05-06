#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(
    name='django-oscar-stores',
    version="1.0-dev",
    url='https://github.com/django-oscar/django-oscar-stores',
    author="David Winterbottom",
    author_email="david.winterbottom@gmail.com",
    description="An extension for Oscar to include stores",
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    keywords="django, oscar, e-commerce",
    license='BSD',
    platforms=['linux'],
    packages=find_packages(exclude=["sandbox*", "tests*"]),
    include_package_data=True,
    install_requires=[
        'django-oscar>=1.1.0dev0',
        'requests>=1.1',
    ],
    dependency_links=[
        'https://github.com/django-oscar/django-oscar/archive/master.zip#egg=django-oscar-1.1.0dev0',
    ],

    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
    ])
