# -*- coding: utf-8 -*-
"""
    shared.py
    ~~~~~~
    
    Shared contains the variables that are shared with many modules.
    by Leonardo Zizzamia
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
import os
from flask import Flask
from pymongo import Connection

VERSION = '0.0.72'

DEBUG = True
PATH = 'http://0.0.0.0:5000'
PROJECT_DIR = os.path.dirname(__file__)
UP_FOLDER = os.path.join(PROJECT_DIR,'static/image/')
PORT = 5000

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'PNG', 'JPG', 'bmp'])
EXTENSIONS_REQUEST = {'png', 'jpg', 'jpeg', 'gif', 'css', 'js'}

LIST_LANGUAGES = ['ar','cn','de','en','es','fr','gr','it','jp','pt','ru','tr']

"""
Is important generate a good secret key:  http://flask.pocoo.org/docs/quickstart/#sessions
    >>> import os
    >>> os.urandom(24)
    "\xef\xb3\xe3\x07\x1c\xf0V2\x11\x8bx\x8b\xf0\x9b\xac\xe3'v)\xa4^\xbb\x1e\xf6"
"""
SECRET_KEY = '\xc4\nE\xcc\x87\xbe]\xb9kf\xe9\xd3\x9e\xdcF\x9f\x8f\xc9\xaf\x1e-+\x88\xa2'

# Create application and configuration
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # 10 Mb Max Upload

# Create db - The first step when working with PyMongo is to create  
# a Connection to the running mongod instance. 
connection = Connection()
db = connection.bombolone
app.test_request_context().push()

