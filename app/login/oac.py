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

CLIENT_ID = 'b5a86b5a296dc0307307'
CLIENT_SECRET = '2cb123b50293fe742e238c81bd2b684f62a6565a'

def get_token(client_id, client_secret, username, password):
    """
    Returns an OAuth2 authorization token or None in case
    of errors. This is the flow for non-web clients."""

    # post parameters, and request path
    params = {'client_id': client_id, 'client_secret': client_secret}
    path = '{}/authorizations'.format(PATH_API)

    # api request to 
    # dev : http://0.0.0.0:5000/api/authorizations
    r = requests.post( path
        , data=params
        , auth=(username, password))

    if r.status_code == 200:
        res = r.json()
        if 'token' in res:
            return res['token']
        else:
            return res
    else:
        return None

def refresh_token(refresh_token):
    """Returns a new valid token or None, in case of error."""
    
    return None