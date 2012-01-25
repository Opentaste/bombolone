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
from decorators import check_authentication, check_admin 
from helpers import create_password
from upload import upload_file

MODULE_DIR = 'admin/pages'

pages = Blueprint('pages', __name__)


@pages.route('/admin/pages/')    
@check_authentication
def overview():
    """

    """
    pages = g.db.pages.find()
    return render_template( MODULE_DIR+'/index.html', **locals() )
    
    
def request_form(page):
    """
    """
    len_label = [ int(x.split('_')[3]) for x in request.form if x.startswith('label_it_name_') ]
    len_of_label = 0
    
    # there are label
    if len(len_label) > 0:
        len_of_label = max(len_label) + 1
    
    form = request.form
    
    if g.my['rank'] is 10:
        page['name'] = form['name']
        page['file'] = form['name_file']
        page['url'] = { 
            'it' : form['url_it'], 
            'en' : form['url_en'] 
        }
        page['input_label'] = [ int(form['input_label_'+str(i)]) for i in range(len_of_label) if 'input_label_'+str(i) in form ]
        type_label = { str(i) : int(form['input_label_'+str(i)]) for i in range(len_of_label) if 'input_label_'+str(i) in form }
        
        print page['input_label']
        print type_label

    page['title'] = { 
        'it' : form['title_it'], 
        'en' : form['title_en'] 
    }
    page['description'] = { 
        'it' : form['description_it'], 
        'en' : form['description_en'] 
    }
    page['content'] = { 
        'it' : [], 
        'en' : [] 
    }

    # get all the languages
    for lan in ['en','it']:
        
        # check until the number of last label
        for i in range(len_of_label):
            
            # if label exist I append in "page"
            if 'label_'+lan+'_name_'+str(i) in form:
                
                label = form['label_'+lan+'_name_'+str(i)]
                alias = form['alias_'+lan+'_name_'+str(i)]
                
                # if label is an image
                if type_label[str(i)] is 3:
                    name_file = upload_file(lan+'_'+str(i), 'page')
                    if name_file is None:
                        name_file = form['label_'+lan+'_'+str(i)+'_hidden']
                    row_label = { 'label' : label, 'alias' : alias, 'value' : name_file }
                    page['content'][lan].append( row_label)
                    
                else:
                    row_label = { 'label' : label, 'alias' : alias, 'value' : form['label_'+lan+'_'+str(i)] }
                    page['content'][lan].append( row_label )
            
    return page


@pages.route('/admin/pages/new/', methods=['POST', 'GET'])
@check_authentication 
@check_admin
def new():
    """
    
    """
    if request.method == 'POST':
        page = {} 
        page = request_form(page)
        g.db.pages.insert( page )
        return redirect(url_for('pages.overview'))
        
    return render_template( MODULE_DIR+'/new.html' )
 

@pages.route('/admin/pages/<_id>/', methods=['POST', 'GET'])
@check_authentication 
def content(_id):
    """

    """
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
    for lan_label in ['en','it']:
        result += render_template( MODULE_DIR+'/label.html', **locals() ) + '__Bombolone__'
        
    return result