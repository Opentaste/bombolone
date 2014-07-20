# -*- coding: utf-8 -*-
"""
before.py
~~~~~~
It's much important to access before and after any request.

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
import random
import json
from flask import session, g, request, current_app

# Imports inside Bombolone
from config import (DEBUG, ENV, JS_FILES_STEP_ONE, JS_FILES_STEP_TWO,
                    NOTACTIVATED, CSS_FONT_AWESOME)
from core.utils import get_hash_map, GetValue
from core.languages import Languages
import model.users
import model.js

def get_headers():
    """
    Different HTTP header fields are check.

    The X-Forwarded-For (XFF) HTTP header field is a de facto standard for
    identifying the originating IP address of a client connecting to a web
    server through an HTTP proxy or load balancer.
    X-Forwarded-For: client1, proxy1, proxy2

    Language inside the session.

    The Accept-Language header can include more than one language.
    Each additional language is separated by a comma. For example:
    accept-language: it,en-us;q=0.7,en;q=0.3 or en-us,en;q=0.8,it;q=0.6
    accept_language: it or en

    """
    g.ip = None
    x_forwarded_for = request.headers.get('X-Forwarded-For', None)
    language = session.get('language', None)
    if x_forwarded_for:
        g.ip = x_forwarded_for.split(',')[0]
    if language:
        g.lang = language
        g.language = g.available_languages[language]
    else:
        g.lang = 'en'
        g.language = 'English'
        accept_language = request.headers.get('Accept-Language', None)
        if accept_language:
            accept_language = accept_language[:2].lower()
            if g.available_languages.get(accept_language, None):
                g.lang = accept_language
                g.language = g.available_languages[accept_language]

def core_before_request():
    """ Run before each request.
    - It's save variable db in the global variable "g"

    """
    g.my = None
    g.languages_object = Languages()
    # Get all the available languages
    # e.g. {u'en': u'English', u'it': u'Italiano'}
    g.available_languages = g.languages_object.available_lang
    get_headers()
    g.all_the_languages = g.languages_object.all_lang_by_tuple
    user_id = session.get('user_id', None)
    # Check that user has login
    if user_id:
        # get the user's personal data.
        my = model.users.find(user_id=user_id, my_id=user_id)
        # If user_id not exist in the user list g.my is None
        if my and my['status'] > NOTACTIVATED:
            g.my = my
            # get user language
            g.lang = g.my.get('lan', 'en')
            g.language = g.available_languages[g.lang]

def core_context_processor():
    """
    Context processors run before the template is rendered and have
    the ability to inject new values into the template context.
    A context processor is a function that returns a dictionary.

    """
    inject_object = {}
    # Check there is "my" attribute in "g" variable,
    # "my" varible contains all the my user data
    if hasattr(g, 'my') and g.my:
        inject_object['my'] = g.my
        inject_object['user_id'] = str(g.my["_id"])
        inject_object['username'] = g.my['username'].lower()
        inject_object['rank'] = g.my['rank']

    # All the available languages
    inject_object['all_languages'] = g.available_languages

    # All the languages
    inject_object['all_the_languages'] = json.dumps(g.all_the_languages)

    # "lan" contains the language codes like : it, es, fr
    # "language" contains the full name of the language
    inject_object['lan'] = g.lang
    inject_object['language'] = g.language

    # Enviroment
    if ENV == "prod":
        inject_object['path'] = request.url_root[:-1]
    elif ENV == "home":
        inject_object['path'] = "http://0.0.0.0\\:5000"

    inject_object['url'] = request.url
    inject_object['url_path'] = request.path
    inject_object['js_files_step_one'] = JS_FILES_STEP_ONE
    inject_object['js_files_step_two'] = JS_FILES_STEP_TWO
    inject_object['css_font_awesome'] = CSS_FONT_AWESOME

    # Create the name javascript files :
    # - Debug mode, e.g. name_file.js?34321  means  name_file.js?random_number
    # - Production mode, e.g. name_file-13345231.js  means  name_file-timestamp_last_version.js
    app_json = model.js.find(file_name='version', only_one=True)
    if DEBUG:
        rand = random.randint(1, 10000)
        dict_app_json = { x : '{}.js?{}'.format(val, rand) for x , val in app_json['js_file'].iteritems() }
    else:
        dict_app_json = { x : '{}.js'.format(val) for x , val in app_json['js_file_version'].iteritems() }
    inject_object['js_version'] = dict_app_json

    return inject_object
