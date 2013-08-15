# -*- coding: utf-8 -*-
"""
utils.py
~~~~~~~~~~~

Generic helper functions (for helper functions related to 
Flask and Bombolone check helpers.py).

:copyright: (c) 2013 by Bombolone
"""

from collections import Iterable
from types import StringTypes

import string
import random
import smtplib
import unicodedata
import re
from hashlib import md5, sha1
from flask import g, request
from werkzeug import secure_filename

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        raise ImportError
import datetime
from bson.objectid import ObjectId
from werkzeug import Response

def ensure_objectid(stuff):
    """
    If the argument is a string, returns the corresponding ObjectId, otherwise
    returns the argument itself.
    """
    
    if not stuff or stuff == 'None':
        return None
    else:
        try:
            return isinstance(stuff, StringTypes) and ObjectId(stuff) or stuff
        except BaseException, e:
            return None


def is_iterable(stuff):
    """
    Returns True if stuff is iterable, unless stuff is a string; returns False
    otherwise.
    """
    
    return not isinstance(stuff, StringTypes) and isinstance(stuff, Iterable)
 
class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return unicode(obj)
        return json.JSONEncoder.default(self, obj)
 
def jsonify(*args, **kwargs):
    """ jsonify with support for MongoDB ObjectId
    """
    return Response(json.dumps(dict(*args, **kwargs), cls=MongoJsonEncoder), mimetype='application/json')

def create_password(word):
    new_pass_left = md5() 
    new_pass_right = sha1()
    new_pass_left.update(word)
    new_pass_right.update(word + 'magic_string')
    new_pass = new_pass_right.hexdigest() + new_pass_left.hexdigest()
    return new_pass

def secure_url(url):
    return secure_filename(''.join((c for c in unicodedata.normalize('NFD', url) if unicodedata.category(c) != 'Mn'))).lower()

def msg_status(success):
    """ """
    if success is not None:
        return 'msg msg-error' if success is False else 'msg msg-success'
    return ''

def get_content_dict(page, code):
    """
    Generate the content dictionary used inside the template.
    The key id the name label, and the value is get by the language code
    used in that moment on the page.
    """
    content = { x[0]["name"]: x[1]["value"][code] for x in zip(page['labels'], page['content']) }
    return content
