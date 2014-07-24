# -*- coding: utf-8 -*-
"""
model.hash_table.py
~~~~~~~~~~~

Manages the hash_table.

{
    "_id" : ObjectId("123456"),
    "module" : true,
    "name" : "admin",
    "value" : {
        "profile" : {
            "en" : "Profile",
            "it" : "Profilo"
        },
        ...
        "save" : {
            "en" : "Save",
            "it" : "Salva"
        },
        "settings" : {
            "en" : "Settings",
            "it" : "Impostazioni"
        }
    }
}

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
# Imports inside Bombolone
from model import db
from model_engine import db_engine
from core.utils import ensure_objectid

def find(hash_table_id=None,
         name=None,
         count=None,
         only_one=False):
    """ """
    # First, builds the filter conditions list
    conditions = []

    if name:
        conditions.append({'name': name})

    return db_engine(collection=db.hash_table, 
                     item_id=hash_table_id,
                     conditions=conditions,
                     only_one=only_one, 
                     count=count)

def create(hash_map=None):
    """ """
    db.hash_table.insert(hash_map)

def update(hash_table_id=None, hash_map=None):
    """ """
    db.hash_table.update({ '_id' : ensure_objectid(hash_table_id)}, hash_map)

def remove(hash_table_id=None):
    """ """
    db.hash_table.remove({ '_id' : ensure_objectid(hash_map_id) })
