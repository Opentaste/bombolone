# -*- coding: utf-8 -*-
"""
api.users.py
~~~~~~~~~~~

Manages the users.

:copyright: (c) 2012 by OpenTaste
"""


# Imports outside OpenTaste
import re
from flask import current_app, g
from pymongo import ASCENDING, DESCENDING

# Imports inside OpenTaste
from shared import db

from core.utils import ensure_objectid, is_iterable


def find(user_id=None,
         ot_name=None,
         sort_ascending=True,
         only_one=False):
    """
    Returns a list of users or a single user, if user_id or only_one are specified.
    
    user_id: a single user identifier (a string or an ObjectId) or a list of them
    ot_name: the unique user's name
    sort_ascending: if True, sorts the results from first to last, if False sorts them the other way
    only_one: if True, returns one tag at most
    """

    def denormalize(user):
        if not user:
            return user

        if len(user["image"]):
            user["image_show"] =  "/static/avatars/{}/{}".format(user["_id"], user["image"][2])
        else:
            user["image_show"] =  "/static/avatars/default.jpg"
        
        return user
    
    # Looking specifically for one or more users?
    # No further filtering needed!
    if user_id:
        if is_iterable(user_id):
            list_users = list(db.users.find({"_id" : {"$in": [ensure_objectid(x) for x in user_id]}}))
            return [ denormalize(u) for u in list_users ]
        else:
            return denormalize(db.users.find_one({"_id" : ensure_objectid(user_id)}))
    
    if ot_name:
        if is_iterable(ot_name):
            list_users = list(db.users.find({"ot_name" : {"$in": list(ot_name)}}))
            return [ denormalize(u) for u in list_users ]
        else:
            regex = re.compile('^'+ot_name+'$', re.IGNORECASE)
            return denormalize(db.users.find_one({"ot_name" : regex}))
    
    
    # First, builds the filter conditions list
    conditions = [{'rank': 80}] # TODO: what is rank 80?
    
    # Looking for one user only or more?
    if only_one:
        f = db.users.find_one
    else:
        f = db.users.find
    
    # Queries the users
    if conditions:
        users = f({'$and': conditions}) # And, by default
    else:
        users = f()
        
    # Sorts the filtered query results, if they're more than one
    if not only_one:
        users = users.sort('ot_name', sort_ascending and ASCENDING or DESCENDING)
      
    if only_one:
        return denormalize(users) # A dictionary
    else:
        list_users = list(users)
        return [ denormalize(u) for u in list_users ] # A list
