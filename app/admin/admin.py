# -*- coding: utf-8 -*-
"""
admin.py
~~~~~~
The admin module 

:copyright: (c) 2013 by Leonardo Zizzamia
:license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
from flask import Blueprint, render_template

# Imports inside Bombolone
from decorators import check_rank

MODULE_DIR = 'admin'
admin = Blueprint('admin', __name__)

@admin.route('/admin/')
@check_rank(10)
def dashboard():
    """ The dashboard contains a collection of information, 
    such as statistics and other useful stuff. """
    return render_template('{}/dashboard.html'.format(MODULE_DIR))

@admin.route('/admin/hash_table/overview/')
@check_rank(10)
def hash_table_index():
    """ """
    return render_template('{}/overview_hash_table.html'.format(MODULE_DIR), **locals())

@admin.route('/admin/test/')
@check_rank(10)
def test_index():
    """ """
    return render_template('{}/overview_test.html'.format(MODULE_DIR), **locals())