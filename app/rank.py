# -*- coding: utf-8 -*-
"""
    rank.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
from flask import Blueprint, g, render_template

# Imports inside Bombolone
from decorators import check_authentication, check_admin, get_hash_rank
    
MODULE_DIR = 'modules/rank'
rank = Blueprint('rank', __name__)


@rank.route('/admin/rank/')
@check_authentication 
@check_admin
@get_hash_rank
def overview():
    """ Overview """    
    list_ranks = list(g.db.ranks.find().sort('rank'))
    number_user = {}
    
    # TO DO -> MAP REDUCE HERE
    for x in list_ranks:
        count = g.db.users.find({ 'rank' : x['rank'] }).count()
        number_user[x['rank']] = count
    
    return render_template('{}/index.html'.format(MODULE_DIR), **locals())
