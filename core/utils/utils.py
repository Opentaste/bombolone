# -*- coding: utf-8 -*-
"""
utils.py
~~~~~~~~~~~

Generic helper functions

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
import os
import datetime
import time
import json
import string
import re
import binascii
import unicodedata
from collections import Iterable
from types import StringTypes
from hashlib import md5, sha1
from unicodedata import normalize
from flask import g, request
from werkzeug import secure_filename, Response
from bson.objectid import ObjectId

def linkify(string):
    """
    Make a string url-friendly.
    First try to normalize the string, substituting some unicode
    characters with similar ones in the ASCII table. Then, remove special
    characters and replace whitespaces with hyphens.

    :param string: string to linkify
    :return: a new string with the linkification applied

    """
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
    string = unicode(re.sub('[^\w\s-]', '', string).strip().lower())
    return re.sub('[-\s]+', '-', string)

def ensure_objectid(item_id):
    """
    If the argument is a string, returns the corresponding ObjectId, otherwise
    returns the argument itself.

    """
    try:
        return isinstance(item_id, StringTypes) and ObjectId(item_id) or item_id
    except BaseException, e:
        return None

def is_iterable(stuff):
    """
    Returns True if stuff is iterable, unless stuff is a string; returns False
    otherwise.

    """
    return not isinstance(stuff, StringTypes) and isinstance(stuff, Iterable)

def get_extension(file_name):
    """
    Returns the file extension without 'dot'

    """
    return file_name.rsplit('.', 1)[1].lower()

class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return unicode(obj)
        return json.JSONEncoder.default(self, obj)

def get_json(*args, **kwargs):
    """
    jsonify with support for MongoDB ObjectId
    """
    return json.dumps(dict(*args, **kwargs), cls=MongoJsonEncoder)

def jsonify(*args, **kwargs):
    """
    jsonify with support for MongoDB ObjectId
    """
    return Response(json.dumps(dict(*args, **kwargs), cls=MongoJsonEncoder), mimetype='application/json')

def create_password(word):
    """ """
    new_pass_left = md5()
    new_pass_right = sha1()
    new_pass_left.update(word)
    new_pass_right.update('my' + word + 'app')
    new_pass = new_pass_right.hexdigest() + new_pass_left.hexdigest()
    return new_pass

def get_content_dict(page, code):
    """
    Generate the content dictionary used inside the template.
    The key id the name label, and the value is get by the language code
    used in that moment on the page.
    """
    content = { x[0]["name"]: x[1]["value"][code] for x in zip(page['labels'], page['content']) }
    return content

