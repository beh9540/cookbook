'''
Created on Mar 12, 2013

@author: bhowell
Scripting file for repeated development tasks
'''
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
import os



@task 
def test():
    local("./manage.py test")
    
@task 
def freeze():
    local("pip freeze > REQUIREMENTS")

@task
def requirements():
    local("pip install -r REQUIREMENTS")

@task
def create_database():
    database = settings_dev.DATABASES['default']
    database_name = database.NAME
    database_user = database.USER
    database_pass = database.PASSWORD
    local("mysql -uroot 'CREATE DATABASE {0} CHARACTER SET utf8;'"\
          .format(database_name))
    local("mysql -uroot \"GRANT ALL ON `{0}`.`*` TO '{1}'@'localhost' "+
          "IDENTIFIED BY '{2}';\"".format(database_name,database_user,
          database_pass))

@task
def commit():
    local("git add -p && git commit")

@task
def push():
    local("git push origin master")

@task
def pull():
    local("git pull origin master")
    
@task
def sync_db():
    local("./manage.py syncdb")

@task
def create_migration(initial=False):
    if initial:
        local("./manage.py schemamigration recipes --initial")
    else:
        local("./manage.py schemamigration recipes --auto --update")
    
@task
def migrate():
    local("./manage.py migrate recipes")
    
@task 
def devel_environment():
    local("mkvirtualenv cookbook")
    requirements()
    create_database()
    sync_db()
    migrate()

@task 
def prepare_commit():
    test()
    freeze()
    create_migration()
    commit()
    push()
    
@task
def deploy():
    code_dir = '/usr/local/lib/django_prov/django_prov'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git.hdcomm.lan:/repo/django_prov.git %s" % code_dir)
    with cd(code_dir):
        run("git pull origin master")
        run("touch django_prov.wsgi")