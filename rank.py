# -*- coding: utf-8 -*-
"""
    rank.py
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
from decorators import check_authentication, check_admin, get_hash_rank
    
MODULE_DIR = 'modules/rank'
rank = Blueprint('rank', __name__)

 
@rank.route('/admin/rank/')
@check_authentication
@check_admin
@get_hash_rank
def overview():
    """  """
    rank_list = g.db.rank.find()
    return render_template( MODULE_DIR+'/index.html', **locals() )
 
  
@rank.route('/admin/rank/new/', methods=['POST', 'GET'])
@check_authentication
@check_admin
@get_hash_rank
def new():
    """ """       
        
    return render_template( MODULE_DIR+'/new.html', **locals())


@rank.route('/admin/rank/remove/<_id>/')      
@check_authentication 
@check_admin
def remove(_id):
    """

    :param _id: 
    """
    if g.my_id != _id:
        g.db.rank.remove({ '_id' : ObjectId(_id) })
        return 'ok'
    return 'nada'


@rank.route('/admin/rank/<_id>/', methods=['POST', 'GET'])
@check_authentication
@check_admin
@get_hash_rank
def update(_id):
    """

    :param _id: 
    """
    
    return render_template( MODULE_DIR+'/update.html', **locals() )
    