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

from shared import PATH


def home_page():
	"""
	
	"""
	page_data = g.db.pages.find_one({ "name" : 'home_page' }) #{ "_id" : 'blablablablalba' }
	content = page_data['content']
	lan = g.lan
	title = page_data['title']
	url = { 'it' : PATH+'/it/', 'en' : PATH+'/en/' }
	return render_template('pages/home.html', **locals())
	
def page_base(lan, title):
    content = g.db.pages.find_one({ "url.it" : title })
    lan = 'it'
    if content is None:
        content = g.db.pages.find_one({ "url.en" : title })
        lan = 'en'
    if content is None:
        abort(404)
    else:
        page_url = { 'it' : PATH+'/it/'+content['url']['it']+'/', 'en' : PATH+'/en/'+content['url']['en']+'/' }
        return render_template('pages/'+content['file']+'.html', content=content, url=page_url, lan=lan)
        

def page_five_base():
	"""

	"""
	content = g.db.pages.find_one({ "name" : 'page_5' })
	return render_template('pages/page_five.html', content=content)