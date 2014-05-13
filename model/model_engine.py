# -*- coding: utf-8 -*-
"""
model.model_engine.py
~~~~~~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
from pymongo import ASCENDING, DESCENDING

# Imports inside Bombolone
from shared import db
from core.utils import ensure_objectid, is_iterable

def denormalize(item):
	""" """
	return item

def sort_if_you_must(items, only_one, sorted_by, sort_lang, sort_ascending):
	""" Sorts the filtered query results, if they're more than one """
	if only_one == False and (sorted_by or sort_lang):
		return items.sort(sorted_by or 'name.' + sort_lang, sort_ascending and ASCENDING or DESCENDING)
	else:
		return items

def db_engine(collection=None, 
			  item_id=None,
			  only_one=False, 
			  conditions=None, 
			  sorted_by=None, 
			  sort_lang=None,
			  sort_ascending=True,
			  skip=None,
			  limit=None,
			  count=None,
			  denormalize=denormalize):
	""" 
	MongoDB Engine of Bombolone
	There are several main steps that every model need it.
	- Looking specifically for one or more items?
      No further filtering needed!
	- Looking for one user only or more
	- Queries the collection conditions
	- Sorts the filtered query results, if they're more than one
	- The skip() expression allows to implementing "paging"
	- Limit the maximum number of results to return.
      For best performance, use limit() whenever possible.
      Otherwise, the database may return more objects than are required for processing.
    - Count the items

    :return a number, when count is True
	:return a dictionary, when only_one is True
	:return a list, when only_one is False

	"""
	if item_id:
		if is_iterable(item_id):
			list_items = collection.find({"_id" : {"$in": [ensure_objectid(x) for x in item_id]}})
			list_items = sort_if_you_must(list_items, only_one, sorted_by, sort_lang, sort_ascending)
			return [ denormalize(item) for item in list_items]
		else:
			return denormalize(collection.find_one({"_id" : ensure_objectid(item_id)}))

	if only_one:
		f = collection.find_one
	else:
		f = collection.find

	if conditions:
		items = f({'$and': conditions})
	else:
		items = f()

	items = sort_if_you_must(items, only_one, sorted_by, sort_lang, sort_ascending)
	
	if skip:
		items = items.skip(skip * limit)

	if only_one == False and limit:
		items = items.limit(limit)

	if count:
		return items.count()

	if only_one:
		return denormalize(items)
	else:
		list_items = list(items)
		return [ denormalize(item) for item in list_items ]

