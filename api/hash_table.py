# -*- coding: utf-8 -*-
"""
api.hash_table.py
~~~~~~
The Hash Table allows you to store multiple Hash Map,
each of which has an Name Map and an Hash useful to
write the content for use on the web site.

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
from flask import Blueprint, request

# Imports inside Bombolone
import core.hash_table
from core.utils import jsonify
from decorators import get_hash, authentication, check_rank

MODULE_DIR = 'admin/hash_table'
api_hash_table = Blueprint('api_hash_table', __name__)

@api_hash_table.route('/api/1.0/hash_table/list.json')
@authentication
@check_rank(10)
@get_hash('hash_table')
def overview():
    """ List all the documents, each has a name
    that identifies it, and an hash map. """
    data = core.hash_table.get_list()
    return jsonify(data)

@api_hash_table.route('/api/1.0/hash_table/get.json')
@authentication
@check_rank(10)
@get_hash('hash_table')
def get():
    """ """
    _id = request.args.get("_id", None)
    data = core.hash_table.get(_id)
    return jsonify(data)

@api_hash_table.route('/api/1.0/hash_table/new.json', methods=['POST'])
@authentication
@check_rank(10)
@get_hash('hash_table')
def new():
    """ Create a new document within the hash table. """
    params = request.json
    data = core.hash_table.new(params=params)
    return jsonify(data)

@api_hash_table.route('/api/1.0/hash_table/remove.json', methods=['DELETE'])
@authentication
@check_rank(10)
def remove():
    """ This method removes an hash map"""
    _id = request.args.get("_id", None)
    data = core.hash_table.remove(_id=_id)
    return jsonify(data)

@api_hash_table.route('/api/1.0/hash_table/update.json', methods=['POST'])
@authentication
@check_rank(10)
@get_hash('hash_table')
def update():
    """ """
    params = request.json
    data = core.hash_table.update(params=params)
    return jsonify(data)
