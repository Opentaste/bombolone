# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
import re
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect, abort
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

# Imports inside bombolone
from decorators import check_authentication
from helpers import create_password
from language import dict_login, setting_message
from upload import upload_file


admin = Blueprint('admin', __name__)


@admin.route('/login/', methods=['POST', 'GET'])
def login():
	"""
	
	"""
	if request.method == 'POST':
	    username = request.form['username'].lower()
	    password = request.form['password']
	    user = g.db.users.find_one({'username' : username})
	    if not username and not password:
	        g.status = 'mes-red'
	        g.message = dict_login['error_1']
	    elif user is None or user['password'] != create_password(password):
	        g.status = 'mes-red'
	        g.message = dict_login['error_2']
	    else:
	        session['user_id'] = user['_id']
	        return redirect(url_for('admin.dashboard'))
	return render_template('admin/login.html')
	
	
@admin.route('/logout/')
def logout():
	"""

	"""
	session.pop('user_id', None)
	return redirect(url_for('content.home'))
	
	
@check_authentication
@admin.route('/admin/')
def dashboard():
    """
    
    """
    return render_template('admin/dashboard.html')
 
 
@check_authentication 
@admin.route('/admin/profile/', methods=['POST', 'GET'])  
def profile():
    """

    """
    if request.method == 'POST':
		# get request ot_name
		username = request.form['username']
		password = request.form['password']
		password_check = request.form['password_check']
		regx = re.compile('^'+username+'$', re.IGNORECASE)
		result = g.db.users.find_one({"username" : regx })
		old_username = g.my['username']
		
		if len(password) < 6 and len(password) > 0:
		    g.message = setting_message['password_error_1']	
		    g.status = 'mes-red'
		elif password != password_check and len(password) > 0:
		    g.message = setting_message['password_error_2']	
		    g.status = 'mes-red'
		# control several things:
		# - username wrote
		# - username's length is greater than 2
		# - username is available and it is not the same as 
		# - the format of username is incorrect
		elif not len(username):
		    g.message = setting_message['account_error_1']
		    g.status = 'mes-red'
		elif len(username) < 2:
		    g.message = setting_message['account_error_2']
		    g.status = 'mes-red'
		elif result is not None and username != old_username:
		    g.message = setting_message['account_error_4']
		    g.status = 'mes-red'
		elif not re.match(r'^[a-zA-Z0-9_]+$', username):
		    g.message = setting_message['account_error_7']
		    g.status = 'mes-red'
		else:
		    g.my['username'] = username
		    g.my['password'] = create_password(password)
		    g.db.users.update({"_id": g.my['_id']}, g.my)
		    g.message = setting_message['account_ok']
		    g.status = 'mes-green'

    return render_template('admin/profile.html')