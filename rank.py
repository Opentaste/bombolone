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

  
@rank.route('/admin/rank/', methods=['POST', 'GET'])
@check_authentication 
@check_admin
@get_hash_rank
def overview():
    """ Overview """    
    if request.method == 'POST':
        pass
    
    list_ranks = g.db.ranks.find()
    
    number_user = {
        '10' : g.db.users.find({ 'rank' : 10 }).count(),
        '20' : g.db.users.find({ 'rank' : 20 }).count(),
        '30' : g.db.users.find({ 'rank' : 30 }).count()
    }
    
    return render_template( MODULE_DIR+'/index.html', **locals())
