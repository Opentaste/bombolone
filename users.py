# -*- coding: utf-8 -*-
"""
    users.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
import re
from flask import request, session, g, Response, render_template, url_for, redirect, abort, Markup
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

from admin import check_authentication
from language import dict_login, setting_message
    
MODULE_DIR = 'admin/users'
    
@check_authentication 
def users_page():
    """

    """
    users_list = g.db.users.find()
    return render_template( MODULE_DIR+'/index.html', **locals() )
    
def users_new_page():
    """
    
    """
    if g.my['rank'] is not 10:
        abort(401)
        
    if request.method == 'POST':
        pass
        
    return render_template( MODULE_DIR+'/new.html' )

@check_authentication
def user_profile_page(_id):
    """

    """
    user = g.db.users.find_one({ '_id' : ObjectId(_id) })
    return render_template( MODULE_DIR+'/update.html', **locals() )