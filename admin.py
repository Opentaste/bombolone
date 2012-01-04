# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
from flask import request, session, g, Response, render_template, url_for, redirect, abort, Markup
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

from helpers import init_mongodb, create_password

dict_login = {
    'error_1' : {
        'en' : 'error 1',
        'it' : 'errore 1'
    },
    'error_2' : {
        'en' : 'error 2',
        'it' : 'errore 2'
    }
}

def check_authentication(function_to_decorate):
    def wrapped_function():
        if g.my_id is None or g.my['rank'] != 10:
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
    #init_mongodb()
    return render_template('admin/dashboard.html')
 
@check_authentication   
def profile_page():
    """

    """
    return render_template('admin/profile.html')

@check_authentication     
def pages_page():
    """

    """
    list_pages = g.db.pages.find()
    return render_template('admin/pages.html', pages=list_pages)
 
@check_authentication   
def pages_content_page(_id):
    """

    """
    if request.method == 'POST':
        name = request.form['name']
        title_it = request.form['title_it']
        title_en = request.form['title_en']
        page = {
            'name' : name,
            'title': {
                'it' : title_it,
                'en' : title_en
            },
            'content' : {
                'it' : [],
                'en' : []
            }
        }
        
        len_of_label = len([int(x.split('_')[2]) for x in request.form if x.startswith('label_it_')])
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