# -*- coding: utf-8 -*-
"""
    users.py
    ~~~~~~
    
    :copyright: (c) 2013 by Bombolone
""" 
# Imports outside Bombolone
import re
from datetime import datetime
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect, abort 
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

from decorators import get_hash, jsonp, check_token, check_token_post

# Imports inside Bombolone
from core.users.users import User, core_users_show, core_users_list
from core.utils import ensure_objectid, jsonify

users_api = Blueprint('users_api', __name__)

@users_api.route('/api/users/show.json')
@jsonp
def show():
    """ """

    user_id = request.args.get("user-id", None)
    user = core_users_show(user_id=user_id)

    return jsonify(user)


@users_api.route('/api/users/list.json')
@check_token
@jsonp
def list():
    """ """

    list_id = request.args.get("list-id", None)
    user = core_users_list(user_id=list_id)

    return jsonify(user)


@users_api.route('/api/users/new.json', methods=['POST'])
@check_token_post
@get_hash('users')
def new():
    """ """

    params = request.json
    user_object = User(params=params)
    user_object.new()

    data = {
        "success": user_object.success,
        "message": user_object.message,
        "user": user_object.user
    }

    return jsonify(data)