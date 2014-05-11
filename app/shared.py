# -*- coding: utf-8 -*-
"""
shared.py
~~~~~~
Shared contains the variables that are shared with many modules.

:copyright: (c) 2014 by Leonardo Zizzamia
:license: BSD (See LICENSE for details)
"""
from flask import Flask
from pymongo import Connection
from pymongo.errors import PyMongoError

# Imports inside Opentaste
from config import PORT_DATABASE, DATABASE
path_config = 'config.py'

# Create application and configuration
app = Flask(__name__)
app.config.from_pyfile(path_config)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # 10 Mb Max Upload

# Create db - The first step when working with PyMongo is to create
# a Connection to the running mongod instance.
try:
	if PORT_DATABASE:
		connection = Connection(port=PORT_DATABASE)
	else:
		connection = Connection()
	db = connection[DATABASE]
except PyMongoError, e:
	db = None
	print 'Error Database connection at PORT : {}'.format(PORT_DATABASE)

app.test_request_context().push()
