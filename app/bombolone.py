# -*- coding: utf-8 -*-
"""
bombolone.py
~~~~~~

:copyright: (c) 2013 by Leonardo Zizzamia
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

from core.utils import msg_status

# Imports api modules Bombolone
from api.admin.hash_table import hash_table_api
from api.admin.pages import pages_api
from api.users.account import account_api
from api.users.users import users_api

# Imports Admin modules Bombolone
from admin.admin import admin
from admin.languages import languages
from admin.hash_table import hash_table
from admin.pages import pages
from admin.test import test
from admin.rank import rank
from admin.users import users

# Imports Users modules Bombolone
from users.settings import settings

# Imports Login modules Bombolone
from login.login import login

# Imports modules Bombolone
from content import content
from home import home

LIST_MODULES = [home, 
                login,
                hash_table_api,
                pages_api,
                account_api,
                users_api,
                admin, 
                pages, 
                test,
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

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

# regular expressions inside url routing
app.url_map.converters['regex'] = RegexConverter

for module in LIST_MODULES:
    app.register_blueprint(module)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)