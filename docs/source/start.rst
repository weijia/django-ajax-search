Getting started
---------------
---------------

- Python 2.6 or Python 2.7
- `Django <http://www.djangoproject.com/>`_ >= 1.3
- `jQuery <http://jquery.com/>`_ >= 1.4.4

To install::
    
    easy_install django-ajax-search

Next add `ajax-search` to your `INSTALLED_APPS` to include the related css/js::

    INSTALLED_APPS = (
        'django.contrib.staticfiles',
        # Other apps here
        'ajax-search',
    )

The jQuery and jQuery UI libraries are not included in the distribution but must be included
in your templates. See the example project for an example using these libraries from the
Google CDN.

Once installed you should add the urls to your root url patterns::

    urlpatterns = patterns('',
        # Other patterns go here
        url(r'^ajax-search/',include('ajax-search.urls')),
    )

Now that you're done with the setup, :doc:`configure your installation</config>`.
