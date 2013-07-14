# -*- coding: utf-8 -*-
"""
setting.py
~~~~~~

:copyright: (c) 2013 by Bombolone
""" 
# Imports outside Bombolone
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId

# Imports from Bombolone
from decorators import check_authentication, get_hash

# Imports from Bombolone's CORE
from core.users.account import core_settings
from core.users.users import User
from core.utils import ensure_objectid, msg_status
from core.verify import check_verify_email

MODULE_DIR = 'admin/settings'
settings = Blueprint('settings', __name__)


@settings.route('/settings/profile/')
@check_authentication
@get_hash('users')
@get_hash('settings')
@get_hash('upload')
def profile():
    """ """

    list_ranks = g.db.ranks.find()
    data = core_settings(g.my['_id'])
        
    user = data["user"]
    return render_template('{}/profile.html'.format(MODULE_DIR), **locals())


@settings.route('/settings/account/')
@check_authentication
@get_hash('users')
@get_hash('settings')
def account():
    """ """

    list_ranks = g.db.ranks.find()
    language_name = g.languages_object.get_languages(3)
    data = core_settings(g.my['_id'])
        
    user = data["user"]
    return render_template('{}/account.html'.format(MODULE_DIR), **locals())


@settings.route('/settings/password/')
@check_authentication
@get_hash('users')
@get_hash('settings')
def password():
    """ """
    
    data = core_settings(g.my['_id'])
        
    user = data["user"]
    return render_template('{}/password.html'.format(MODULE_DIR), **locals())


@settings.route('/change_email/<check>/')
@get_hash('settings')
def change_email(check):
    """ """
    
    user = check_verify_email(check)
    if user and "new_email" in user:
        user['email'] = user['new_email']
        del(user['new_email'])
        del(user['email_verify'])
        g.db.users.update({ '_id' : ensure_objectid(user['_id']) }, user)
        message = g.settings_msg('success_update_email')
        status = 'msg msg-success'
    else:
        message = g.settings_msg('error_update_email')
        status = 'msg msg-error'
    return render_template('{}/change_email.html'.format(MODULE_DIR), **locals())