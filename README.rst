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

A comprehensive description on how to setup ``django-oscar-stores``
will follow very soon.

License
=======

Oscar is released under the permissive `New BSD license`_.

.. _`New BSD license`: http://github.com/tangentlabs/django-oscar-stores/blob/master/LICENSE
