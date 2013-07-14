# -*- coding: utf-8 -*-
"""
rank.py
~~~~~~

:copyright: (c) 2013 by Leonardo Zizzamia
:license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
from flask import Blueprint, g, render_template

# Imports inside Bombolone
from decorators import check_rank, get_hash
    
MODULE_DIR = 'admin/rank'
rank = Blueprint('rank', __name__)


@rank.route('/admin/rank/')
@check_rank(10)
@get_hash('rank')
def overview():
    """ Overview """    
    list_ranks = list(g.db.ranks.find().sort('rank'))
    number_user = {}
    
    # TO DO -> MAP REDUCE HERE
    for x in list_ranks:
        count = g.db.users.find({ 'rank' : x['rank'] }).count()
        number_user[x['rank']] = count
    
    return render_template('{}/index.html'.format(MODULE_DIR), **locals())
