# -*- coding: utf-8 -*-
"""
model.js.py
~~~~~~~~~~~

Manages the js.

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
# Imports inside Bombolone
from bombolone.model import db
from model_engine import db_engine

def find(file_name=None,
         only_one=False):
    """
    """
    conditions = []
    if file_name:
        conditions.append({'file': file_name})
    return db_engine(collection=db.js, 
                     conditions=conditions,
                     only_one=only_one)

