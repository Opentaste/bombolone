# -*- coding: utf-8 -*-
"""
    hash_table.py
    ~~~~~~
    The Hash Table allows you to store multiple Hash Map, 
    each of which has an Name Map and an Hash useful to 
    write the content for use on the web site.
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
from flask import Blueprint, request, g, render_template, url_for, redirect
from pymongo.objectid import ObjectId
from pymongo.errors import InvalidId, PyMongoError

# Imports inside Bombolone
from decorators import check_authentication, check_chief, check_admin, get_hash_table
from languages import Languages
from config import LIST_LANGUAGES
from validators import CheckValue
    
MODULE_DIR = 'modules/hash_table'
hash_table = Blueprint('hash_table', __name__)

languages_object = Languages()

class HashTable(object):
    """ This class allows to :
    - get_hash
    - reset
    - new
    - update
    - remove
    """

    def __init__(self, _id=None):
        self.hash_map    = {}
        self.message     = None            # Error or succcess message
        self.status      = 'msg msg-error'
        self.languages   = languages_object.get_languages(4)
        if _id is None:
            self.reset()
        else:
            self.get_hash(2, _id)
        
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
                _id = var_two
                _id = ObjectId(_id)
                self.hash_map = g.db.hash_table.find_one({ '_id' : ObjectId(_id) })
            except InvalidId:
                self.hash_map = {}
        
    def reset(self):
        """ Reset hash_map value in HashTable.hash_map """
        self.message  = None
        self.status   = 'msg msg-error'
        self.hash_map = { 
        	"name" : "",
        	"value" : {},
        	"module" : False
        }
        
    def new(self):
        """ Add hash map """
        self.__request_hash_map()
        
        if self.message is None:
            try:
                g.db.hash_table.insert( self.hash_map )
                return True
            except PyMongoError:
                self.message = g.hash_table_msg('error_mongo_new')
                return False
                
        return False
        
    def update(self, _id):
        """ Update hash map """
        if g.my['rank'] < 15:
            self.__request_hash_map()
        else:
            self.__request_hash_map_user()
        
        if self.message is None:
            try:
                g.db.hash_table.update({ '_id' : ObjectId(_id)}, self.hash_map )
                self.status = 'msg msg-success'
                self.message = g.hash_table_msg('hash_updated')
            except PyMongoError:
                self.message = g.hash_table_msg('error_mongo_update')
        
    def remove(self, _id):
        """ Remove hash map """
        #  TO DO
        # Controllare che posso eliminare l'hash map
        if True:
            g.db.hash_table.remove({ '_id' : ObjectId(_id) })
            return 'ok'
        return 'nada'
        
    def __request_hash_map_user(self):
        """ """
        form = request.form
        for i, key in enumerate(sorted(self.hash_map['value'])):
            val = {}
            for code in self.languages:
                key_name = 'label_%s_%s' % (code, i)
                val[code] = form[key_name]
            self.hash_map['value'][key] = val
            
    def __request_hash_map(self):
        """ Get from request.form the hash map values and check it """
        form                     = request.form
        self.hash_map['name']    = form['name']
        self.hash_map['value']   = {}
        
        # Check that the name hash map has between 2 and 20 characters
        if not check.length(self.hash_map['name'], 2, 20):
            self.message = g.hash_table_msg('error_1')
            
        # Verify that the format of the username is correct
        elif not check.username(self.hash_map['name']):
            self.message = g.hash_table_msg('error_2')
            
        # Get list labels added
        list_label = [ int(x.split('_')[3]) for x in form if x.startswith('label_name_') ]
        
        # If there exists at least one field, 
        # I can continue the adventure.
        if len(list_label) > 0:
            len_label = max(list_label) + 1
            
            # I look for fields that contain the keys, 
            # then I browse to the field until the larger number.
            for i in range(len_label):
                label_key = 'label_name_%s_%s' % (g.lan, i)
                
                # Check there is label in request.form
                if label_key in form:
                    key = form[label_key].strip()
                    
                    # ~
                    if not check.length(key, 2, 30):
                        self.message = g.hash_table_msg('error_11')
                        
                    # ~
                    elif not check.username(key):
                        self.message = g.hash_table_msg('error_12')
                    
                    # It doesn't take into dictionary the empty keys
                    if check.length(key, 2, 30):
                        # Initial language values
                        self.hash_map['value'][key] = {}
                    
                        for code in self.languages:
                            label_key   = 'label_name_%s_%s' % (code, i)
                            label_value = 'label_%s_%s' % (code, i)
                        
                            # Check there is label in request.form 
                            # with this specific language
                            if label_key in form:
                                value = form[label_value]
                                self.hash_map['value'][key][code] = value
                            else:
                                self.hash_map['value'][key][code] = ''
            
check   = CheckValue()

@hash_table.route('/admin/hash_table/')
@check_authentication 
@check_admin 
@get_hash_table
def overview():
    """ List all the documents, each has a name 
    that identifies it, and an hash map. """
    hash_map_list = g.db.hash_table.find()
    return render_template( '%s/index.html' % MODULE_DIR, **locals() )
    
   
@hash_table.route('/admin/hash_table/new/', methods=['POST', 'GET'])
@check_authentication
@check_chief
@get_hash_table
def new():
    """ Create a new document within the hash table. """
    language_name = languages_object.get_languages(3)
    
    # Initial default user
    hash_object = HashTable()
    hash_map = hash_object.hash_map
    
    # Creation new hash map
    if request.method == 'POST': 
        if hash_object.new():
            return redirect(url_for('hash_table.overview'))
                
    # Come back a message when there is an error	
    if not hash_object.message is None:
        message = hash_object.message
        status  = hash_object.status
       
    return render_template( '%s/new.html' % MODULE_DIR, **locals())
 
 
@hash_table.route('/admin/hash_table/remove/<_id>/')  
@check_authentication 
@check_chief   
def remove(_id):
    """ This method removes an hash map.
    :param _id: MongoDB ObjectId
    """
    hash_object = HashTable()
    return hash_object.remove(_id)


@hash_table.route('/admin/hash_table/<_id>/', methods=['POST', 'GET'])
@check_authentication 
@check_admin
@get_hash_table
def update(_id):
    """ """
    language_name = languages_object.get_languages(3)

    hash_object = HashTable(_id)
    hash_map = hash_object.hash_map

    if request.method == 'POST':
        hash_object.update(_id)	

    # Come back a message when there is a message	
    if not hash_object.message is None:
        message = hash_object.message
        status = hash_object.status
    
    return render_template( '%s/update.html' % MODULE_DIR, **locals() )
  