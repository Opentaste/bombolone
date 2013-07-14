# -*- coding: utf-8 -*-
"""
login.py
~~~~~~

:copyright: (c) 2013 by Bombolone.
""" 
# Imports outside Bombolone
import re
import httplib
import oauth.oauth as oauth
from time import time
from flask import Blueprint, request, session, g, render_template, url_for, redirect, Markup, abort
from recaptcha.client import captcha
from bson import ObjectId

# Imports inside Bombolone
from config import PATH, PATH_API

from decorators import check_authentication, get_hash, jsonp
from oac import get_token, CLIENT_SECRET, CLIENT_ID

from core.emails import RememberPassword
from core.verify import verify_remember, check_verify_remember
from core.utils import create_password

MODULE_DIR = 'intro/login'
login = Blueprint('login', __name__)

class Login(object):
    """ This class allows to :
    - sign_in
    - logout
    """
    
    message = None
    status = 'msg msg-error'
    
    def __init__(self):
        """ """
        pass
        
    def sign_in(self):
        """ """
        input_login = request.form['username']
        password = request.form['password']
        
        if 'permanent' in request.form:
            permanent = request.form['permanent']
        else:
            permanent = None
        
        if not input_login and not password:
            self.message = g.login_msg('login_error_1')
        else:
            regx = re.compile('^'+input_login+'$', re.IGNORECASE)
            user = g.db.users.find_one({"username" : regx})
            no_valid = False
            
            if user is None:
                user = g.db.users.find_one({"email" : regx})
                
            if user is None:
                self.message = g.login_msg('login_error_2')
                return False
            elif self.check_ip_in_black_list(g.ip):
                no_valid = self.recaptcha()

            if user["status"] is 0:
                self.message = g.login_msg('login_error_3')
                return False
                
            if no_valid:
                self.add_ip_in_black_list(g.ip)
                self.message = g.login_msg('captcha_error')
            elif not user['password'] == create_password(password):
                # Important login error
                self.add_ip_in_black_list(g.ip)
                self.message = g.login_msg('login_error_2')
            else:
                # Save session in main domain
                token = get_token(CLIENT_ID, CLIENT_SECRET, user['username'], user['password'])
                if token is None:
                    self.message = g.login_msg('login_error_4')
                    return False
                g.db.users.update({ '_id' : ObjectId(user['_id']) }, { "$set": { "token": token } })
                session['user_id'] = str(user['_id'])
                if permanent is not None:
                    session.permanent = True
                return True
                
        return False
    
    def remember(self):
        """ """
        if request.method == 'POST':
            email = request.form['email'].lower()
            regx = re.compile('^'+email+'$', re.IGNORECASE)
            result_1 = g.db.users.find_one({"username" : regx})
            result_2 = g.db.users.find_one({"email" : email })
            
            if result_1:
                user = result_1
            else:
                user = result_2
                
            if user is None:
                self.message = g.login_msg('remember_error_1')
            
            if self.message is None:
                verify = verify_remember(user)
                user['remember_verify'] = verify
                g.db.users.update({"_id": user['_id'] }, user)
                context = {
                    "path": '{}/remember'.format(PATH),
                    "verify": verify,
                    "name": user['name']
                }
                msg = RememberPassword(user['email'], context)
                email_response = msg.send()
                if not email_response['error']:
                    self.status = 'msg msg-success'
                    self.message = g.remember_msg('remember_ok')
                else:
                    self.message = g.remember_msg('remember_no')
    
    def check_ip_in_black_list(self, ip):
        """ """
        value = time() - 300
        g.db.black_ip.remove({ "time" : { '$lt': value } })
        count = g.db.black_ip.find({'ip' : ip}).count()
        if count > 5:
            return True
        else:
            return False
    
    def add_ip_in_black_list(self, ip):
        """ """
        g.chtml = ''
        value = time()
        black_ip = {
                    'ip' : ip,
                  'time' : value
        }
        g.db.black_ip.insert(black_ip)
        if self.check_ip_in_black_list(ip):
            chtml = captcha.displayhtml(
              public_key = "6Ldph8cSAAAAAGJK1OCZwgqWxctr6gS2FTCM3B1r",
              use_ssl = False,
              error = None)
            g.chtml = Markup(chtml)
    
    def recaptcha(self):    
        """ """
        try:
            challenge = request.form['recaptcha_challenge_field']
            response  = request.form['recaptcha_response_field']
            cResponse = captcha.submit(
                         challenge,
                         response,
                         "6Ldph8cSAAAAAFZt4S2na02xnflgTC3jDNBX91_C",
                         request.remote_addr)
            return cResponse.is_valid
        except:
            return True
    
    def change_password(self, check):
        """ """
        user = check_verify_remember(check)
        if user:
            g.chtml = ''
            chtml = captcha.displayhtml(
              public_key = "6Ldph8cSAAAAAGJK1OCZwgqWxctr6gS2FTCM3B1r",
              use_ssl = False,
              error = None)
            g.chtml = Markup(chtml)
            g.check = check
            if request.method == 'POST':
                valid = self.recaptcha()
                if valid:
                    new_password = request.form['new_password'] 
                    new_password_two = request.form['new_password_two'] 
                    if len(new_password) < 6:
                        message = g.users_msg('error_password_1')
                        status = 'msg msg-error'
                    elif new_password != new_password_two:
                        message = g.users_msg('error_password_2')
                        status = 'msg msg-error'
                    else:
                        g.db.users.update({"_id": user['_id']}, {"$set": { "password": create_password(new_password) } })
                        message = g.users_msg('success_update_password')
                        status = 'msg msg-success'
                else:
                    message = g.login_msg('captcha_error')
                    status = 'msg msg-error'
            return render_template('{}/change_password.html'.format(MODULE_DIR), **locals())
        else:
            message = g.login_msg('not_change_password')
            status = 'msg msg-error'
            return render_template('{}/verify.html'.format(MODULE_DIR), **locals())


@login.route('/login/', methods=['POST', 'GET'])
@get_hash('login')
def index():
    """ """
    if g.my:
        abort(401)
        
    login_object = Login()
    
    if request.method == 'POST':
        if login_object.sign_in():
            print 10
            return redirect(url_for('home.index'))
    
    # Come back a message when there is an error	
    if login_object.message:
        message = login_object.message
        status = login_object.status
    return render_template('{}/login.html'.format(MODULE_DIR), **locals())


@login.route('/logout/')
@check_authentication
def logout():
    """ """
    login_object = Login()
    session.pop('user_id', None)
    session.pop('language', None)
    session.pop('token', None)
    session.pop('synchronization', None)
    g.db.users.update({ '_id' : g.my["_id"] }, { "$set": { "token": "" } })
    return redirect("/")


@login.route('/remember/', methods=['POST', 'GET'])
@get_hash('login')
@get_hash('remember')
def remember():
    """ """
    login_object = Login()
    login_object.remember()
    # Come back a message when there is an error	
    if login_object.message:
        message = login_object.message
        status= login_object.status
    return render_template('{}/remember.html'.format(MODULE_DIR), **locals())


@login.route('/remember/<check>/', methods=['POST', 'GET'])
@get_hash('login')
@get_hash('users')
@get_hash('remember')
def change_password(check):
    """ """
    login_object = Login()
    return login_object.change_password(check)
