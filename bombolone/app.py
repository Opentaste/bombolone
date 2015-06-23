# -*- coding: utf-8 -*-
"""
app.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
# Let's check if the symlink config.py exists
try:
    import config
except:
    print "\n    config.py not found\n"
    print "You should create a symlink of config_home.py or config_production.py\n"
    import sys
    sys.exit(0)

# Imports outside Bombolone
from flask import Flask, render_template, request, jsonify
from jinja2 import contextfunction 
from werkzeug.routing import BaseConverter

# Imports inside Bombolone
from before import core_before_request, core_context_processor
from config import PORT, DEBUG

from core.utils import msg_status, errorhandler

# Imports login modules Bombolone
from routes.login.login import login

# Imports users modules Bombolone
from routes.users.settings import settings

# Imports admin modules Bombolone
from routes.admin.admin import admin
from routes.admin.pages import pages
from routes.admin.hash_table import hash_table
from routes.admin.languages import languages
from routes.admin.rank import rank
from routes.admin.users import users

# Import content module Bombolone
from routes.content import content

# Imports API modules
from api.account import api_account
from api.hash_table import api_hash_table
from api.languages import api_languages
from api.pages import api_pages
from api.rank import api_rank
from api.users import api_users


# Create application and configuration
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # 10 Mb Max Upload
app.test_request_context().push()

# regular expressions inside url routing
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

LIST_MODULES = [login,
                api_account,
                api_hash_table,
                api_languages,
                api_pages,
                api_rank,
                api_users,
                admin, 
                pages,
                users, 
                rank, 
                languages, 
                hash_table, 
                settings, 
                content]

for module in LIST_MODULES:
    app.register_blueprint(module)

            
# ========================================================================	
# Before zone
                  
@app.before_request
def before_request():
    """Function called on each request.
    We need to avoid calling core_before_request on /static/ pages.
    In a production environment this is not needed since static requests are
    server by Apache/Nginx, but we need to check if Bombolone is run locally.
    
    """
    if DEBUG == False:
        return core_before_request()
    if not request.path.startswith('/static/'): 
        return core_before_request()

@app.context_processor
def context_processor():
    """ """
    return core_context_processor()
	
# ========================================================================	
# Error zone

@app.errorhandler(400)
def bad_request(error):
    """Raise if the browser sends something to the application the 
    application or server cannot handle."""
    message = "Raise if the browser sends something to the "
    message += "application the application or server cannot handle."
    return errorhandler(400, message)

@app.errorhandler(401)
def unauthorized(error):
    """Raise if the user is not authorized. Also used if you want 
    to use HTTP basic auth."""
    message = "Raise if the user is not authorized. Also used if you want to use HTTP basic auth."
    return errorhandler(401, message)

@app.errorhandler(404)
def not_found(error):
    """Raise if a resource does not exist and never existed.
    If we are running App locally, we have to avoid calling
    context processors and thus we return just an empty string."""
    if DEBUG == False:
        return render_template('error/404.html'), 404
    if request.path.startswith('/static/'):
        return '', 404
    message = "Raise if a resource does not exist and never existed."
    return errorhandler(404, message)

@app.errorhandler(405)
def not_found(error):
    """The method is not allowed for the requested URL."""
    message = "Method Not Allowed"
    return errorhandler(405, message)

@app.errorhandler(408)
def request_timeout(error):
    """Raise to signalize a timeout."""
    message = '408 - Error caught in {1} : {0}'.format(error, request.path)
    app.logger.critical(message)
    return errorhandler(408, message)
    
@app.errorhandler(413)
def request_too_large(error):
    """Like 413 but for too long URLs."""
    message = '413 - Error caught in {1} : {0}'.format(error, request.path)
    app.logger.critical(message)
    return errorhandler(408, message)
    
@app.errorhandler(500)
def bad_request(error):
    """Raise if the browser sends something to the application the
    application or server cannot handle."""
    app.logger.critical("Path: {}".format(request.path))
    app.logger.critical(logging.exception("Exception"))
    message = "Something went wrong!"
    return errorhandler(500, message)
     
     
# ========================================================================	
# Jinja zone   
            
def sorted_thing(context, key):
    return sorted(key)
		
def int_thing(context, key):
    return int(key)

def str_thing(context, key):
    return str(key)

def unicode_thing(context, key):
    return unicode(key)
	
def type_thing(context, key):
    return type(key)
	
def len_thing(context, key):
    return len(key)
	
def enumerate_thing(context, key):
    return enumerate(key)

# Add some functions to jinja
app.jinja_env.globals['sorted'] = contextfunction(sorted_thing)  
app.jinja_env.globals['int'] = contextfunction(int_thing)   
app.jinja_env.globals['str'] = contextfunction(str_thing) 
app.jinja_env.globals['unicode'] = contextfunction(unicode_thing) 
app.jinja_env.globals['type'] = contextfunction(type_thing) 
app.jinja_env.globals['len'] = contextfunction(len_thing) 
app.jinja_env.globals['enumerate'] = contextfunction(enumerate_thing) 
app.jinja_env.filters['msg'] = msg_status


def main():
    app.run(host='0.0.0.0', port=config.PORT)


if __name__ == '__main__':
    main()
