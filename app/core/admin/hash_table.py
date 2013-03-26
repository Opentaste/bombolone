# -*- coding: utf-8 -*-
"""
hash_table.py
~~~~~~
The Hash Table allows you to store multiple Hash Map, 
each of which has an Name Map and an Hash useful to 
write the content for use on the web site.

:copyright: (c) 2012 by Opentaste
""" 
# Imports outside Opentaste
from flask import Blueprint, request, g, render_template, url_for, redirect
from pymongo.objectid import ObjectId
from pymongo.errors import InvalidId, PyMongoError

# Imports from Opentaste's Core
from core.utils import jsonify, ensure_objectid
from core.languages import Languages
from core.validators import CheckValue

# Imports inside Opentaste
from config import LIST_LANGUAGES
from decorators import check_rank, get_hash, jsonp
    
MODULE_DIR = 'admin/hash_table'
hash_table = Blueprint('hash_table', __name__)

languages_object = Languages()
check = CheckValue()

class HashTable(object):
    """ This class allows to :
    - get_hash
    - reset
    - new
    - update
    - remove
    """
    
    hash_map = {}
    message = None            # Error or succcess message
    status = 'msg msg-error'

    def __init__(self, params={}, _id=None):
        """ """
        self.languages = languages_object.get_languages(4)
        self.success = False
        self.params = params
        if _id:
            self.get_hash(2, _id)
        else:
            self.reset()
    
    def get_hash(self, choice, var_two=''):
        """ Different kind of select query in 
        hash_table collection """
        # Return a dictionary with hash map
        # for the choosen module
        if choice is 1:
            module = var_two
            module_map = g.db.hash_table.find_one({ 'name' : module })
            return { x : y[g.lan] for x, y in module_map['value'].iteritems() }
        
        # Save in self.hash_map the hash_map with that _id,
        # and check it the _id is valid ObjectId
        elif choice is 2:
            try:
                _id = ObjectId(var_two)
                self.hash_map = g.db.hash_table.find_one({ '_id' : _id })
            except InvalidId:
                self.hash_map = {}
    
    def reset(self):
        """ Reset hash_map value in HashTable.hash_map """
        self.message = None
        self.status = 'msg msg-error'
        self.hash_map = { 
            "name" : "",
            "value" : {},
            "module" : False
        }
    
    def new(self):
        """ Add hash map """
        self.__request_hash_map()
        
        if not self.message:
            try:
                g.db.hash_table.insert( self.hash_map )
                self.success = True
                self.status = 'msg msg-success'
                self.message = g.hash_table_msg('hash_created')
            except PyMongoError:
                self.message = g.hash_table_msg('error_mongo_new')
                return False
                
        return False
    
    def update(self):
        """ Update hash map """
        if g.my['rank'] < 25:
            self.__request_hash_map()
        else:
            self.__request_hash_map_user()
        
        if not self.message:
            try:
                g.db.hash_table.update({ '_id' : ObjectId(self.hash_map["_id"])}, self.hash_map )
                self.success = True
                self.status = 'msg msg-success'
                self.message = g.hash_table_msg('hash_updated')
            except PyMongoError:
                self.message = g.hash_table_msg('error_mongo_update')
    
    def remove(self):
        """ Remove hash map """
        list_main_id = [
            '4f2b3e3918429f1b86000016',
            '4f2b3e3918429f1b86000018'
        ]
        if self.hash_map["_id"] in list_main_id:
            return 'nada'
        try:
            g.db.hash_table.remove({ '_id' : ObjectId(self.hash_map["_id"]) })
            return 'ok'
        except PyMongoError:
            return 'nada'
    
    def __request_hash_map_user(self):
        """ """
        form = self.params
        # I look for fields that contain the keys, 
        # then I browse to the field until the larger number.
        for i in range(len(self.hash_map['value'])):
            label_key = 'label-name-{}'.format(i)
            key = form[label_key].strip()
            
            # It doesn't take into dictionary the empty keys
            if check.length(key, 2, 30):
                # Initial language values
                self.hash_map['value'][key] = {}
                
                for code in self.languages:
                    label_value = 'label-{}-{}'.format(code, i)

                    value = form[label_value]
                    self.hash_map['value'][key][code] = value
            
    def __request_hash_map(self):
        """ Get from request.form the hash map values and check it """
        form = self.params
        old_name = self.hash_map['name']
        self.hash_map['name'] = form['name']
        self.hash_map['value'] = {}
        
        # Check that the name hash map has between 2 and 20 characters
        if not check.length(self.hash_map['name'], 2, 20):
            self.message = g.hash_table_msg('error_1')
        
        # Verify that the format of the name is correct
        elif not check.username(self.hash_map['name']):
            self.message = g.hash_table_msg('error_2')

        # Check that the name is new
        if not self.message and old_name != self.hash_map['name']:
            hash_map = g.db.hash_table.find_one({ 'name' : self.hash_map['name'] })
            if hash_map:
                self.message = g.hash_table_msg('error_5')
        
        # Get len label
        len_label = int(form["len"])
            
        # I look for fields that contain the keys, 
        # then I browse to the field until the larger number.
        for i in range(len_label):
            label_key = 'label-name-{}'.format(i)
            key = form[label_key].strip()
                
            # Check that the key has between 2 and 30 characters
            if not check.length(key, 2, 30):
                self.message = g.hash_table_msg('error_3')
                
            # Verify that the format of the key is correct
            elif not check.username(key):
                self.message = g.hash_table_msg('error_4')
            
            # It doesn't take into dictionary the empty keys
            if check.length(key, 2, 30):
                # Initial language values
                self.hash_map['value'][key] = {}
                
                for code in self.languages:
                    label_value = 'label-{}-{}'.format(code, i)
                    
                    value = form[label_value]
                    self.hash_map['value'][key][code] = value


def hash_table_list():
    """ List all the documents, each has a name 
    that identifies it, and an hash map. """
    hash_map_list = list(g.db.hash_table.find().sort('name'))
    return hash_map_list

def hash_table_get(_id=None):
    """ """
    hash_map = g.db.hash_table.find_one({ "_id": ensure_objectid(_id) })
    return hash_map