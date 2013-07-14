# -*- coding: utf-8 -*-
"""
shared.py
~~~~~~

Shared contains the variables that are shared with many modules.

:copyright: (c) 2012 by Leonardo Zizzamia
:license: BSD (See LICENSE for details)
"""
# Imports outside Bombolone
from flask import Flask
from pymongo import Connection

# Imports inside Bombolone
from config import PORT_DATABASE, DATABASE

# Create application and configuration
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # 10 Mb Max Upload

# Create db - The first step when working with PyMongo is to create  
# a Connection to the running mongod instance. 
if PORT_DATABASE:
    connection = Connection(port=PORT_DATABASE)
else:
    connection = Connection()
db = connection[DATABASE]
app.test_request_context().push()