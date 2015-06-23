# -*- coding: utf-8 -*-
"""
utils.py
~~~~~~~~~~~

Generic helper functions

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
from flask import current_app

# Imports inside Bombolone
import bombolone.model.hash_table

def get_hash_map(module, lan):
    """ """
    module_map = model.hash_table.find(name=module, only_one=True)
    if module_map is None:
        current_app.logger.critical("Important, you have to restore last database!")
        return None
    return { x : y.get(lan, '') for x, y in module_map['value'].iteritems() }

class GetValue(object):
    """ """
    def __init__(self, dictionary):
        self.dictionary = dictionary
        
    def check_key(self, key):
        return self.dictionary.get(key, 'Error code : {}'.format(key))
