What is it?
===========

Portlets are pieces of content which are managed in Slots. Slots can be freely defined and placed 
anywhere within a HTML page. There are also some more advanced features like inheriting and blocking 
of portlets.

django-portlets provides just a generic engine to manage portlets. You can find a comprehensive 
implementation within `LFS`_.

Example
===========
django-portlets comes with a simple example application which shows how to use it.

.. _LFS: http://bitbucket.org/diefenbach/django-lfs

Changes
=======

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