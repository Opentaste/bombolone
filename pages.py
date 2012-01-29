# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
import re
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

# Imports inside bombolone
from decorators import check_authentication, check_admin, get_hash_pages
from helpers import language_check
from shared import LIST_LANGUAGES
from upload import upload_file

MODULE_DIR = 'modules/pages'
pages = Blueprint('pages', __name__)


@pages.route('/admin/pages/')    
@check_authentication
@get_hash_pages
def overview():
    """

    """
    pages = g.db.pages.find()
    return render_template( MODULE_DIR+'/index.html', **locals() )


@pages.route('/admin/pages/new/', methods=['POST', 'GET'])
@check_authentication 
@check_admin
@get_hash_pages
def new():
    """
    
    """
    language_name = language_check()
    
    page = { 'content' : {} }
    for code in LIST_LANGUAGES:
        page['content'][code] = []
    
    if request.method == 'POST':
        page = request_form(page)
        
        print page['content']
        
        g.db.pages.insert(page)
        return redirect(url_for('pages.overview'))

    return render_template( MODULE_DIR+'/new.html', **locals() )
 

@pages.route('/admin/pages/<_id>/', methods=['POST', 'GET'])
@check_authentication 
@get_hash_pages
def update(_id):
    """

    """
    language_name = language_check()
    
    page = g.db.pages.find_one({ '_id' : ObjectId(_id) })
    
    if request.method == 'POST': 
        page = request_form(page)
        g.db.pages.update( { '_id' : ObjectId(_id) }, page)
            
    return render_template( MODULE_DIR+'/update.html', **locals() )
 
 
@pages.route('/admin/pages/remove/<_id>/')  
@check_authentication  
@check_admin  
def remove(_id):
    """

    """
    g.db.pages.remove({ '_id' : ObjectId(_id) })
    
    return 'ok'


@pages.route('/admin/pages/add_label/<number_label>/')
@check_authentication 
def add_label(number_label):
    """

    """ 
    i = number_label
    j = str( int(i) + 3)
    
    result = ''
    for code in LIST_LANGUAGES:
        result += render_template( MODULE_DIR+'/label.html', **locals() ) + '__Bombolone__'
        
    return result
    
    
def request_form(page):
    """
    """
    form = request.form
    len_label = [ int(x.split('_')[3]) for x in form if x.startswith('alias_') ]
    len_of_label = 0

    # there are label
    if len(len_label) > 0:
        len_of_label = max(len_label) + 1

    if g.my['rank'] is 10:
        page['name'] = form['name']
        page['file'] = form['name_file']
        page['url'] = {}
        for code in LIST_LANGUAGES:
            if 'url_'+code in form:
                page['url'][code] = form['url_'+code]
            else:
                page['url'][code] = ''

        page['input_label'] = [ int(form['input_label_'+str(i)]) for i in range(len_of_label) if 'input_label_'+str(i) in form ]
        type_label = { str(i) : int(form['input_label_'+str(i)]) for i in range(len_of_label) if 'input_label_'+str(i) in form }
        
    page['title'] = {}
    page['description'] = {}
    for code in LIST_LANGUAGES:
        if 'title_'+code in form:
            page['title'][code] = form['title_'+code]
            page['description'][code] = form['description_'+code]
        else:
            page['title'][code] = ''
            page['description'][code] = ''

    # get all the languages
    for code in LIST_LANGUAGES:

        # check until the number of last label
        for i in range(len_of_label):

            # if label exist I append in "page"
            if 'label_'+code+'_name_'+str(i) in form:

                label = form['label_'+code+'_name_'+str(i)]
                alias = form['alias_'+code+'_name_'+str(i)]

                # if label is an image
                if type_label[str(i)] is 3:
                    name_file = upload_file(code+'_'+str(i), 'page')
                    if name_file is None:
                        name_file = form['label_'+code+'_'+str(i)+'_hidden']
                    row_label = { 'label' : label, 'alias' : alias, 'value' : name_file }
                    page['content'][code].append( row_label)

                else:
                    row_label = { 'label' : label, 'alias' : alias, 'value' : form['label_'+code+'_'+str(i)] }
                    page['content'][code].append( row_label )

    return page