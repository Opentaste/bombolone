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

def check_authentication(function_to_decorate):
    def wrapped_function(*args,**kwargs):
        if g.my_id is None:
            abort(401)
        return function_to_decorate(*args,**kwargs)
       
    return wrapped_function
    
def check_admin(function_to_decorate):
    def wrapped_function(*args,**kwargs):
        if g.my['rank'] is not 10:
            abort(401)
        return function_to_decorate(*args,**kwargs)

    return wrapped_function   
 
def get_hash_login(function_to_decorate):
    def wrapped_function(*args,**kwargs):
        dict_login = g.db.hash_table.find_one({ 'name' : 'login' }, {'value': 1})
        return function_to_decorate(*args,**kwargs)

    return wrapped_function   
    
def get_hash_users(function_to_decorate):
    def wrapped_function(*args,**kwargs):
        dict_users = g.db.hash_table.find_one({ 'name' : 'users' }, {'value': 1})
        return function_to_decorate(*args,**kwargs)

    return wrapped_function
    