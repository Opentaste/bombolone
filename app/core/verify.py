# -*- coding: utf-8 -*-
"""
verify.py
~~~~~~

:copyright: (c) 2012 by OpenTaste
"""
# Imports outside OpenTaste
import re
import os
import string
import pytz
import random
import smtplib
from PIL import Image 
from imghdr import what
from datetime import datetime 
from urlparse import urlparse
from hashlib import md5, sha1
from flask import session, g, request, abort, current_app

# Imports inside OpenTaste
from core.utils import ensure_objectid, create_password

def verify_email(magic_base_string):
    fake_magic_string = str(magic_base_string) + 'leo'
    md = md5() 
    sh = sha1()
    md.update(fake_magic_string)
    rand_one = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
    rand_two = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    sh.update('verifica_muahahah_email')
    verify = md.hexdigest() + rand_one + sh.hexdigest() + rand_two + '_' + str(magic_base_string)
    return verify

def verify_remember(user):
    fake_email = user['email'] + 'leonardo'
    md = md5()
    sh = sha1()
    sh_two = sha1()
    sh_two.update(user['ot_name'])
    check = sh_two.hexdigest()
    g.db.users.update({ '_id' : user['_id'] }, {'remember_password' : check})
    md.update(fake_email)
    rand_one = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
    rand_two = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    rand_three = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))
    sh.update('ma_ke_stai_a_di_muahahah_email')
    verify = md.hexdigest()+rand_one+sh.hexdigest()+rand_two+'_'+check+rand_three+'_'+str(user['_id'])
    return verify

def check_verify_email(verify, is_email=False):
    """ """
    str_verify = verify.split('_')
    if len(str_verify) != 2:
        return None 
    
    if is_email:
        email = str_verify[1]
        user = g.db.users.find_one({ 'email' : email })
    else:
        _id = str_verify[1]
        user = g.db.users.find_one({ '_id' : ensure_objectid(_id) })

    if user and "email_verify" in user and user['email_verify'] == verify:
        return user
    else:
        return None

def check_verify_remember(verify):
    """
    """
    str_verify = verify.split('_')
    if len(str_verify) != 3:
        return None
    _id = str_verify[2]
    user = g.db.users.find_one({ '_id' : ensure_objectid(_id) })
    if user and user['remember_verify'] == verify:
        return user
    else:
        return None
