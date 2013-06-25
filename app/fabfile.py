# -*- coding: utf-8 -*-
"""
fabfile.py
~~~~~~
It provides a basic suite of operations for executing local 
or remote shell commands, as well as auxiliary functionality 
such as prompting the running user for input, or aborting 
execution.

:copyright: (c) 2013 by Leonardo Zizzamia
:license: BSD (See LICENSE for details)
"""
import os
import time
import simplejson as json 
from fabric.api import settings, run, env, cd, lcd, local
from shared import db
from config import DATABASE

LIST_JS_FILES = [x[:-3] for x in os.listdir('static/js/') if x[-3:] == '.js']

# Database ========================================================================
def local_backup():
    """ """
    print '\n####### Backup MongoDB App #######'
    local('mongodump --db '+DATABASE+' --out ../data/backup/mongodb/$(date +%F)')
        
def mongodb_restore(date_backup=None):
    """ """
    print '\n####### Restore MongoDB #######'
    # when date backup is None allows to update the database to the last backup
    if date_backup is None:
        list_backup = sorted([ x for x in os.listdir('../data/backup/mongodb') if x[0] != '.'])
        date_backup = list_backup[-1]
    
    local('mongorestore --db %s --drop ../data/backup/mongodb/%s/%s' % (DATABASE, date_backup, DATABASE))
    

# Javascript tools ================================================================       
def coffee():
    print '\n####### Coffee #######'
    local('coffee --watch --bare --compile --output static/js/ static/coffee/')

def minify():
    print '\n####### Minify and change version js files #######'
    version = int(time.time()*0.01)

    # Get file version
    app_json = db.js.find_one({ "file": "version" })

    if app_json is None:
        app_json = {}

    if not 'js_file' in app_json:
        app_json["file"] = "version"
        app_json['js_file'] = {}
        app_json['js_file_version'] = {}

    local('rm -fr static/js/min/*')
    for name in LIST_JS_FILES:
        app_json['js_file'][name] = name
        app_json['js_file_version'][name] = 'min/{0}-{1}'.format(name, version)
        local('cp static/js/{0}.js static/js/min/{0}-{1}.js'.format(name, version))
        local('yuicompressor --nomunge -o static/js/min/{0}-{1}-min.js static/js/min/{0}-{1}.js'.format(name, version))
        local('mv static/js/min/{0}-{1}-min.js static/js/min/{0}-{1}.js'.format(name, version))

    # Update file version
    db.js.update({ "file": "version" }, app_json, True)
    local("mongodump --db {} --collection js --out dump".format(DATABASE))


# Tests tools =====================================================================        
def tests():
    """ """
    print '\n####### Copy Database in Test Dev #######'
    local('mongo --eval "db = db.getMongo().getDB(\'{0}\'); db.copyDatabase(\'{0}\', \'app_test\')"'.format(DATABASE))
    local('mongo --eval "db = db.getMongo().getDB(\'app_test\');"')
    print '\n####### Run Tests #######'
    try:
        with lcd('tests/'):
            local('python check_admin.py')
            local('python check_settings.py')
    finally:
        drop_db_tests()
    
def drop_db_tests():
    """ """
    print '\n####### Drop Test Database #######'
    local('mongo --eval "db = db.getMongo().getDB(\'app_test\'); db.dropDatabase()"')
    