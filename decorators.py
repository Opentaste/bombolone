# -*- coding: utf-8 -*-
"""
decorators.py
~~~~~~
A collection of all the decorators

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
from flask import g, abort
from functools import wraps

# Imports inside Bombolone
from config import NOTACTIVATED
from core.utils import GetValue, get_hash_map

def authentication(function_to_decorate):
    """Requires standard login credentials"""
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        """ """
        if g.my is None:
            abort(401)
        status = g.my.get('status', None)
        if status is None or status == NOTACTIVATED:
            abort(401)
        return function_to_decorate(*args, **kwargs)
    return decorated_function

def check_rank(rank):
    """
    Check the user rank, if the user has not the 
    right rank is redirect to a 401 page.

    It can be used like this:
    @check_rank(40)

    """
    def real_decorator(function_to_decorate):
        @wraps(function_to_decorate)
        def decorated_function(*args, **kwargs):
            if g.my is None:
                abort(401)
            status = g.my.get('status', None)
            if status is None or status == NOTACTIVATED:
                abort(401)
            if g.my.get('rank', 80) > rank:
                abort(401)
            return function_to_decorate(*args, **kwargs)
        return decorated_function
    return real_decorator

def get_hash(hash_map_name):
    """
    Set the hashmap called inside the 'g' global Flask variable.

    It can be called like this:
    @get_hash('admin')

    """
    def real_decorator(function_to_decorate):
        @wraps(function_to_decorate)
        def decorated_function(*args, **kwargs):
            dictionary = get_hash_map(hash_map_name, g.lang)
            get_value = GetValue(dictionary)
            setattr(g, hash_map_name + '_msg', get_value.check_key)
            setattr(g, hash_map_name, dictionary)
            return function_to_decorate(*args, **kwargs)
        return decorated_function
    return real_decorator
