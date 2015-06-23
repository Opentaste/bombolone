# -*- coding: utf-8 -*-
"""
rank.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
""" 
from flask import Blueprint, g, render_template

# Imports inside Bombolone
from bombolone.decorators import check_rank, get_hash
    
MODULE_DIR = 'admin/rank'
rank = Blueprint('rank', __name__)

@rank.route('/admin/rank/')
@check_rank(10)
@get_hash('rank')
@get_hash('admin')
def index():
    """ Overview """    
    return render_template('{}/index.html'.format(MODULE_DIR))


@rank.route('/admin/rank/new/')
@rank.route('/admin/rank/update/<rank_id>/')
@check_rank(10)
@get_hash('rank')
@get_hash('admin')
def upsert(rank_id=None):
    """ Upsert """   
    return render_template('{}/upsert.html'.format(MODULE_DIR))
