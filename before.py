# -*- coding: utf-8 -*-
"""
    before.py
    ~~~~~~
    
    Yep!
    by Leonardo Zizzamia and Stefano Biancorosso
    
    :copyright: (c) 2011 by OpenTaste.
    :license:
"""
from flask import g

from shared import db

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
	return b