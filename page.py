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

from helpers import init_mongodb
from shared import PATH


def home_page():
	""" Manages the contents of the home page """
	# It's important to leave the commentary below, 
	# the first launch of the web application
	#init_mongodb()
	
	page_data = g.db.pages.find_one({ "name" : 'home_page' }) #{ "_id" : 'blablablablalba' }
	if not page_data:
	    return redirect(url_for('login'))
	lan = g.lan
	title = page_data['title'][lan]
	description = page_data['description'][lan]
	content = page_data['content'][lan]
	url = { 'it' : PATH+'/it/', 'en' : PATH+'/en/' }
	
	return render_template('pages/home.html', **locals())
	
def page_base(lan, title):
    """ Manages the deployment of the contents 
    of the pages of Bombolone.
    """
    
    # Save a part of the query into a variable.
    query_pages = g.db.pages
    
    # If the page is Italian I verify that the 
    # title is listed in the Italian pages
    if lan == 'it':
        page_data = query_pages.find_one({ "url.it" : title })
    
    # If the page is English I verify that the 
    # title is listed in the English pages
    if lan == 'en':
        page_data = query_pages.find_one({ "url.en" : title })
        
    # If page_data is None then there doesn't exist 
    # the page for that title
    if page_data is None:
        abort(404)
    else:
        # To simplify access to different content, 
        # I have divided the content into different variables.
        title = page_data['title'][lan]
        description = page_data['description'][lan]
        content = page_data['content'][lan]
        url = { 'it' : PATH+'/it/'+page_data['url']['it']+'/', 'en' : PATH+'/en/'+page_data['url']['en']+'/' }
        
        # For every page you must specify the file where you want 
        # to use the contents stored in the database.
        return render_template('pages/'+page_data['file']+'.html', **locals())
