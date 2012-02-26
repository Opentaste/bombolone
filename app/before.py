# -*- coding: utf-8 -*-
"""
    before.py
    ~~~~~~

    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
# Imports outside Bombolone
import os
import simplejson as json
from flask import g, request, session, abort
from urlparse import urlparse
from pymongo.objectid import ObjectId

# Imports inside Bombolone
from config import DEBUG, EXTENSIONS_REQUEST, PATH, PROJECT_DIR
from languages import Languages
from shared import db

def core_before_request():
	""" To run before each request
	Retrieves the url's extesion and if it isn't part of the list of 
	files ['css', 'jpg', etc] then it means that we can determine the 
	personal data to use in page. """
	url = urlparse(request.url)
	extension = url.path.split('.')[-1]
	if not extension.lower() in EXTENSIONS_REQUEST:
	    # Personal data are obtained within this function
	    core_before()
	
def core_inject_user():
	"""Context processors run before the template is rendered and have 
	the ability to inject new values into the template context. 
	A context processor is a function that returns a dictionary."""
		
	inject_object = {}
	
	# Different url paths useful to the web application
	inject_object['path']   = PATH
	inject_object['admin']  = '%s/admin' % PATH
	inject_object['layout'] = '%s/static/layout' % PATH
	inject_object['image']  = '%s/static/image' % PATH
	
	# Check there is "lan" attribute in "g" variable,
	# "lan" contains the language codes like : it, es, fr 
	# "language" contains the full name of the language
	if hasattr(g, 'lan'):
	    inject_object['lan'] = g.lan
	    inject_object['language'] = g.language
	
	# Check there is "my" attribute in "g" variable,
	# "my" varible contains all the my user data
	if hasattr(g, 'my'):
	    inject_object['my'] = g.my
	    
	# read app.json
	f = open(os.path.join(PROJECT_DIR,'app.json'), 'r')
	app_json = json.load(f)
	if DEBUG:
	    inject_object['js_version'] = app_json['js_file']
	else:
	    inject_object['js_version'] = app_json['js_file_version']
	f.close()
		
	return inject_object
	
def core_before():
    """ Here are obtained the personal data. 
    It's save variable db in the global variable "g" """
    g.db = db
    
    languages_object = Languages()
    g.languages = languages_object.get_languages(0)
    
    # Check that user has login
    if 'user_id' in session:
        # get user_id from session
        user_id = session['user_id']
        # get the user's personal data.
        g.my = g.db.users.find_one({ '_id' : ObjectId(user_id) })
        
        # If user_id not exist in the user list g.my is None
        if g.my is None:
            abort(401)
        else:
            # get user language
            g.lan = g.my['lan']
            g.language = g.languages[g.lan]
            # get the hash map for the administration
            if g.my['rank'] < 25:
                admin_map = g.db.hash_table.find_one({ 'name' : 'admin' })
                g.admin = { x : y[g.lan] for x, y in admin_map['value'].iteritems() }
    else:
        g.lan = 'en'
        g.language = 'English'
		    
		    