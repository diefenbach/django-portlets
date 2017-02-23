Introduction
============

*Portlets* are content objects which are managed in *Slots*. *Slots* can be
freely defined and placed anywhere within a HTML page.

Portlets are usual content objects, that means they can have arbitrary fields
and functionalities.

There are also some more advanced features like inheriting and blocking of
portlets.

django-portlets provides just a generic engine to manage portlets. You can
find a comprehensive implementation within `LFS`_.

Example
=======
django-portlets comes with a simple example application which shows how to use it.

Documentation
=============
For more documentation please visit: http://django-portlets.rtfd.org

Changes
=======

1.5 (2017-02-23)
----------------
* Add Django 1.10 support


1.4 (2015-05-05)
----------------

* Resolves RemovedInDjango19Warnings.
* Removes deprecated functions.

1.3 (2015-04-20)
----------------

* Adds Django 1.8 support

1.2 (2014-07-08)
----------------

* Sets logging to __name__
* Moves utilities functions for Slots to the Slot model

1.1.1 (2012-03-18)
------------------
* Added polish translations (Maciej Wiśniowski)
* Added german translations

1.1 (2011-11-21)
----------------
* Added base class (from which can inherited)
* API change: changed the order of parameters for get_portlets and has_portlets

1.0 (2010-08-24)
----------------
* First final release

1.0 beta 4 (2010-07-07)
-----------------------
* Changed: cache keys are using CACHE_MIDDLEWARE_PREFIX now
* Bugfix caching: added language to cache key

1.0 beta 3 (2010-06-28)
-----------------------
* Bugfix: make registration working for postgres; issue #1
* Bugfix caching: use class name instead of content type for cache key

1.0 beta 2 (2010-05-21)
------------------------

* Improved caching
* Added license

1.0 beta 1 (2010-05-17)
-----------------------

* First beta release.

0.4.0 (2010-04-16)
------------------

* Display only registered portlets

0.3.2 (2009-10-15)
------------------

* Changed documentation to one page (for now)

* Example TextPortlet: made ``context`` paramenter of ``render`` method optional.

* Added tests for models

0.3.1 (2009-10-14)
------------------

* Added tests

* Bugfix: Check whether the content object implements ``get_parent_for_portlets``
  within ``utils.has_portlets``

0.3.0 (2009-10-12)
------------------

* Added documentation

0.2.0 (2009-10-12)
------------------

* Added simple example implementation

0.1.0 (2009-10-12)
------------------

* Initial public release

.. _LFS: http://bitbucket.org/diefenbach/django-lfs
