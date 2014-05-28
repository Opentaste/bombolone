# -*- coding: utf-8 -*-
"""
content.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
""" 
from flask import Blueprint, abort, request, session, g, render_template, redirect

# Imports inside Bombolone
import model.pages
from core.utils import get_content_dict

content = Blueprint('content', __name__)

def get_page_content(code_lan, num_of_path, path):
    """
    By passing the language code and path, 
    is return the page content object
    """
    # Inside any page it saved the path with this format
    url = "url_{}.{}".format(num_of_path, code_lan)

    # Create a list of pages
    list_pages = [ page for page in model.pages.find(url={ "$exists" : True })]
    for page in list_pages:
        count  = 0

        # Any time the "path" is the same or we have some
        # value like "<i_am_variable>" increase the counter
        for i in range(num_of_path):
            word = page["url_"+str(num_of_path)][code_lan][i]
            if path[i] == word:
                count += 1
            #if word[0] == '<' and word[-1] == '>':
            #    count += 1

        # If the counter is the same of num_of_path
        # means we found the page we need it
        if count == num_of_path:
            return page
    return None
	
def render_content_page(num_of_path, path):
    """ 
    Using the path of the url, look inside the collection of pages 
    that matches the page. If it matches, then it is rendered. 

    The main for loop is searching the "page_document" by 
    the languages "code_lan", inside every page we serch the kind of
    url with a specific "num_of_path", like url_1.en or url_2.it 
        { 
            "_id" : ObjectId("123456"), 
            ...
            "url" : { 
                "en" : "about/story", 
                "it" : "chi_siamo/storia" 
            }, 
            "url_2" : { 
                "en" : [  "about",  "story" ], 
                "it" : [  "chi_siamo",  "storia" ] 
            }, 
            ... 
        }
    """
    languages = g.languages_object.available_lang_code

    # Retrive page document by g.lan
    code = g.lang
    page_document = get_page_content(code, num_of_path, path)

    if page_document is None: 
        # Retrive page document by one of the available languages
        for code_lan in languages:
            code = code_lan
            page_document = get_page_content(code, num_of_path, path)
            if page_document is not None:
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
            page_from = "pages."+page_from
            modules = page_from.split(".")
            if len(modules) == 1:
                module = __import__(page_from, globals(), locals(), [], -1)
                method_to_call = getattr(module, page_import)
            else:
                module = __import__(page_from, globals(), locals(), [], -1)
                module_called = getattr(module, modules[1])
                method_to_call = getattr(module_called, page_import)
            return method_to_call(page_document, path, code)
        
        # 2) static page
        # ===============================================================
        title       = page_document['title'][code]
        description = page_document['description'][code]
        content     = {}
        if page_document['content']:
            content = get_content_dict(page_document, code)
            
        # For every page you must specify the file where you want 
        # to use the contents stored in the database.
        return render_template('pages/'+page_document['file']+'.html', **locals())

@content.route('/', methods=['POST', 'GET'])
def home():
    """Path home page level deep"""
    path = ['']
    return render_content_page(1, path)

@content.route('/<regex("((?!static).*)"):one>/', methods=['POST', 'GET'])
def one(one):
    """Path one level deep"""
    path = [one]
    return render_content_page(1, path)

@content.route('/<regex("((?!static).*)"):one>/<two>/', methods=['POST', 'GET'])
def two(one, two):
    """Path two level deep"""
    path = [one, two]
    return render_content_page(2, path)
 
@content.route('/<regex("((?!static).*)"):one>/<two>/<three>/', methods=['POST', 'GET'])
def three(one, two, three):
    """Path three level deep"""
    path = [one, two, three]
    return render_content_page(3, path)
    
@content.route('/<regex("((?!static).*)"):one>/<two>/<three>/<four>/', methods=['POST', 'GET'])
def four(one, two, three, four):
    """Path four level deep"""
    path = [one, two, three, four]
    return render_content_page(4, path)
