# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
from flask import g
from hashlib import md5, sha1

from shared import db, ALLOWED_EXTENSIONS

def init_mongodb():
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
        
    db.languages.update( { 'code' : 'it' }, { 'name' : 'Italiano', 'code' : 'it' }, True)
    db.languages.update( { 'code' : 'en' }, { 'name' : 'English', 'code' : 'en' }, True)
    
def clean_database():
    """
    """
    db.languages.remove()
    db.pages.remove()
    db.users.remove()
    
def create_password(word):
    """
    """
    new_pass_left = md5() 
    new_pass_right = sha1()
    new_pass_left.update(word)
    new_pass_right.update(word + 'magic_string')
    new_pass = new_pass_right.hexdigest() + 'f9eAf$2' + new_pass_left.hexdigest() + 'dY!sFd'
    return new_pass
    
def allowed_file(filename):
    """Check if the file has correct extension.
    Return True or False"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS