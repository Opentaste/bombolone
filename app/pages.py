# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
import re
from flask import Blueprint, request, session, g, render_template, url_for, redirect
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId
from pymongo.errors import InvalidId, PyMongoError

# Imports inside bombolone
from decorators import check_authentication, check_admin, get_hash_pages
from languages import Languages
from validators import CheckValue

MODULE_DIR = 'modules/pages'
pages = Blueprint('pages', __name__)

check            = CheckValue()   # Check Value class
languages_object = Languages()
    
class Pages(object):
    """ This class allows to :
    - get_page
    - reset
    - new
    - remove
    """

    def __init__(self, _id=None):
        """ """
        self.page         = {}
        self.languages    = languages_object.get_languages(4)
        self.message      = None            # Error or succcess message
        self.status       = 'msg msg-error'
        self.type_label   = {}
        self.len_of_label = 0
        if _id is None:
            self.reset()
        else:
            self.get_page(_id)
        
    def get_page(self, _id):
        """ Get the user document from Database """
        try:
            _id = ObjectId(_id)
            self.page = g.db.pages.find_one({ '_id' : _id })
        except InvalidId:
            self.page = {}
            
    def reset(self):
        """ Reset user value in Pages.page"""
        self.message      = None
        self.status       = 'msg msg-error'
        self.type_label   = {}
        self.len_of_label = 0
        self.page = { 
        	"name": "",
        	"from": "",
        	"import": "",
        	"url": {},
        	"title": {},
        	"description": {},
        	"content": {},
        	"file": "",
            "label": []
        }
        for code in self.languages:
            self.page['url'][code] = ''
            self.page['title'][code] = ''
            self.page['description'][code] = ''
            self.page['content'][code] = []
        
    def new(self):
        """ Insert new page in the database """
        if g.my['rank'] < 15:
            self.__request_first_block()
            
        self.__request_second_block()
        self.__request_label_and_alias()
        self.__request_values()
        
        if self.message is None:
            try:
                g.db.pages.insert(self.page)
                return True
            except PyMongoError:
                self.message = g.pages_msg('error_mongo_new')
                
        return False
        
    def update(self):
        """ Update page in the database """
        if g.my['rank'] < 15:
            self.__request_first_block()
            
        self.__request_second_block()
        self.__request_label_and_alias()
        self.__request_values()
        
        if self.message is None:
            try:
                g.db.pages.update({ '_id' : ObjectId(self.page['_id']) }, self.page)
                self.status = 'msg msg-success'
                self.message = g.pages_msg('success_update_page')
            except PyMongoError:
                self.message = g.pages_msg('error_mongo_update')
                
        return False
        
    def remove(self, _id):
        """ Remove page from the database """
        self.get_page(_id)
        
        # It checks page _id exist and that
        # you have permission to remove that page
        if len(self.user) and g.my['rank'] < 15:
            try:
                g.db.pages.remove({ '_id' : ObjectId(_id) })
                return 'ok'
            except PyMongoError:
                return 'nada'
        return 'nada'
        
    def __request_first_block(self):
        """ """
        form                = request.form
        old_name            = self.page['name']
        self.page['name']   = form['name']
        self.page['from']   = form['from']
        self.page['import'] = form['import']
        self.page['file']   = form['file']
                
        # Check that the name field is not empty
        if not len(form['name']):
            self.message = g.pages_msg('error_1')

        # If the name is changed
        elif old_name != self.page['name']:
            try:
                new_name = str.lower(str(self.page['name']))
                regx = re.compile('^'+new_name+'$', re.IGNORECASE)
                available_name = g.db.pages.find_one({"name" : regx })
            except:
                available_name = 'Error invalid expression'

            # Check that the name has between 2 and 20 characters
            if not check.length(self.page['name'], 2, 20):
                self.message = g.pages_msg('error_2')

            # Verify that the format of the name is correct
            elif not check.username(self.page['name']):
                self.message = g.pages_msg('error_3')

            # Raises an error message if username is not available.
            elif not available_name is None:
                self.message = g.pages_msg('error_4')
                
        # ~
        if len(self.page['from']) and self.message is None:
            # Check that the "from" value has between 2 and 20 characters
            if not check.length(self.page['from'], 2, 20):
                self.message = g.pages_msg('error_5')

            # Verify that the format of the "from" value is correct
            elif not check.username(self.page['from']):
                self.message = g.pages_msg('error_6')
                             
            # Check that the "import" value has between 2 and 20 characters
            elif not check.length(self.page['import'], 2, 20):
                self.message = g.pages_msg('error_7')

            # Verify that the format of the "import" value is correct
            elif not check.username(self.page['import']):
                self.message = g.pages_msg('error_8')
                
        # Check that the file name field is not empty
        elif not len(self.page['file']) and self.message is None:
            self.message = g.pages_msg('error_9')
    
    def __request_second_block(self):
        """ """            
        form                     = request.form
        old_url                  = self.page['url']
        self.page['url']         = {}
        self.page['title']       = {}
        self.page['description'] = {}
        
        for i in range(10):
            key = 'url_%s' % i
            if key in self.page:
                del(self.page[key])
        
        if not self.message is None:
            return False
            
        # Get URL, Title and Description in any languages
        for code in self.languages:
            self.page['url'][code]         = form['url_'+code]
            self.page['title'][code]       = form['title_'+code]
            self.page['description'][code] = form['description_'+code]
            
            error_in = ' ( ' + code + ' )'
            
            # Check that the url field is not empty
            if not len(self.page['url'][code]):
                self.message = g.pages_msg('error_b_1') + error_in
    
            # If the url is changed
            elif old_url[code] != self.page['url'][code]:
                lista_url = self.page['url'][code].split('/')
                # Convert list with strings all to lowercase
                map(lambda x:x.lower(),lista_url) 
                if self.page['url'][code][-1] == '/':
                    lista_url.pop()
                num_urls = len(lista_url)
                
                try:
                    for code_two in self.languages:
                        field = "url_%s.%s" % (num_urls, code_two)
                        available_url = g.db.pages.find_one({ field : lista_url })
                except:
                    available_url = 'Error invalid expression'
        
                # Check that the url is a maximum of 200 characters
                if not check.length(self.page['url'][code], 0, 200):
                    self.message = g.pages_msg('error_b_2') + error_in

                # Verify that the format of the url is correct
                elif not check.url_two(self.page['url'][code]):
                    self.message = g.pages_msg('error_b_3') + error_in

                # Raises an error message if url is not available.
                elif not available_url is None:
                    self.message = g.pages_msg('error_b_4') + error_in
            else:
                lista_url = old_url[code].split('/')
                if old_url[code][-1] == '/':
                    lista_url.pop()
                num_urls = len(lista_url)
                
                    
            kind_of_url = 'url_%s' % num_urls
            if not kind_of_url in self.page:
                self.page[kind_of_url] = {}
            self.page[kind_of_url][code] = lista_url
            
    def __request_label_and_alias(self):
        """ """
        form      = request.form
        len_label = [ int(x.split('_')[3]) for x in form if x.startswith('label_name') ]
                
        # there are label
        if len(len_label) > 0:
            self.len_of_label = max(len_label) + 1
            
            if g.my['rank'] < 15:
                self.type_label = { int(x.split('_')[1]) : int(form[x]) for x in form if x.startswith('type_')}
                self.page['label'] = [ type_label for type_label in self.type_label ]
            else:
                pass
           
    def __request_values(self):
        """ """
        form = request.form
        # get all the languages
        for code in self.languages:            
            self.page['content'][code] = []
            
            # check until the number of last label
            for i in range(self.len_of_label):
                label = 'label_name_%s_%s' % (code, i)
                alias = 'alias_name_%s_%s' % (code, i)

                # if label exist I append in "page"
                if label in form and i in self.type_label:
                    
                    row_label = { 
                        'label' : form[label], 
                        'alias' : form[alias], 
                        'value' : '' 
                    }
                    
                    error_in = ' ( ' + form[label] + ' )'
                    
                    # Verify that the format of the "name label" is correct
                    if not check.username(row_label['label']) and len(row_label['label']):
                        self.message = g.pages_msg('error_c_1') + error_in
                    
                    # if label is an image
                    if self.type_label[i] is 3:
                        name_file = upload_file(code+'_'+str(i), 'page')
                        if name_file is None:
                            name_file = form['label_'+code+'_'+str(i)+'_hidden']
                        row_label['value'] = name_file
                    else:
                        row_label['value'] = form['label_'+code+'_'+str(i)] 
                        
                    self.page['content'][code].append( row_label )  

@pages.route('/admin/pages/')    
@check_authentication
@get_hash_pages
def overview():
    """ The overview shows the list of the pages registered """
    pages_list = g.db.pages.find()
    return render_template('%s/index.html' % MODULE_DIR, **locals() )


@pages.route('/admin/pages/new/', methods=['POST', 'GET'])
@check_authentication 
@check_admin
@get_hash_pages
def new():
    """ The administrator can create a new page """       
    # Initial default page
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

    return render_template('%s/new.html' % MODULE_DIR, **locals())
    

@pages.route('/admin/pages/<_id>/', methods=['POST', 'GET'])
@check_authentication 
@get_hash_pages
def update(_id):
    """ The administrator can update a page """       
    # Initial default page
    pages_object = Pages(_id)
    page = pages_object.page
    
    language_name = languages_object.get_languages(3)
    
    # Update page
    if request.method == 'POST':
        if pages_object.update():
            return redirect(url_for('pages.overview'))
    
    # Come back a message when there is an error	
    if not pages_object.message is None:
        message = pages_object.message
        status  = pages_object.status

    return render_template('%s/update.html' % MODULE_DIR, **locals())
 
 
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
        result += render_template( MODULE_DIR+'/label.html', **locals() ) + '__Bombolone__'
    
    return result
    