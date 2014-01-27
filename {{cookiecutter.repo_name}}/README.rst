{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}

Developer Installation
-----------------------

For getting this running on your local machine:


1. Set up a virtualenv.
2. Install all the supporting libraries into your virtualenv::

    pip install -r requirements/local.txt

3. Install Grunt Dependencies.

    npm install

4. Run development server. (For browser auto-reload, use Livereload_ plugins.)

    grunt serve

.. _livereload: https://github.com/gruntjs/grunt-contrib-watch#using-live-reload-with-the-browser-extension

