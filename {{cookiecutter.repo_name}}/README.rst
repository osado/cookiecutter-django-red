{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}


Deployment
------------

* heroku create
* heroku addons:add heroku-postgresql:dev
* heroku addons:add pgbackups
* heroku addons:add sendgrid:starter
* heroku addons:add memcachier:dev
* heroku pg:promote HEROKU_POSTGRESQL_COLOR
* heroku config:add DJANGO_CONFIGURATION=Production
* heroku config:add DJANGO_SECRET_KEY=RANDOM_SECRET_KEY
* heroku config:add DJANGO_AWS_ACCESS_KEY_ID=YOUR_ID
* heroku config:add DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_KEY
* heroku config:add DJANGO_AWS_STORAGE_BUCKET_NAME=BUCKET
* git push heroku master