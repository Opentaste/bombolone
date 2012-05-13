# -*- coding: utf-8 -*-
"""
    before.py
    ~~~~~~

    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
# Imports outside Bombolone
import os
import simplejson as json
from flask import g, request, session, abort
from urlparse import urlparse
from pymongo.objectid import ObjectId

# Imports inside Bombolone
from config import DEBUG, EXTENSIONS_REQUEST, PATH, PROJECT_DIR, LIST_LANGUAGES
from decorators import get_hash_admin
from languages import Languages
from shared import db

def get_headers():
    """ """
    # The X-Forwarded-For (XFF) HTTP header field is a de facto standard for 
    # identifying the originating IP address of a client connecting to a web 
    # server through an HTTP proxy or load balancer.
    # X-Forwarded-For: client1, proxy1, proxy2
    if 'X-Forwarded-For' in request.headers:
        g.ip = request.headers['X-Forwarded-For'].split(',')[0]
        
    # The Accept-Language header can include more than one language. 
    # Each additional language is separated by a comma. For example:
    # accept-language: es-mx,es,en
    if 'Accept-Language' in request.headers:
        accept_language = request.headers['Accept-Language'].lower()
        lan = [ item.split(';') for item in accept_language.split(',')]
        if lan[0][0][:2] in LIST_LANGUAGES:
            g.lan = lan[0][0][:2]
            g.language = g.languages[g.lan]
    else:
        g.lan = 'en'
        g.language = 'English'

def core_before_request():
    """ To run before each request"""
    my = None
    g.db = db
    languages_object = Languages()
    g.languages = languages_object.get_languages(0)
    
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
            # get user language
            g.lan = g.my['lan']
            g.language = g.languages[g.lan]
    
    get_hash_admin()

def core_inject_user():
    """Context processors run before the template is rendered and have 
    the ability to inject new values into the template context. 
    A context processor is a function that returns a dictionary."""
    
    inject_object = {}
    
    # Different url paths useful to the web application
    inject_object['path']   = PATH
    inject_object['admin']  = '{}/admin'.format(PATH)
    inject_object['layout'] = '{}/static/layout'.format(PATH)
    inject_object['images']  = '{}/static/images'.format(PATH)
    
    # Check there is "lan" attribute in "g" variable,
    # "lan" contains the language codes like : it, es, fr 
    # "language" contains the full name of the language
    if hasattr(g, 'lan'):
        inject_object['lan'] = g.lan
        inject_object['language'] = g.language
        
    # Check there is "my" attribute in "g" variable,
    # "my" varible contains all the my user data
    if hasattr(g, 'my'):
        inject_object['my'] = g.my
        inject_object['rank'] = g.my['rank']
    
    # Working with app.json
    with open(os.path.join(PROJECT_DIR,'app.json'), 'r') as f:
        app_json = json.load(f)
        
        # Create the name javascript files :
        # - Debug mode, e.g. name_file.js?34321  means  name_file.js?random_number
        # - Production mode, e.g. name_file-13345231.js  means  name_file-timestamp_last_version.js
        if DEBUG:
            import random
            rand = random.randint(1, 100000)
            dict_app_json = { x : '%s.js?%s' % (val, rand) for x , val in app_json['js_file'].iteritems() }
            inject_object['js_version'] = dict_app_json
        else:
            dict_app_json = { x : '%s.js' % val for x , val in app_json['js_file_version'].iteritems() }
            inject_object['js_version'] = dict_app_json
    
    return inject_object