# -*- coding: utf-8 -*-
"""
    hash_table.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

from admin import check_authentication, check_admin
    
MODULE_DIR = 'admin/hash_table'

hash_table = Blueprint('hash_table', __name__)


@check_authentication 
@hash_table.route('/admin/hash_table/')
def overview():
    """

    """
    hash_table_list = g.db.hash_table.find()
    return render_template( MODULE_DIR+'/index.html', **locals() )
 

@check_admin  
@hash_table.route('/admin/hash_table/new/', methods=['POST', 'GET'])
def new():
    """
    
    """            
    return render_template( MODULE_DIR+'/new.html' )
 
 
@check_authentication 
@check_admin 
@hash_table.route('/admin/hash_table/remove/<_id>/')      
def remove(_id):
    """

    """ 
    if g.my_id != _id:
        g.db.hash_table.remove({ '_id' : ObjectId(_id) })
        return 'ok'
    return 'nada'


@check_authentication
@hash_table.route('/admin/hash_table/<_id>/', methods=['POST', 'GET'])
def profile(_id):
    """

    """
    user = g.db.hash_table.find_one({ '_id' : ObjectId(_id) })
    return render_template( MODULE_DIR+'/update.html', **locals() )