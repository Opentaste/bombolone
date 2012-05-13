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
	
def render_content_page(num_of_path, path):
    """ Using the path of the url, look inside the collection of pages 
    that matches the page. If it matches, then it is rendered. """
    languages = languages_object.get_languages(4)
    page_document = None
    
    # Search the page for any language code
    for code_lan in languages:
        # Inside any page it saved the path with this format
        url = "url_{}.{}".format(num_of_path, code_lan)
        # Create a list of pages
        list_pages = [ page for page in g.db.pages.find({ url : { "$exists" : True } }) ]
        for page in list_pages:
            count  = 0
            # Any time the "path" is the same or we have some
            # value like "<i_am_variable>" increase the counter
            for i in range(num_of_path):
                word = page["url_"+str(num_of_path)][code_lan][i]
                if path[i] == word:
                    count += 1
                if word[0] == '<' and word[-1] == '>':
                    count += 1
            # If the counter is the same of num_of_path
            # means we found the page we need it
            if count == num_of_path:
                code = code_lan
                page_document = page
                break
    
    # If page is None then there doesn't exist 
    # the page for that url
    if page_document is None:
        abort(404)
    else:
        
        # 1) dinamic page
        # ===============================================================
        page_from = page_document['from']
        page_import = page_document['import']
        if page_from and page_import:
            name = __import__(page_from, globals(), locals(), [], -1)
            method_to_call = getattr(name, page_import)
            return method_to_call(page_document, path, code)
        
        # 2) static page
        # ===============================================================
        title       = page_document['title'][code]
        description = page_document['description'][code]
        content     = { x['label'] : x['value'] for x in page_document['content'][code]}
        # For every page you must specify the file where you want 
        # to use the contents stored in the database.
        return render_template('pages/'+page_document['file']+'.html', **locals())


@content.route('/<regex("((?!static).*)"):one>/', methods=['POST', 'GET'])
def one(one):
    """ """
    path = [one]
    return render_content_page(1, path)

@content.route('/<regex("((?!static).*)"):one>/<two>/', methods=['POST', 'GET'])
def two(one, two):
    """ """
    path = [one, two]
    return render_content_page(2, path)
 
@content.route('/<regex("((?!static).*)"):one>/<two>/<three>/', methods=['POST', 'GET'])
def three(one, two, three):
    """ """
    path = [one, two, three]
    return render_content_page(3, path)
    
@content.route('/<regex("((?!static).*)"):one>/<two>/<three>/<four>/', methods=['POST', 'GET'])
def four(one, two, three, four):
    """ """
    path = [one, two, three, four]
    return render_content_page(4, path)