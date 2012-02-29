# -*- coding: utf-8 -*-
"""
    fabfile.py
    ~~~~~~
    It provides a basic suite of operations for executing local 
    or remote shell commands, as well as auxiliary functionality 
    such as prompting the running user for input, or aborting 
    execution.
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
import os, time
import simplejson as json 
from fabric.api import settings, run, env, cd, lcd, local

from config import DATABASE

LIST_JS_FILES = [x[:-3] for x in os.listdir('static/js/') if x[-3:] == '.js']


# Database ========================================================================
def local_backup():
    """ """
    print '\n####### Backup MongoDB App #######'
    local('mongodump --db %s --out ../data/backup/mongodb/$(date +%F)' % DATABASE)
        
def mongodb_restore(date_backup=None):
    """ """
    print '\n####### Restore MongoDB #######'
    # when date backup is None allows to update the database to the last backup
    if date_backup is None:
        list_backup = sorted([ x for x in os.listdir('../data/backup/mongodb') if x[0] != '.'])
        date_backup = list_backup[-1]
    
    local('mongorestore --db %s --drop ../data/backup/mongodb/%s/%s' % (DATABASE, date_backup, DATABASE))
    

# Javascript tools ================================================================       
def beautify_js():
    """ """
    print '\n####### Beautifying js files #######'
    for name in LIST_JS_FILES:
        path = 'static/js/%s' % name
        local('python jsbeautifier.py %s.js > %s-beautified.js' % (path, path))
        local('mv %s-beautified.js %s.js' % (path, path))
        local('rm -f %s-beautified.js' % path)
        
def minify_js(name_js_file='',minify='yes'):
    """ """
    print '\n####### Minify and change version js files #######'
    version = int(time.time()*0.01)
    
    # read app.json
    f = open('app.json', 'r')
    app_json = json.load(f)
    f.close()
    
    if len(name_js_file) == 0:
        local('rm -fr static/js/min/*')
        for name in LIST_JS_FILES:
            app_json['js_file'][name] = name
            app_json['js_file_version'][name] = 'min/'+name+'-'+str(version)
            local('cp static/js/%s.js static/js/min/%s-%s.js' % (name, name, version))
            if minify == 'yes':
                local('yuicompressor -o static/js/min/%s-%s-min.js static/js/min/%s-%s.js' % (name, version, name, version))
                local('mv static/js/min/%s-%s-min.js static/js/min/%s-%s.js' % (name, version, name, version))
    else:
        if name_js_file in LIST_JS_FILES:
            old_version = app_json['js_file_version'][name_js_file]
            local('rm -fr static/js/min/%s-%s.js' % (name_js_file, old_version))
            app_json['js_file'][name_js_file] = name
            app_json['js_file_version'][name_js_file] = 'min/'+name+'-'+str(version)
            local('cp static/js/%s.js static/js/min/%s-%s.js' % (name_js_file, name_js_file, version))
            if minify == 'yes':
                local('yuicompressor -o static/js/min/%s-%s-min.js static/js/min/%s-%s.js' % (name_js_file, version, name_js_file, version))
                local('mv static/js/min/%s-%s-min.js static/js/min/%s-%s.js' % (name_js_file, version, name_js_file, version))
        else:
            print 'Name js file doesn\'t exist.'
        
    # write app.json
    outfile = open("app.json", "w")
    outfile.write(json.dumps(app_json))
    outfile.close()


# Tests tools =====================================================================        
def tests():
    """ """
    print '\n####### Copy Database in Test Dev #######'
    local('mongo --eval "db = db.getMongo().getDB(\'%s\'); db.copyDatabase(\'%s\', \'app_test\')"' % (DATABASE, DATABASE))
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
    