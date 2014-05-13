# -*- coding: utf-8 -*-
"""
model.languages.py
~~~~~~~~~~~

Manages the languages.

{
    "_id" : ObjectId("123456"),
    "check" : false,
    "code" : "fr",
    "value" : {
        "ru" : "Russes",
        "fr" : "Française",
        "en" : "Anglaise",
        "cn" : "Chinoise",
        "pt" : "Portugaise",
        "no" : "Norwegian",
        "jp" : "Japonaise",
        "de" : "Allemande",
        "tr" : "Turque",
        "it" : "Italienne",
        "ar" : "",
        "es" : "",
        "gr" : "Grecs"
    }
}

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
# Imports inside Bombolone
from shared import db
from model_engine import db_engine

def find(name=None,
         code=None,
         check=None,
         only_one=False,
         sorted_by=None):
    """
    """
    conditions = []

    if code:
        conditions.append({'code': code})

    if check:
        conditions.append({'check': check})
    
    return db_engine(collection=db.languages, 
                     conditions=conditions,
                     only_one=only_one,
                     sorted_by=sorted_by)

