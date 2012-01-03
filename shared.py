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

VERSION = '0.0.25'

DEBUG = True
PATH = 'http://0.0.0.0:5000'
PORT = 5000

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

