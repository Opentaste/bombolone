# -*- coding: utf-8 -*-
"""
fabfile.py
~~~~~~
It provides a basic suite of operations for executing local 
or remote shell commands, as well as auxiliary functionality 
such as prompting the running user for input, or aborting 
execution.

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
import os
import time
import hashlib
import shutil
from fabric.api import settings, run, env, cd, lcd, local, sudo
try:
    from model.model_engine import db
except:
    db = None
from config import DATABASE


# Helpers =========================================================================
def check_database(name_function):
    """
    Check if is running the MongoDB database
    """
    if db is None:
        print "\nYou need run MongoDB for complete the {} function".format(name_function)
        return False
    return True


# Database ========================================================================
def local_backup():
    """ """
    print '\n####### Backup MongoDB App #######'
    local('mongodump --db {} --out data/backup/mongodb/$(date +%F)'.format(DATABASE))
        

def mongodb_restore(new_database=None, database=None, date_backup=None):
    """ """
    print '\n####### Restore MongoDB from {0} to {1} #######'.format(database, new_database)

    if new_database is None:
        new_database = DATABASE
    
    # When date backup is None allows to update the database to the last backup
    if date_backup is None:
        list_backup = sorted([ x for x in os.listdir('data/backup/mongodb') if x[0] != '.'])
        date_backup = list_backup[-1]
    
    local('mongorestore --db {0} --drop data/backup/mongodb/{1}/{2}'.format(new_database, date_backup, database))
   

def init_database(name_database=None):
    """
    Init the basic database
    """
    print '\n####### Init new database #######'
    write_db_in_config(name_database=name_database)
    mongodb_restore(new_database=name_database, database="bombolone")


def write_db_in_config(name_database=None):
    """
    """
    new_line = "DATABASE = '{0}'\n".format(name_database)
    with open("config.py","r") as fp:
        lines = fp.readlines()
    for i, line in enumerate(lines):
        if line.startswith('DATABASE ='):
            lines[i] = new_line
            break
    else:
        print "damn could not find the line"
        raise SystemExit("Damn!")
    with open("new_config.py","w") as fp:
        fp.writelines(lines)
    shutil.copy("new_config.py", "config.py")
    os.remove("new_config.py")


# Javascript tools ================================================================   
LIST_JS_DIRECTORIES = ['admin', 'controllers', 'directives', 'services', 'filters']

def get_list_js():
    list_js = [x[:-3] for x in os.listdir('static/js/') if x[-3:] == '.js']
    for name_folder in LIST_JS_DIRECTORIES:
        list_js += [name_folder+"/"+x[:-3] for x in os.listdir('static/js/'+name_folder+'/') if x[-3:] == '.js']
    return list_js

def get_list_js_already_min(js_dir):
    js_min_dir = os.path.join(js_dir, 'min')
    list_js = [x[:-3].split('-v')[0] for x in os.listdir(js_min_dir) if x[-3:] == '.js']
    for name_folder in LIST_JS_DIRECTORIES:
        js_min_dir_two = os.path.join(js_min_dir, name_folder)
        list_js += [name_folder+"/"+x[:-3].split('-v')[0] for x in os.listdir(js_min_dir_two) if x[-3:] == '.js']
    return list_js

LIST_JS_FILES = get_list_js()

def minify():
    """
    Minify .js files that have been changed since last run
    """
    if not db:
        print "\nMinify JS need you run mongodb"
        return
    print "\nMinify JS files and update their version number"

    time_now = int(time.time()*0.01)
    version = 'v{}'.format(time_now)
    js_dir = os.path.join('static', 'js')
    already_minified = get_list_js_already_min(js_dir)

    files = {}

    # On first run, create a .minifycache file 
    if not os.path.isfile('.minifycache'):
        print "Creating empty .minifycache...\n"
        local("touch .minifycache")

    # Get file version
    app_json = db.js.find_one({ "file": "version" })

    if app_json is None:
        app_json = {}

    if not 'js_file' in app_json:
        app_json["file"] = "version"
        app_json['js_file'] = {}
        app_json['js_file_version'] = {}

    print "Reading .minifycache"
    cache = open('.minifycache', 'r')

    for record in cache.readlines():
        files[record.split(':')[0]] = record.split(':')[1].strip()

    cache.close()

    print "Checking for new .js files..."

    for filename in LIST_JS_FILES:

        app_json['js_file'][filename] = filename

        if filename not in files.keys() or filename not in already_minified:
            # Always compile and store MD5s for new files or files without
            # a matching minified version

            print "New .js file: " + filename
            files[filename] = hashlib.md5(open(os.path.join(js_dir, filename + ".js")).read()).hexdigest()

            origin_min = "static/js/min/{}-{}.js".format(filename, version)
            destination_min = "static/js/min/{}-{}-min.js".format(filename, version)

            local("cp static/js/{}.js {}".format(filename, origin_min))
            local("yuicompressor --nomunge -o {} {}".format(destination_min, origin_min))
            local("mv {} {}".format(destination_min, origin_min))
            app_json['js_file_version'][filename] = 'min/{0}-{1}'.format(filename, version)
        else:
            # Compare hash with the known one

            new_md5 = hashlib.md5(open(os.path.join(js_dir, filename + ".js")).read()).hexdigest()

            if files[filename] != new_md5:

                # If they don't match...
                print "Updating " + filename + "..."

                # Remove the old minified file (if any)
                local('rm -f static/js/min/{0}*.js'.format(filename))

                origin_min = "static/js/min/{}-{}.js".format(filename, version)
                destination_min = "static/js/min/{}-{}-min.js".format(filename, version)

                local('cp static/js/{}.js {}'.format(filename, origin_min))
                local("yuicompressor --nomunge -o {} {}".format(destination_min, origin_min))
                local("mv {} {}".format(destination_min, origin_min))
                files[filename] = new_md5
                app_json['js_file_version'][filename] = 'min/{0}-{1}'.format(filename, version)
            else:
                print filename + " has not changed"

    # Update file version
    db.js.update({ "file": "version" }, app_json, True)
    local("mongodump --db {} --collection js --out dump".format(DATABASE))

    # Update cache
    cache = open('.minifycache', 'w')
    for f, md5 in files.items():
        cache.write(':'.join((f, md5)) + '\n')

    cache.close()

   
# Update Bombolone  ===============================================================      
def update():
    """ """
    print '\n####### Update Bombolone #######'
    local("rm -fr tmp_update")
    local("git clone https://github.com/Opentaste/bombolone.git tmp_update")
    try:
        list_core_module = ['hash_table', 'languages', 'pages', 'users']
        for module in list_core_module:
            for item in ['api', 'core', 'model']:
                local("rsync -avz --delete tmp_update/{0}/{1} .".format(item, module))
        local("rsync -avz --delete tmp_update/api/account .")
        local("rsync -avz --delete tmp_update/api/rank .")
        local("rsync -avz --delete tmp_update/core/utils .")
        local("rsync -avz --delete tmp_update/core/login .")
        local("rsync -avz --delete tmp_update/core/rank .")
        local("rsync -avz --delete tmp_update/core/upload .")
        local("rsync -avz --delete tmp_update/core/validators .")
        local("rsync -avz --delete tmp_update/model/ranks .")
    except:
        print "Got an error!!!"
    finally:
        local("rm -fr tmp_update")
    