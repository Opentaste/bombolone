# -*- coding: utf-8 -*-
"""
    before.py
    ~~~~~~

    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
from flask import g, request, session, abort
from urlparse import urlparse
from pymongo.objectid import ObjectId

from shared import db, PATH, EXTENSIONS_REQUEST

def core_before_request():
	"""
	- To run before each request
	- It's save variable db in the global variable "g"
	- Retrieves the url's extesion and if it isn't part of the list of 
	  files ['css', 'jpg', etc] then it means that we can determine the 
	  personal data to use in page.
	- Personal data are obtained within the function core_bombolone.
	"""
	url = urlparse(request.url)
	extension = url.path.split('.')[-1]
	if not extension.lower() in EXTENSIONS_REQUEST:
	    core_bombolone()
	
def core_inject_user():
	"""Context processors run before the template is rendered and have the ability 
	to inject new values into the template context. A context processor is a function 
	that returns a dictionary."""
	
	url = urlparse(request.url)
	
	b = {}
	b['path'] = PATH
	b['admin'] = PATH + '/admin'
	b['layout'] = PATH + '/static/layout'
	b['image'] = PATH + '/static/image'
	b['page'] = { x['name'] : x['url'] for x in g.db.pages.find()}
	
	return b
	
def core_bombolone():
    """
    """
    g.db = db
    g.my_id = None
    if 'user_id' in session:
		user_id = session['user_id']
		g.my = g.db.users.find_one({ '_id' : ObjectId(user_id) })
		if g.my is None:
			abort(401)
		else:
		    g.my_id = user_id