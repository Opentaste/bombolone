# -*- coding: utf-8 -*-
"""
pages.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
""" 
from flask import Blueprint, request, g, render_template, url_for, redirect

# Imports inside Bombolone
from core.utils import jsonify, ensure_objectid
from core.languages import Languages
from core.validators import CheckValue
from core.pages import Pages
from decorators import authentication, check_rank, get_hash

api_pages = Blueprint('api_pages', __name__)

languages_object = Languages()
check = CheckValue()

@api_pages.route('/api/1.0/pages/list.json')
@authentication
@check_rank(10)
@get_hash('pages')
def overview():
    """ List all the documents, each has a name 
    that identifies it, and an hash map. """
    page_list = list(g.db.pages.find().sort('name'))
    data = {
        "success": True,
        "page_list": page_list
    }
    return jsonify(data)

@api_pages.route('/api/1.0/pages/get.json')
@authentication
@check_rank(10)
@get_hash('pages')
def get():
    """ """
    _id = request.args.get("_id", None)
    page = g.db.pages.find_one({ "_id": ensure_objectid(_id) })
    data = {
        "success": True,
        "page": page
    }
    return jsonify(data)

@api_pages.route('/api/1.0/pages/create.json', methods=['POST'])
@authentication
@check_rank(10)
@get_hash('pages')
def new():
    """ Create a new document within the hash table. """
    language_name = languages_object.get_languages(5)
    params = request.json

    page_object = Pages(params=params)
    page_object.new()

    data = {
        "success": page_object.success,
        "message": page_object.message,
        "page": page_object.page
    }
    return jsonify(data)

@api_pages.route('/api/1.0/pages/update.json', methods=['POST'])
@authentication
@check_rank(10)
@get_hash('pages')
def update():
    """ """
    language_name = languages_object.get_languages(5)
    params = request.json

    success = False
    message = ""
    page = {}

    if "_id" in params:
        page_object = Pages(params=params, _id=params["_id"])
        page_object.update()

        success = page_object.success
        message = page_object.message
        page = page_object.page

    data = {
        "success": success,
        "message": message,
        "page": page
    }
    return jsonify(data)

@api_pages.route('/api/1.0/pages/remove.json')
@authentication
@check_rank(10)
def remove():
    """ This method removes an hash map.
    :param _id: MongoDB ObjectId """
    _id = request.args.get("_id", None)
    page_object = Pages(_id=_id)

    success = False
    if _id:
        success = page_object.remove()

    data = {
        "success": success
    }
    return jsonify(data) 
