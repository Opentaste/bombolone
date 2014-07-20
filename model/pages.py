# -*- coding: utf-8 -*-
"""
model.pages.py
~~~~~~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
# Imports inside Bombolone
from model_engine import db, db_engine
from core.utils import ensure_objectid, is_iterable

def find(page_id=None,
         name=None,
		 url=None,
         field=None,
         field_value=None,
         page_id_ne=None,
         sorted_by=None,
         sort_ascending=True,
         limit=None,
         only_one=False,
         skip=None,
         count=None):
    """ """
    conditions = []

    if url:
        conditions.append({'url': url})

    if name:
        conditions.append({'name': name})

    if field:
        conditions.append({field: field_value})

    if page_id_ne:
        conditions.append({'_id': { "$ne": page_id_ne }})

    return db_engine(collection=db.pages, 
                     item_id=page_id,
                     conditions=conditions,
                     only_one=only_one,
                     sorted_by=sorted_by,
                     sort_ascending=sort_ascending,
                     limit=limit,
                     skip=skip,
                     count=count)

def create(page=None):
    """Create page"""
    _id = db.pages.insert(page)
    return (_id, None)

def update(page_id=None, page=None):
    """
    """
    if page_id is None:
        return False
    if page:
        db.pages.update({'_id': ensure_objectid(page_id)}, page)
    return page_id

def remove(page_id=None):
    """
    """
    if page_id is None:
        return False
    else:
        db.pages.remove({'_id' : ensure_objectid(page_id)})
        return True
