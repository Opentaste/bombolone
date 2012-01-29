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

# Imports inside bombolone modules
from helpers import get_hash_map


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
    
    
def get_hash_languages(function_to_decorate):
    """  """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        g.languages = get_hash_map('languages')
        return function_to_decorate(*args, **kwargs)
    return decorated_function    

    
def get_hash_login(function_to_decorate):
    """  """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        g.login = get_hash_map('login')
        return function_to_decorate(*args, **kwargs)
    return decorated_function
   
    
def get_hash_pages(function_to_decorate):
    """ Requires admin login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        g.pages = get_hash_map('pages')
        return function_to_decorate(*args, **kwargs)
    return decorated_function
    
    
def get_hash_rank(function_to_decorate):
    """ Requires admin login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        g.rank = get_hash_map('rank')
        return function_to_decorate(*args, **kwargs)
    return decorated_function


def get_hash_table(function_to_decorate):
    """ Requires admin login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        g.hash_table = get_hash_map('hash_table')
        return function_to_decorate(*args, **kwargs)
    return decorated_function


def get_hash_users(function_to_decorate):
    """ Requires admin login credentials """
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        g.users = get_hash_map('users')
        return function_to_decorate(*args, **kwargs)
    return decorated_function 
      