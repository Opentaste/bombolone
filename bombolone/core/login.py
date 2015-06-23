# -*- coding: utf-8 -*-
"""
login.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
# Imports inside Bombolone
import bombolone.model.users
from bombolone.config import NOTACTIVATED
from bombolone.core.utils import create_password

def sign_in(username_or_email=None,
            password=None,
            permanent=None):
    """
    Sign the user in.
    We check the user by both the username or email. 

    """
    error_code = None

    if not username_or_email or not password:
        error_code = ('login_msg', 'login_error_1')

    if not error_code:
        user = model.users.find(username=username_or_email, only_one=True, my_rank=10)

        if user is None:
            user = model.users.find(email=username_or_email, only_one=True, my_rank=10)

        if user is None:
            error_code = ('login_msg', 'login_error_2')

        if not error_code and user["status"] == NOTACTIVATED:
            error_code = ('login_msg', 'login_error_3')

        elif not error_code and not user['password'] == create_password(password):
            error_code = ('login_msg', 'login_error_2')

        if not error_code:
            model.users.update(user_id=user["_id"])
            if permanent is not None:
                permanent = True
            return {
                "success": True,
                "user_id": str(user['_id']),
                "permanent": permanent
            }
    return dict(success=False, errors=[{ "code": error_code }])
