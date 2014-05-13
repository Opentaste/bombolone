# -*- coding: utf-8 -*-
"""
languages.py
~~~~~~
The language module manages the languages you want 
to use within application.

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
""" 
from flask import Blueprint, g, request, render_template, session, redirect

# Imports inside Bombolone
from core.languages import Languages
from decorators import check_rank, get_hash
import model.users

MODULE_DIR = 'admin/languages'
languages = Blueprint('languages', __name__)

@languages.route('/admin/languages/', methods=['POST', 'GET'])
@check_rank(10)
@get_hash('languages')
@get_hash('admin')
def index():
    """ 
    Overview and tool update of all languages supported!
    """
    # Update the list of languages allowed on the site, 
    # except for the language used by your users at that time.
    if request.method == 'POST':
        lan_object = Languages()
        lan_object.update()
        message = lan_object.message
        status = lan_object.status
    
    # Gets documents from the collections of all languages 
    languages_list = g.languages_object.all_lang
    language_chosen = g.languages_object.get_all_lang_by_code(g.lang)
    return render_template( '{}/index.html'.format(MODULE_DIR), **locals())


@languages.route('/language/<lan>/')
def change(lan):
    """ 
    Change language
    """
    if lan in g.available_languages:
        path = request.args.get('path', "/")
        # With the user logged set the language in his profile, 
        # but the user isn't logged set the language inside the session.
        if hasattr(g, 'my') and g.my:
            model.users.update(user_id=g.my['_id'],
                               lan=lan,
                               language=g.available_languages[lan])
        session['language'] = lan
        return redirect(path)
    return '{ "result" : false, "value" : "Error #1" }'
