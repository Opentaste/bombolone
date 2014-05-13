# -*- coding: utf-8 -*-
"""
api.login.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
import re
from flask import Blueprint, request, g, render_template

# Imports inside Bombolone
from decorators import get_hash
from core.utils import jsonify

api_login = Blueprint('api_login', __name__)

@api_login.route('/api/1.0/login')
def index():
    """
    
    """
    data = {
    }
    return jsonify(data)

@api_login.route('/api/1.0/login/join')
def join():
    """
    
    """
    data = {
    }
    return jsonify(data)

@api_login.route('/api/1.0/logout')
def logout():
    """
    
    """
    data = {
    }
    return jsonify(data)
