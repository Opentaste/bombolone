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
            'content' : [
                { 'label' : 'label_1' , 'value' : '' },
                { 'label' : 'label_2' , 'value' : '' },
                { 'label' : 'label_3' , 'value' : '' },
                { 'label' : 'label_4' , 'value' : '' },
                { 'label' : 'label_5' , 'value' : '' },
                { 'label' : 'label_6' , 'value' : '' },
                { 'label' : 'label_7' , 'value' : '' },
                { 'label' : 'label_8' , 'value' : '' }
            ]
        }
        g.db.pages.update( { 'name' : 'Page '+str(num) }, page, True)
        
    g.db.languages.update( { 'code' : 'it' }, { 'name' : 'Italiano', 'code' : 'it' }, True)
    g.db.languages.update( { 'code' : 'en' }, { 'name' : 'English', 'code' : 'en' }, True)