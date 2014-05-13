 # -*- coding: utf-8 -*-
"""
core.rank.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
# Imports inside Bombolone
from core.utils import ensure_objectid
from core.validators import CheckValue
import model.ranks
import model.users

check = CheckValue()

def show(rank_id=None):
    """ """
    if rank_id is None:
        list_ranks = model.ranks.find(sorted_by='rank', expand_number=True)
        data = {
            "success": True,
            "ranks": list_ranks
        }
    else:
        rank = model.ranks.find(rank_id=rank_id, expand_number=True)
        data = {
            "success": True,
            "rank": rank
        }
    return data

def create(name=None, rank=None):
    """ """
    error_code = None
    if name is None or len(name) == 0:
        error_code = ('rank_msg', 'error_1')
    elif rank is None:
        error_code = ('rank_msg', 'error_2')
    elif check.is_integer(rank) == False:
        error_code = ('rank_msg', 'error_3')
    else:
        rank = int(rank)
        rank = model.ranks.create(name=name, rank=rank)
        data = {
            "success": True,
        }
        return data
    data = {
        "success": False,
        "errors": [{
            "code": error_code
        }]
    }
    return data

def update(rank_id=None, name=None, rank=None):
    """ """
    error_code = None
    if ensure_objectid(rank_id) is None:
        error_code = ('rank_msg', 'error_0')
    elif name is None or len(name) == 0:
        error_code = ('rank_msg', 'error_1')
    elif rank is None:
        error_code = ('rank_msg', 'error_2')
    elif check.is_integer(rank) == False:
        error_code = ('rank_msg', 'error_3')
    else:
        rank = int(rank)
        result = model.ranks.update(rank_id=rank_id, name=name, rank=rank)
        if result:
            data = {
                "success": True,
            }
            return data
        error_code = ('rank_msg', 'error_4')
    data = {
        "success": False,
        "errors": [{
            "code": error_code
        }]
    }
    return data

def remove(rank_id=None, my_rank=None):
    """ """
    error_code = None
    if rank_id is None:
        error_code = ('rank_msg', 'error_1')
    elif my_rank is None:
        error_code = ('rank_msg', 'error_2')
    else:
        result = model.ranks.remove(rank_id=rank_id, my_rank=my_rank)
        if result:
            data = {
                "success": True,
            }
            return data
        error_code = ('rank_msg', 'error_4')
    data = {
        "success": False,
        "errors": [{
            "code": error_code
        }]
    }
    return data
