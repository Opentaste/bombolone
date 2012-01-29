# -*- coding: utf-8 -*-
"""
    validators.py
    ~~~~~~
        
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
import re

def length(data, minimum=-1, maximum=-1):
    """
    Validates the length of a string
    
    :param min:
        The minimum required length of the string. 
    :param max:
        The maximum length of the string
    """
    len_input = len(data)
    
    if len_input < minimum or maximum != -1 and len_input > maximum:
        return False
    return True
            
            
def required(data):
    """
        Validates that the field contains data.
        
    """
    pass
    
    
def regexp(data, regex, flags=0):
    """
    Validates the data with regexp

    :param regex:
        The regular expression string to use. 
    :param flags:
        The regexp flags eg. re.I (case-insensitive)
    """
    regex = re.compile(regex, flags)
    if regex.match(data):
        return True
    return False
    
    
def username(data):
    """
    Validates the username 

    :param username:
        The string  
    """
    regex = re.compile(r'^[a-z0-9_]+$', re.I)
    if regex.match(data):
        return True
    return False
    
    
def full_name(data):
    """
    Validates the full name 

    :param full_name:
        The string  
    """
    regex = re.compile(r'^[a-z\' ]+$', re.I)
    if regex.match(data):
        return True
    return False
    
    
def email(data):
    """
    Validates the email 

    :param email:
        The string  
    """
    regex = re.compile(r'^.+@[^.].*\.[a-z]{2,10}$', re.IGNORECASE)
    if regex.match(data):
        return True
    return False
    
    
def url(data):
    """
    Validates the url 

    :param url:
        The string  
    """
    regex = re.compile(ur'^[a-z]+://([^/:]+%s|([0-9]{1,3}\.){3}[0-9]{1,3})(:[0-9]+)?(\/.*)?$', re.IGNORECASE)
    if regex.match(data):
        return True
    return False