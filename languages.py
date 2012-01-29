# -*- coding: utf-8 -*-
"""
    languages.py
    ~~~~~~
    The language module manages the languages you want to use within Bombolone.
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
from flask import Blueprint, g, request, render_template, url_for

# Imports inside bombolone
from decorators import check_admin, check_authentication, get_hash_languages 
from shared import LIST_LANGUAGES

MODULE_DIR = 'modules/languages'
languages = Blueprint('languages', __name__)
languages_permits = ['overview']
    

@languages.route('/admin/languages/', methods=['POST', 'GET'])
@check_authentication 
@check_admin
@get_hash_languages
def overview():
    """ Overview and tool update of all languages supported!"""    
    # Update the list of languages allowed on the site, 
    # except for the language used by your users at that time.
    if request.method == 'POST':
        for code in LIST_LANGUAGES:
            if code != g.lan:
                if code in request.form and 'on' == request.form[code]:
                    check = True
                else:
                    check = False
                
                try:
                    # Update the permissions of the languages 
                    # and prepares the message of operation success
                    g.db.languages.update( {'code' : code}, {'$set' : { 'check' : check } } )
                    message = g.languages['update_ok']	
                    status = 'mes_green'
                except:
                    message = g.languages['update_no']
                    status = 'mes_red'
                
    # Gets documents from the collections of all languages 
    languages_list = g.db.languages.find().sort('code')
    language_chosen = g.db.languages.find_one({ 'code' : g.lan })
    return render_template( MODULE_DIR+'/index.html', **locals())
    