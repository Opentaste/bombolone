# -*- coding: utf-8 -*-
"""
    account.py
    ~~~~~~
    
    :copyright: (c) 2013 by Bombolone
""" 
# Imports outside Bombolone
import re
import os
from datetime import datetime
from flask import jsonify as flask_jsonify
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect, abort
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId
from werkzeug import secure_filename

from config import UP_AVATARS_TMP_FOLDER
from decorators import check_token, check_token_post, check_token_ajax, get_hash, jsonp

from core.upload import Upload
from core.users.users import User
from core.users.account import core_settings
from core.utils import ensure_objectid, jsonify

account_api = Blueprint('account_api', __name__)

@account_api.route('/api/account/settings.json', methods=['POST'])
@check_token_post
@get_hash('users')
def settings():
    """ """

    params = request.json
    user = core_settings(params)

    return jsonify(user)


@account_api.route('/api/account/update.json', methods=['POST'])
@check_token_post
@get_hash('users')
def update():
    """ """

    params = request.json
    user_object = User(params=params, _id=params["_id"])
    user_object.update()

    data = {
        "success": user_object.success,
        "message": user_object.message,
        "user": user_object.user
    }

    return jsonify(data)


@account_api.route('/api/account/update_profile.json', methods=['POST'])
@check_token_post
@get_hash('users')
def update_profile():
    """ """

    params = request.json
    user_object = User(params=params, _id=params["_id"])
    user_object.update_profile()

    data = {
        "success": user_object.success,
        "message": user_object.message,
        "user": user_object.user
    }

    return jsonify(data)


@account_api.route('/api/account/update_account.json', methods=['POST'])
@check_token_post
@get_hash('users')
def update_account():
    """ """

    params = request.json
    user_object = User(params=params, _id=params["_id"])
    user_object.update_account()

    data = {
        "success": user_object.success,
        "message": user_object.message,
        "user": user_object.user
    }

    return jsonify(data)


@account_api.route('/api/account/update_password.json', methods=['POST'])
@check_token_post
@get_hash('users')
def update_password():
    """ """

    params = request.json
    user_object = User(params=params, _id=params["_id"])
    user_object.update_password()

    data = {
        "success": user_object.success,
        "message": user_object.message,
        "user": user_object.user
    }

    return jsonify(data)


@account_api.route('/api/account/upload_avatar.json', methods=['POST'])
@check_token_ajax
@get_hash('users')
def upload_avatar():
    """ """

    name = secure_filename(request.headers.get('X-File-Name'))
    extension = name.rsplit('.', 1)[1].lower()
    
    up = Upload()
    path_image = up.ajax_upload(UP_AVATARS_TMP_FOLDER, extension)
    
    if not up.allowed_file():
        success = False
        message = g.users_msg('error_upload_1')
    else:
        up.thumb((128, 128), os.path.join(UP_AVATARS_TMP_FOLDER, path_image))
        if path_image != 'error':
            success = True
            message = path_image

    data = {
        "success": success,
        "message": message
    }

    return jsonify(data)