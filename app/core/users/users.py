# -*- coding: utf-8 -*-
"""
users.py
~~~~~~
The user module allows administrators to create, modify and 
delete users. There are these kind of users:
  user                  |   rank   |
------------------------------------
  Administrator         |    10    |
  User                  |    80    |

:copyright: (c) 2013 by Bombolone
""" 
# Imports outside Bombolone
import cStringIO # *much* faster than StringIO
import os
import re
import shutil
import urllib
import Image
from datetime import datetime
from flask import Blueprint, abort, request, g, render_template, url_for, redirect, session
from random import randint
from werkzeug import secure_filename
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId
from pymongo.errors import InvalidId, PyMongoError

# Imports inside Bombolone
from config import PATH, LIST_LANGUAGES, UP_AVATARS_TMP_FOLDER
from decorators import check_rank, get_hash

# Imports from Bombolone's Core
from core.emails import ChangeEmail
from core.not_allowed import PROHIBITED_NAME_LIST
from core.utils import create_password
from core.upload import Upload
from core.validators import CheckValue
from core.verify import verify_email

import core.api.users
    
MODULE_DIR = 'admin/users'
users = Blueprint('users', __name__)

check = CheckValue()

class User(object):
    """ This class allows to :
    - get_user
    - reset
    - new
    - update
    - update_account
    - update_profile
    - update_password
    - remove
    """
    
    user = {}
    params = {}
    message = None            # Error or success message
    success = False
    image = ''
    list_images = []
    changed_email = False
    
    def __init__(self, params={}, _id=None):
        """ """

        self.params = params
        if _id:
            self.get_user(_id)
        else:
            self.reset()
        
    def get_user(self, _id):
        """ Get the user document from Database """
        try:
            _id = ObjectId(_id)
            self.user = g.db.users.find_one({ '_id' : _id })
            if len(self.user["image"]):
                self.user["image_show"] =  "/static/avatars/{}/{}".format(self.user["_id"], self.user["image"][2])
            else:
                self.user["image_show"] =  "/static/avatars/default.jpg"
        except InvalidId:
            self.user = {}
            
    def reset(self):
        """ Reset user value in Users.user """
        self.image   = ''
        self.list_images = []
        self.message = None
        self.success = False
        self.changed_username = False
        self.user = { 
            "created": datetime.utcnow(),
            "description": "",
            "email": "",
            "email_verify" : "",
            "favorite": [],
            "followers": {},
            "followers_count": 0,
            "following": {},
            "following_count": 0,
            "history": {
                "recipe": []
            },
            "image": [],
            "invite": None,
            "location": "",
            "name": "",
            "notifications" : {
                "comments" : [ ]
            },
            "username": "",
            "password": "",
            "remember_verify": "",
            "rank": 80,
            "lan": "en",
            "language": "English",
            "time_zone": "Europe/London",
            "web": "",
            "status": 1
        }
        
        
    def new(self):
        """ Insert new user in the database """
        form = self.params
        self.__request_account()
        self.__request_profile()
        self.__request_password(True)

        if self.changed_email:
            self.user['email'] = self.user['new_email']
        
        if not self.message:
            self.user['password'] = create_password(form['password_new'])
            del(self.user['password_new'])
            del(self.user['password_check'])
            self.user['status'] = 1
                        
            if 'image_tmp' in self.user:
                del(self.user['image_tmp'])
            
            try:
                self.user['_id'] = g.db.users.insert(self.user)
                
                if 'image_uploaded' in form and len(form['image_uploaded']):
                    if self.__upload_avatar():
                        self.user['image'] = self.list_images
                        g.db.users.update({ '_id' : ObjectId(self.user['_id']) }, self.user)
                
                self.success = True
                self.message = g.users_msg('success_new_user')
            except PyMongoError, e:
                print 'Error caught in users.new : {0}'.format(e)
                self.message = g.users_msg('error_mongo_new')
        
        return False
    
    def update(self):
        """ Update user values in the database """
        form = self.params
        self.__request_account()
        self.__request_profile()
        self.__request_password()
        
        if self.changed_email:
            self.user['email'] = self.user['new_email']
        
        if 'image_uploaded' in form and len(form['image_uploaded']):
            if self.__upload_avatar():
                self.user['image'] = self.list_images
        
        if not self.message:
            if len(form['password_new']):
                self.user['password'] = create_password(form['password_new'])
                del(self.user['password_new'])
                del(self.user['password_check'])
            
            if 'image_tmp' in self.user:
                del(self.user['image_tmp'])
            
            try:
                g.db.users.update({ '_id' : ObjectId(self.user['_id']) }, self.user)
                self.success = True
                self.message = g.users_msg('success_update_user')
            except PyMongoError, e:
                print 'Error caught in users.update : {0}'.format(e)
                self.message = g.users_msg('error_mongo_update')

        self.user['password_new'] = ""
        self.user['password_check'] = ""
    
    def update_account(self):
        """ Update user values in the database """
        self.__request_account(True)
        
        if not self.message and self.changed_email:
            response = self.__check_new_email()
            if response['error']:
                self.message = g.users_msg('account_error_email_1')
        
        if not self.message:
            try:
                g.db.users.update({ '_id' : ObjectId(self.user['_id']) }, self.user)
                self.success = True
                self.message = g.users_msg('success_update_account')
            except PyMongoError, e:
                print 'Error caught in users.update_account : {0}'.format(e)
                self.message = g.users_msg('account_error_1')
    
    def update_profile(self):
        """ Update user values in the database """
        form = self.params
        self.__request_profile()
        
        if 'image_uploaded' in form and self.__upload_avatar():
            self.user['image'] = self.list_images
        
        if self.message is None:
            try:
                g.db.users.update({ '_id' : ObjectId(self.user['_id']) }, self.user)
                self.success = True
                self.message = g.users_msg('success_update_profile')
            except PyMongoError, e:
                print 'Error caught in users.update_profile : {0}'.format(e)
                self.message = g.users_msg('account_error_1')
    
    def update_password(self):
        """ Update user values in the database """
        form = self.params
        self.__request_password(True, True)
        if not self.message:
            self.user['password'] = create_password(form['password_new'])
            del(self.user['password_new'])
            del(self.user['password_check'])
            
            try:
                g.db.users.update({ '_id' : ObjectId(self.user['_id']) }, self.user)
                self.success = True
                self.message = g.users_msg('success_update_password')
            except PyMongoError, e:
                print 'Error caught in users.update_password : {0}'.format(e)
                self.message = g.users_msg('account_error_1')
        
        self.user['password'] = ""
        self.user['password_new'] = ""
        self.user['password_check'] = ""
    
    def remove(self, _id):
        """ Remove user from the database """
        # It checks my id is different from what I want to delete
        if g.my['_id'] != _id:
            self.get_user(_id)
            
            # It checks user _id exist and that
            # you don't remove an other Software Engineer
            if self.user and g.my['rank'] < self.user['rank']:
                try:
                    g.db.users.remove({ '_id' : ObjectId(_id) })
                    return 'ok'
                except PyMongoError:
                    return 'nada'
        
        return 'nada'
    
    def __request_account(self, settings=None): 
        """ Get from request.form the account values and check it """
        form = self.params
        old_username = self.user['username']
        self.user['username'] = form['username']
        old_email = self.user['email']
        new_email = str.lower(str(form['email']))
        self.user['lan'] = form['lan']
        self.user['time_zone'] = form['time_zone'] 
        
        if 'status' in form:
            self.user['status'] = int(form['status'])
        
        if not settings and g.my["rank"] == 10:
            if form['rank'] in map(str, range(10, 90, 10)):
                self.user['rank'] = int(form['rank'])
        
        # Check that the username field is not empty
        if not len(self.user['username']):
            self.message = g.users_msg('error_account_1')
        
        # If the username is changed
        elif old_username != self.user['username']:
            # It's important to change directory avatars
            # Changed username from old_username to new_username
            new_username = unicode(self.user['username']).lower()
            old_username = unicode(old_username).lower()
            
            # Check the username is available and if is different from old username
            if new_username != old_username:
                try:
                    regx = re.compile('^'+new_username+'$', re.IGNORECASE)
                    available_username = g.db.users.find_one({"username" : regx })
                except:
                    available_username = 'Error invalid expression'
            else:
                available_username = None
            
            # Check that the username has between 2 and 20 characters
            if not check.length(self.user['username'], 2, 20):
                self.message = g.users_msg('error_account_2')
            
            # Verify that the format of the username is correct
            elif not check.username(self.user['username']):
                self.message = g.users_msg('error_account_3')
            
            # Check that the username is not among those prohibited.
            elif self.user['username'] in PROHIBITED_NAME_LIST:
                self.message = g.users_msg('error_account_4')
            
            # Raises an error message if username is not available.
            elif not available_username is None:
                self.message = g.users_msg('error_account_5')
        
        
        # Check that the email field is not empty
        if not self.message and not len(form['email']):
            self.message = g.users_msg('error_account_6')
        
        # If the email is changed
        elif not self.message and old_email != new_email:
            self.user['new_email'] = new_email
            available_email = g.db.users.find_one({"email" : self.user['new_email'] })
            
            # Verify that the format of the email is correct
            if not check.email(self.user['new_email']):
                self.message = g.users_msg('error_account_7')
            
            # Raises an error message if email is not available.
            elif available_email:
                self.message = g.users_msg('error_account_8') 
            
            self.changed_email = True

        # Check that the language field is checked
        if not self.message and not self.user['lan'] in LIST_LANGUAGES:
            self.message = g.users_msg('error_account_9')

        # Check that the timezone field is checked
        if not self.message and not len(self.user['time_zone']):
            self.message = g.users_msg('error_account_10')
    
    def __request_profile(self):
        """ Get from request.form the profile values and check it """
        form = self.params
        self.user['name'] = form['name'].strip()
        self.user['description'] = form['description'].strip()
        self.user['location'] = form['location']
        self.user['web'] = form['web'].strip()
        
        if self.message:
            return False
        
        # Check that the name field is not empty
        if not len(self.user['name']):
            self.message = g.users_msg('error_profile_1')
        
        # Check that the name has between 2 and 60 characters.
        elif not check.length(self.user['name'], 2, 60):
            self.message = g.users_msg('error_profile_2')
        
        # Check that the format of the full name is correct
        # and verify that its field is not empty
        elif not check.full_name(self.user['name']) or not len(self.user['name']):
            self.message = g.users_msg('error_profile_3')
        
        # Check that the format of the web url is correct
        # and verify that its field is not empty
        elif not check.url(self.user['web']) and len(self.user['web']):
            self.message = g.users_msg('error_profile_4')
    
    def __request_password(self, new_user=False, old_password=False):
        """ Get from request.form the password values and check it """
        form = self.params

        if self.message:
            return False
        
        # Check that the password_new field is not empty
        if new_user and (not "password_new" in form or not len(form['password_new'])):
            self.message = g.users_msg('error_password_0')

        # Check that the password_check field is not empty
        elif new_user and (not "password_check" in form or not len(form['password_check'])):
            self.message = g.users_msg('error_password_2')
        
        elif "password_new" in form and len(form['password_new']):
            self.user['password_new'] = form['password_new']
            self.user['password_check'] = form['password_check']
            
            # Check that the new password has between 6 and 30 characters.
            if not check.length(self.user['password_new'], 6, 30):
                self.message = g.users_msg('error_password_1')  
            
            # Check that both passwords are the same
            elif self.user['password_new'] != self.user['password_check']:
                self.message = g.users_msg('error_password_2')

        if old_password:
            # Verify that the old password matches the one entered.
            old_password = create_password(form['password'])
            if self.user['password'] != old_password: 
                self.message = g.users_msg('error_password_3')
    
    def __upload_avatar(self):
        """ Upload the avatar """
        form = self.params
        self.user['image_tmp'] = form['image_uploaded']
        
        if self.message or not self.user['image_tmp']:
            return False
        
        file_name = os.path.join(UP_AVATARS_TMP_FOLDER, self.user['image_tmp'])
        if os.path.exists(file_name):
            with open(file_name) as image:
                up = Upload(self.user['username'], image)
                up.avatar_upload(self.user['_id'])
            
            self.list_images = up.names_list
            return True
        
        self.message = g.users_msg('error_upload_2')
        return False
    
    def __check_new_email(self):
        """ """
        verify = verify_email(g.my['_id'])
        self.user['email_verify'] = verify
        context = {
            "path": '{}/change_email'.format(PATH),
            "verify": verify,
            "username": g.my['username']
        }
        msg = ChangeEmail(self.user['new_email'], context)
        email_response = msg.send()
        return email_response


def core_users_show(user_id=None):
    """ """

    success = False
    message = ""

    if user_id:
        success = True
        message = ""
        user = core.api.users.find(user_id=user_id)
    
    data = {
        "success": success,
        "message": message,
        "user": user
    }

    return data


def core_users_list(list_user_id=[]):
    """ """

    success = False
    message = ""

    if len(list_user_id):
        success = True
        message = ""
        users = core.api.users.find(user_id=list_user_id)
    
    data = {
        "success": success,
        "message": message,
        "users": users
    }

    return data