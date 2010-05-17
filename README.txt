What is it?
===========

*Portlets* are content objects which are managed in *Slots*. *Slots* can be 
freely defined and placed anywhere within a HTML page.

Portlets are usual content objects, that means they can have arbitrary fields 
and functionalities.

There are also some more advanced features like inheriting and blocking of
portlets.

django-portlets provides just a generic engine to manage portlets. You can
find a comprehensive implementation within `LFS`_.

Example
===========
django-portlets comes with a simple example application which shows how to use it.

Documentation
=============
For more documentation please visit: http://packages.python.org/django-portlets/

Changes
=======

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