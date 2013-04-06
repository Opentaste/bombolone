# -*- coding: utf-8 -*-
"""
test.py
~~~~~~

:copyright: (c) 2013 by Bombolone
""" 
import unittest
import time
from datetime import datetime 
from flask import g, Blueprint, render_template, request
from pymongo import ASCENDING, DESCENDING
from xml.dom.minidom import parseString

# Imports inside Bombolone
from shared import app
from decorators import check_rank

# Imports from Bombolone's Core
from core.utils import ensure_objectid

test = Blueprint('test', __name__)

@test.route('/admin/test/scenario/')
@check_rank(30)
def scenario():
    """ Generate the sitemap """
    timestamp = int(time.time()*0.01)
    return render_template('admin/test/scenario.html', timestamp=timestamp)

@test.route('/admin/test/admin/')
@check_rank(30)
def admin():
    """ Generate the sitemap """
    timestamp = int(time.time()*0.01)
    return render_template('admin/test/scenario_admin.html', timestamp=timestamp)

@test.route('/admin/test/basic/')
@check_rank(30)
def basic():
    """ Generate the sitemap's tests """
    errors = ['Zona 1 out: <b style="color:green">ok</b>',
            'Zona 1 in: <b style="color:green">ok</b>',
            'Zona admin: <b style="color:green">ok</b>']
    
    def check_404_500(client, list_urls, message, index_error, username=None, password=None):
        """ """
        if username:
            rv = client.post('/login/', data={
                "username" : username,
                "pass" : password
            }, follow_redirects=True)
        for url in list_urls:
            try:
                rv = client.get(url)
            except BaseException, e:
                errors[index_error] = '<b style="color:red">{2}: down</b><br />Error {0} at {1}'.format(e, url, message)
            else:
                if 'Not found' in rv.data:
                    errors[index_error] = '<b style="color:red">{1}: down</b><br />Page Not found at {0}'.format(url, message)
                elif 'Error 500' in rv.data:
                    errors[index_error] = '<b style="color:red">{1}: down</b><br />Error 500 at {0}'.format(url, message)
        return None, None
            
    # Zona 1 out ======================================================
    list_urls = [
        '/',
        '/remember/',
        '/remember/asdf/',
        '/about/contact/',
        '/login/'
    ]
    with app.test_client() as c:
        check_404_500(c, list_urls, 'Zona 1 out', 0)
    
    # Zona 1 in =======================================================
    list_urls = [
        '/',
        '/remember/',
        '/remember/asdf/',
        '/about/contact/',
        '/login/',
        'notification',
        '/settings/profile/',
        '/settings/account/',
        '/settings/password/',
        '/change_email/asdf/',
        '/settings/social/'
    ]
    with app.test_client() as c:
        check_404_500(c, list_urls, 'Zona 1 in', 3, username='user_test', password='user_test_123')
    
    # Zona admin ======================================================
    list_urls = [
        '/admin/',
        '/admin/hash_table/',
        '/admin/languages/',
        '/admin/users/'
    ]
    with app.test_client() as c:
        check_404_500(c, list_urls, 'Zona 1 out', 10, username='manager_test', password='manager_test_123')
    
    return render_template('admin/test/basic.html', **locals())
