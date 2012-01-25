# -*- coding: utf-8 -*-
"""
    decorators.py
    ~~~~~~
    A collection of all the decorators used within Bombolone
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
from flask import g, abort
from functools import wraps


def check_authentication(function_to_decorate):
    """ Requires standard login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        if g.my_id is None:
            abort(401)
        return function_to_decorate(*args, **kwargs)
    return decorated_function
    
    
def check_admin(function_to_decorate):
    """ Requires admin login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        if g.my['rank'] is not 10:
            abort(401)
        return function_to_decorate(*args, **kwargs)
    return decorated_function   
    
    
def get_hash_login(function_to_decorate):
    """  """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        login_map = g.db.hash_table.find_one({ 'name' : 'login' })
        g.login = { x : y[g.lan] for x, y in login_map['value'].iteritems() }
        return function_to_decorate(*args, **kwargs)
    return decorated_function


def get_hash_users(function_to_decorate):
    """ Requires admin login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        users_map = g.db.hash_table.find_one({ 'name' : 'users' })
        g.users = { x : y[g.lan] for x, y in users_map['value'].iteritems() }
        return function_to_decorate(*args, **kwargs)
    return decorated_function 
   
    
def get_hash_table(function_to_decorate):
    """ Requires admin login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        hash_table_map = g.db.hash_table.find_one({ 'name' : 'hash_table' })
        g.hash_table = { x : y[g.lan] for x, y in hash_table_map['value'].iteritems() }
        return function_to_decorate(*args, **kwargs)
    return decorated_function     
    