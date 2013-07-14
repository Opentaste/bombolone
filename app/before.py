# -*- coding: utf-8 -*-
"""
before.py
~~~~~~
It's much important to access before and after any request.

:copyright: (c) 2013 by Leonardo Zizzamia
:license: BSD (See LICENSE for details)
"""
# Imports outside Bombolone
import os
import random
import simplejson as json
from flask import g, request, session, abort
from urlparse import urlparse
from bson import ObjectId

# Imports inside Bombolone
from config import DEBUG, EXTENSIONS_REQUEST, PATH, PATH_API, PROJECT_DIR, LIST_LANGUAGES, JS_FILES, ENV
from shared import db
from login.oac import get_token, CLIENT_SECRET, CLIENT_ID

# Imports from Bombolone's Core
from decorators import get_hash_admin
from core.languages import Languages

def get_headers():
    """ """
    # The X-Forwarded-For (XFF) HTTP header field is a de facto standard for 
    # identifying the originating IP address of a client connecting to a web 
    # server through an HTTP proxy or load balancer.
    # X-Forwarded-For: client1, proxy1, proxy2
    g.ip = None
    if 'X-Forwarded-For' in request.headers:
        g.ip = request.headers['X-Forwarded-For'].split(',')[0]
        
    if 'language' in session:
        g.lan = session['language']
        g.language = g.available_languages[g.lan]
        
    else:
        # The Accept-Language header can include more than one language. 
        # Each additional language is separated by a comma. For example:
        # accept-language: es-mx,es,en
        g.lan = 'en'
        g.language = 'English'
        if 'Accept-Language' in request.headers:
            accept_language = request.headers['Accept-Language'].lower()
            lan = [ item.split(';') for item in accept_language.split(',')]
            if lan[0][0][:2] in g.available_languages:
                g.lan = lan[0][0][:2]
                g.language = g.available_languages[g.lan]

def core_before_request():
    """
    - To run before each request
    - It's save variable db in the global variable "g"
    """
    g.db = db
    g.my = None
    g.languages_object = Languages()
    # Get all the available languages
    # e.g. {u'en': u'English', u'it': u'Italiano'}
    g.available_languages = g.languages_object.get_languages(0)
    get_headers()
    
    # Check that user has login
    if 'user_id' in session:
        # get user_id from session
        user_id = session['user_id']
        # get the user's personal data.
        my = g.db.users.find_one({ '_id' : ObjectId(user_id) })
        
        # If user_id not exist in the user list g.my is None
        if my:
            g.my = my
            # generate token if 
            # - you don't have a token field
            # - you have None as value
            # - you have everything is not 72 characters
            if not "token" in g.my or g.my["token"] is None or len(g.my["token"]) != 72:
                generate_token()
            # get user language
            g.lan = g.my['lan']
            g.language = g.available_languages[g.lan]
            if my['rank'] < 80:
                get_hash_admin()

def generate_token():
    """ """
    token = get_token(CLIENT_ID, CLIENT_SECRET, g.my['username'], g.my['password'])
    g.my['token'] = token
    g.db.users.update({ "_id" : g.my["_id"] }, g.my)

def core_inject_user():
    """Context processors run before the template is rendered and have 
    the ability to inject new values into the template context. 
    A context processor is a function that returns a dictionary."""
    
    inject_object = {
        "sync": request.args.get("sync", None)
    }
    
    # Different url paths useful to the web application
    inject_object['path'] = PATH
    inject_object['api_path'] = PATH_API
    inject_object['admin']  = '{}/admin'.format(PATH)
    inject_object['layout'] = '{}/static/layout'.format(PATH)
    inject_object['images']  = '{}/static/images'.format(PATH)
    
    # Check there is "my" attribute in "g" variable,
    # "my" varible contains all the my user data
    if g.my:
        inject_object['my'] = g.my
        inject_object['username'] = g.my['username'].lower()
        inject_object['rank'] = g.my['rank']
        inject_object['token'] = g.my['token'] if "token" in g.my else ""
    
    # All the available languages
    inject_object['all_languages'] = g.available_languages
    
    # "lan" contains the language codes like : it, es, fr 
    # "language" contains the full name of the language
    inject_object['lan'] = g.lan
    inject_object['language'] = g.language

    # Enviroment
    if ENV == "prod":
        inject_object['api_path'] = "yourdomain"
        inject_object['path'] = "yourdomain"
    elif ENV == "home":
        inject_object['api_path'] = "http://0.0.0.0\\\:5000/api"
        inject_object['path'] = "http://0.0.0.0\\:5000"

    inject_object['js_files'] = JS_FILES

    # Create the name javascript files :
    # - Debug mode, e.g. name_file.js?34321  means  name_file.js?random_number
    # - Production mode, e.g. name_file-13345231.js  means  name_file-timestamp_last_version.js
    app_json = g.db.js.find_one({ "file": "version" })
    if DEBUG:
        rand = random.randint(1, 10000)
        dict_app_json = { x : '{}.js?{}'.format(val, rand) for x , val in app_json['js_file'].iteritems() }
    else:
        dict_app_json = { x : '{}.js'.format(val) for x , val in app_json['js_file_version'].iteritems() }
    inject_object['js_version'] = dict_app_json
    
    return inject_object