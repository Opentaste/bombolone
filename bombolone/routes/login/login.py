# -*- coding: utf-8 -*-
"""
login.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
from flask import (Blueprint, request, session, g, render_template, 
                   redirect)

# Imports inside Bombolone
from bombolone.decorators import get_hash, authentication
from bombolone.core.login import sign_in
from bombolone.core.utils import get_message

login = Blueprint('login', __name__)

@login.route('/login/', methods=['POST', 'GET'])
@get_hash('login')
@get_hash('email')
def index():
    """
    Login page, is visible only for user had not sign in,
    otherwise the 401 page shows up.
    post : sign in, if succeed is going to redirect in home page,
           otherwise the error message shows up in the login page
    get : show login page

    """
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        permanent = request.form.get('permanent', None)
        data = sign_in(username_or_email=username,
                       password=password,
                       permanent=permanent)
        success, message = get_message(data)
        if success:
            session['user_id'] = data['user_id']
            if data['permanent']:
                session.permanent = True
            return redirect("/")
    return render_template('admin/login/login.html', **locals())

@login.route('/logout/')
@authentication
def logout():
    """ """
    session.pop('user_id', None)
    session.pop('language', None)
    return redirect("/")
