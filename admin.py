# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
import re
from flask import request, session, g, Response, render_template, url_for, redirect, abort, Markup
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

from helpers import init_mongodb, create_password
from language import dict_login, setting_message


def check_authentication(function_to_decorate):
    def wrapped_function():
        if g.my_id is None:
            abort(401)
        return function_to_decorate()
       
    return wrapped_function


def login_page():
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
	        return redirect(url_for('admin'))
	return render_template('admin/login.html')
	
def logout_page():
	"""

	"""
	session.pop('user_id', None)
	return redirect(url_for('home'))
	
@check_authentication
def admin_page():
    """
    
    """
    init_mongodb()
    return render_template('admin/dashboard.html')
 
@check_authentication   
def profile_page():
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

@check_authentication     
def pages_page():
    """

    """
    list_pages = g.db.pages.find()
    return render_template('admin/pages.html', pages=list_pages)
  
def pages_content_page(_id):
    """

    """
    if g.my_id is None:
        abort(401)
    if request.method == 'POST':
        name = request.form['name']
        name_file = request.form['name_file']
        title_it = request.form['title_it']
        title_en = request.form['title_en']
        url_it = request.form['url_it']
        url_en = request.form['url_en']
        page = {
            'name' : name,
            'file' : name_file,
            'title': {
                'it' : title_it,
                'en' : title_en
            },
            'url': {
                'it' : url_it,
                'en' : url_en
            },
            'content' : {
                'it' : [],
                'en' : []
            }
        }
        
        len_of_label = len([int(x.split('_')[2]) for x in request.form if x.startswith('label_it_')])
        
        page['input_label'] = [ int(request.form['input_label_'+str(i)]) for i in range(len_of_label)]
        
        for i in range(len_of_label):
            page['content']['it'].append( { 'label' : 'label_it_'+str(i) , 'value' : request.form['label_it_'+str(i)] })
        for i in range(len_of_label):
            page['content']['en'].append( { 'label' : 'label_en_'+str(i) , 'value' : request.form['label_en_'+str(i)] })
                
        g.db.pages.update( { '_id' : ObjectId(_id) }, page)
        
    page_content = g.db.pages.find_one({ '_id' : ObjectId(_id) })
    
    return render_template('admin/pages_content.html', page=page_content)
    
@check_authentication 
def languages_page():
    """

    """
    list_languages = g.db.languages.find()
    return render_template('admin/languages.html', lan=list_languages)