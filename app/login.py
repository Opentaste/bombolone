# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~
    The admin module allows users to register, log in, log out...
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
import re
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect, abort
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

# Imports inside Bombolone
from decorators import check_authentication, get_hash_login, get_hash_users
from helpers import create_password
from languages import Languages

MODULE_DIR = 'modules/login'
login = Blueprint('login', __name__)

languages_object = Languages()

@login.route('/login/', methods=['POST', 'GET'])
@get_hash_login
def login_page():
	""" """
	if request.method == 'POST':
	    username = request.form['username']
	    password = request.form['password']
	    regx = re.compile('^'+username+'$', re.IGNORECASE)
	    user = g.db.users.find_one({'username' : regx})
	    status = 'mes_red'
	    
	    # If the field isn't complete
	    if not username and not password:
	        message = g.login['error_1']
	        	        
	    # If there are wrong Username/Email and password combination.
	    elif user is None or user['password'] != create_password(password):
	        message = g.login['error_2']
	           
	    else:
	        session['user_id'] = user['_id']
	        return redirect(url_for('home.index'))
	        
	return render_template(MODULE_DIR+'/login.html', **locals())
	
	
@login.route('/logout/')
@check_authentication
def logout():
	"""

	"""
	session.pop('user_id', None)
	return redirect(url_for('home.index'))
