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

class CrossOriginResourceSharing(object):
    app = None
    allow_credentials = True
    allowed_origins = ""
    max_age = 1728000
    methods = "GET,POST,PUT,DELETE,OPTIONS"
    
    def __init__(self, app):
        self.app = app
        self.app.after_request(self.process_request)
    
    def add_allowed_origin(self, origin):
        self.allowed_origins.append(origin)
    
    def add_allowed_origin_pattern(self, pattern):
        if isinstance(pattern, basestring):
            pattern = re.compile(pattern)
        self.allowed_origins.append(pattern)
    
    def allow_origin(self, response, origin):
        headers = request.headers.get('Access-Control-Request-Headers', "")
        
        response.headers['Access-Control-Allow-Headers'] = headers
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = self.allow_credentials
        response.headers['Access-Control-Allow-Methods'] = self.methods
        response.headers['Access-Control-Max-Age'] =  self.max_age
        
        return response
    
    @classmethod
    def check_origin(self, pattern):
        origin = request.headers.get('Origin', '')
        allowed = False
        if isinstance(pattern, basestring):
            if origin == pattern:
                allowed = True
        
        elif re.match(pattern, origin):
            allowed = True
        
        return allowed, origin
    
    def process_request(self, response):
        origin = request.headers.get('Origin', '')
        self.allow_origin(response, origin)        
        return response
    
    def set_allow_credentials(self, allowed):
        self.allow_credentials = allowed
    
    def set_allowed_methods(self, *args):
        self.methods = ','.join(args)
    
    def set_allowed_origins(self, *args):
        self.allowed_origins = args
    
    def set_max_age(self, max_age):
        self.max_age = max_age
