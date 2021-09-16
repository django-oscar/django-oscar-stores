=========
Changelog
=========

3.0.2
=====

* Minor fixes to dashboard templates.
* Dynamically load dashboard formsets for easier overriding.
* Add blocks to dashboard templates for easier overriding.
* Move Google Maps init code to JavaScript file.

3.0.1
=====

* Add support for Django 3.2, and drop support for Django 3.0.
* Add support for Python 3.8, drop support for Python 3.6.

3.0
===

* Add support for Oscar 3.0 and refactor templates to work with Bootstrap 4.
* Add support for Django 3.1.
* Drop support for Django 2.1 and lower.


2.2
===

* Declare support for Oscar 2.1 and Django 3.0.
* Drop support for Django 1.11.
* Drop support for Python 3.5.

2.1
===

* Remove GeoIP-based location detection in the dashboard.
* Fix handling of missing images in store list view.
* Fix images in store list/detail view to be responsive.

2.0
===

* Add support for Oscar 2.0
* Drop support for Oscar 1.6 and lower, and drop support for Python 2.

1.1.1
=====

* Fix validation of empty start and end times on opening periods.

1.1
===

* Load app models dynamically to allow overriding.
* Add a `PUBLIC_HOLIDAYS` option to `OpeningPeriod.weekday` choices.

1.0
===

* Added support for Oscar 1.6, and Django 1.11 to 2.1
* Dropped support for Django 1.10 and lower.

0.8
===

* Django 1.7 support
* Fix localisation bug

0.7
===

* Load geocode service dynamically
* Drop support for Oscar 0.5

0.6.1
=====

* Support Oscar 0.7

0.6
===

* Support Django 1.6
* Templates now load assets over HTTPS where appropriate

0.5.1
=====

A couple of extensions.

* Fix cancel link for store form
* Allow HTML map box to be more easily customised
* Allow search results to be distance limited

0.5
===

* Support Oscar 0.6

* Support Django 0.5

0.4.1
=====

* Allow opening hours form to pick up new fields.

0.4
===

* Upgrade to Oscar 0.5.  This involves upgrading the JS to use jQuery 1.9 and
  adjusting the dashboard templates.

* Improve support for multiple opening hours for a single day.

* Tests now run on Travis.  Test coverage is monitored on coveralls.io

* Allow GeoIP to be disabled with a setting.
