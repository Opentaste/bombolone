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
import hashlib
import simplejson as json 
import shutil
from fabric.api import settings, run, env, cd, lcd, local, sudo
try:
    from shared import db
except:
    db = None
from config import DATABASE

LIST_JS_FILES = [x[:-3] for x in os.listdir('static/js/') if x[-3:] == '.js']


# Install =========================================================================
def install():
    """ 
    Install all the requirements to run Bombolone
    """
    if not check_database("install"):
        return False

    print '\n####### Install Bombolone #######'
    print 'For Install correctly some library we need be Administrator'

    # Install requirements 
    local("sudo pip install -r ../REQUIREMENTS.txt")
    # Install Compass (http://compass-style.org/install/)
    local("gem update --system")
    local("gem install compass")
    # Install h5bp (https://github.com/sporkd/compass-h5bp)
    local("gem install compass-h5bp")
    # Install coffeescript (http://coffeescript.org/#installation)
    local("sudo npm install -g coffee-script")


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
    local('mongodump --db {} --out ../data/backup/mongodb/$(date +%F)'.format(DATABASE))
        

def mongodb_restore(database=None, date_backup=None):
    """ """
    print '\n####### Restore MongoDB #######'

    if database is None:
        database = DATABASE
    
    # When date backup is None allows to update the database to the last backup
    if date_backup is None:
        list_backup = sorted([ x for x in os.listdir('../data/backup/mongodb') if x[0] != '.'])
        date_backup = list_backup[-1]
    
    local('mongorestore --db {0} --drop ../data/backup/mongodb/{1}/{2}'.format(DATABASE, date_backup, database))
   

def init_database(name_database=None):
    """
    Init the basic database
    """
    # to do, here we need write in the config file the name of database
    #DATABASE = name_database

    new_line = "DATABASE = 'leo'\n"

    with open("config.py","r") as fp:
        lines = fp.readlines()

    for i, line in enumerate(lines):
        if line.startswith('DATABASE ='):
            print line
            lines[i] = new_line
            break
    else:
        print "damn could not find the line"
        raise SystemExit("Damn!")

    with open("new_config.py","w") as fp:
        fp.writelines(lines)

    shutil.copy("new_config.py", "config.py")

    #mongodb_restore(database="bombolone")


def write_db_in_config(name_database):
    """
    """
    pass


# Javascript tools ================================================================   
def coffee():
    """
    Run coffee daemon to watch for changes in static/coffee/
    """
    
    print "\n##### Coffee #####"
    local('coffee --watch --bare --compile --output static/js/ static/coffee/')


def coffeeshot():
    """
    Compile .coffee files that have been changed since last run
    """
    
    print
    print "This script will compile .coffee files that have been changed since last run\n\n"
    
    coffee_dir = os.path.join('static', 'coffee')
    files = {}

    # On first run, create a .coffeecache file 
    if not os.path.isfile('.coffeecache'):
        print "Creating empty .coffeecache...\n"
        open('.coffeecache', 'w+').close()

    print "Reading .coffeecache"
    cache = open('.coffeecache', 'r')

    for record in cache.readlines():
        files[record.split(':')[0]] = record.split(':')[1].strip()

    cache.close()

    print "Checking for new .coffee files..."
        
    for filename in os.listdir(os.path.join('static', 'coffee')):
        filename = filename.split('.')[0] # Remove file extension

        if filename not in files.keys():
            # Always compile and store MD5s for new files

            print "New .coffee file: " + filename
            files[filename] = hashlib.md5(open(os.path.join(coffee_dir, filename + ".coffee")).read()).hexdigest()
            local('coffee --bare --compile --output static/js/ static/coffee/{}.coffee'.format(filename))
        else:
            # Compare hash with the known one

            new_md5 = hashlib.md5(open(os.path.join(coffee_dir, filename + ".coffee")).read()).hexdigest()

            if files[filename] != new_md5:

                # If they don't match...
                print "Updating {}...".format(filename)
                local("coffee --bare --compile --output static/js/ static/coffee/{}.coffee".format(filename))
                files[filename] = new_md5
            else:
                print filename + " has not changed"

    cache = open('.coffeecache', 'w')
    for f, md5 in files.items():
        cache.write(':'.join((f, md5)) + '\n')

    cache.close()

      
def minify():
    """
    Minify .js files that have been changed since last run
    """
    if not check_database("minify"):
        return False

    print "\nMinify JS files and update their version number"

    version = int(time.time()*0.01)

    js_dir = os.path.join('static', 'js')
    js_min_dir = os.path.join(js_dir, 'min')

    already_minified =  [x[:-3].split('-')[0] for x in os.listdir(js_min_dir) if x[-3:] == '.js']

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

            new_md5 = hashlib.md5(open(os.path.join(js_dir,
                filename + ".js")).read()).hexdigest()

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
        local("rsync -avz --delete tmp_update/app/admin .")
        local("rsync -avz --delete tmp_update/app/api .")
        local("rsync -avz --delete tmp_update/app/core .")
        local("rsync -avz --delete tmp_update/app/templates/admin templates")
    except:
        print "Got an error!!!"
    finally:
        local("rm -fr tmp_update")


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
    