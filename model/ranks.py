# -*- coding: utf-8 -*-
"""
model.ranks.py
~~~~~~~~~~~

Manages the ranks.

{
    "_id" : ObjectId("123456"),
    "name" : "Admin",
    "rank" : 10
}

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
# Imports inside Bombolone
from model import db
from model_engine import db_engine
from core.utils import ensure_objectid, is_iterable
import model.users

def find(rank_id=None,
         expand_number=False,
         sorted_by='rank',
         sort_ascending=True,
         only_one=False):
    """
    Returns a list of ranks or a single rank, if rank_id or only_one are specified.

    rank_id: a single rank identifier (a string or an ObjectId) or a list of them
    expand_number: add an extra field with the number of user for every rank returned
    sorted_by: the field to sort the result with; by default it's the rank field
    sort_ascending: if True, sorts the results from first to last, if False sorts them the other way
    only_one: if True, returns one rank at most

    """
    def denormalize(rank):
        if rank is None:
            return rank
        if expand_number:
            rank['number_user'] = len(model.users.find(rank=rank['rank']))
        return rank
    
    conditions = []
    return db_engine(item_id=rank_id,
                     collection=db.ranks, 
                     conditions=conditions,
                     only_one=only_one,
                     sorted_by=sorted_by,
                     sort_ascending=sort_ascending,
                     denormalize=denormalize)

def create(name=None, rank=None):
    """
    Create a new rank.
    Returns the id of the inserted rank (a string) if everything went well, False otherwise.

    name: the name of the rank
    rank: numbare value of the rank

    """
    if name is None and rank is None:
        return False
    new_rank = {
        'name': name,
        'rank': rank
    }
    rank_id = db.ranks.insert(new_rank)
    return rank_id

def update(rank_id=None, name=None, rank=None):
    """
    """
    if rank_id is None:
        return False
    dict_set = {}
    if name:
        dict_set["name"] = name
    if rank:
        dict_set["rank"] = rank
    set_rank = {
        '$set': dict_set
    }
    db.ranks.update({'_id': ensure_objectid(rank_id)}, set_rank)
    return rank_id

def remove(rank_id=None, my_rank=None):
    """
    """
    if my_rank is None or my_rank > 10:
        return False
    if rank_id is None:
        return False
    else:
        rank = model.ranks.find(rank_id=rank_id, expand_number=True)
        if rank is None:
            return False
        if rank["number_user"] != 0:
            return False
        db.ranks.remove({'_id' : ensure_objectid(rank_id)})
        return True
