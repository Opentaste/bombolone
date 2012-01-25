# -*- coding: utf-8 -*-
"""
    hash_table.py
    ~~~~~~
    The Hash Table allows you to store multiple MongoDB documents, 
    each of which has a hash map useful to write the content 
    for use on the web site.
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect
from pymongo.objectid import ObjectId

# Imports inside bombolone
from decorators import check_authentication, check_admin, get_hash_table
from shared import LIST_LANGUAGES
    
MODULE_DIR = 'admin/hash_table'
hash_table = Blueprint('hash_table', __name__)


@hash_table.route('/admin/hash_table/')
@check_authentication 
@get_hash_table
def overview():
    """ List all the documents, each has a name that identifies it, and an hash map. """
    
    hash_table_list = g.db.hash_table.find()
    return render_template( MODULE_DIR+'/index.html', **locals() )
 
   
@hash_table.route('/admin/hash_table/new/', methods=['POST', 'GET'])
@check_authentication
@check_admin
def new():
    """ Create a new document within the hash table. """
    list_lan = LIST_LANGUAGES            
    return render_template( MODULE_DIR+'/new.html', **locals())
 
 
@hash_table.route('/admin/hash_table/remove/<_id>/')  
@check_authentication 
@check_admin    
def remove(_id):
    """

    """ 
    if g.my_id != _id:
        g.db.hash_table.remove({ '_id' : ObjectId(_id) })
        return 'ok'
    return 'nada'


@hash_table.route('/admin/hash_table/<_id>/', methods=['POST', 'GET'])
@check_authentication
def profile(_id):
    """

    """
    user = g.db.hash_table.find_one({ '_id' : ObjectId(_id) })
    return render_template( MODULE_DIR+'/update.html', **locals() )