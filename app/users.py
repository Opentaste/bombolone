# -*- coding: utf-8 -*-
"""
    users.py
    ~~~~~~
    The user module allows administrators to create, modify and delete users.
    The user module supports user rank, which can be set up permissions 
    allowing each rank to do only what the administrator permits. 
    By default there are two users:
      username |  rank  |
    -------------------------------
      Admin    |   10   |
      User     |   20   |
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
import os, re, shutil
from flask import Blueprint, abort, request, g, render_template, url_for, redirect
from pymongo.objectid import ObjectId
from pymongo.errors import InvalidId, PyMongoError

# Imports inside Bombolone
from decorators import check_authentication, check_admin, get_hash_users
from helpers import create_password
from languages import Languages
from not_allowed import PROHIBITED_NAME_LIST
from config import UP_AVATARS_FOLDER, UP_IMAGE_FOLDER
from validators import CheckValue
from upload import Upload

MODULE_DIR = 'modules/users'
users = Blueprint('users', __name__)

check            = CheckValue()   # Check Value class
languages_object = Languages()


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
    
    user        = {}
    message     = None            # Error or succcess message
    status      = 'msg msg-error'
    image       = ''
    list_images = []
    changed_username = False
    
    def __init__(self, _id=None):
        """ """
        if _id is None:
            self.reset()
        else:
            self.get_user(_id)
        
    def get_user(self, _id):
        """ Get the user document from Database """
        try:
            _id = ObjectId(_id)
            self.user = g.db.users.find_one({ '_id' : _id })
        except InvalidId:
            self.user = {}
            
    def reset(self):
        """ Reset user value in Users.user """
        self.image   = ''
        self.list_images = []
        self.message = None
        self.status  = 'msg msg-error'
        self.changed_username = False
        self.user = { 
            "username" : "",
            "email" : "",
            "password" : "",
            "name" : "",
            "description" : "",
            "rank" : 20,
            "lan" : "en",
            "language" : "English",
            "time_zone" : "Europe/London",
            "image" : "",
            "location" : "",
            "web" : ""
        }
    
    def new(self):
        """ Insert new user in the database """
        self.__request_account()
        self.__request_profile()
        self.__request_password(True)
        
        if self.message is None:
            password_new = create_password(request.form['password_new'])
            self.user['image'] = ''
            self.user['password'] = password_new
            try:
                g.db.users.insert(self.user)
                return True
            except PyMongoError:
                self.message = g.users_msg('error_mongo_new')
        
        return False
    
    def update(self):
        """ Update user values in the database """
        self.__request_account()
        self.__request_profile()
        self.__request_password()
        
        if 'file' in request.files and self.__upload_avatar():
            self.user['image'] = self.list_images
        
        if self.message is None:
            if len(request.form['password_new']):
                password_new = create_password(request.form['password_new'])
                self.user['password'] = password_new     
            
            # If is changed the username it's important
            # the old avatars directory in the new position
            if self.changed_username and len(self.user['image']):
                src = os.path.join(UP_AVATARS_FOLDER,self.changed_username[0])
                dst = os.path.join(UP_AVATARS_FOLDER,self.changed_username[1])
                shutil.move(src,dst)
            
            try:
                g.db.users.update({ '_id' : ObjectId(self.user['_id']) }, self.user)
                self.status = 'msg msg-success'
                self.message = g.users_msg('success_update_user')
            except PyMongoError:
                self.message = g.users_msg('error_mongo_update')
    
    def update_account(self):
        """ Update user values in the database """
        self.__request_account(True)
        
        if self.message is None:
            # If is changed the username it's important
            # the old avatars directory in the new position
            if self.changed_username and len(self.user['image']):
                src = os.path.join(UP_AVATARS_FOLDER,self.changed_username[0])
                dst = os.path.join(UP_AVATARS_FOLDER,self.changed_username[1])
                shutil.move(src,dst)
            
            try:
                g.db.users.update({ '_id' : ObjectId(self.user['_id']) }, self.user)
                self.status = 'msg msg-success'
                self.message = g.users_msg('success_update_account')
            except PyMongoError:
                self.message = g.users_msg('account_error_1')
                          
    def update_profile(self):
        """ Update user values in the database """
        self.__request_profile()
        
        if 'file' in request.files and self.__upload_avatar():
            self.user['image'] = self.list_images
        
        if self.message is None:
            try:
                g.db.users.update({ '_id' : ObjectId(self.user['_id']) }, self.user)
                self.status = 'msg msg-success'
                self.message = g.users_msg('success_update_profile')
            except PyMongoError:
                self.message = g.users_msg('account_error_1')
                
    def update_password(self):
        """ Update user values in the database """
        self.__request_password()
        if self.message is None:
            password_new = create_password(request.form['password_new'])
            self.user['password'] = password_new     
            
            try:
                g.db.users.update({ '_id' : ObjectId(self.user['_id']) }, self.user)
                self.status = 'msg msg-success'
                self.message = g.users_msg('success_update_password')
            except PyMongoError:
                self.message = g.users_msg('account_error_1')
    
    def remove(self, _id):
        """ Remove user from the database """
        # It checks my id is different from what I want to delete
        if g.my['_id'] != _id:
            self.get_user(_id)
            
            # It checks user _id exist and that
            # you don't remove an other Software Engineer
            if not self.user is None and g.my['rank'] < self.user['rank']:
                try:
                    g.db.users.remove({ '_id' : ObjectId(_id) })
                    return 'ok'
                except PyMongoError:
                    return 'nada'
        
        return 'nada'
    
    def __request_account(self, settings=None): 
        """ Get from request.form the account values and check it """
        form                     = request.form
        old_username             = self.user['username']
        old_email                = self.user['email']
        self.user['username']    = form['username']
        self.user['email']       = str.lower(str(form['email']))
        self.user['lan']         = form['language']
        self.user['time_zone']   = form['time_zone'] 
        
        if settings is None:
            self.user['rank'] = int(form['rank']) 
        
        # Check that the username field is not empty
        if not len(form['username']):
            self.message = g.users_msg('error_account_1')     
        
        # If the username is changed
        elif old_username != self.user['username']:
            # It's important to change directory avatars
            # Changed username from old_username to new_username
            new_username = str.lower(str(self.user['username']))
            old_username = str.lower(str(old_username))
            self.changed_username = (old_username, new_username)
            
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
        if not len(form['email']):
            self.message = g.users_msg('error_account_6')
                
        # If the email is changed
        elif old_email != self.user['email']:
            available_email = g.db.users.find_one({"email" : self.user['email'] })
                        
            # Verify that the format of the email is correct
            if not check.email(self.user['email']):
                self.message = g.users_msg('error_account_7')
            
            # Raises an error message if email is not available.
            elif not available_email is None:
                self.message = g.users_msg('error_account_8')            
        
    def __request_profile(self):
        """ Get from request.form the profile values and check it """
        form                     = request.form
        self.user['name']        = form['name']
        self.user['description'] = form['description']
        self.user['location']    = form['location']
        self.user['web']         = form['web']
        
        if not self.message is None:
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
        
    def __request_password(self, new_user=False):
        """ Get from request.form the password values and check it """
        if not self.message is None:
            return False
        
        # Check that the password_new field is not empty
        if not len(request.form['password_new']) and new_user:
            self.message = g.users_msg('error_password_0')
        
        if len(request.form['password_new']):
            self.user['password_new'] = request.form['password_new']
            self.user['password_check'] = request.form['password_check']
                   
            # Check that the new password has between 6 and 30 characters.
            if not check.length(self.user['password_new'], 6, 30):
                self.message = g.users_msg('error_password_1')	
            
            # Check that both passwords are the same
            elif self.user['password_new'] != self.user['password_check']:
                self.message = g.users_msg('error_password_2')
            
        if 'password' in request.form:
            # Verify that the old password matches the one entered.
            old_password = create_password(request.form['password'])
            if self.user['password'] != old_password: 
                self.message = g.users_msg('error_password_3')
                    
    def __upload_avatar(self):
        """ Upload the avatar """
        self.image = request.files['file']
        
        if not self.message is None:
            return False
                
        if len(self.image.filename) > 3:
            up = Upload(self.user['username'], self.image)
            
            # ~
            if not up.allowed_file():
                self.message = g.users_msg('error_upload_1')
                
            # ~
            elif not up.check_aspect_ratio(1):
                self.message = g.users_msg('error_upload_2')
            
            # ~
            else:
                up.avatar_upload()
                self.list_images = up.names_list
                return True
                
        return False


@users.route('/admin/users/')
@check_authentication
@check_admin
@get_hash_users
def overview():
    """ The overview shows the list of the users registered, 
    can sort the users depending on the field want. """
    ranks_list = { x['rank'] : x['name'] for x in g.db.ranks.find() }
    users_list = g.db.users.find().sort("name")
    return render_template('{}/index.html'.format(MODULE_DIR), **locals() )


@users.route('/admin/users/new/', methods=['POST', 'GET'])
@check_authentication
@check_admin
@get_hash_users
def new():
    """ The administrator can create a new user """       
    language_name = languages_object.get_languages(3)
    g.list_ranks = g.db.ranks.find()
    
    user_object = User()
    
    # Creation new user
    if request.method == 'POST':
        if user_object.new():
            return redirect(url_for('users.overview'))	
    
    # get the user info after POST request
    user = user_object.user
    
    # Come back a message when there is an error	
    if not user_object.message is None:
        message = user_object.message
        status  = user_object.status
    
    return render_template('{}/new.html'.format(MODULE_DIR), **locals())


@users.route('/admin/users/remove/<_id>/')      
@check_authentication 
@check_admin
def remove(_id):
    """ This method removes a user.
    :param _id: MongoDB ObjectId
    """
    user_object = User()
    return user_object.remove(_id)


@users.route('/admin/users/<_id>/', methods=['POST', 'GET'])
@check_authentication
@check_admin
@get_hash_users
def update(_id):
    """
    
    :param _id: 
    """
    language_name = languages_object.get_languages(3)
    g.list_ranks = g.db.ranks.find()
    
    user_object = User(_id)
    
    if g.my['rank'] > user_object.user['rank'] and g.my['rank'] > 15:
        abort(401)
        
    if request.method == 'POST':
        user_object.update()
    
    # get the user info after POST request
    user = user_object.user
    
    # Come back a message when there is a message	
    if not user_object.message is None:
        message = user_object.message
        status = user_object.status
    
    return render_template('{}/update.html'.format(MODULE_DIR), **locals() )