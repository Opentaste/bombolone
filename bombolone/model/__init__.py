from pymongo import Connection
from pymongo.errors import PyMongoError

# Imports inside Bombolone
from bombolone import config

# Create db - The first step when working with PyMongo is to create
# a Connection to the running mongod instance.
try:
	if config.PORT_DATABASE:
		connection = Connection(port=config.PORT_DATABASE)
	else:
		connection = Connection()
	db = connection[config.DATABASE]
except PyMongoError, e:
	db = None
	print 'Error Database connection at PORT : {}'.format(config.PORT_DATABASE)