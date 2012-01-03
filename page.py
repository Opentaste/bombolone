# -*- coding: utf-8 -*-
"""
    page.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
from flask import request, session, g, Response, render_template, url_for, redirect, abort, Markup

from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId


def home_page():
	"""
	
	"""
	content = g.db.pages.find_one({ "name" : 'home_page' }) #{ "_id" : 'blablablablalba' }
	return render_template('pages/home.html', content=content)
	
def page_two_base():
	"""

	"""
	content = g.db.pages.find_one({ "name" : 'page_2' })
	return render_template('pages/page_two.html', content=content)
	
def page_three_base():
	"""

	"""
	content = g.db.pages.find_one({ "name" : 'page_3' })
	return render_template('pages/page_three.html', content=content)
	
def page_four_base():
	"""

	"""
	content = g.db.pages.find_one({ "name" : 'page_4' })
	return render_template('pages/page_four.html', content=content)
	
def page_five_base():
	"""

	"""
	content = g.db.pages.find_one({ "name" : 'page_5' })
	return render_template('pages/page_five.html', content=content)