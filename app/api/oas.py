# -*- coding: utf-8 -*-
"""
oas.py
~~~~~~

Bombolone OAuth2 Flask server
===========================================================
Supports only the flow for non-web clients.
The server flow is:
  1) 
  2) 
  3) 

:copyright: (c) 2013 by Bombolone
""" 
import logging
import json
import random
import string
from flask import Blueprint, g, request
from hashlib import md5, sha1

from decorators import jsonp
from api.oauth2db import oauth2db
from core.utils import jsonify

oas = Blueprint('oas', __name__)

@oas.route('/api/authorizations', methods=['post'])
@jsonp
def authorizations():
    """ """
    client_id = request.form['client_id']
    client_secret = request.form['client_secret']
    auth = request.authorization

    res = { "error": "" }
    if auth and oauth2db.check_client(client_id, client_secret):
        if oauth2db.check_user(auth.username, auth.password):
            token, refresh = oauth2db.generate_token(client_id, auth.username)
            res = { "token": token }
    
    return jsonify(res)