# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
from flask import g

def init_mongodb():
    """ fixtures MongoDB
    """
    g.db.languages.update( { 'code' : 'it' }, { 'name' : 'Italiano', 'code' : 'it' }, True)
    g.db.languages.update( { 'code' : 'en' }, { 'name' : 'English', 'code' : 'en' }, True)
    pass