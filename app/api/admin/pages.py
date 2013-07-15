# -*- coding: utf-8 -*-
"""
pages.py
~~~~~~

:copyright: (c) 2013 by Bombolone
""" 
# Imports outside Bombolone
from flask import Blueprint, request, g, render_template, url_for, redirect
from bson import ObjectId
from pymongo.errors import InvalidId, PyMongoError

# Imports from Bombolone's Core
from core.utils import jsonify, ensure_objectid
from core.languages import Languages
from core.validators import CheckValue
from core.admin.pages import Pages

# Imports inside Bombolone
from config import LIST_LANGUAGES
from decorators import check_token, check_token_post, check_rank, get_hash, jsonp

pages_api = Blueprint('pages_api', __name__)

languages_object = Languages()
check = CheckValue()

@pages_api.route('/api/pages/list.json')
@check_token
@check_rank(20)
@get_hash('pages')
@jsonp
def overview():
    """ List all the documents, each has a name 
    that identifies it, and an hash map. """
    page_list = list(g.db.pages.find().sort('name'))
    data = {
        "success": True,
        "page_list": page_list
    }
    return jsonify(data)

@pages_api.route('/api/pages/get.json')
@check_token
@check_rank(20)
@get_hash('pages')
@jsonp
def get():
    """ """
    _id = request.args.get("_id", None)
    page = g.db.pages.find({ "_id": ensure_objectid(_id) })
    data = {
        "success": True,
        "page": page
    }
    return jsonify(data)

@pages_api.route('/api/pages/new.json', methods=['POST'])
@check_token_post
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

@pages_api.route('/api/pages/remove.json')
@check_token
@check_rank(10)  
@jsonp
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

@pages_api.route('/api/pages/update.json', methods=['POST'])
@check_token_post
@check_rank(20)
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
        page = page_object.hash_map

    data = {
        "success": success,
        "message": message,
        "page": page
    }
    return jsonify(data)
  