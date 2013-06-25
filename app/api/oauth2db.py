# Bombolone OAuth2 Flask server test
# ==================================
#
# Supports only the flow for non-web clients.

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
        self.CLIENT_ID = 'b5a86b5a296dc0307307'
        self.CLIENT_SECRET = '2cb123b50293fe742e238c81bd2b684f62a6565a'
        self.TOKEN = '473c8b27613670664e4963c8f7869d045aaa378c'
        self.REFRESH_TOKEN = '42aa90f10abe4ef3788d'
    
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
        if user is None:
            return False
        if not 'password' in user:
            return False
        if user['password'] != password:
            return False
        return True

    def generate_token(self, client_id, username):
        """Returns a tuple containing an authorization token and a
        refresh token, both associated to the given client_id and 
        the given username."""

        # MADE A FAKE TOKEN
        # md5 - 128 bits, 32 chars as hexdecimal representation, thats 2 chars per byte.
        new_token_left = md5() 
        # sha1 - 160 bits, 40 chars string
        new_token_right = sha1()
        new_token_left.update(username)
        new_token_right.update(self.TOKEN + 'bombolone')
        # username + bombolone == 32 + 40 chars == 72
        new_token = new_token_left.hexdigest() + new_token_right.hexdigest()

        return (new_token, self.REFRESH_TOKEN)
    
    def check_token(self, token):
        """If the token is valid, returns a tuple containing the
        client_id and the username associated to it. If the token
        is not valid, it returns None."""
        
        my = g.db.users.find_one({ 'token' : token })

        if my:
            #print my["rank"]
            #print my["ot_name"]
            g.my = my
            # get user language
            g.lan = g.my['lan']
            g.language = g.available_languages[g.lan]
            return {'success': True}
        else:
            return {'success': False}

oauth2db = OAuth2DB()