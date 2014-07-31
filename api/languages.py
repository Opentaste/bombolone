# -*- coding: utf-8 -*-
"""
api.languages.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
from flask import Blueprint, request, g

# Imports inside Bombolone
import core.languages
from core.utils import jsonify, set_message
from decorators import get_hash, authentication, check_rank

api_languages = Blueprint('api_languages', __name__)

@api_languages.route('/api/1.0/languages/list.json')
@authentication
@check_rank(10)
@get_hash('languages')
def overview():
    """ List all the documents, each has a name
    that identifies it, and an hash map. """
    data = core.languages.get_list()
    data = set_message(data)
    return jsonify(data)

@api_languages.route('/api/1.0/languages/get.json')
@authentication
@check_rank(10)
@get_hash('languages')
def get():
    """ """
    _id = request.args.get("_id", None)
    data = core.languages.get(_id)
    data = set_message(data)
    return jsonify(data)

@api_languages.route('/api/1.0/languages/new.json', methods=['POST'])
@authentication
@check_rank(10)
@get_hash('languages')
def new():
    """"""
    data = core.languages.new()
    data = set_message(data)
    return jsonify(data)

@api_languages.route('/api/1.0/languages/update.json', methods=['POST'])
@authentication
@check_rank(10)
@get_hash('languages')
def update():
    """ """
    params = request.json
    data = core.languages.update(params=params, my_rank=g.my['rank'])
    data = set_message(data)
    return jsonify(data)

@api_languages.route('/api/1.0/languages/remove.json', methods=['DELETE'])
@authentication
@check_rank(10)
def remove():
    """ This method removes an hash map"""
    _id = request.args.get("_id", None)
    data = core.languages.remove(_id=_id)
    data = set_message(data)
    return jsonify(data)

@api_languages.route('/api/1.0/languages/change.json')
def change():
    """
    Change language
    """
    lang = request.args.get("lang", None)
    my_id = None
    if hasattr(g, 'my') and g.my:
        my_id = g.my['_id']
    data = core.languages.change(lang=lang, my_id=my_id)
    return jsonify(data)

