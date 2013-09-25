# -*- coding: utf-8 -*-
# Nikolay Udalov (nikolaj.udalov@gmail.com)
from fabric.api import *

env.hosts = ['{{cookiecutter.remote_host}}']
code_dir = '{{cookiecutter.remote_path}}'

@task
def commit(description):
	local('git status')
	prompt('Press <Enter> to continue or <Ctrl+C> to cancel.')
	local(u"git commit -a -m '%s'" % description)
	local('git push')

@task
def lint():
	env.warn_only = True
	ret = local("django-lint -f colorized -r")
	env.warn_only = False
	if ret.return_code == 6:
		abort('Aborted, see django-lint errors')

@task
def remote_deploy():
	with cd(code_dir):
		env.warn_only = True
		run("git pull")
		run("touch %sreload.wsgi" % code_dir)
		env.warn_only = False

@task
def deploy(description):
	commit(description)
	remote_deploy()


def run_manage(cmd, lr):
	if lr == 'local':
		local('venv/bin/python {{cookiecutter.repo_name}}/manage.py %s --settings=config.settings' % cmd)
	else:
		run('venv/bin/python {{cookiecutter.repo_name}}/manage.py %s --settings=config.settings' % cmd)

@task
def create_db(side='local'):
	if side == 'local':
		local('psql -U postgres -c "drop database if exists {{cookiecutter.repo_name}}"')
		local('psql -U postgres -c "create database {{cookiecutter.repo_name}}"')
	run_manage("syncdb --noinput", side)
	run_manage("migrate", side)
	run_manage("collectstatic", side)
	print """
from django.contrib.sites.models import Site;
site = Site.objects.get()
site.domain = "{{cookiecutter.domain_name}}"
site.name = "{{cookiecutter.project_name}}"
site.save()"""
	shell()
	

@task
def venv(side='local'):
	apt = "apt-get install build-essential python-dev libxml2-dev libxslt1-dev libjpeg-turbo8-dev libjpeg8-dev libfreetype6-dev libwebp-dev libmemcached-dev libtidy-dev"
	if p == 'local':
		local("sudo %s" % apt)
		local("virtualenv venv/")
	else:
		run("%s" % apt)
		with cd(code_dir):
			run("virtualenv venv/")

@task
def pip(side='local'):
	if p == 'local':
		local("venv/bin/pip install -r requirements/local.txt")
	else:
		with cd(code_dir):
			run("venv/bin/pip install -r requirements/production.txt")

@task
def devserver():
	local("venv/bin/python {{cookiecutter.repo_name}}/manage.py runserver_plus 0.0.0.0:8000 --settings=config.settings")

@task
def rq():
	local("venv/bin/python {{cookiecutter.repo_name}}/manage.py rqworker default --settings=config.settings")

@task
def shell():
	local("venv/bin/python {{cookiecutter.repo_name}}/manage.py shell --settings=config.settings")

@task
def cpdb():
	run("pg_dump -U postgres {{cookiecutter.repo_name}} > %sbase.sql" % code_dir)
	local("rsync -rlptzv --progress --compress-level=9 -e ssh %s:%sbase.sql ./" % (env.hosts[0], code_dir))
	local('psql -U postgres -c "drop database if exists {{cookiecutter.repo_name}}"')
	local('psql -U postgres -c "create database {{cookiecutter.repo_name}}"')
	local('psql -U postgres {{cookiecutter.repo_name}} < base.sql')