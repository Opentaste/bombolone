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
from languages import language_check
from shared import LIST_LANGUAGES
from validators import length, username
    
MODULE_DIR = 'admin/hash_table'
hash_table = Blueprint('hash_table', __name__)


@hash_table.route('/admin/hash_table/')
@check_authentication 
@get_hash_table
def overview():
    """ List all the documents, each has a name that identifies it, and an hash map. """
    
    hash_table_list = g.db.hash_table.find()
    return render_template( MODULE_DIR+'/index.html', **locals() )
    
    
def request_form(hash_map):
    """
    """
    form = request.form
    
    message = None
    name = form['name']
    hash_map['name'] = name
    hash_map['value'] = {}
    
    if not length(name, 2, 20):
        message = 'nada 1'
    elif not username(name):
        message = 'nada 2'
    
    list_label = [ int(x.split('_')[3]) for x in form if x.startswith('label_name_') ]
    
    if len(list_label) > 0:    
        len_label = max(list_label) + 1
        for i in range(len_label):
            
            i = str(i)
            if 'label_name_'+g.lan+'_'+i in form:
                key = form['label_name_'+g.lan+'_'+i].strip()
                
                if not length(key, 2, 20):
                    message = 'nada 3'
                elif not username(key):
                    message = 'nada 4'
    
                hash_map['value'][key] = {}

                for code in LIST_LANGUAGES:
                    if 'label_name_'+code+'_'+i in form:
                        value = form['label_'+code+'_'+i]
                        hash_map['value'][key][code] = value

                    else:
                        hash_map['value'][key][code] = ''

    if message is None:
        return (message, hash_map)
    return (message, hash_map) 
    
   
@hash_table.route('/admin/hash_table/new/', methods=['POST', 'GET'])
@check_authentication
@check_admin
def new():
    """ Create a new document within the hash table. """
    language_name = language_check()
    
    hash_map = { 'name' : '', 'value' : {} }
    
    if request.method == 'POST': 
        hash_map = request_form(hash_map)
        if hash_map[0] is None:
            g.db.hash_table.insert( hash_map[1] )
            return redirect(url_for('hash_table.overview'))
        
        status = 'mes_red'
        message = hash_map[0]
        hash_map = hash_map[1]
       
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
def update(_id):
    """

    """
    language_name = language_check()
    
    hash_map = g.db.hash_table.find_one({ '_id' : ObjectId(_id) })
    
    if request.method == 'POST': 
        hash_map = request_form(hash_map)
        if hash_map[0] is None:
            g.db.hash_table.update({ '_id' : ObjectId(_id)}, hash_map[1] )
            status = 'mes_green'
            message = 'tutto ok'
        else:
            status = 'mes_red'
            message = hash_map[0]
            
        hash_map = hash_map[1]
    
    return render_template( MODULE_DIR+'/update.html', **locals() )