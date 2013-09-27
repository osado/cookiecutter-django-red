# -*- coding: utf-8 -*-
# Nikolay Udalov (nikolaj.udalov@gmail.com)
from fabric.api import *

env.hosts = ['{{cookiecutter.remote_host}}']
code_dir = '{{cookiecutter.remote_path}}'

venv_dep = "build-essential python-dev libxml2-dev libxslt1-dev libjpeg-turbo8-dev libjpeg8-dev libfreetype6-dev libwebp-dev libtiff4-dev libtidy-dev libpq-dev"

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
		with cd(code_dir):
			run('venv/bin/python {{cookiecutter.repo_name}}/manage.py %s --settings=config.settings' % cmd)

@task
def install_remote():
	from fabric.contrib.files import append
	run("apt-get install software-properties-common python-software-properties -y")
	run("add-apt-repository -y ppa:chris-lea/nginx-devel")
	run("add-apt-repository -y ppa:chris-lea/redis-server")
	append("/etc/apt/sources.list.d/pgdg.list", "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main")
	run("wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -")
	run("apt-get update && apt-get upgrade -qq --force-yes")
	run("apt-get install nginx nginx-common nginx-full redis-server python-virtualenv postgresql-9.3 logrotate supervisor -qq --force-yes")
	run("apt-get install %s -qq --force-yes" % venv_dep)
	run("ln -s -t /etc/nginx/sites-enabled/ %snginx_{{cookiecutter.repo_name}}.conf" % code_dir)
	run("ln -s -t /etc/supervisor/conf.d/ %ssupervisor_{{cookiecutter.repo_name}}.conf" % code_dir)

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
	if side == 'local':
		local("sudo apt-get install %s -y" % venv_dep)
		local("virtualenv venv/")
	else:
		with cd(code_dir):
			run("virtualenv venv/")

@task
def pip(side='local'):
	if side == 'local':
		local("venv/bin/pip install -U -r requirements/local.txt")
	else:
		with cd(code_dir):
			run("venv/bin/pip install -U -r requirements/production.txt")

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