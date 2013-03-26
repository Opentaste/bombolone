# -*- coding: utf-8 -*-
"""
languages.py
~~~~~~
The language module manages the languages you want 
to use within application.

:copyright: (c) 2013 by Leonardo Zizzamia
:license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
from flask import Blueprint, g, request, render_template
from pymongo.errors import PyMongoError

# Imports inside Bombolone
from decorators import check_rank, get_hash 
from config import LIST_LANGUAGES

MODULE_DIR = 'admin/languages'
languages = Blueprint('languages', __name__)

@languages.route('/admin/languages/', methods=['POST', 'GET'])
@check_rank(10)
@get_hash('languages')
def overview():
    """ Overview and tool update of all languages supported!"""
    # Update the list of languages allowed on the site, 
    # except for the language used by your users at that time.
    if request.method == 'POST':
        data = language_object.update()
    
    # Gets documents from the collections of all languages 
    languages_list = g.languages_object.get_languages(1)
    language_chosen = g.languages_object.get_languages(2)
    return render_template( '{}/index.html'.format(MODULE_DIR), **locals())

@languages.route('/language/<lan>/')
def change(lan):
    """ """
    # Return an internal error if isn't an ajax request
    if request.is_xhr:
        if lan in g.available_languages:
            # With the user logged set the language in his profile, 
            # but the user isn't logged set the language inside the session.
            if g.my:
                g.db.users.update({"_id": g.my['_id']}, {"$set": { "lan" : lan, "language": g.available_languages[lan] } })
            else:
                session['language'] = lan
            # Return a json string
            return '{ "result" : true }'
        return '{ "result" : false, "value" : "Error #1" }'
    abort(401)