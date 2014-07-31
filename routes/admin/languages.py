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
    return render_template( '{}/index.html'.format(MODULE_DIR), **locals())


@languages.route('/admin/languages/new/')
@languages.route('/admin/languages/update/<language_id>/')
@check_rank(10)
@get_hash('languages')
@get_hash('admin')
def upsert(language_id=None):
    """ Upsert """   
    return render_template('{}/upsert.html'.format(MODULE_DIR))


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
