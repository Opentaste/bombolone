# -*- coding: utf-8 -*-
"""
oauth2db.py
~~~~~~
OAuth2 Flask server test
Supports only the flow for non-web clients.

:copyright: (c) 2013 by Bombolone
"""
import logging
import json
import random
import string
from flask import Blueprint, g, request
from hashlib import md5, sha1

##################### STUB FOR THE OAUTH2 DATABASE

class OAuth2DB:
    def __init__(self):
        print('Initializing OAuth2 database...')
        self.CLIENT_ID = '47a69c6a267cd0807408'
        self.CLIENT_SECRET = '2cb223b50493fe842e138d61bd2caa4f62c6565b'
        self.TOKEN = 'a73a8c25617870967e2960c2f7869d045aaa3786'
        self.REFRESH_TOKEN = '52ac90f10a6e4ef17882'
    
    def id_generator(self, size=6, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    def generate_client(self):
        """Generates a random pair of client_id and client_secret."""

        return (self.CLIENT_ID, self.CLIENT_SECRET)

    def register_client(self, client_id, client_secret):
        """Registers the given client (id, secret) in the DB."""
        
        pass
    
    def check_client(self, client_id, client_secret):
        """Returns True if the given client_id and client_secret
        are registered in the DB, False otherwise."""
        
        return client_id \
                and client_secret \
                and client_id == self.CLIENT_ID \
                and client_secret == self.CLIENT_SECRET
    
    def check_user(self, username, password):
        """Returns True if the given username and password are
        registered in the DB, False otherwise."""

        user = g.db.users.find_one({"username" : username})
        if user['password'] == password:
            return True
        return False

    def generate_token(self, client_id, username):
        """Returns a tuple containing an authorization token and a
        refresh token, both associated to the given client_id and 
        the given username."""

        # MADE A FAKE TOKEN
        new_token_left = md5() 
        new_token_right = sha1()
        new_token_left.update(username)
        new_token_right.update(self.TOKEN + 'bombolone')
        new_token = new_token_left.hexdigest() + new_token_right.hexdigest()

        return (new_token, self.REFRESH_TOKEN)
    
    def check_token(self, token):
        """If the token is valid, returns a tuple containing the
        client_id and the username associated to it. If the token
        is not valid, it returns None."""

        my = g.db.users.find_one({ 'token' : token })

        if my:
            g.my = my
            # get user language
            g.lan = g.my['lan']
            g.language = g.available_languages[g.lan]
            return {'success': True}
        else:
            return {'success': False}

oauth2db = OAuth2DB()