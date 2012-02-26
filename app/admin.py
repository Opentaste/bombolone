# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~
    The admin module 
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
from flask import Blueprint, render_template

# Imports inside Bombolone
from decorators import check_authentication

MODULE_DIR = 'modules/admin'
admin = Blueprint('admin', __name__)

@admin.route('/admin/')
@check_authentication
def dashboard():
    """ The dashboard contains a collection of information, 
    such as statistics and other useful stuff. """
    return render_template('%s/dashboard.html' % MODULE_DIR)
