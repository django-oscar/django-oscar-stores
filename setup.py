#!/usr/bin/env python
import os

from setuptools import find_packages, setup

setup(
    name='django-oscar-stores',
    version="2.0",
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
        'django-oscar>=2.0,<2.1',
        'requests>=1.1',
        'sorl-thumbnail>=12.4.1,<12.5',
    ],

    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ])
