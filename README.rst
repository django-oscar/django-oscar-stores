============
Oscar stores
============

.. image:: https://secure.travis-ci.org/django-oscar/django-oscar-stores.png
    :target: http://travis-ci.org/#!/django-oscar/django-oscar-stores

.. image:: https://coveralls.io/repos/django-oscar/django-oscar-stores/badge.png?branch=master
    :alt: Coverage
    :target: https://coveralls.io/r/django-oscar/django-oscar-stores

This is an extension for django-oscar_ that adds support for stores.  It
provides:

.. _django-oscar: https://github.com/django-oscar/django-oscar

* A store locator page using Google maps for geocoding.  It also supports using
  the browser's location to show the nearest stores.
* Store detail pages including opening hours
* Store groups
* A dashboard for managing stores

It's highly extensible and can be used as a foundation for building sophisticated
stores functionality within Oscar sites.

Screenshots
-----------

Customer-facing pages:

.. image:: https://github.com/django-oscar/django-oscar-stores/raw/master/docs/images/locator.thumb.png
    :target: https://github.com/django-oscar/django-oscar-stores/raw/master/docs/images/locator.png

.. image:: https://github.com/django-oscar/django-oscar-stores/raw/master/docs/images/detail.thumb.png
    :target: https://github.com/django-oscar/django-oscar-stores/raw/master/docs/images/detail.png

Dashboard pages:

.. image:: https://github.com/django-oscar/django-oscar-stores/raw/master/docs/images/dashboard-list.thumb.png
    :target: https://github.com/django-oscar/django-oscar-stores/raw/master/docs/images/dashboard-list.png

.. image:: https://github.com/django-oscar/django-oscar-stores/raw/master/docs/images/dashboard-detail.thumb.png
    :target: https://github.com/django-oscar/django-oscar-stores/raw/master/docs/images/dashboard-detail.png

Dependencies
------------

GeoDjango_ is used so a spatial database is required.  We recommend PostGIS.
Django's docs include some `installation instructions`_ although it is renowned
for being tricky.

.. _GeoDjango: https://docs.djangoproject.com/en/1.4/ref/contrib/gis
.. _`installation instructions`: https://docs.djangoproject.com/en/1.4/ref/contrib/gis/install

Spatialite is another option although it can be tricky to set up.  On Ubuntu,
you can do the following:

.. code:: bash

    $ sudo apt-get install spatialite-bin libspatialite3 libgeos++-dev libgdal-dev libproj0

The ``pysqlite`` python package is also required although it doesn't support C
extensions by default.  To work-around this, there are two options:

1. Download the package, edit ``setup.cfg`` to enable C extensions and install:

.. code:: bash

    $ pip install pysqlite --no-install
    $ vim $VIRTUAL_ENV/build/pysqlite/setup.cfg
    $ pip install pysqlite

2. Use a custom branch:

.. code:: bash

   $ pip install git+git://github.com/tinio/pysqlite.git@extension-enabled#egg=pysqlite

.. _`pysqlite`: http://code.google.com/p/pysqlite

Installation
------------

First, ensure you are using a spatial database and have django-oscar installed.

Install package:

.. code:: bash
    $ pip install django-oscar-stores

then add ``stores`` to ``INSTALLED_APPS``.  Now update your root ``urls.py``:

.. code:: python

    from oscar.app import shop
    from stores.app import application as stores_app
    from stores.dashboard.app import application as dashboard_app

    urlpatterns = patterns('',
        # basic configuration for Oscar
        url(r'', include(shop.urls)),

        # adds URLs for the dashboard store manager
        url(r'^dashboard/stores/', include(dashboard_app.urls)),

        # adds URLs for overview and detail pages
        url(r'^stores/', include(stores_app.urls)),

        # adds internationalization URLs
        (r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
    )

You also need to download the `GeoIP data files`_ and set ``GEOIP_PATH`` to point to the
appropriate directory.

.. _`GeoIP data files`: https://docs.djangoproject.com/en/dev/ref/contrib/gis/geoip/

Settings
--------

* ``STORES_GEOGRAPHIC_SRID`` (default: ``3577``).  This is used for distance
  calculations.  See http://spatialreference.org for more details.

* ``STORES_GEODETIC_SRID`` (default: ``4326``).

* ``STORES_MAX_SEARCH_DISTANCE`` (default: None). This filters stores
  in queries by distance. Units can be set using distance object:

.. code:: python

    from django.contrib.gis.measure import D
    # Maximal distance of 150 miles
    STORES_MAX_SEARCH_DISTANCE = D(mi=150)
    # Maximal distance of 150 kilometers
    STORES_MAX_SEARCH_DISTANCE = D(km=150)

Contributing
------------

There is sandbox site within the repo which is a sample Oscar project that uses
the stores extension.  Set this up with:

.. code:: bash

    $ make sandbox

then fetch the GeoIP files with:

.. code:: bash

    $ make geoip

This loads a fixture which provides a superuser to test the dashboard with::

    email: superuser@example.com
    username: superuser
    password: testing

Run tests with:

.. code:: bash

    $ ./runtests.py

License
-------

``django-oscar-stores`` is released under the permissive `New BSD license`_.

.. _`New BSD license`: http://github.com/django-oscar/django-oscar-stores/blob/master/LICENSE
