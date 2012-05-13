# -*- coding: utf-8 -*-
"""
    languages.py
    ~~~~~~
    The language module manages the languages you want 
    to use within application.
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
from flask import Blueprint, g, request, render_template
from pymongo.errors import PyMongoError

# Imports inside Bombolone
from decorators import check_admin, check_authentication, get_hash_languages 
from config import LIST_LANGUAGES

MODULE_DIR = 'modules/languages'
languages = Blueprint('languages', __name__)


class Languages(object):
    """ This class allows to :
    - get_languages
    - update
    """
    
    def __init__(self):
        self.user        = {}
        self.message     = None         # Error or succcess message
        self.status      = 'msg msg-error'
        self.image       = ''
        
    def get_languages(self, choose):
        """ Different kind of select query """
        # Get all available languages
        if choose is 0:
            return { x['code'] : x['value'][x['code']] for x in g.db.languages.find({ 'check' : True })}
        # Get all the languages
        elif choose is 1:
            return g.db.languages.find().sort('code')
        # Get language with a specific code
        elif choose is 2:
            return g.db.languages.find_one({ 'code' : g.lan })
        # Get all available languages
        elif choose is 3:
            names          = self.get_languages(2)
            list_languages = self.get_languages(0)
            return [ (x , y) for x, y in sorted(names['value'].iteritems()) if x in list_languages ]
        # Get all available languages
        elif choose is 4:
            names          = self.get_languages(2)
            list_languages = self.get_languages(0)
            return [ x for x, y in sorted(names['value'].iteritems()) if x in list_languages ]
        # Get all the languages
        elif choose is 5:
            names          = self.get_languages(2)
            list_languages = self.get_languages(0)
            return [ (x , y) for x, y in sorted(names['value'].iteritems()) ]
    
    def update(self):
        """ Saves which languages to use in web application """
        for code in LIST_LANGUAGES:
            if code != g.lan:
                if code in request.form and 'on' == request.form[code]:
                    check = True
                else:
                    check = False
                
                try:
                    # Update the permissions of the languages 
                    # and prepares the message of operation success
                    set_update = {'$set' : { 'check' : check } }
                    g.db.languages.update({'code' : code}, set_update )
                    self.message = g.languages_msg('success_update')	
                    self.status = 'msg msg-success'
                except PyMongoError:
                    self.message = g.languages_msg('error_mongo_update')


@languages.route('/admin/languages/', methods=['POST', 'GET'])
@check_authentication 
@check_admin
@get_hash_languages
def overview():
    """ Overview and tool update of all languages supported!"""    
    language_object = Languages()
    
    # Update the list of languages allowed on the site, 
    # except for the language used by your users at that time.
    if request.method == 'POST':
        language_object.update()
    
    # Come back a message when there is a message	
    if not language_object.message is None:
        message = language_object.message
        status = language_object.status
    
    # Gets documents from the collections of all languages 
    languages_list = language_object.get_languages(1)
    language_chosen = language_object.get_languages(2)
    return render_template( '{}/index.html'.format(MODULE_DIR), **locals())