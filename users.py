# -*- coding: utf-8 -*-
"""
    users.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
import re
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

# Imports inside bombolone
from decorators import check_authentication, check_admin
from helpers import create_password, language_check
from hash_table import get_hash_map
from not_allowed import NAME_LIST
from validators import email, length, username
    
MODULE_DIR = 'admin/users'

users = Blueprint('users', __name__)

 
@users.route('/admin/users/')
@check_authentication
def overview():
    """

    """
    users_list = g.db.users.find()
    return render_template( MODULE_DIR+'/index.html', **locals() )
 
  
@users.route('/admin/users/new/', methods=['POST', 'GET'])
@check_authentication
@check_admin
def new():
    """
    
    """       
    language_name = language_check()
    # get the hash map for the users
    g.users = get_hash_map('users')
    message = None
    
    my = { 
         'username' : '', 
            'email' : '',
         'password' : '', 
             'rank' : 20,
         'language' : '',
              'lan' : '',
        'time_zone' : 'Europe/London',
             'name' : '',
      'description' : '',
         'location' : '',
              'web' : ''
    }

    if request.method == 'POST':
        form = request.form    
        my = { 
             'username' : form['username'], 
                'email' : form['email'],
             'password' : form['password'], 
       'password_check' : form['password_check'], 
                 'rank' : form['rank'],
                  'lan' : form['language'],
            'time_zone' : form['time_zone'],
                 'name' : form['name'],
          'description' : form['description'],
             'location' : form['location'],
                  'web' : form['web']
        }
        message = request_account_form(my, '', '')
        if message is None:
            my['password'] = create_password(my['password'])
            del(my['password_check'])
            g.db.users.insert(my)			
            return redirect(url_for('users.overview'))
			
	if not message is None:
	    status = 'mes_red'
        
    return render_template( MODULE_DIR+'/new.html', **locals())
    
def request_account_form(my, old_username, old_email):
    """
    """
    check_result = check_username(my['username'])
    res_email = None
    message = None
    
    # ~~~~~
    if my['email'] != old_email:
        res_email = g.db.users.find_one({"email" : my['email'] })
    
    # ~~~~~
    if not len(my['username']):
        message = g.users['account_error_1']
    
    # ~~~~~
    if not length(my['username'], 2, 20):
        message = g.users['account_error_2']
    
    # ~~~~~
    if check_result is not None:
        message = g.users['account_error_4']
    
    # ~~~~~
    if my['username'] in NAME_LIST:
        message = g.users['account_error_3']
    
    # ~~~~~
    if not username(my['username']):
        message = g.users['account_error_7']
    
    # ~~~~~
    if not email(my['email']):
        message = g.users['account_error_5']
    
    # ~~~~~
    if not check_result is None:
        message = g.users['account_error_6']
    
    # ~~~~~    
    return message
    
    
def check_username(new_username):
    """
    """
    new_username = str.lower(str(new_username))
    regx = re.compile('^'+new_username+'$', re.IGNORECASE)
    return g.db.user.find_one({"username" : regx })
 
 
@users.route('/admin/users/remove/<_id>/')      
@check_authentication 
@check_admin
def remove(_id):
    """

    """ 
    if g.my_id != _id:
        g.db.users.remove({ '_id' : ObjectId(_id) })
        return 'ok'
    return 'nada'


@users.route('/admin/users/<_id>/', methods=['POST', 'GET'])
@check_authentication
def profile(_id):
    """

    """
    user = g.db.users.find_one({ '_id' : ObjectId(_id) })
    return render_template( MODULE_DIR+'/update.html', **locals() )