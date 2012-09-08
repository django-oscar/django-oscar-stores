Store Extension for the Oscar Ecommerce Platform
================================================

**NOTE:** This project is currently a work in progress. It works
for the most part but there's most likely unfixed issues in there.
If you feel the need to try it out, use with care.
Feedback welcome :)

This package is an extension to
`django-oscar`_ that
provides an interface to add and update store location and group
them together. An address, a geographical location and an
arbitrary number of opening times can be specified for each store
location. Creating and editting of stores is done in the dashboard
and requires the corresponding permission.

All stores are diplayed on the website in an overview map followed
by a listing of each store ordered by store groups. For each store
the address and opening times are displayed and a link to an
individual store page is provided that shows additional
information: such as a picture and a description.

.. _`django-oscar`: http://github.com/tangentlabs/django-oscar

Installation
============

Setting up ``django-oscar-stores`` with Oscar_ is fairly simple and
straight forward. If you don't have an Oscar project up and running
please refer to its documentation_ to set it up. With your Oscar
project ready to go, you can install ``django-oscar-stores`` simply
by running::

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

    urlpatterns = patterns('',
        # basic configuration for Oscar
        url(r'', include(shop.urls)),

        # adds URLs for the dashboard store manager
        url(r'^dashboard/stores/', include(dashboard_app.urls)),

        # adds URLs for overview and detail pages
        url(r'^stores/', include(stores_app.urls)),
    )

And that's all you need to do. Running the server of your Oscar
project, you should now have access to the `store manager`_ in
the dashboard as well as a overview_ page displayed to your
customers.


.. _Oscar: http://oscarcommerce.com
.. _documentation: http://django-oscar.readthedocs.org/en/latest/
.. _`store manager`: http://localhost:8000/dashboard/stores
.. _overview: http://localhost:8000/stores


License
=======

``django-oscar-stores`` is released under the permissive `New BSD license`_.

.. _`New BSD license`: http://github.com/tangentlabs/django-oscar-stores/blob/master/LICENSE
