# -*- coding: utf-8 -*-
"""
core.languages.py
~~~~~~
The language module manages the languages you want
to use within application.

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
from flask import g, request, session

# Imports inside Bombolone
import model.languages

LIST_LANGUAGES = ['ar','cn','de','en','es','fr','gr','it','jp','pt','ru','tr']

class Languages(object):
    """ This class allows to """

    def __init__(self):
        self.message = None         # Error or success message
        self.status = 'msg msg-error'

    @property
    def available_lang(self):
        """ 
        Get all available languages 
        {u'en': u'English', u'it': u'Italiano'}

        """
        return { x['code'] : x['value'][x['code']] for x in model.languages.find(check=True)}

    @property
    def all_lang(self):
        """ 
        Get all the languages.
        Return the entire collection sorted by code.

        """
        return model.languages.find(sorted_by='code')

    def get_all_lang_by_code(self, code):
        """ 
        Get language with a specific code 
        Return all the language by my lang code
        {   u'code': u'en', 
               u'_id': ObjectId('123456'), 
             u'check': True, 
             u'value': {
                u'ru': u'Russian', 
                u'fr': u'French', 
                u'en': u'English', 
                u'cn': u'Chinese', 
                u'pt': u'Portuguese', 
                u'no': u'Norwegian', 
                u'tr': u'Turkish', 
                u'de': u'German', 
                u'jp': u'Japanese', 
                u'it': u'Italian', 
                u'ar': u'Arabic', 
                u'es': u'Spanish', 
                u'gr': u'Greek'
            }
        }

        """
        return model.languages.find(code=code, only_one=True)

    @property
    def available_lang_by_tuple(self):
        """ 
        Get all available languages by a list of tuple.
        Return [(u'en', u'English'), (u'it', u'Italian')]

        """
        names = self.get_all_lang_by_code(g.lang)
        list_languages = self.available_lang
        return [ (x , y) for x, y in sorted(names['value'].iteritems()) if x in list_languages ]

    @property
    def available_lang_code(self):
        """ 
        Get all available languages code.
        Return [u'en', u'it']

        """
        names = self.get_all_lang_by_code(g.lang)
        list_languages = self.available_lang
        return [ x for x, y in sorted(names['value'].iteritems()) if x in list_languages ]

    @property
    def all_lang_code(self):
        """ 
        Get all languages code.
        Return [u'en', ..., u'it']

        """
        return [ lang['code'] for lang in self.all_lang ]

    @property
    def all_lang_by_tuple(self):
        """ 
        Get all languages by a list of tuple.
        Return 
        [   (u'ar', u'Arabic'), 
            (u'cn', u'Chinese'), 
            (u'de', u'German'), 
            (u'en', u'English'), 
            (u'es', u'Spanish'), 
            (u'fr', u'French'), 
            (u'gr', u'Greek'), 
            (u'it', u'Italian'), 
            (u'jp', u'Japanese'), 
            (u'no', u'Norwegian'), 
            (u'pt', u'Portuguese'), 
            (u'ru', u'Russian'), 
            (u'tr', u'Turkish')
        ]

        """
        names = self.get_all_lang_by_code(g.lang)
        return [ (x , y) for x, y in sorted(names['value'].iteritems())]

    def update(self):
        """Saves which languages to use in web application."""
        for code in LIST_LANGUAGES:
            if code != g.lang:
                if code in request.form and 'on' == request.form[code]:
                    check = True
                else:
                    check = False
                language = model.languages.find(code=code, only_one=True)
                model.languages.update(language_id=language['_id'], check=check)
                self.message = g.languages_msg('success_update')
                self.status = 'msg msg-success'

def get_list():
    """ """
    lan_object = Languages()
    languages_list = lan_object.all_lang
    language_chosen = lan_object.get_all_lang_by_code(g.lang)
    data = {
        "success": True,
        "languages": languages_list,
        "chosen": language_chosen
    }
    return data

def show():
    """ """
    data = {
        "success": True,
    }
    return data

def new():
    """ """
    data = {
        "success": True,
    }
    return data

def update():
    """ """
    lan_object = Languages()
    lan_object.update()
    message = lan_object.message
    status = lan_object.status
    data = {
        "success": True,
    }
    return data

def remove():
    """ """
    data = {
        "success": True,
    }
    return data

def change(lang=None, my_id=None):
    """
    """
    if not lang in g.available_languages:
        data = {
            "result": False,
            "value": "Error #1"
        }
    else:
        # With the user logged set the language in his profile, 
        # but the user isn't logged set the language inside the session.
        if my_id:
            model.users.update(item_id=my_id,
                               lan=lang,
                               language=g.available_languages[lang])
        else:
            session['language'] = lang
        data = {
            "result": True,
            "value": ""
        }
    return data
