# -*- coding: utf-8 -*-
"""
utils.py
~~~~~~~~~~~

Generic helper functions

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
import os
import datetime
import time
import json
import string
import re
import binascii
from collections import Iterable
from types import StringTypes
from hashlib import md5, sha1
from unicodedata import normalize
from flask import g, request
from werkzeug import secure_filename, Response

# Imports inside Bombolone
from shared import app

def get_message(data):
    """
    Extract status and message from the given dictionary.
    The message is translated according to the hash map.

    :param data: status and message hash/key pair
    :type data: dict
    :returns: (success, message) tuple
    """
    success = data['success']
    message = ""
    if success:
        if 'message' in data and len(data['message']) == 2:
            hash_map = data['message'][0]
            message_code = data['message'][1]
            message = getattr(g, hash_map)(message_code)
    else:
        if 'errors' in data and len(data['errors']) > 0:
            error_tuple = data['errors'][0].get('code')
            if error_tuple and len(error_tuple) == 2:
                hash_map = error_tuple[0]
                error_code = error_tuple[1]
                message = getattr(g, hash_map)(error_code)
    return success, message

def set_message(data):
    """
    Set status and message on the given dictionary.
    The message is translated according to the hash map.

    :param data: status and message hash/key pair
    :type data: dict
    :returns: the passed dict with "message" or "errors" field updated
    """
    success = data['success']
    message = ""
    if success:
        if 'message' in data and len(data['message']) == 2:
            hash_map = data['message'][0]
            message_code = data['message'][1]
            data['message'] = getattr(g, hash_map)(message_code)
    else:
        if 'errors' in data and len(data['errors']) > 0:
            error_tuple = data['errors'][0].get('code')
            if error_tuple and len(error_tuple) == 2:
                hash_map = error_tuple[0]
                error_code = error_tuple[1]
                data['errors'][0]['code'] = error_code
                data['errors'][0]['message'] = getattr(g, hash_map)(error_code)
    return data

def msg_status(success):
    """ """
    if success is not None:
        return 'msg msg-error' if success is False else 'msg msg-success'
    return ''
