# -*- coding: utf-8 -*-
"""
    home.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
from flask import Blueprint, request, session, g, render_template, redirect
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

# Imports inside Bombolone
from config import PATH

home = Blueprint('home', __name__)

@home.route('/')
def index():
    """ Manages the contents of the home page """
    
    # If exist my attribute means that user is login
    if hasattr(g, "my"):
        return render_template('content/home.html', **locals())
    else:
        return render_template('intro/home.html', **locals())