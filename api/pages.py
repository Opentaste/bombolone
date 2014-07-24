# -*- coding: utf-8 -*-
"""
pages.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
""" 
from flask import Blueprint, request, g

# Imports inside Bombolone
import core.pages
from core.utils import jsonify, set_message
from core.pages import Pages
from decorators import authentication, check_rank, get_hash

api_pages = Blueprint('api_pages', __name__)

@api_pages.route('/api/1.0/pages/list.json')
@authentication
@check_rank(80)
@get_hash('pages')
def overview():
    """ List all the documents, each has a name 
    that identifies it, and an hash map. """
    data = core.pages.get_list(sorted_by='name')
    data = set_message(data)
    return jsonify(data)

@api_pages.route('/api/1.0/pages/get.json')
@authentication
@check_rank(80)
@get_hash('pages')
def get():
    """ """
    page_id = request.args.get("_id", None)
    data = core.pages.get(page_id=page_id)
    data = set_message(data)
    return jsonify(data)

@api_pages.route('/api/1.0/pages/create.json', methods=['POST'])
@authentication
@check_rank(10)
@get_hash('pages')
def new():
    """ Create a new document within the hash table. """
    params = request.json
    data = core.pages.create(params=params, my_rank=g.my['rank'])
    data = set_message(data)
    return jsonify(data)

@api_pages.route('/api/1.0/pages/update.json', methods=['POST'])
@authentication
@check_rank(80)
@get_hash('pages')
def update():
    """ """
    params = request.json
    data = core.pages.update(params=params)
    data = set_message(data)
    return jsonify(data)

@api_pages.route('/api/1.0/pages/remove.json')
@authentication
@check_rank(10)
def remove():
    """ This method removes an hash map.
    :param _id: MongoDB ObjectId """
    page_id = request.args.get("_id", None)
    data = core.pages.remove(page_id=page_id)
    data = set_message(data)
    return jsonify(data) 
