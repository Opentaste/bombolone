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

from helpers import init_mongodb


def login_page():
	"""
	
	"""
	if request.method == 'POST':
	    username = request.form['username']
	    password = request.form['password']
	    return redirect(url_for('admin'))
	return render_template('admin/login.html')
	
def logout_page():
	"""

	"""
	return redirect(url_for('home'))
	
def admin_page():
    """
    
    """
    init_mongodb()
    return render_template('admin/dashboard.html')
    
def profile_page():
    """

    """
    return render_template('admin/profile.html')
    
def pages_page():
    """

    """
    list_pages = g.db.pages.find()
    return render_template('admin/pages.html', pages=list_pages)
    
def languages_page():
    """

    """
    list_languages = g.db.languages.find()
    return render_template('admin/languages.html', lan=list_languages)