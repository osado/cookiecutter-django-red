cookiecutter-django-red
========================

Soviet cookiecutter_ template for Django.

.. _cookiecutter: https://github.com/audreyr/cookiecutter

Features
---------

* Cutting edge: For Django 1.6 and other bleeding edge stuff
* Twitter Bootstrap 3
* AngularJS
* Registration via django-allauth
* User avatars via django-avatar

Отличия от оригинального cookiecutter-django
=============================================

* Деплой и управление через Fabric
* Запуск через uwsgi (+ nginx)
* Redis для кеша
* django-compressor + локальные копии bootstrap, AngularJS и прочего
* оставлен django-storages, но по умолчанию локальный storage


Constraints
------------

* Only maintained 3rd party libraries are used.
* PostgreSQL everywhere
* Environment variables for configuration (This won't work with Apache/mod_wsgi)

Caution: Bleeding Edge Requirements
------------------------------------

The cookiecutter-django project is bleeding edge in that it uses unreleased versions of several packages like Django,
South, django-crispy-forms, django-avatar, and more. 

Consider yourself warned.

Usage
------

First, get cookiecutter. Trust me, it's awesome::

    $ pip install cookiecutter

Now run it against this repo::

    $ cookiecutter https://github.com/osado/cookiecutter-django.git

You'll be prompted for some questions, answer them, then it will create a Django project for you.

Не совсем то, что вам нужно?
-----------------------------

Это то, что МНЕ нужно. *Это может быть не то, что нужно вам.* Просто форкните и сделайте по своему.

Or Submit a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~~

I also accept pull requests on this, if they're small, atomic, and if they make my own project development
experience better. 
