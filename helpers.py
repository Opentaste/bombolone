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
    
    for num in range(1,9):
        print num
        page = {
            'name' : 'Page '+str(num),
            'title': 'Title '+str(num),
            'content' : {
                'label_1' : '',
                'label_2' : '',
                'label_3' : '',
                'label_4' : '',
                'label_5' : '',
                'label_6' : '',
                'label_7' : ''
            }
        }
        g.db.pages.update( { 'name' : 'Page '+str(num) }, page, True)
        
    g.db.languages.update( { 'code' : 'it' }, { 'name' : 'Italiano', 'code' : 'it' }, True)
    g.db.languages.update( { 'code' : 'en' }, { 'name' : 'English', 'code' : 'en' }, True)