# -*- coding: utf-8 -*-
"""
api.users.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
from flask import Blueprint, request, g

# Imports inside Bombolone
from core import users
from core.utils import jsonify
from decorators import authentication, check_rank, get_hash

api_users = Blueprint('api_users', __name__)

@api_users.route('/api/1.0/users/show.json')
def show():
    """
    By passing a user id, return an object with the user info.
    That object could be different in base of different rank permission.

    :param user-id: user id
    :returns: an object with all the user information

    """
    my_rank = g.my['rank'] if g.my else None
    my_id = g.my['_id'] if g.my else None
    user_id = request.args.get("user_id", None)
    data = users.get(user_id=user_id, my_rank=my_rank, my_id=my_id)
    return jsonify(data)

@api_users.route('/api/1.0/users/list.json')
@authentication
def list():
    """
    Returns a JSON object with the users list
    """
    my_rank = g.my['rank'] if g.my else None
    my_id = g.my['_id'] if g.my else None
    data = users.get_list(my_rank=my_rank, my_id=my_id)
    return jsonify(data)

@api_users.route('/api/1.0/users/new.json', methods=['POST'])
@authentication
@check_rank(10)
@get_hash('users')
def new():
    """ """
    params = request.json
    data = users.new(params=params, lan=g.lang, language=g.language)
    return jsonify(data)

@api_users.route('/api/1.0/users/remove.json', methods=['DELETE'])
@authentication
@check_rank(10)
def remove():
    """
    Removes a user.
    :param _id: MongoDB ObjectId
    """
    user_id = request.args.get("_id", None)
    data = users.remove(user_id=user_id)
    return jsonify(data)
