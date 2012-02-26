# -*- coding: utf-8 -*-
"""
    decorators.py
    ~~~~~~
    A collection of all the decorators
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
from flask import g, abort
from functools import wraps

# Imports inside Bombolone
from validators import GetValue

def get_hash_map(module):
    module_map = g.db.hash_table.find_one({ 'name' : module })
    return { x : y[g.lan] for x, y in module_map['value'].iteritems() }

### Authentication Zone ###
def check_authentication(function_to_decorate):
    """ Requires standard login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, "my"):
            abort(401)
        return function_to_decorate(*args, **kwargs)
    return decorated_function


def check_chief(function_to_decorate):
    """ Requires chief login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        if g.my['rank'] > 15:
            abort(401)
        return function_to_decorate(*args, **kwargs)
    return decorated_function   


def check_admin(function_to_decorate):
    """ Requires admin login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        if g.my['rank'] > 25:
            abort(401)
        return function_to_decorate(*args, **kwargs)
    return decorated_function

### Zone ###
def get_hash_languages(function_to_decorate):
    """  """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        dictionary = get_hash_map('languages')
        get_value = GetValue(dictionary)
        g.languages_msg = get_value.check_key
        g.languages = dictionary
        return function_to_decorate(*args, **kwargs)
    return decorated_function    


def get_hash_login(function_to_decorate):
    """  """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        dictionary = get_hash_map('login')
        get_value = GetValue(dictionary)
        g.login_msg = get_value.check_key
        g.login = dictionary
        return function_to_decorate(*args, **kwargs)
    return decorated_function


def get_hash_pages(function_to_decorate):
    """  """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        dictionary = get_hash_map('pages')
        get_value = GetValue(dictionary)
        g.pages_msg = get_value.check_key
        g.pages = dictionary
        return function_to_decorate(*args, **kwargs)
    return decorated_function


def get_hash_rank(function_to_decorate):
    """  """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        dictionary = get_hash_map('rank')
        get_value = GetValue(dictionary)
        g.rank_msg = get_value.check_key
        g.rank = dictionary
        return function_to_decorate(*args, **kwargs)
    return decorated_function


def get_hash_table(function_to_decorate):
    """  """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        dictionary = get_hash_map('hash_table')
        get_value = GetValue(dictionary)
        g.hash_table_msg = get_value.check_key
        g.hash_table = dictionary
        return function_to_decorate(*args, **kwargs)
    return decorated_function


def get_hash_users(function_to_decorate):
    """  """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        dictionary = get_hash_map('users')
        get_value = GetValue(dictionary)
        g.users_msg = get_value.check_key
        g.users = dictionary
        return function_to_decorate(*args, **kwargs)
    return decorated_function
    
    
def get_hash_pages(function_to_decorate):
    """  """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        dictionary = get_hash_map('pages')
        get_value = GetValue(dictionary)
        g.pages_msg = get_value.check_key
        g.pages = dictionary
        return function_to_decorate(*args, **kwargs)
    return decorated_function
    
    
def get_hash_settings(function_to_decorate):
    """  """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        dictionary = get_hash_map('settings')
        get_value = GetValue(dictionary)
        g.settings_msg = get_value.check_key
        g.settings = dictionary
        return function_to_decorate(*args, **kwargs)
    return decorated_function 