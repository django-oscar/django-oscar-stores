================================================
Store Extension for the Oscar Ecommerce Platform
================================================

.. image:: https://secure.travis-ci.org/elbaschid/django-oscar-stores.png
    :target: http://travis-ci.org/#!/elbaschid/django-oscar

Warning
-------
This project is currently a work in progress. It works
for the most part but there's most likely unfixed issues in there.
If you feel the need to try it out, use with care.
Feedback welcome :)

Introduction
============

This package is an extension to `django-oscar`_ that provides an interface to
add and update store locations as well as grouping them together. An address, a
geographical location and an arbitrary number of opening times can be specified
for each store location. Creating and editing of stores is done in the
dashboard and requires the corresponding permission.

All stores are displayed on the website in an overview map followed
by a listing of each store ordered by store groups. For each store,
the address and opening times are displayed and a link to an
individual store page is provided that shows additional
information such as a picture and a description.

.. _`django-oscar`: http://github.com/tangentlabs/django-oscar

Installation
============

``django-oscar-stores`` uses geodjango_ which is part of the regular Django
installation but has additional installation requirements for a GIS-enabled
database. GIS extensions are available for all the database backends shipped
with Django (with some limitations) for more details on setting them up please
refer to the `geodjango's installation guide`_.

Setting up ``django-oscar-stores`` with Oscar_ is fairly simple.  If you don't
have an Oscar project up and running please refer to its documentation_ to set
it up. With your Oscar project ready to go, you can install
``django-oscar-stores`` simply by running::

    pip install django-oscar-stores

Now that you have the stores app installed, all you need to do
add it to your ``INSTALLED_APPS`` settings::

    INSTALLED_APPS = [
        ....
        'stores',
        ....
    ]

and update your ``urls.py`` to be able to access the stores section
in the dashboard and see the overview and detail pages for stores. A
sample configuration (as used in the sandbox) might look similar to
this::

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
    )

You also need to include the default settings::

    from stores.defaults import *

And that's all you need to do. Running the server of your Oscar project, you
should now have access to the `store manager`_ in the dashboard as well as a
overview_ page displayed to your customers.

Setting up *spatialite* in Ubuntu
---------------------------------

I am using *spatialite* for local development and found the install
instructions on geodjango_ a bit too much as most of the required
libaries come packed for Ubuntu. In general, all you have to do
to setup *spatialite* is run::

    $ sudo apt-get install spatialite-bin libspatialite3 libgeos++-dev libgdal-dev libproj0

I am assuming that you want to setup the actual python package
`pysqlite`_ in ``virtualenv`` instead of installing globally. This
is it a bit tricky because *pysqlite* has extension support
disabled by default (installing through pip). One way is to download
the source, enable the extension support and install it manually.
The nicer solution is to use a *pysqlite* clone that has the support
enabled by default and can be installed from github using pip. You
can do it by either installing::

    $ pip install git+git://github.com/tinio/pysqlite.git@extension-enabled#egg=pysqlite

Or by installing all the development-specific requirements for
``django-oscar-stores`` in the ``requirements.txt`` file in the
project root::

    $ pip install -r requirements.txt

.. _Oscar: http://oscarcommerce.com
.. _documentation: http://django-oscar.readthedocs.org/en/latest
.. _`store manager`: http://localhost:8000/dashboard/stores
.. _overview: http://localhost:8000/stores
.. _geodjango: https://docs.djangoproject.com/en/1.4/ref/contrib/gis
.. _`geodjango's installation guide`: https://docs.djangoproject.com/en/1.4/ref/contrib/gis/install
.. _`pysqlite`: http://code.google.com/p/pysqlite

Contributing
============

There is sandbox site within the repo which is a sample Oscar project that uses
the stores extension.  Set this up with::

    make sandbox

A fixture is loaded which provides a superuser to test the dashboard with::

    email: superuser@example.com
    username: superuser
    password: testing


License
=======

``django-oscar-stores`` is released under the permissive `New BSD license`_.

.. _`New BSD license`: http://github.com/tangentlabs/django-oscar-stores/blob/master/LICENSE
