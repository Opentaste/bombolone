# -*- coding: utf-8 -*-
"""
model.users.py
~~~~~~~~~~~

Manages the users.

> db.users.findOne()
{
    "_id" : ObjectId("4f4a8387d8e40802ea000001"),
    "description" : "",
    "email" : "admin@bombolone.com",
    "image" : [],
    "lan" : "en",
    "language" : "English",
    "location" : "",
    "name" : "Admin Name",
    "password" : "9c1303484c9e5e33f14a0da9628478f6e3d62b610192023a7bbd73250516f069df18b500",
    "rank" : 10,
    "status" : 1,
    "time_zone" : "Europe/London",
    "username" : "Admin",
    "web" : ""
}

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
import re
from datetime import datetime
from pymongo import ASCENDING, DESCENDING

# Imports inside Bombolone
import bombolone.model.ranks
from bombolone.config import ACTIVATED
from bombolone.model import db
from model_engine import db_engine
from bombolone.core.utils import ensure_objectid, is_iterable

def find(user_id=None,
         username=None,
         email=None,
         rank=None,
         lan=None,
         expand_rank=False,
         sorted_by='username',
         sort_ascending=True,
         only_one=False,
         my_rank=None,
         my_id=None):
    """
    Returns a list of users or a single user, if user_id or only_one are specified.

    user_id: a single user identifier (a string or an ObjectId) or a list of them
    username: the unique user's name
    sort_ascending: if True, sorts the results from first to last, if False sorts them the other way
    only_one: if True, returns one tag at most
    
    """
    def denormalize(user):
        if user is None:
            return user

        if expand_rank:
            user['rank_name'] = { x['rank'] : x['name'] for x in model.ranks.find() }[user['rank']]

        # Data we want to show to our Soft Eng or the private user
        if isinstance(my_rank, int) and my_rank <= 70:
            return user

        # Data we want to show to our private user
        if str(my_id) == str(user["_id"]):
            return user

        # Data we want to show after sign in, to all
        user_to_show = {
            "_id" : user.get("_id", None),
            "rank": user.get("rank", None),
            "description": user.get("description", ""),
            "image": user.get("image", ""),
            "location": user.get("location", ""),
            "name": user.get("name", ""),
            "username": user.get("username", ""),
            "web": user.get("web", "")
        }
        return user_to_show

    if username:
        if is_iterable(username):
            list_users = list(db.users.find({"username" : {"$in": list(username)}}))
            return [ denormalize(u) for u in list_users ]
        else:
            regex = re.compile('^'+username+'$', re.IGNORECASE)
            return denormalize(db.users.find_one({"username" : regex}))


    # First, builds the filter conditions list
    conditions = []

    if email:
        email = email.lower()
        conditions.append({'email': email})

    if rank:
        conditions.append({'rank': rank})

    if lan:
        conditions.append({'lan': lan})

    return db_engine(collection=db.users, 
                     item_id=user_id,
                     only_one=only_one, 
                     conditions=conditions,
                     sorted_by=sorted_by,
                     sort_ascending=sort_ascending,
                     denormalize=denormalize)

def create(user=None):
    """
    Create user
    """
    if not "username" in user:
        return (None, "error_model_users_create_username")

    if not "lan" in user:
        return (None, "error_model_users_create_ot_lan")

    if not "language" in user:
        return (None, "error_model_users_create_ot_language")

    new_user = {
        "created": datetime.utcnow(),
        "description": "",
        "email": user.get("email"),
        "image": [],
        "location": "",
        "name": "",
        "username": user["username"],
        "password": user["password"],
        "rank": 80,
        "lan": user.get("lan", "en"),
        "language": user.get("language", "english"),
        "time_zone": "Europe/London",
        "web": "",
        "status": user.get("status", ACTIVATED)
    }

    _id = db.users.insert(new_user)
    return (_id, None)

def update(user_id=None,
           email=None,
           lan=None,
           language=None,
           image=None,
           password=None,
           status=None,
           unset=None,
           pull=None,
           addToSet=None,
           user=None):
    """
    Update one or more users
    """
    user_id = ensure_objectid(user_id)
    if user_id is None:
        return False

    if user:
        db.users.update({"_id": user_id}, user)
        return True

    if pull:
        db.users.update({"_id": user_id}, {"$pull": pull })
        return True

    if addToSet:
        db.users.update({"_id": user_id}, {"$addToSet": addToSet })
        return True

    # First, builds the filter conditions list
    dict_set = {}

    local = locals()
    for item in ["email",
                 "lan",
                 "language",
                 "image",
                 "password",
                 "status"]:
        if not local[item] is None:
            dict_set[item] = local[item]

    if not unset is None:
        dict_unset = {}
        for item in unset:
            dict_unset[item] = 1

    if is_iterable(user_id):
        for _id in user_id:
            if ensure_objectid(_id):
                if unset:
                    db.users.update({"_id": _id}, {"$unset": dict_unset}, False)
                db.users.update({"_id": _id}, {"$set": dict_set})
    else:
        if unset:
            db.users.update({"_id": user_id}, {"$unset": dict_unset}, False)
        db.users.update({"_id": user_id}, {"$set": dict_set})
    db.users.ensure_index('username')
    return True

def remove(username=None, my_rank=None):
    """
    Update one or more users
    """
    if my_rank is None or my_rank > 30:
        return False
    if username is None:
        return False
    else:
        user = db.users.find_one({"username": username})

        if user is None:
            return False

        if user.get('rank') is None or user["rank"] <= my_rank:
            return False

        db.users.remove({"username": username})
        return True
