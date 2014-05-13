# -*- coding: utf-8 -*-
"""
core.users.py
~~~~~~
The user module allows administrators to create, modify and delete users.

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
import os
import re
import urllib
from datetime import datetime
from flask import request, g, session

# Imports inside Bombolone
import model.users
from config import PATH, UP_AVATARS_TMP_FOLDER, ACTIVATED
from decorators import check_rank, get_hash
from core.languages import LIST_LANGUAGES
from core.utils import create_password, ensure_objectid, get_extension
from core.upload import UploadAvatar, AVATAR_IMAGE_SIZE
from core.validators import CheckValue

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
    message = None
    success = False
    image = ''
    list_images = []
    changed_email = False

    def __init__(self, params={}, _id=None, lan="en", language="English"):
        """ """

        self.params = params
        if _id:
            self.get_user(_id)
        else:
            self.reset(lan=lan, language=language)

    def get_user(self, _id):
        """ Get the user document from Database """
        _id = ensure_objectid(_id)
        self.user = model.users.find(user_id=_id, my_id=_id)

    def reset(self, lan="en", language="English"):
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
            "image": [],
            "location": "",
            "name": "",
            "username": "",
            "password": "",
            "rank": 80,
            "lan": lan,
            "language": language,
            "time_zone": "Europe/London",
            "web": "",
            "status": ACTIVATED
        }


    def new(self):
        """ Insert new user in the database """
        form = self.params
        self.__request_account()
        self.__request_profile()
        self.__request_password(new_user=True)

        if self.changed_email:
            self.user['email'] = self.user['new_email']

        if self.message is None:
            self.user['password'] = create_password(form['password_new'])
            del(self.user['password_new'])
            del(self.user['password_check'])
            self.user['status'] = ACTIVATED

            if 'image_tmp' in self.user:
                del(self.user['image_tmp'])

            self.user['_id'] = model.users.create(self.user)
            if len(form.get('image_uploaded', '')) > 0:
                if self.__upload_avatar():
                    self.user['image'] = self.list_images
                    model.users.update(user_id=self.user['_id'],
                                       user=self.user)

            self.success = True
            self.message = g.users_msg('success_new_user')

        return False

    def update(self):
        """ Update user values in the database """
        form = self.params
        self.__request_account()
        self.__request_profile()
        self.__request_password()

        if self.changed_email:
            self.user['email'] = self.user['new_email']

        if len(form.get('image_uploaded', '')) > 0:
            if self.__upload_avatar():
                self.user['image'] = self.list_images

        if self.message is None:
            if len(form['password_new']):
                self.user['password'] = create_password(form['password_new'])
                del(self.user['password_new'])
                del(self.user['password_check'])

            if 'image_tmp' in self.user:
                del(self.user['image_tmp'])

            model.users.update(user_id=self.user['_id'],
                               user=self.user)
            self.success = True
            self.message = g.users_msg('success_update_user')

        self.user['password_new'] = ""
        self.user['password_check'] = ""

    def update_account(self):
        """ Update user values in the database """
        self.__request_account(True)

        if self.message is None and self.changed_email:
            response = _check_new_email(user=self.user)
            if not response['success']:
                self.message = g.users_msg('account_error_email_1')
            else:
                model.users.update(user_id=self.user['_id'], user=self.user)
                self.success = True
                self.message = g.users_msg('success_update_email')
        
        if self.message is None:
            model.users.update(user_id=self.user['_id'], user=self.user)
            self.success = True
            self.message = g.users_msg('success_update_account')

    def update_profile(self):
        """ Update user values in the database """
        form = self.params
        self.__request_profile()

        if form.get('image_uploaded') and self.__upload_avatar():
            self.user['image'] = self.list_images

        if self.user.get('image_tmp'):
            del(self.user['image_tmp'])

        if self.message is None:
            model.users.update(user_id=self.user['_id'],
                               user = self.user)
            self.success = True
            self.message = g.users_msg('success_update_profile')

    def update_password(self):
        """ Update user values in the database """
        form = self.params
        old_password = self.user.get('password', False)
        self.__request_password(old_password=old_password)
        if self.message is None:
            self.user['password'] = create_password(form['password_new'])
            del(self.user['password_new'])
            del(self.user['password_check'])

            model.users.update(user_id=self.user['_id'],
                               user = self.user)
            self.success = True
            self.message = g.users_msg('success_update_password')

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
                return model.users.remove(user_id=_id)
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
        self.user['newsletter'] = form['newsletter']

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

            # Raises an error message if username is not available.
            elif not available_username is None:
                self.message = g.users_msg('error_account_5')


        # Check that the email field is not empty
        if not self.message and not len(form['email']):
            self.message = g.users_msg('error_account_6')

        # If the email is changed
        elif not self.message and old_email != new_email:
            self.user['new_email'] = new_email
            available_email = model.users.find(email=self.user['new_email'], 
                                               my_rank=10, 
                                               only_one=True)

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
        password = form.get('password')
        password_new = form.get('password_new')
        password_check = form.get('password_check')

        if self.message:
            return False

        # Check that the password_new field is not empty
        if new_user and (password_new is None or len(password_new) == 0):
            self.message = g.users_msg('error_password_0')

        # Check that the password_check field is not empty
        elif new_user and (password_check is None or len(password_check) == 0):
            self.message = g.users_msg('error_password_2')

        elif password_new and len(password_new):
            self.user['password_new'] = password_new
            self.user['password_check'] = password_check

            # Check that the new password has between 6 and 30 characters.
            if not check.length(self.user['password_new'], 6, 30):
                self.message = g.users_msg('error_password_1')

            # Check that both passwords are the same
            elif self.user['password_new'] != self.user['password_check']:
                self.message = g.users_msg('error_password_2')

        if old_password:
            # Verify that the old password matches the one entered.
            old_password = create_password(password)
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
                up = UploadAvatar()
                up.upload(image=image, user=self.user)
                self.list_images = up.names_list
                return True
        self.message = g.users_msg('error_upload_2')
        return False


def get(user_id=None, my_rank=None, my_id=None):
    """
    By passing a user id, return an object with the user info.
    That object could be different in base of different rank permission.

    :param user_id: user id
    :returns: an object with all the user information
    """
    if user_id is None:
        errors = [{ "message": "User id required" }]
    elif not ensure_objectid(user_id):
        errors = [{ "message": "Bad user id" }]
    else:
        user = model.users.find(user_id=user_id, my_rank=my_rank, my_id=my_id)
        if user:
            return dict(success=True, user=user)
        else:
            errors = [{ "message": "Bad user id" }]        
    return dict(success=False, errors=errors)

def get_list(my_rank=None, my_id=None):
    """
    Returns the users list
    """
    users = model.users.find(expand_rank=expand_rank, 
                             my_rank=my_rank, 
                             my_id=my_id)
    if users:
        return dict(success=True, users=users)
    else:
        errors = [{ "message": "Error" }]
    return dict(success=False, errors=errors)

def new(params={}, lan=None, language=None):
    """
    """
    user_object = User(params=params,
                       lan=lan,
                       language=language)
    user_object.new()
    if user_object.success:
        data = {
            "success": True,
            "message": user_object.message,
            "user": user_object.user
        }
    else:
        errors = [{ "message": user_object.message }]
        data = dict(success=False, errors=errors)
    return data


def update(user_id=None, params={}):
    """
    """
    user_object = User(params=params, _id=user_id)
    user_object.update()
    if user_object.success:
        data = {
            "success": True,
            "message": user_object.message,
            "user": user_object.user
        }
    else:
        errors = [{ "message": user_object.message }]
        data = dict(success=False, errors=errors)
    return data


def update_profile(user_id=None, params={}):
    """
    """
    user_object = User(params=params, _id=user_id)
    user_object.update_profile()
    if user_object.success:
        data = {
            "success": True,
            "message": user_object.message,
            "user": user_object.user
        }
    else:
        errors = [{ "message": user_object.message }]
        data = dict(success=False, errors=errors)
    return data


def update_account(user_id=None, params={}):
    """
    """
    user_object = User(params=params, _id=user_id)
    user_object.update_account()
    if user_object.success:
        data = {
            "success": True,
            "message": user_object.message,
            "user": user_object.user
        }
    else:
        errors = [{ "message": user_object.message }]
        data = dict(success=False, errors=errors)
    return data


def update_password(user_id=None, params={}):
    """
    """
    user_object = User(params=params, _id=user_id)
    user_object.update_password()
    if user_object.success:
        data = {
            "success": True,
            "message": user_object.message,
            "user": user_object.user
        }
    else:
        errors = [{ "message": user_object.message }]
        data = dict(success=False, errors=errors)
    return data

def remove(user_id=None):
    """
    Returns the users list
    """
    try:
        user = User(user_id)
        user.remove(user_id)
        data = dict(success=True)
    except:
        errors = [{ "message": "Error" }]
        data = dict(success=False, errors=errors)
    return data

def upload_avatar(name=None):
    """
    """
    extension = get_extension(name)
    up = UploadAvatar()
    path_image = up.ajax_upload(UP_AVATARS_TMP_FOLDER, extension)
    if up.allowed_file() == False:
        success = False
        message = g.users_msg('error_upload_1')
    else:
        up.thumb(AVATAR_IMAGE_SIZE['large'], os.path.join(UP_AVATARS_TMP_FOLDER, path_image))
        if path_image:
            success = True
            message = path_image
    if success:
        return dict(success=True, message=message)
    return dict(success=False, errors=[{ "message": message }])

def _upload_image(user, image_file):
    """ """
    error_code = None
    message = None
    up = UploadAvatar()
    up.upload(network_object=image_file, user=user)
    user['image'] = up.names_list
    model.users.update(user_id=user["_id"], image=user['image'])
    message = ('users_msg', 'success_update_user')
    return error_code, message

