# -*- coding: utf-8 -*-
"""
hash_table.py
~~~~~~
The Hash Table allows you to store multiple Hash Map, 
each of which has an Name Map and an Hash useful to 
write the content for use on the web site.

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
""" 
from flask import Blueprint, request, g, render_template

# Imports inside Bombolone
from decorators import get_hash, check_rank, get_hash

MODULE_DIR = 'admin/hash_table'
hash_table = Blueprint('hash_table', __name__)

@hash_table.route('/admin/hash-table/')
@check_rank(10) 
@get_hash('hash_table')
@get_hash('admin')
def index():
    """ 
    List all the documents, each has a name 
    that identifies it, and an hash map. 
    """
    return render_template('{}/index.html'.format(MODULE_DIR), **locals())


@hash_table.route('/admin/hash-table/new/')
@hash_table.route('/admin/hash-table/update/<_id>/')
@check_rank(10)
@get_hash('hash_table')
@get_hash('admin')
def upsert(_id=None):
    """ """
    view = False
    return render_template('{}/upsert.html'.format(MODULE_DIR), **locals())


@hash_table.route('/admin/hash-table/view/<_id>/')
@check_rank(10)
@get_hash('hash_table')
@get_hash('admin')
def view(_id=None):
    """ """
    view = True
    return render_template('{}/upsert.html'.format(MODULE_DIR), **locals())
