# -*- coding: utf-8 -*-
"""
    validators.py
    ~~~~~~
    
    This file was inspired by the famous WTForms
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
import re

def length(label, minimum=-1, maximum=-1):
    """
    Validates the length of a string.
    
    :param min:
        The minimum required length of the string. If not provided, minimum
        length will not be checked.
    :param max:
        The maximum length of the string. If not provided, maximum length
        will not be checked.
    """
    assert min != -1 or max!=-1, 'At least one of `min` or `max` must be specified.'
    assert max == -1 or min <= max, '`min` cannot be more than `max`.'
    
    len_label = len(field)
    
    if len_label < minimum or maximum != -1 and len_label > maximum:
        
        if maximum == -1:
            return 1 # Case 1 : Field must be at least minimum character long
        elif minimum == -1:
            return 2 # Case 2 : Field cannot be longer than max character
        else:
            return 3 # Case 3 : Field must be between min and max characters long