# -*- coding: utf-8 -*-
"""
    languages.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
import re
from flask import request, session, g, Response, render_template, url_for, redirect, abort, Markup
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

from admin import check_authentication

MODULE_DIR = 'admin/languages'

@check_authentication 
def languages_page():
    """

    """
    languages_list = g.db.languages.find()
    return render_template( MODULE_DIR+'/index.html', **locals())