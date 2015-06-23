# -*- coding: utf-8 -*-
"""
users.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
""" 
from flask import Blueprint, abort, request, g, render_template, url_for, redirect

# Imports inside Bombolone
from bombolone.config import PATH
import bombolone.core.users
from bombolone.decorators import check_rank, get_hash
import bombolone.model

MODULE_DIR = 'admin/users'
users = Blueprint('users', __name__)

@users.route('/admin/users/')
@check_rank(10)
@get_hash('users')
@get_hash('admin')
def index():
    """ 
    The overview shows the list of the users registered, 
    can sort the users depending on the field want. 
    """
    return render_template('{}/index.html'.format(MODULE_DIR), **locals())


@users.route('/admin/users/new/', methods=['POST', 'GET'])
@check_rank(10)
@get_hash('users')
@get_hash('upload')
@get_hash('admin')
def new():
    """ 
    The administrator can create a new user 
    """       
    language_name = g.languages_object.available_lang_by_tuple
    list_ranks = g.db.ranks.find().sort('rank')
    if request.method == 'POST':
        if user_object.new():
            user = user_object.user
            return redirect(url_for('users.index'))
    if request.method == 'GET':
        data = core.users.get(user_id=g.my['_id'], my_id=g.my['_id'])
    user = data["user"]
    return render_template('{}/new.html'.format(MODULE_DIR), **locals())


@users.route('/admin/users/<user_id>/')
@check_rank(10)
@get_hash('users')
@get_hash('upload')
@get_hash('admin')
def update(user_id):
    """ """
    data = core.users.get(user_id=user_id, my_rank=g.my['rank'])
    if data['success'] is False:
        abort(404)
    user = data["user"]
    language_name = g.languages_object.available_lang_by_tuple
    list_ranks = g.db.ranks.find().sort('rank')
    return render_template('{}/update.html'.format(MODULE_DIR), **locals())
