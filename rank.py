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
from languages import languages_permits
from hash_table import hash_table_permits
from pages import pages_permits
from users import users_permits
    
MODULE_DIR = 'modules/rank'
rank = Blueprint('rank', __name__)

  
@rank.route('/admin/rank/', methods=['POST', 'GET'])
@check_authentication 
@check_admin
@get_hash_rank
def overview():
    """ Overview """    
    
    list_permits = {
       'hash_table' : hash_table_permits,
        'languages' : languages_permits,
            'pages' : pages_permits,
            'users' : users_permits
    }

    if request.method == 'POST':
        pass
    
    list_ranks = g.db.ranks.find()
    return render_template( MODULE_DIR+'/index.html', **locals())
