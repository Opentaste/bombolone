# -*- coding: utf-8 -*-
"""
    check_admin_pages.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
import sys
import unittest
sys.path.append('..')

# Change Database
import config
config.DATABASE = 'app_test'
config.PROJECT_STATIC_FILES = 'data/test'

# Run
import bombolone
from helpers import create_password
from pymongo import Connection
from pymongo.objectid import ObjectId

# Imports modules application
from admin import admin
from content import content
from languages import languages
from login import login
from hash_table import hash_table
from home import home
from pages import pages
from rank import rank
from settings import settings
from users import users

USERNAME = 'test'
PASSWORD = 'test123'

# Save connectio test database
connection = Connection()
db = connection.app_test
db.users.remove({'username' : USERNAME})
data = { "username" : USERNAME, "email" : "", "password" : create_password(PASSWORD),
         "name" : "", "description" : "", "rank" : 10, "lan" : "en", 
         "language" : "English", "time_zone" : "Europe/London", "image" : "",
         "location" : "", "web" : "" }
db.users.insert(data)

class CheckAdminPages(unittest.TestCase):
    
    user_data = {
        "username" : "Leonardo",
    	"email" : "",
    	"password_new" : "",
    	"password_check" : "",
    	"name" : "",
    	"description" : "",
    	"rank" : "12",
    	"lan" : "en",
    	"language" : "English",
    	"time_zone" : "Europe/London",
    	"image" : "",
    	"location" : "",
    	"web" : ""
    }
    new_user = None
    
    languages_data = {
        'es' : 'on', 
        'it' : 'on',
        'pt' : 'on'
    }
    
    hash_table_data = {
        'name' : '',
        'label_name_es_1' : '',
        'label_name_pt_1' : '', 
        'label_name_it_1' : '',
        'label_name_en_1' : '',
        'label_es_1' : '',
        'label_pt_1' : '',
        'label_it_1' : '',
        'label_en_1' : ''
    }
    
    def setUp(self):
        """Before each test, set up a database test"""
        bombolone.app.config['DATABASE'] = 'app_test'
        self.app = bombolone.app.test_client()
        
    ######## LOGIN #########
    def login(self, username, password):
        return self.app.post('/login/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout/', follow_redirects=True)
        
    # 0 - ADMIN AUTHENTICATION #########
    def test_login(self):
        rv = self.login(USERNAME, PASSWORD)
        assert not 'Error 401' in rv.data
        
    # 1 - ADMIN AUTHENTICATION #########
    def test_authentication_admin(self):
        """ The error code in test_authentication_admin should be 401"""
        rv_0  = self.app.get('/admin/')
        rv_1  = self.app.get('/admin/users/')
        rv_2  = self.app.get('/admin/users/new/')
        rv_3  = self.app.get('/admin/rank/')
        rv_4  = self.app.get('/admin/languages/')
        rv_5  = self.app.get('/admin/hash_table/')
        rv_6  = self.app.get('/admin/hash_table/new/')
        assert 'Error 401' in rv_0.data
        assert 'Error 401' in rv_1.data
        assert 'Error 401' in rv_2.data
        assert 'Error 401' in rv_3.data
        assert 'Error 401' in rv_4.data
        assert 'Error 401' in rv_5.data
        assert 'Error 401' in rv_6.data
        
    # 2 - CHECK ADMIN PAGES #########
    def test_admin_dashboard(self):
        """ The error code in test_admin_dashboard should not be 500"""
        rv = self.login(USERNAME, PASSWORD)
        rv_0 = self.app.get('/admin/')
        rv_1  = self.app.get('/admin/users/')
        rv_2  = self.app.get('/admin/users/new/')
        rv_3  = self.app.get('/admin/rank/')
        rv_4  = self.app.get('/admin/languages/')
        rv_5  = self.app.get('/admin/hash_table/')
        rv_6  = self.app.get('/admin/hash_table/new/')
        assert not 'Error 500' in rv_0.data
        assert 'Software Engineer' in rv_1.data
        assert not 'Error 500' in rv_1.data
        assert not 'Error 500' in rv_2.data
        assert not 'Error 500' in rv_3.data
        assert not 'Error 500' in rv_4.data
        assert not 'Error 500' in rv_5.data
        assert not 'Error 500' in rv_6.data
        
    # 3 - CHECK USERS METHODS #########    
    def test_users_1(self):
        """ Check message error in User Module"""
        self.login(USERNAME, PASSWORD)
        rv = self.app.post('/admin/users/new/', data=self.user_data)
        assert not 'Error 400' in rv.data
        assert not 'Error 500' in rv.data
        
    def test_users_2(self):
        """  """
        # Add user
        self.login(USERNAME, PASSWORD)
        self.user_data['username'] = 'new_username'
        self.user_data['name'] = 'Full Name'
        self.user_data['email'] = 'test@test.com'
        self.user_data['password_new'] = '123456'
        self.user_data['password_check'] = '123456'
        
        # Check the user is saved correctly in the index users page 
        rv = self.app.post('/admin/users/new/', data=self.user_data, follow_redirects=True)
        assert '>new_username</a>' in rv.data
        
        # Check the user is saved correctly in database   
        self.new_user = db.users.find_one({ 'username' : 'new_username' })
        assert self.new_user['username'] == self.user_data['username']
        
        # Check again if the user is saved correctly in the update user page 
        rv = self.app.get('/admin/users/%s/' % self.new_user['_id'])
        assert 'value="new_username"' in rv.data
        
        # Update user
        self.user_data['username'] = 'new_username_two'
        rv = self.app.post('/admin/users/%s/' % self.new_user['_id'], data=self.user_data, follow_redirects=True)
        update_user = db.users.find_one({ 'username' : 'new_username' })
        assert update_user is None
        
        # Check the user is saved correctly in database  
        check_user = db.users.find_one({ 'username' : 'new_username_two' })
        assert check_user['username'] == self.user_data['username']
        
        # Check again if the user is saved correctly in the update user page 
        rv = self.app.get('/admin/users/%s/' % self.new_user['_id'])
        assert 'value="new_username_two"' in rv.data
        
        # Remove user
        rv = self.app.get('/admin/users/remove/%s/' % self.new_user['_id'])
        remove_user = db.users.find_one({ '_id' : ObjectId(self.new_user['_id']) })
        assert remove_user is None
        

    ######### CHECK LANGUAGES METHODS #########
    def test_languages(self):
        """ The error code should not be 500"""
        self.login(USERNAME, PASSWORD)
        rv  = self.app.post('/admin/languages/', data=self.languages_data)
        assert not 'Error 400' in rv.data
        assert not 'Error 500' in rv.data
        
    ######### CHECK HASH TABLE METHODS #########
    def test_hash_table_1(self):
        """ The error code should not be 500"""
        self.login(USERNAME, PASSWORD)
        rv = self.app.post('/admin/hash_table/new/', data=self.hash_table_data)
        assert not 'Error 400' in rv.data
        assert not 'Error 500' in rv.data
    
    def test_hash_table_2(self):
        """  """
        # Add hash map
        self.login(USERNAME, PASSWORD)
        self.hash_table_data['name'] = 'italy_map'
        self.hash_table_data['label_name_it_1'] = 'my_town'
        self.hash_table_data['label_name_en_1'] = 'my_town'
        self.hash_table_data['label_name_pt_1'] = 'my_town'
        self.hash_table_data['label_name_es_1'] = 'my_town'
        self.hash_table_data['label_it_1'] = 'Taranto'
        self.hash_table_data['label_en_1'] = 'Taranto'
        self.hash_table_data['label_pt_1'] = 'Taranto'
        self.hash_table_data['label_es_1'] = 'Taranto'
        
        # Check the hash map is saved correctly in the index hash table page 
        rv = self.app.post('/admin/hash_table/new/', data=self.hash_table_data, follow_redirects=True)
        assert '>italy_map</a>' in rv.data
        
        # Check the hash_map is saved correctly in database   
        self.new_map = db.hash_table.find_one({ 'name' : 'italy_map' })
        assert self.new_map['name'] == self.hash_table_data['name']
        
        # Check again if the hash map is saved correctly in the update hash table page 
        rv = self.app.get('/admin/hash_table/%s/' % self.new_map['_id'])
        assert 'value="italy_map"' in rv.data
        
        # Update hash map
        self.hash_table_data['name'] = 'usa_map'
        rv = self.app.post('/admin/hash_table/%s/' % self.new_map['_id'], data=self.hash_table_data, follow_redirects=True)
        update_map = db.hash_table_data.find_one({ 'name' : 'italy_map' })
        assert update_map is None
        
        # Check the user is saved correctly in database  
        check_map = db.hash_table.find_one({ 'name' : 'usa_map' })
        assert check_map['name'] == self.hash_table_data['name']
        
        # Check again if the user is saved correctly in the update user page 
        rv = self.app.get('/admin/hash_table/%s/' % self.new_map['_id'])
        assert 'value="usa_map"' in rv.data
        
        # Remove hash map
        rv = self.app.get('/admin/hash_table/remove/%s/' % self.new_map['_id'])
        remove_map = db.hash_table.find_one({ '_id' : ObjectId(self.new_map['_id']) })
        assert remove_map is None
    

if __name__ == '__main__':
    bombolone.app.register_blueprint(home)
    bombolone.app.register_blueprint(login)
    bombolone.app.register_blueprint(admin)
    bombolone.app.register_blueprint(users)
    bombolone.app.register_blueprint(pages)
    bombolone.app.register_blueprint(rank)
    bombolone.app.register_blueprint(languages)
    bombolone.app.register_blueprint(hash_table)
    bombolone.app.register_blueprint(settings)
    bombolone.app.register_blueprint(content)
    unittest.main()
