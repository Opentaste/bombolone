# -*- coding: utf-8 -*-
"""
admin.py
~~~~~~

:copyright: (c) 2013 by Leonardo Zizzamia
:license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
import re
from flask import Blueprint, request, session, g, render_template, url_for, redirect
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId
from pymongo.errors import InvalidId, PyMongoError

# Imports inside bombolone
from decorators import check_rank, get_hash
from core.languages import Languages
from core.validators import CheckValue

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
    
    page         = {}
    type_label   = {}
    len_of_label = 0
    
    message      = None            # Error or succcess message
    status       = 'msg msg-error'
    
    def __init__(self, params={}, _id=None):
        """ """
        self.languages = languages_object.get_languages(4)
        self.success = False
        self.params = params
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
            "labels": []
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
        self.__request_content()
        self.__request_values()
        
        if self.message is None:
            try:
                g.db.pages.insert(self.page)
                self.success = True
                self.status = 'msg msg-success'
                self.message = g.pages_msg('success_update_page')
            except PyMongoError:
                self.message = g.pages_msg('error_mongo_new')
                
        return False
        
    def update(self):
        """ Update page in the database """
        if g.my['rank'] < 15:
            self.__request_first_block()
            
        self.__request_second_block()
        self.__request_content()
        self.__request_values()
        
        if self.message is None:
            try:
                g.db.pages.update({ '_id' : ObjectId(self.page['_id']) }, self.page)
                self.success = True
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
        form                = self.params
        old_name            = self.page['name']
        self.page['name']   = form['name']
        self.page['from']   = form['from']
        self.page['import'] = form['import']
        self.page['file']   = form['file']
                
        # Check that the name field is not empty
        if not len(form['name']):
            self.message = g.pages_msg('error_1')
        
        # If the name is changed
        elif old_name.lower() != self.page['name'].lower():
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
        form                     = self.params
        old_url                  = self.page['url']
        self.page['url']         = {}
        self.page['title']       = {}
        self.page['description'] = {}
        
        for i in range(10):
            key = 'url_%s' % i
            if key in self.page:
                del(self.page[key])

        self.page['url']         = form['url']
        self.page['title']       = form['title']
        self.page['description'] = form['description']
        
        # Get URL, Title and Description in any languages
        for code in self.languages:

            if self.message is None:
                error_in = ' ( ' + code + ' )'
                
                # If the url is changed
                if old_url[code] != self.page['url'][code]:
                    url_list = self.__get_url_list(code)
                    num_urls = len(url_list)
                    
                    try:
                        for code_two in self.languages:
                            field = "url_%s.%s" % (num_urls, code_two)
                            available_url = g.db.pages.find_one({ field : url_list })
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
                    url_list = self.__get_url_list(code)
                    num_urls = len(url_list)
                
                if not self.message:
                    kind_of_url = 'url_{}'.format(num_urls)
                    if not kind_of_url in self.page:
                        self.page[kind_of_url] = {}
                    self.page[kind_of_url][code] = url_list
            
    def __request_content(self):
        """ """
        form      = self.params
        self.page['labels'] = form["labels"]
        self.page['content'] = form["content"]
           
    def __request_values(self):
        """ """
        form = self.params
        
        for index, label in enumerate(self.page['content']):
            # get all the languages
            for code in self.languages:            
        
                # if label is an image
                if self.page['labels'][index]["type"] is "image":
                    name_file = upload_file(code+'_'+str(i), 'page')
                    row_label['value'] = name_file

    def __get_url_list(self, code):
        """  """
        url_list = self.page['url'][code].split('/')
        # Convert list with strings all to lowercase
        map(lambda x:x.lower(),url_list)
        # Save the url without slash in the end ( '/' )
        if len(self.page['url'][code]):
            if self.page['url'][code][-1] == '/':
                url_list.pop()
        return url_list
