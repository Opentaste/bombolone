# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
import re
from flask import request, session, g, Response, render_template, url_for, redirect, abort, Markup
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

from admin import check_authentication
from helpers import create_password
from language import dict_login, setting_message
from upload import upload_file

@check_authentication     
def pages_page():
    """

    """
    pages = g.db.pages.find()
    return render_template('admin/pages.html', **locals())
    
def page_request_form(page):
    """
    """
    len_of_label = len([x for x in request.form if x.startswith('label_it')]) / 2
    
    if g.my['rank'] is 10:
        page['name'] = request.form['name']
        page['file'] = request.form['name_file']
        url_it = request.form['url_it']
        url_en = request.form['url_en']
        page['url'] = { 'it' : url_it, 'en' : url_en }
        page['input_label'] = [ int(request.form['input_label_'+str(i)]) for i in range(len_of_label)]
        
    title_it = request.form['title_it']
    title_en = request.form['title_en']

    description_it = request.form['description_it']
    description_en = request.form['description_en']

    page['title'] = { 'it' : title_it, 'en' : title_en }
    page['description'] = { 'it' : description_it, 'en' : description_en }
    page['content'] = { 'it' : [], 'en' : [] }

    for i in range(len_of_label):
        label = 'label_it_'+str(i)
        if 'label_it_name_0' in request.form:
            label = request.form['label_it_name_'+str(i)]
        alias = request.form['alias_it_name_'+str(i)]
        if page['input_label'][i] is 3:
            name_file = upload_file('it_'+str(i), 'page')
            page['content']['it'].append( { 'label' : label, 'alias' : alias, 'value' : name_file })
        else:
            page['content']['it'].append( { 'label' : label, 'alias' : alias, 'value' : request.form['label_it_'+str(i)] })

    for i in range(len_of_label):
        label = 'label_en_'+str(i)
        if 'label_en_name_0' in request.form:
            label = request.form['label_en_name_'+str(i)]
        alias = request.form['alias_en_name_'+str(i)]
        if page['input_label'][i] is 3:
            name_file = upload_file('en_'+str(i), 'page')
            page['content']['en'].append( { 'label' : label, 'alias' : alias, 'value' : name_file } )
        else:
            page['content']['en'].append( { 'label' : label, 'alias' : alias, 'value' : request.form['label_en_'+str(i)] })
            
    return page

@check_authentication    
def pages_new_page():
    """
    
    """
    if g.my['rank'] is not 10:
        abort(401)
        
    if request.method == 'POST':
        page = {} 
        page = page_request_form(page)
        g.db.pages.insert( page )
        return redirect(url_for('pages'))
        
    return render_template('admin/pages_new.html')
 
@check_authentication 
def pages_content_page(_id):
    """

    """
    page = g.db.pages.find_one({ '_id' : ObjectId(_id) })
    
    if request.method == 'POST':       
        page = page_request_form(page)
        g.db.pages.update( { '_id' : ObjectId(_id) }, page)
            
    return render_template('admin/pages_content.html', **locals())
 
@check_authentication      
def pages_remove_page(_id):
    """

    """
    if g.my['rank'] is not 10:
        abort(401)
    
    g.db.pages.remove({ '_id' : ObjectId(_id) })
    
    return 'ok'

@check_authentication  
def add_label_page(number_label):
    """

    """ 
    i = number_label
    j = str( int(i) + 3)
    
    result = ''
    for lan_label in ['en','it']:
        result += render_template('admin/label.html', **locals()) + '__Bombolone__'
        
    return result