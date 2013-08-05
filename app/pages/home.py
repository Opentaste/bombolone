# -*- coding: utf-8 -*-
"""
home.py
~~~~~~

:copyright: (c) 2013 by Leonardo Zizzamia
:license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
from flask import Blueprint, request, session, g, render_template, redirect
from pymongo import ASCENDING, DESCENDING

home = Blueprint('home', __name__)

@home.route('/')
def index():
    """ Manages the contents of the home page """
    # If the "my" attribute exists, it means that user is logged in
    return render_template('home.html', **locals())