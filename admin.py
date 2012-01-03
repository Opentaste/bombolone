# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
from flask import request, session, g, Response, render_template, url_for, redirect, abort, Markup

from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId


def login_page():
	"""
	
	"""
	return render_template('admin/login.html')