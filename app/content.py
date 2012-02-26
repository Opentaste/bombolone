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
	    
def render_content_page(num, lista):
    """ """
    languages = languages_object.get_languages(4)
    for code in languages:
        url = "url_%s.%s" % (num, code)
        page = g.db.pages.find_one({ url : lista })
        if not page is None:
            break
        
    # If page is None then there doesn't exist 
    # the page for that url
    if page is None:
        abort(404)
    else:
        # TO DO
        # print page['from']
        # print page['import']
        
        title       = page['title'][code]
        description = page['description'][code]
        content     = page['content'][code]
        # For every page you must specify the file where you want 
        # to use the contents stored in the database.
        return render_template('pages/'+page['file']+'.html', **locals())
	    
@content.route('/<one>/')
def one(one):
	""" """
	lista = [one]
	return render_content_page(1, lista)

#
# BIG ISSUE
# This patter override the /stati/css/.... files
#
#  
#
#@content.route('/<one>/<two>/')	
#def two(one, two):
#    """ """
#    lista = [one, two]
#    return render_content_page(2, lista)
# 
#@content.route('/<one>/<two>/<three>/')	
#def three(one, two, three):
#    """ """
#    lista = [one, two, three]
#    return render_content_page(3, lista)
#    
#@content.route('/<one>/<two>/<three>/<four>/')	
#def four(one, two, three, four):
#    """ """
#    lista = [one, two, three, four]
#    return render_content_page(4, lista)