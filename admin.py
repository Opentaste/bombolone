# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~
    The admin module allows users to register, log in, log out...
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
import re
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect, abort
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

# Imports inside bombolone
from decorators import check_authentication, get_hash_login, get_hash_users
from helpers import create_password, language_check
from upload import upload_file
from users import request_account_form, upload_avatar

MODULE_DIR = 'modules/admin'
admin = Blueprint('admin', __name__)


@admin.route('/login/', methods=['POST', 'GET'])
@get_hash_login
def login():
	"""
	
	"""
	if request.method == 'POST':
	    username = request.form['username'].lower()
	    password = request.form['password']
	    user = g.db.users.find_one({'username' : username})
	    status = 'mes_red'
	    if not username and not password:
	        message = g.login['error_1']
	    elif user is None or user['password'] != create_password(password):
	        message = g.login['error_2']
	    else:
	        session['user_id'] = user['_id']
	        return redirect(url_for('admin.dashboard'))
	        
	return render_template(MODULE_DIR+'/login.html', **locals())
	
	
@admin.route('/logout/')
@check_authentication
def logout():
	"""

	"""
	session.pop('user_id', None)
	return redirect(url_for('content.home'))
	
	
@admin.route('/admin/')
@check_authentication
def dashboard():
    """
    
    """
    return render_template(MODULE_DIR+'/dashboard.html')
 

@admin.route('/admin/profile/', methods=['POST', 'GET'])  
@check_authentication 
@get_hash_users
def profile():
    """

    """
    language_name = language_check()
    message = None
    
    my = g.my

    if request.method == 'POST':
        file = request.files['file']
        form = request.form   
        
        old_username = my['username']
        old_email = my['email']
        
        my['username'] = form['username']
        my['email'] = form['email']
        my['lan'] = form['language']
        my['time_zone'] = form['time_zone']
        my['name'] = form['name']
        my['description'] = form['description']
        my['location'] = form['location']
        my['web'] = form['web']

        message = request_account_form(my, old_username, old_email, form['password'], form['password_new'], form['password_check'])
        if message is None:
            
            if len(form['password_new']):
                my['password'] = create_password(form['password_new'])
            
            if file and allowed_file(file.filename):
                my['image'] = upload_avatar(file, my)
            
            g.db.users.update({ '_id' : ObjectId(my['_id']) }, my)			
            return redirect(url_for('admin.profile'))
			
	if not message is None:
	    status = 'mes_red'

    return render_template(MODULE_DIR+'/profile.html', **locals())