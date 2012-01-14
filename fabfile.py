# -*- coding: utf-8 -*-
"""
    fabfile.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
from flask import session

from helpers import init_mongodb, clean_database

def init():
    print 'Initialization Bombolone'
    print '##########################'
    print '\n'
    init_mongodb()
    print ' - Start Database'
    print '\n'
    
def clean_db():
    print 'Clean database'
    print '##########################'
    print '\n'
    clean_database()
    print ' - Clean Database'
    init_mongodb()
    print ' - Start Database'
    print '\n'