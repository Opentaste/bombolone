# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
from flask import g
from hashlib import md5, sha1

from shared import db, ALLOWED_EXTENSIONS
    
    
def create_password(word):
    """
    """
    new_pass_left = md5() 
    new_pass_right = sha1()
    new_pass_left.update(word)
    new_pass_right.update(word + 'magic_string')
    new_pass = new_pass_right.hexdigest() + 'f9eAf$2' + new_pass_left.hexdigest() + 'dY!sFd'
    return new_pass
    
    
def allowed_file(filename):
    """Check if the file has correct extension.
    Return True or False"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
    
def language_check():
    """ Finding the available languages """
    language_name = g.db.languages.find_one({ 'code' : g.lan })
    return [ (x , y) for x, y in sorted(language_name['value'].iteritems()) if x in g.languages ]