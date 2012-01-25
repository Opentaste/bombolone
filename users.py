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
from helpers import create_password
    
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
    if request.method == 'POST':
        username = request.form['username']
        rank = int(request.form['rank'])
        password = request.form['password']
        user = { 
            'username' : username, 
            'password' : create_password(password), 
            'rank' : rank 
        }
        g.db.users.insert(user)
        return redirect(url_for('users.overview'))
        
    return render_template( MODULE_DIR+'/new.html' )
 
 
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