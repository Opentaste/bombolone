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
from flask import render_template, request, jsonify
from jinja2 import contextfunction 
from werkzeug.routing import BaseConverter

# Imports inside Bombolone
from before import core_before_request, core_context_processor
from config import PORT, DEBUG
from shared import app, db

from core.utils import msg_status

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

# Imports hash_table modules Bombolone
from api.hash_table import api_hash_table

# Imports users modules Bombolone
from api.account import api_account
from api.users import api_users

# Imports pages modules Bombolone
from api.pages import api_pages

# Imports rank modules Bombolone
from api.rank import api_rank

# Imports languages modules Bombolone
from api.languages import api_languages

LIST_MODULES = [login,
                api_account,
                api_languages,
                api_hash_table,
                api_pages,
                api_rank,
                api_login,
                api_users,
                admin, 
                pages,
                users, 
                rank, 
                languages, 
                hash_table, 
                settings, 
                content]

            
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
    if request.path.startswith('/api/1.0/'): 
        message = "Raise if the browser sends something to the application the application or server cannot handle."
        data = dict(success=False, errors=[{ "message": message, "code": 400 }])
        response = jsonify(data)
        response.status_code = 400
        return response
    return render_template('error/400.html'), 400

@app.errorhandler(401)
def unauthorized(error):
    """Raise if the user is not authorized. Also used if you want 
    to use HTTP basic auth."""
    if request.path.startswith('/api/1.0/'): 
        message = "Raise if the user is not authorized. Also used if you want to use HTTP basic auth."
        data = dict(success=False, errors=[{ "message": message, "code": 401 }])
        response = jsonify(data)
        response.status_code = 401
        return response
    return render_template('error/401.html'), 401

@app.errorhandler(404)
def not_found(error):
    """Raise if a resource does not exist and never existed.
    If we are running App locally, we have to avoid calling
    context processors and thus we return just an empty string."""
    if DEBUG == False:
        return render_template('error/404.html'), 404
    if request.path.startswith('/static/'):
        return '', 404
    if request.path.startswith('/api/1.0/'):
        message = "Raise if a resource does not exist and never existed."
        data = dict(success=False, errors=[{ "message": message, "code": 404 }])
        response = jsonify(data)
        response.status_code = 404
        return response
    return render_template('error/404.html'), 404

@app.errorhandler(405)
def not_found(error):
    """
    The method is not allowed for the requested URL.
    """
    if request.path.startswith('/api/1.0/'):
        message = "Method Not Allowed"
        data = dict(success=False, errors=[{ "message": message, "code": 405 }])
        response = jsonify(data)
        response.status_code = 405
    return render_template('error/404.html'), 405

@app.errorhandler(408)
def request_timeout(error):
    """Raise to signalize a timeout."""
    message = '408 - Error caught in {1} : {0}'.format(error, request.path)
    app.logger.critical(message)
    if request.path.startswith('/api/1.0/'):
        data = dict(success=False, errors=[{ "message": message, "code": 408 }])
        response = jsonify(data)
        response.status_code = 408
        return response
    return render_template('error/408.html'), 408
    
@app.errorhandler(413)
def request_too_large(error):
    """Like 413 but for too long URLs."""
    message = '413 - Error caught in {1} : {0}'.format(error, request.path)
    app.logger.critical(message)
    return render_template('error/413.html'), 413
    
@app.errorhandler(500)
def bad_request(error):
    """Raise if the browser sends something to the application the
    application or server cannot handle."""
    if request.path.startswith('/api/1.0/'):
        app.logger.critical("Path: {}".format(request.path))
        app.logger.critical(logging.exception("Exception"))
        data = dict(success=False, errors=[{ "message": message, "code": 500 }])
        response = jsonify(data)
        response.status_code = 500
        return response
    return render_template('error/500.html'), 500
     
     
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

def date_time_format(value, format='%d-%m-%Y - %H:%M', localized=False):
    if type(value) is unicode or type(value) is str:
        return 'We need fix it'
    
    if localized:
        utc_time = pytz.utc.localize(value)
        if g.my:
            nation = pytz.timezone(g.my['time_zone'])
        else:
            nation = pytz.timezone('Europe/Rome')
        nation_time = utc_time.astimezone(nation)
        return str(nation_time.day) + ' ' + dict_month[g.lan][nation_time.month] + ' ' + str(nation_time.year)
    else:
        return value.strftime(format)

def split_word_format(value, letters=30):
    if len(value) > (letters * 2):
        return value[:letters] + '<br />' + value[letters:(letters*2)] + '<br />' + value[(letters*2):]
    if len(value) > letters:
        return value[:letters] + '<br />' + value[letters:]
    return value

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

# add some functions to jinja
app.jinja_env.globals['sorted'] = contextfunction(sorted_thing)  
app.jinja_env.globals['int'] = contextfunction(int_thing)   
app.jinja_env.globals['str'] = contextfunction(str_thing) 
app.jinja_env.globals['unicode'] = contextfunction(unicode_thing) 
app.jinja_env.globals['type'] = contextfunction(type_thing) 
app.jinja_env.globals['len'] = contextfunction(len_thing) 
app.jinja_env.globals['enumerate'] = contextfunction(enumerate_thing) 

app.jinja_env.filters['date'] = date_time_format
app.jinja_env.filters['split_word'] = split_word_format
app.jinja_env.filters['msg'] = msg_status

# regular expressions inside url routing
app.url_map.converters['regex'] = RegexConverter

for module in LIST_MODULES:
    app.register_blueprint(module)
    
if __name__ == '__main__':
    if db is None:
        app.logger.critical("App needs running MongoDB instance.")
    else:
        app.run(host='0.0.0.0', port=config.PORT)
