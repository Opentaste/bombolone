# -*- coding: utf-8 -*-
"""
    content.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
from flask import Blueprint, abort, request, session, g, render_template, redirect
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

# Imports inside Bombolone
from config import PATH
from languages import Languages

content = Blueprint('content', __name__)

languages_object = Languages()
	    
def render_content_page(num, path):
    """ """
    languages = languages_object.get_languages(4)
    for code in languages:
        url = "url_%s.%s" % (num, code)
        page = g.db.pages.find_one({ url : path })
        if not page is None:
            break
        
    # If page is None then there doesn't exist 
    # the page for that url
    if page is None:
        abort(404)
    else:
        
        # 1) dinamic page
        # ===============================================================
        page_from = page['from']
        page_import = page['import']
        if page_from and page_import:
            name = __import__(page_from, globals(), locals(), [], -1)
            method_to_call = getattr(name, page_import)
            url = "/".join(path)
            return method_to_call(page, url, code)
        
        # 2) static page
        # ===============================================================
        title       = page['title'][code]
        description = page['description'][code]
        content     = page['content'][code]
        # For every page you must specify the file where you want 
        # to use the contents stored in the database.
        return render_template('pages/'+page['file']+'.html', **locals())
	    
	    
@content.route('/<regex("((?!static).*)"):one>/')
def one(one):
	""" """
	path = [one]
	return render_content_page(1, path)

@content.route('/<regex("((?!static).*)"):one>/<two>/')	
def two(one, two):
    """ """
    path = [one, two]
    return render_content_page(2, path)
 
@content.route('/<regex("((?!static).*)"):one>/<two>/<three>/')	
def three(one, two, three):
    """ """
    path = [one, two, three]
    return render_content_page(3, path)
    
@content.route('/<regex("((?!static).*)"):one>/<two>/<three>/<four>/')	
def four(one, two, three, four):
    """ """
    path = [one, two, three, four]
    return render_content_page(4, path)