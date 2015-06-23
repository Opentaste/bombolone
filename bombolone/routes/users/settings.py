# -*- coding: utf-8 -*-
"""
setting.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
""" 
from flask import Blueprint, request, session, g, Response, render_template, redirect

# Imports inside Bombolone
import bombolone.core.users
from bombolone.core.utils import msg_status, get_message
from bombolone.decorators import authentication, get_hash
import bombolone.model.ranks

MODULE_DIR = 'admin/settings'
settings = Blueprint('settings', __name__)

@settings.route('/settings/profile/')
@authentication
@get_hash('users')
@get_hash('settings')
@get_hash('upload')
@get_hash('admin')
def profile():
    """ """
    list_ranks = model.ranks.find()
    data = core.users.get(user_id=g.my['_id'], my_id=g.my['_id'])
    user = data["user"]
    return render_template('{}/profile.html'.format(MODULE_DIR), **locals())

@settings.route('/settings/account/')
@authentication
@get_hash('users')
@get_hash('settings')
@get_hash('admin')
def account():
    """ """
    list_ranks = model.ranks.find()
    language_name = g.languages_object.available_lang_by_tuple
    data = core.users.get(user_id=g.my['_id'], my_id=g.my['_id'])
    user = data["user"]
    return render_template('{}/account.html'.format(MODULE_DIR), **locals())

@settings.route('/settings/password/')
@authentication
@get_hash('users')
@get_hash('settings')
@get_hash('admin')
def password():
    """ """
    data = core.users.get(user_id=g.my['_id'], my_id=g.my['_id'])
    user = data["user"]
    return render_template('{}/password.html'.format(MODULE_DIR), **locals())
