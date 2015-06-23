# -*- coding: utf-8 -*-
"""
admin.py
~~~~~~
The admin module 

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
""" 
from flask import Blueprint, render_template

# Imports inside Bombolone
from bombolone.decorators import get_hash, check_rank

MODULE_DIR = 'admin'
admin = Blueprint('admin', __name__)

@admin.route('/admin/')
@check_rank(80)
@get_hash('admin')
def dashboard():
    """ The dashboard contains a collection of information, 
    such as statistics and other useful stuff. """
    return render_template('{}/dashboard.html'.format(MODULE_DIR))

@admin.route('/admin/hash_table/overview/')
@check_rank(80)
@get_hash('admin')
def hash_table_index():
    """ """
    return render_template('{}/overview_hash_table.html'.format(MODULE_DIR), **locals())
