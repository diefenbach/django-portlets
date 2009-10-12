Example
=======

django-portlets provides a simple example. If you want to see a more 
sophisticated implementation please refer to `django-lfs`_

**Installation**

1. Install `flatpages`_: (flatpages serve as our example content)

2. Add the portlets and portlets.example to INSTALLED_APPS

3. Sync the database

4. Go to django admin and:

    1. add a flatpage

    2. add a TextPortlet

    3. assign the TextPortlet to the flatpage (via PortletAssignment)

5. Browse to the flatpage

.. _`django-lfs`: http://bitbucket.org/diefenbach/django-lfs.
.. _`flatpages`: http://docs.djangoproject.com/en/dev/ref/contrib/flatpages/ 