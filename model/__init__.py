from pymongo import Connection
from pymongo.errors import PyMongoError

# Imports inside Bombolone
from config import PORT_DATABASE, DATABASE

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