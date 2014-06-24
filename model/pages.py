# -*- coding: utf-8 -*-
"""
model.pages.py
~~~~~~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
# Imports inside Bombolone
from shared import db
from model_engine import db_engine

def find(page_id=None,
		 url=None,
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

    return db_engine(collection=db.pages, 
                     item_id=page_id,
                     conditions=conditions,
                     only_one=only_one,
                     sorted_by=sorted_by,
                     sort_ascending=sort_ascending,
                     limit=limit,
                     skip=skip,
                     count=count)
