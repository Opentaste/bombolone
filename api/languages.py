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
from core.utils import jsonify

api_languages = Blueprint('api_languages', __name__)

@api_languages.route('/api/1.0/languages/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
    """ """
    if request.method == "GET":
        data = core.languages.show()
    elif request.method == "POST":
        data = core.languages.new()
    elif request.method == "PUT":
        data = core.languages.update()
    elif request.method == "DELETE":
        data = core.languages.remove()
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
