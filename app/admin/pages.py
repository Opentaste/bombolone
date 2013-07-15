# -*- coding: utf-8 -*-
"""
pages.py
~~~~~~

:copyright: (c) 2013 by Leonardo Zizzamia
:license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
from flask import Blueprint, request, session, g, render_template, url_for, redirect
from bson import ObjectId
from pymongo.errors import InvalidId, PyMongoError

# Imports inside bombolone
from decorators import check_rank, get_hash

MODULE_DIR = 'admin/pages'
pages = Blueprint('pages', __name__)

@pages.route('/admin/pages/')
@check_rank(30) 
@get_hash('pages')
def overview():
    """ 
    List all the documents, each has a name 
    that identifies it, and an hash map. 
    """
    return render_template('{}/index.html'.format(MODULE_DIR), **locals())


@pages.route('/admin/pages/new/')
@pages.route('/admin/pages/update/<_id>/')
@check_rank(30)
@get_hash('pages')
def upsert(_id=None):
    """ """
    new = True
    return render_template('{}/upsert.html'.format(MODULE_DIR), **locals())


@pages.route('/admin/pages/view/<_id>/')
@check_rank(40)
@get_hash('pages')
def view(_id=None):
    """ """
    new = False
    return render_template('{}/upsert.html'.format(MODULE_DIR), **locals())