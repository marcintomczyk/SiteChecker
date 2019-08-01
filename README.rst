=====
Site Checker
=====

The Site Checker is a simple Django app for checking the status of remote web sites.
Key things to note:

- app was created as 'reusable app' in django terms (see Introduction below)
- structure of the code was enhanced to some extent ie: default files such as views.py, models.py were 'transformed'
  to packages so when more code appear it would be for example easier to maintain/develop etc.
- some async were introduced (including tests)
- it was created using Python 3.6

Introduction
-----------
This app is intended to be build as python package
ie: python setup.py sdist - run from inside the folder where setup.py is present)

- when the app is build it can be installed via pip install and used in parent project
- in terms of django vocabulary etc. this code is a django app which is some kind of submodule something bigger
and this 'bigger' is django project

How to add the site_checker app to the django project
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


-- TESTS
1. To execute tests invoke the following command from the directory of the main project:
   python manage.py test site_checker
2. Some tests are async ones
   - It's very important to use the correct version of asynctest library ( I have asynctest==0.13.0)
     - as stated in 'https://github.com/Martiusweb/asynctest/issues/29' versions below 0.11.1 don't support
       two very important methods (__aentry__, __aexit__) which causes problems
   - there are other tools for async testing ie: django-async-test but the current version uses asynctest in version 0.7, so in case of installing/having it it might be worth
       verifying the asynctest library version

