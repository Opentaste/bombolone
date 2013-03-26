# -*- coding: utf-8 -*-
"""
languages.py
~~~~~~
The language module manages the languages you want 
to use within application.

:copyright: (c) 2012 by Opentaste
""" 
# Imports outside OpenTaste
from flask import Blueprint, g, request, render_template, session, abort
from pymongo.errors import PyMongoError

# Imports inside OpenTaste
from config import LIST_LANGUAGES

class Languages(object):
    """ This class allows to :
    - get_languages
    - update
    """
    
    def __init__(self):
        self.message = None         # Error or success message
        self.status = 'msg msg-error'
        
    def get_languages(self, choose): # TODO: death to magic numbers.
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
            names = self.get_languages(2)
            list_languages = self.get_languages(0)
            return [ (x , y) for x, y in sorted(names['value'].iteritems()) if x in list_languages ]
        # Get all available languages
        elif choose is 4:
            names = self.get_languages(2)
            list_languages = self.get_languages(0)
            return [ x for x, y in sorted(names['value'].iteritems()) if x in list_languages ]
        # Get all the languages
        elif choose is 5:
            names = self.get_languages(2)
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