# -*- coding: utf-8 -*-
"""
    init.py
    ~~~~~~
    Implements several functions to populate the database startup Bombolone.
    
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
from shared import db


def clean_database():
    """ Removes all the collections in the database. """
    db.languages.remove()
    db.pages.remove()
    db.users.remove()


def init_languages():
    """ Initializes the base 8 languages, 
    and in any language is written the name of the other.
    """
    
    dict_languages = {
        'it' : {
            'it' : 'Italiano',
            'en' : '',
            'pt' : '',
            'fr' : '',
            'de' : '',
            'jp' : '',
            'cn' : '',
            'ru' : '',
            'tr' : ''
        },
        'en' : {
            'it' : 'Italiano',
            'en' : '',
            'pt' : '',
            'fr' : '',
            'de' : '',
            'jp' : '',
            'cn' : '',
            'ru' : '',
            'tr' : ''
        },
        'es' : {
            'it' : 'Italiano',
            'en' : '',
            'pt' : '',
            'fr' : '',
            'de' : '',
            'jp' : '',
            'cn' : '',
            'ru' : '',
            'tr' : ''
        },
        'pt' : {
            'it' : 'Italiano',
            'en' : '',
            'pt' : '',
            'fr' : '',
            'de' : '',
            'jp' : '',
            'cn' : '',
            'ru' : '',
            'tr' : ''
        },
        'fr' : {
            'it' : 'Italiano',
            'en' : '',
            'pt' : '',
            'fr' : '',
            'de' : '',
            'jp' : '',
            'cn' : '',
            'ru' : '',
            'tr' : ''
        },
        'de' : {
            'it' : 'Italiano',
            'en' : '',
            'pt' : '',
            'fr' : '',
            'de' : '',
            'jp' : '',
            'cn' : '',
            'ru' : '',
            'tr' : ''
        },
        'jp' : {
            'it' : 'Italiano',
            'en' : '',
            'pt' : '',
            'fr' : '',
            'de' : '',
            'jp' : '',
            'cn' : '',
            'ru' : '',
            'tr' : ''
        },
        'cn' : {
            'it' : 'Italiano',
            'en' : '',
            'pt' : '',
            'fr' : '',
            'de' : '',
            'jp' : '',
            'cn' : '',
            'ru' : '',
            'tr' : ''
        },
        'ru' : {
            'it' : 'Italiano',
            'en' : '',
            'pt' : '',
            'fr' : '',
            'de' : '',
            'jp' : '',
            'cn' : '',
            'ru' : '',
            'tr' : ''
        },
        'tr' : {
            'it' : 'Italiano',
            'en' : '',
            'pt' : '',
            'fr' : '',
            'de' : '',
            'jp' : '',
            'cn' : '',
            'ru' : '',
            'tr' : ''
        }
    }
    
    # Insert the languages dictionaries 
    for lan in dict_languages:
        db.languages.insert( { 'code' : lan, 'value' : dict_languages[lan] })


def init_mongodb():
    """ Initialize the database MongoDB of Bombolone. """
    init_languages()


def init_mongodb_two():
    """ fixtures MongoDB
    """    
    admin_pass = create_password('admin')
    user_pass = create_password('user')
    
    db.users.update( { 'username' : 'admin' }, { 'username' : 'admin', 'password' : admin_pass, 'rank' : 10 }, True)
    db.users.update( { 'username' : 'user' }, { 'username' : 'user', 'password' : user_pass, 'rank' : 20 }, True)
    
    for num in range(1,6):
        page = {
            'name' : 'page_'+str(num),
            'file' : 'page_'+str(num),
            'title': {
                'en' : 'Title '+str(num),
                'it' : 'Titolo '+str(num)
            },
            'description': {
                'en' : 'Description '+str(num),
                'it' : 'Descrizione '+str(num)
            },
            'url': {
                'en' : 'page_'+str(num),
                'it' : 'pagina_'+str(num)
            },
            'content' : {
                'en' : [
                    { 'label' : 'label_1' , 'alias' : 'Label 1', 'value' : '1', 'type' : 0 },
                    { 'label' : 'label_2' , 'alias' : 'Label 2', 'value' : '2', 'type' : 0 },
                    { 'label' : 'label_3' , 'alias' : 'Label 3', 'value' : '3', 'type' : 0 },
                    { 'label' : 'label_4' , 'alias' : 'Label 4', 'value' : '4', 'type' : 0 },
                    { 'label' : 'label_5' , 'alias' : 'Label 5', 'value' : '5', 'type' : 0 }],
                'it' : [
                    { 'label' : 'label_1' , 'alias' : 'Campo 1', 'value' : '1', 'type' : 0 },
                    { 'label' : 'label_2' , 'alias' : 'Campo 2', 'value' : '2', 'type' : 0 },
                    { 'label' : 'label_3' , 'alias' : 'Campo 3', 'value' : '3', 'type' : 0 },
                    { 'label' : 'label_4' , 'alias' : 'Campo 4', 'value' : '4', 'type' : 0 },
                    { 'label' : 'label_5' , 'alias' : 'Campo 5', 'value' : '5', 'type' : 0 }]
            },
            'input_label': [ 1, 1, 1, 1, 1 ]
        }
        
        if num == 1:
            page['name'] = 'home_page'
            page['file'] = 'home'
            page['title'] = { 'en' : 'Home Page', 'it' : 'Home' }
            page['url'] = None
            db.pages.update( { 'name' : 'home_page' }, page, True)
        else:
            db.pages.update( { 'name' : 'page_'+str(num) }, page, True)
        