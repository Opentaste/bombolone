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
from api.oauth2db import oauth_server

CLIENT_ID = 'b5a86b5a296dc0307307'
CLIENT_SECRET = '2cb123b50293fe742e238c81bd2b684f62a6565a'

def get_token(client_id, client_secret, username, password):
    """
    Returns an OAuth2 authorization token or None in case
    of errors. This is the flow for non-web clients."""
    token = None

    if oauth_server.check_client(CLIENT_ID, CLIENT_SECRET):
        if oauth_server.check_user(username, password):
            token, refresh = oauth_server.generate_token(CLIENT_ID, username)
    
    return token

def refresh_token(refresh_token):
    """Returns a new valid token or None, in case of error."""
    
    return None