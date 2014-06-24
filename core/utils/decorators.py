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
from werkzeug import Response

# Imports inside Bombolone
from shared import app
import model.hash_table

def get_hash_map(module, lan):
    """ """
    module_map = model.hash_table.find(name=module, only_one=True)
    if module_map is None:
        app.logger.critical("Important, you have to restore last database!")
        return None
    return { x : y[lan] for x, y in module_map['value'].iteritems() }

class GetValue(object):
    """ """
    def __init__(self, dictionary):
        self.dictionary = dictionary
        
    def check_key(self, key):
        return self.dictionary.get(key, 'Error code : {}'.format(key))
