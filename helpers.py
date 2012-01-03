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
    g.db.pages.remove()
    
    for num in range(1,6):
        page = {
            'name' : 'page_'+str(num),
            'title': {
                'en' : 'Title '+str(num),
                'it' : 'Titolo '+str(num)
            },
            'content' : {
                'en' : [
                    { 'label' : 'label_1' , 'value' : '1' },
                    { 'label' : 'label_2' , 'value' : '2' },
                    { 'label' : 'label_3' , 'value' : '3' },
                    { 'label' : 'label_4' , 'value' : '4' },
                    { 'label' : 'label_5' , 'value' : '5' },
                    { 'label' : 'label_6' , 'value' : '6' },
                    { 'label' : 'label_7' , 'value' : '7' },
                    { 'label' : 'label_8' , 'value' : '8' }],
                'it' : [
                    { 'label' : 'label_1' , 'value' : '1' },
                    { 'label' : 'label_2' , 'value' : '2' },
                    { 'label' : 'label_3' , 'value' : '3' },
                    { 'label' : 'label_4' , 'value' : '4' },
                    { 'label' : 'label_5' , 'value' : '5' },
                    { 'label' : 'label_6' , 'value' : '6' },
                    { 'label' : 'label_7' , 'value' : '7' },
                    { 'label' : 'label_8' , 'value' : '8' }]
            }
        }
        if num == 1:
            page['name'] = 'home_page'
            page['title'] = { 'en' : 'Home Page', 'it' : 'Home' }
            g.db.pages.update( { 'name' : 'home_page' }, page, True)
        else:
            g.db.pages.update( { 'name' : 'page_'+str(num) }, page, True)
        
    g.db.languages.update( { 'code' : 'it' }, { 'name' : 'Italiano', 'code' : 'it' }, True)
    g.db.languages.update( { 'code' : 'en' }, { 'name' : 'English', 'code' : 'en' }, True)