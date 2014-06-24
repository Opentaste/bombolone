# -*- coding: utf-8 -*-
"""
pages.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
""" 
from flask import Blueprint, request, session, g, render_template

# Imports inside bombolone
from decorators import check_rank, get_hash

MODULE_DIR = 'admin/pages'
pages = Blueprint('pages', __name__)

@pages.route('/admin/pages/')
@check_rank(10) 
@get_hash('pages')
@get_hash('admin')
def index():
    """ 
    List all the documents, each has a name 
    that identifies it, and an hash map. 
    """
    return render_template('{}/index.html'.format(MODULE_DIR), **locals())


@pages.route('/admin/pages/new/')
@pages.route('/admin/pages/update/<_id>/')
@check_rank(10)
@get_hash('pages')
@get_hash('admin')
def upsert(_id=None):
    """ """
    new = True
    return render_template('{}/upsert.html'.format(MODULE_DIR), **locals())


@pages.route('/admin/pages/view/<_id>/')
@check_rank(10)
@get_hash('pages')
@get_hash('admin')
def view(_id=None):
    """ """
    new = False
    return render_template('{}/upsert.html'.format(MODULE_DIR), **locals())
