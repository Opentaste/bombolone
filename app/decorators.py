# -*- coding: utf-8 -*-
"""
decorators.py
~~~~~~
A collection of all the decorators

:copyright: (c) 2013 by Leonardo Zizzamia
:license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
from flask import g, abort, request, current_app, render_template
from functools import wraps
from api.oauth2db import oauth_server

class GetValue(object):
    """ """
    def __init__(self, dictionary):
        self.dictionary = dictionary
        
    def check_key(self, key):
        return self.dictionary.get(key, 'Error not defined : {}'.format(key))

def jsonp(f):
    """
    Wraps JSONified output for JSONP
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data) + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)
    return decorated_function

def get_hash(hash_map_name):
    """
    Does everything done by the following piece of code, but in a generic way.
    
    def get_hash_tags(function_to_decorate):
        @wraps(function_to_decorate)
        def decorated_function(*args, **kwargs):
            dictionary = get_hash_map('tags')
            get_value = GetValue(dictionary)
            g.tags_msg = get_value.check_key
            g.tags = dictionary
            return function_to_decorate(*args, **kwargs)
        return decorated_function
    
    
    It can be used like this:
    
    @get_hash('tags')
    """
    
    def real_decorator(function_to_decorate):
        @wraps(function_to_decorate)
        def decorated_function(*args, **kwargs):
            dictionary = get_hash_map(hash_map_name)
            get_value = GetValue(dictionary)
            setattr(g, hash_map_name + '_msg', get_value.check_key)
            setattr(g, hash_map_name, dictionary)
            return function_to_decorate(*args, **kwargs)
        return decorated_function
    
    return real_decorator

def get_hash_map(module):
    """ """
    try:
        module_map = g.db.hash_table.find_one({ 'name' : module })
        return { x : y[g.lan] for x, y in module_map['value'].iteritems() }
    except:
        print "Important, you have to restore last database!"

def get_hash_admin():
    """  """
    dictionary = get_hash_map('admin')
    get_value = GetValue(dictionary)
    g.admin_msg = get_value.check_key
    g.admin = dictionary

def get_template(template_directive):
    """ 
    Run the template from a specific directive

    @get_template("pages")
    """
    def real_decorator(function_to_decorate):
        @wraps(function_to_decorate)
        def decorated_function(*args, **kwargs):
            function_to_decorate(*args, **kwargs)
            return render_template(template_directive+'/'+args[0]['file']+'.html', **locals())
        return decorated_function

    return real_decorator

### Authentication Zone ###
def check_token(function_to_decorate):
    """ Requires standard login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):

        token = request.args.get('token', None)

        if token is None:
            abort(401)

        validation = oauth_server.check_token(token)
        if not validation["success"]:
            abort(401)

        return function_to_decorate(*args, **kwargs)
    return decorated_function

def check_token_post(function_to_decorate):
    """ Requires standard login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):

        if not "token" in request.json:
            abort(401)

        token = request.json['token']

        validation = oauth_server.check_token(token)
        if not validation["success"]:
            abort(401)

        return function_to_decorate(*args, **kwargs)
    return decorated_function

def check_token_ajax(function_to_decorate):
    """ Requires standard login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):

        token = request.headers.get('X-Requested-Token', None)

        if token is None:
            abort(401)

        validation = oauth_server.check_token(token)
        if not validation["success"]:
            abort(401)

        return function_to_decorate(*args, **kwargs)
    return decorated_function

def check_authentication(function_to_decorate):
    """ Requires standard login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        if not g.my or 'status' not in g.my or g.my['status'] is 0:
            abort(401)
        return function_to_decorate(*args, **kwargs)
    return decorated_function

def check_rank(rank):
    """
    Does everything done by the following piece of code, but in a generic way.

    def check_chief(function_to_decorate):
        @wraps(function_to_decorate)
        def decorated_function(*args, **kwargs):
            if g.my['rank'] > 15:
                abort(401)
            return function_to_decorate(*args, **kwargs)
        return decorated_function

    It can be used like this:

    @check_rank(40)
    """

    def real_decorator(function_to_decorate):
        @wraps(function_to_decorate)
        def decorated_function(*args, **kwargs):
            if not g.my or 'status' not in g.my or g.my['status'] is 0:
                abort(401)
            if g.my['rank'] > rank:
                abort(401)
            return function_to_decorate(*args, **kwargs)
        return decorated_function

    return real_decorator