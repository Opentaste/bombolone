# -*- coding: utf-8 -*-
"""
    before.py
    ~~~~~~

    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
from flask import g

from shared import db, PATH

def core_before_request():
	"""
	- To run before each request
	- It's save variable db in the global variable "g"
	"""
	g.db = db
	
def core_inject_user():
	"""Context processors run before the template is rendered and have the ability 
	to inject new values into the template context. A context processor is a function 
	that returns a dictionary."""
	b = {}
	b['path'] = PATH
	b['admin'] = PATH + '/admin'
	b['lan'] = 'en'
	return b