=====
Site Checker
=====

Site checker is a simple Django app for checking the status of remote web sites.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "site_checker" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'site_checker',
    ]

2. Include the site-checker URLconf in your project urls.py like this::

    path('site-checker/', include('site_checker.urls')),

3. Run `python manage.py migrate` to create the site_checker's models.

4. Start the development server and visit http://127.0.0.1:8000/site-checker/
   to see a view allowing to make a check request to a remote site