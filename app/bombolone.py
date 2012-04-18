# -*- coding: utf-8 -*-
"""
    flight_pooling.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
# Imports outside Bombolone
from __future__ import with_statement
from flask import render_template
from jinja2 import contextfunction 
from werkzeug.routing import BaseConverter

# Imports inside Bombolone
from before import core_before_request, core_inject_user
from config import PORT
from shared import app

# Imports modules Bombolone
from admin import admin
from content import content
from languages import languages
from login import login
from hash_table import hash_table
from home import home
from pages import pages
from rank import rank
from settings import settings
from users import users
LIST_MODULES = [home, login, admin, pages, users, rank, languages, 
                hash_table, settings, content]

            
# ========================================================================	
# Before zone
                  
@app.before_request
def before_request():
    return core_before_request()
    
@app.context_processor
def inject_user():
    return core_inject_user()
	
# ========================================================================	
# Error zone

@app.errorhandler(400)
def bad_request(error):
    """ Raise if the browser sends something to the application the 
    application or server cannot handle. """
    return render_template('error/400.html')

@app.errorhandler(401)
def unauthorized(error):
    """Raise if the user is not authorized. Also used if you want 
    to use HTTP basic auth."""
    return render_template('error/401.html')

@app.errorhandler(404)
def not_found(error):
    """ Raise if a resource does not exist and never existed. """
    return render_template('error/404.html')
    
@app.errorhandler(408)
def request_timeout(error):
    """Raise to signalize a timeout."""
    return  render_template('error/408.html')
    
@app.errorhandler(413)
def request_too_large(error):
    """Like 413 but for too long URLs."""
    return  render_template('error/413.html')
    
    
@app.errorhandler(500)
def bad_request(error):
    """ Raise if the browser sends something to the application the 
    application or server cannot handle. """
    return render_template('error/500.html')
     
     
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

# add some functions to jinja
app.jinja_env.globals['sorted'] = contextfunction(sorted_thing)  
app.jinja_env.globals['int'] = contextfunction(int_thing)   
app.jinja_env.globals['str'] = contextfunction(str_thing) 
app.jinja_env.globals['unicode'] = contextfunction(unicode_thing) 
app.jinja_env.globals['type'] = contextfunction(type_thing) 
app.jinja_env.globals['len'] = contextfunction(len_thing) 
app.jinja_env.globals['enumerate'] = contextfunction(enumerate_thing) 

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

# regular expressions inside url routing
app.url_map.converters['regex'] = RegexConverter

if __name__ == '__main__':
    for module in LIST_MODULES:
        app.register_blueprint(module)
    app.run(host='0.0.0.0', port=PORT)