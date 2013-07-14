# -*- coding: utf-8 -*-
"""
users.py
~~~~~~
The user module allows administrators to create, modify and delete users.
The user module supports user rank, which can be set up permissions 
allowing each rank to do only what the administrator permits. 
By default there are two users:
  username |  rank  |
-------------------------------
  Admin    |   10   |
  User     |   20   |

:copyright: (c) 2013 by Leonardo Zizzamia
:license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
import os, re, shutil
from flask import Blueprint, abort, request, g, render_template, url_for, redirect
from bson import ObjectId
from pymongo.errors import InvalidId, PyMongoError

# Imports inside Bombolone
from decorators import check_rank, get_hash
from config import UP_AVATARS_FOLDER, UP_IMAGE_FOLDER

# Imports from Bombolone's Core
from core.users.users import core_users_show, core_users_list
from core.not_allowed import PROHIBITED_NAME_LIST
from core.utils import create_password


MODULE_DIR = 'admin/users'
users = Blueprint('users', __name__)


@users.route('/admin/users/')
@check_rank(10)
@get_hash('users')
def overview():
    """ The overview shows the list of the users registered, 
    can sort the users depending on the field want. """
    ranks_list = { x['rank'] : x['name'] for x in g.db.ranks.find() }
    users_list = list(g.db.users.find().sort("created"))
    num_users = len(users_list)
    return render_template('{}/index.html'.format(MODULE_DIR), **locals())


@users.route('/admin/users/new/', methods=['POST', 'GET'])
@check_rank(10)
@get_hash('users')
@get_hash('upload')
def new():
    """ The administrator can create a new user """       
    language_name = g.languages_object.get_languages(3)
    list_ranks = g.db.ranks.find().sort('rank')

    if request.method == 'POST':
        if user_object.new():
            user = user_object.user
            return redirect(url_for('users.index'))

    if request.method == 'GET':
        data = core_users_show(g.my['_id'])
        
    user = data["user"]
    return render_template('{}/new.html'.format(MODULE_DIR), **locals())
    

@users.route('/admin/users/<_id>/')
@check_rank(10)
@get_hash('users')
@get_hash('upload')
def update(_id):
    """ """
    data = core_users_show(_id)
    user = data["user"]

    if g.my['rank'] < user['rank'] and g.my['rank'] != 10:
        abort(401)

    language_name = g.languages_object.get_languages(3)
    list_ranks = g.db.ranks.find().sort('rank')

    return render_template('{}/update.html'.format(MODULE_DIR), **locals())