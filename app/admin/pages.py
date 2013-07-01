# -*- coding: utf-8 -*-
"""
pages.py
~~~~~~

:copyright: (c) 2013 by Leonardo Zizzamia
:license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
from flask import Blueprint, request, session, g, render_template, url_for, redirect
from pymongo.objectid import ObjectId
from pymongo.errors import InvalidId, PyMongoError

# Imports inside bombolone
from decorators import check_rank, get_hash

MODULE_DIR = 'admin/pages'
pages = Blueprint('pages', __name__)

@pages.route('/admin/pages/')
@check_rank(30) 
@get_hash('pages')
def overview():
    """ 
    List all the documents, each has a name 
    that identifies it, and an hash map. 
    """
    return render_template('{}/index.html'.format(MODULE_DIR), **locals())


@pages.route('/admin/pages/new/')
@pages.route('/admin/pages/update/<_id>/')
@check_rank(30)
@get_hash('pages')
def upsert(_id=None):
    """ """
    view = False
    return render_template('{}/upsert.html'.format(MODULE_DIR), **locals())


@pages.route('/admin/pages/view/<_id>/')
@check_rank(40)
@get_hash('pages')
def view(_id=None):
    """ """
    view = True
    return render_template('{}/upsert.html'.format(MODULE_DIR), **locals())








def overview_old():
    """ The overview shows the list of the pages registered """
    pages_list = g.db.pages.find().sort('name')
    return render_template('{}/index.html'.format(MODULE_DIR), **locals() )


def new_old():
    """ The administrator can create a new page """       
    pages_object = Pages()
    page = pages_object.page
    
    language_name = languages_object.get_languages(3)
    
    # Creation new page
    if request.method == 'POST':
        if pages_object.new():
            return redirect(url_for('pages.overview'))
    
    # Come back a message when there is an error	
    if not pages_object.message is None:
        message = pages_object.message
        status  = pages_object.status
    
    return render_template('{}/new.html'.format(MODULE_DIR), **locals())

def update_old(_id):
    """ The administrator can update a page """       
    pages_object = Pages(_id)
    page = pages_object.page
    
    language_name = languages_object.get_languages(3)
    
    # Update page
    if request.method == 'POST':
        if pages_object.update():
            return redirect(url_for('pages.overview'))
    
    len_of_label = len(page['label'])
    
    # Come back a message when there is an error	
    if not pages_object.message is None:
        message = pages_object.message
        status  = pages_object.status
    
    return render_template('{}/update.html'.format(MODULE_DIR), **locals())


def remove_old(_id):
    """ """
    g.db.pages.remove({ '_id' : ObjectId(_id) })
    
    return 'ok'


@pages.route('/admin/pages/add_label/<number_label>/')
@check_rank(10) 
@get_hash('pages')
def add_label_old(number_label):
    """ """
    pages_object = Pages() 
    i = number_label
    label = { 
        'label' : '', 
        'alias' : '', 
        'value' : '' 
    }
    page = {
        'label' : 1
    }
    result = ''
    for code in pages_object.languages:
        result += render_template( '{}/label.html'.format(MODULE_DIR), **locals() ) + '__Bombolone__'
    
    return result