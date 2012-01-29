# -*- coding: utf-8 -*-
"""
    bombolone.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
# Imports outside bombolone
from __future__ import with_statement
from flask import abort, render_template
from jinja2 import contextfunction 

# Imports inside bombolone
from before import core_before_request, core_inject_user
from content import content
from shared import app, PORT

# Imports modules bombolone
from admin import admin
from pages import pages
from users import users
from rank import rank
from languages import languages
from hash_table import hash_table
LIST_MODULES = [content, admin, pages, users, rank, languages, hash_table]
   
   
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
    """
    Raise if the browser sends something to the application the 
    application or server cannot handle.
    """
    return 'Raise if the browser sends something to the application the application or server cannot handle. 400', 400

@app.errorhandler(401)
def unauthorized(error):
    """Raise if the user is not authorized. Also used if you want 
    to use HTTP basic auth."""
    return render_template('error/401.html')

@app.errorhandler(404)
def not_found(error):
    """
    Raise if a resource does not exist and never existed.
    """
    return render_template('error/404.html')
    
@app.errorhandler(408)
def request_timeout(error):
    """Raise to signalize a timeout."""
    return 'Raise to signalize a timeout. 408', 408
    
@app.errorhandler(413)
def request_too_large(error):
    """Like 413 but for too long URLs."""
    return 'Like 413 but for too long URLs. 413', 413
    
    
@app.errorhandler(500)
def bad_request(error):
    """
    Raise if the browser sends something to the application the 
    application or server cannot handle.
    """
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

if __name__ == '__main__':
    for module in LIST_MODULES:
        app.register_blueprint(module)
    app.run(host='0.0.0.0', port=PORT)