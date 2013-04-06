# -*- coding: utf-8 -*-
"""
oac.py
~~~~~~

Bombolone OAuth2 client test (based on the module requests)
===========================================================
The client flow is:
  1) get a token with the get_token function;
  2) keep using the token until it expires;
  3) if you have a refresh token, refresh it 
     with the refresh_token function, otherwise
     get a new one with get_token.

:copyright: (c) 2013 by Bombolone.
""" 
import json
import requests
from config import PATH_API
from api.oauth2db import oauth2db

CLIENT_ID = '47a69c6a267cd0807408'
CLIENT_SECRET = '2cb223b50493fe842e138d61bd2caa4f62c6565b'

def get_token(client_id, client_secret, username, password):
    """
    Returns an OAuth2 authorization token or None in case
    of errors. This is the flow for non-web clients."""
    try:
        if oauth2db.check_client(client_id, client_secret):
            if oauth2db.check_user(username, password):
                token, refresh = oauth2db.generate_token(client_id, username)
                res = { "token": token }
    except:
        res = { "error": "" }
    
    if 'token' in res:
        return res['token']
    else:
        return None

def refresh_token(refresh_token):
    """Returns a new valid token or None, in case of error."""
    
    return None