# -*- coding: utf-8 -*-
"""
    shared.py
    ~~~~~~
    
    Shared contains the variables that are shared with many modules.
    by Leonardo Zizzamia
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""

from flask import Flask
from pymongo import Connection

VERSION = '0.0.4'

DEBUG = True
PATH = 'http://0.0.0.0:5000'
UP_FOLDER = '/Users/leo/Desktop/git/bombolone/static/image/'
PORT = 5000

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'PNG', 'JPG', 'bmp'])
EXTENSIONS_REQUEST = {'png', 'jpg', 'jpeg', 'gif', 'css', 'js'}

SECRET_KEY = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'

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

