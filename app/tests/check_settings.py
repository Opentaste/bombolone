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
from bson import ObjectId

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
        
    # 0 - LOGIN AUTHENTICATION #########
    def test_login(self):
        rv = self.login(USERNAME, PASSWORD)
        assert not 'Error 401' in rv.data
        
    # 1 - SETTINGS AUTHENTICATION #########
    def test_authentication_settings(self):
       """ The error code in test_authentication_admin should be 401"""
       rv_0  = self.app.get('/settings/account/')
       rv_1  = self.app.get('/settings/profile/')
       rv_2  = self.app.get('/settings/password/')
       assert 'Error 401' in rv_0.data
       assert 'Error 401' in rv_1.data
       assert 'Error 401' in rv_2.data
                

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
