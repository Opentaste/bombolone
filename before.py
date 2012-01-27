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
	
	b['lan'] = 'en'
	if hasattr(g, 'lan'):
	    b['lan'] = g.lan
	
	# Get menu value
	path_lan = PATH+'/'+g.lan+'/'
	b['urls'] = { x['name'] : path_lan+x['url'][g.lan] for x in g.db.pages.find() if x['url'] }
	b['titles'] =  { x['name'] : x['title'][g.lan] for x in g.db.pages.find() }
	
	return b
	
def core_bombolone():
    """ Here are obtained the personal data. """
    
    # Assign different attributes to the global variable.
    # - access to the database, 
    # - language used
    # - _id user when it's logged in.
    g.db = db
    g.lan = 'en'
    g.my_id = None
    
    g.languages = { x['code'] : x['value'][x['code']] for x in g.db.languages.find({ 'check' : True })}
    
    if 'user_id' in session:
        
        # get the user_id from session
		user_id = session['user_id']
		
		# get the user's personal data.
		g.my = g.db.users.find_one({ '_id' : ObjectId(user_id) })
		
		# get the hash map for the administration
		admin_map = g.db.hash_table.find_one({ 'name' : 'admin' })
		g.admin = { x : y[g.lan] for x, y in admin_map['value'].iteritems() }
		
		# If user_id not exist in the user list g.my is None
		if g.my is None:
			abort(401)
		else:
		    g.my_id = user_id
		    
		    