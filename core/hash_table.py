# -*- coding: utf-8 -*-
"""
core.hash_table.py
~~~~~~
The Hash Table allows you to store multiple Hash Map,
each of which has an Name Map and an Hash useful to
write the content for use on the web site.

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
from flask import g

# Imports inside Bombolone
from core.languages import Languages
from core.validators import CheckValue
from decorators import check_rank
import model.hash_table

check = CheckValue()
languages_object = Languages()

LENGTH_MIN_KEY = 2
LENGTH_MAX_KEY = 30
LENGTH_MIN_HASHMAP_NAME = 2
LENGTH_MAX_HASHMAP_NAME = 20

def get_list():
    """ 
    Get all the documents, each has a name
    that identifies it, and an hash map. 
    """
    hash_map_list = model.hash_table.find()
    data = dict(success=True, hash_map_list=hash_map_list)
    return data


def get(_id=None):
    """ 
    Get one of the documents, each has a name
    that identifies it, and an hash map. 
    """
    hash_map = model.hash_table.find(hash_table_id=_id)
    data = dict(success=True, hash_map=hash_map)
    return data


def new(params={}):
    """ """
    hash_map = {
        "name" : "",
        "value" : {},
        "module" : False
    }
    hash_map, error_code = _request_hash_map(hash_map, params)
    if error_code is None:
        model.hash_table.create(hash_map=hash_map)
        message = ("hash_table_msg", "hash_created")
        return dict(success=True, message=message, hash_map=hash_map)
    return dict(success=False, errors=[{ "code": error_code }])


def update(params={}, my_rank=g.my['rank']):
    """ 
    """
    _id = params.get("_id", None)
    hash_map = model.hash_table.find(hash_table_id=_id)
    if my_rank < 25:
        hash_map, error_code = _request_hash_map(hash_map, params)
    else:
        hash_map, error_code = _request_hash_map_user(hash_map, params)
    if error_code is None:
        model.hash_table.update(hash_table_id=hash_map["_id"], hash_map=hash_map)
        message = ("hash_table_msg", "hash_updated")
        return dict(success=True, message=message, hash_map=hash_map)
    return dict(success=False, errors=[{ "code": error_code }])


def remove(_id=None):
    """ 
    """
    if _id is None:
        error_code = ('hash_table_msg', 'error_hash_table_remove')
    else:
        hash_map = model.hash_table.find(hash_table_id=_id)
        model.hash_table.remove(hash_table_id=hash_map["_id"])
        return dict(success=True)
    return dict(success=False, errors=[{ "code": error_code }])


def _request_hash_map_user(hash_map, form):
    """ """
    error_code = None
    # I look for fields that contain the keys,
    # then I browse to the field until the larger number.
    for i in range(len(hash_map['value'])):
        label_key = 'label-name-{}'.format(i)
        key = form[label_key].strip()

        # It doesn't take into dictionary the empty keys
        if check.length(key, LENGTH_MIN_KEY, LENGTH_MAX_KEY):
            # Initial language values
            hash_map['value'][key] = {}

            for code, name in languages_object.all_lang_by_tuple:
                label_value = 'label-{}-{}'.format(code, i)

                value = form.get(label_value, "")
                hash_map['value'][key][code] = value
    return hash_map, error_code


def _request_hash_map(hash_map, form):
    """ Get from request.form the hash map values and check it """
    error_code = None
    old_name = hash_map['name']
    hash_map['name'] = form['name']
    hash_map['value'] = {}

    # Check that the name hash map has between 2 and 20 characters
    if not check.length(hash_map['name'], LENGTH_MIN_HASHMAP_NAME, LENGTH_MAX_HASHMAP_NAME):
        error_code = ('hash_table_msg', 'error_1')

    # Verify that the format of the name is correct
    elif not check.username(hash_map['name']):
        error_code = ('hash_table_msg', 'error_2')

    # Check that the name is new
    if error_code is None and old_name != hash_map['name']:
        hash_map_old = model.hash_table.find(name=hash_map['name'], only_one=True)
        if hash_map_old:
            error_code = ('hash_table_msg', 'error_5')

    # Get len label
    len_label = int(form["len"])

    # I look for fields that contain the keys,
    # then I browse to the field until the larger number.
    for i in range(len_label):
        label_key = 'label-name-{}'.format(i)
        key = form[label_key].strip()

        # Check that the key has between 2 and 30 characters
        if not check.length(key, LENGTH_MIN_KEY, LENGTH_MAX_KEY):
            error_code = ('hash_table_msg', 'error_3')

        # Verify that the format of the key is correct
        elif not check.username(key):
            error_code = ('hash_table_msg', 'error_4')

        # It doesn't take into dictionary the empty keys
        if check.length(key, LENGTH_MIN_KEY, LENGTH_MAX_KEY):
            # Initial language values
            hash_map['value'][key] = {}

            for code, name in languages_object.all_lang_by_tuple:
                label_value = 'label-{}-{}'.format(code, i)

                value = form.get(label_value, "")
                hash_map['value'][key][code] = value
    return hash_map, error_code
