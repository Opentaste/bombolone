# -*- coding: utf-8 -*-
"""
    languages.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
from flask import Blueprint, g, render_template, url_for

from admin import check_authentication

MODULE_DIR = 'admin/languages'

languages = Blueprint('languages', __name__)


@check_authentication 
@languages.route('/admin/languages/')
def overview():
    """

    """
    languages_list = g.db.languages.find()
    return render_template( MODULE_DIR+'/index.html', **locals())