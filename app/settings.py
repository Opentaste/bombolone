# -*- coding: utf-8 -*-
"""
    settings.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

# Imports inside Bombolone
from languages import Languages
from users import User
from decorators import check_authentication, get_hash_settings, get_hash_users
    
MODULE_DIR = 'modules/settings'
settings = Blueprint('settings', __name__)

languages_object = Languages()
 
@settings.route('/settings/account/', methods=['POST', 'GET'])
@check_authentication
@get_hash_settings
@get_hash_users
def account():
    """  """
    language_name = languages_object.get_languages(3)
    g.list_ranks = g.db.ranks.find()

    # Initial default user
    user_object = User(g.my['_id'])
    user = user_object.user

    if request.method == 'POST':
        user_object.update_account()	

    # Come back a message when there is a message	
    if not user_object.message is None:
        message = user_object.message
        status = user_object.status

    return render_template('%s/account.html' % MODULE_DIR, **locals() )
 
    
@settings.route('/settings/profile/', methods=['POST', 'GET'])
@check_authentication
@get_hash_settings
@get_hash_users
def profile():
    """  """
    language_name = languages_object.get_languages(3)
    g.list_ranks = g.db.ranks.find()

    # Initial default user
    user_object = User(g.my['_id'])
    user = user_object.user

    if request.method == 'POST':
        user_object.update_profile()	

    # Come back a message when there is a message	
    if not user_object.message is None:
        message = user_object.message
        status = user_object.status

    return render_template('%s/profile.html' % MODULE_DIR, **locals() )
    
    
@settings.route('/settings/password/', methods=['POST', 'GET'])
@check_authentication
@get_hash_settings
@get_hash_users
def password():
    """  """
    language_name = languages_object.get_languages(3)
    g.list_ranks = g.db.ranks.find()

    # Initial default user
    user_object = User(g.my['_id'])
    user = user_object.user

    if request.method == 'POST':
        user_object.update_password()	

    # Come back a message when there is a message	
    if not user_object.message is None:
        message = user_object.message
        status = user_object.status

    return render_template('%s/password.html' % MODULE_DIR, **locals() )
 