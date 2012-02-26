# -*- coding: utf-8 -*-
"""
    validators.py
    ~~~~~~
        
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
import re

class GetValue(object):
    
    def __init__(self, dictionary):
        self.dictionary = dictionary
        
    def check_key(self, key):
        try:
            value = self.dictionary[key]
            return value
        except KeyError:
            return ''  
             
class CheckValue(object):
    
    def __init__(self):
        pass
        
    def length(self, data, minimum=-1, maximum=-1):
        """
        Validates the length of a string

        :param min: The minimum required length of the string. 
        :param max: The maximum length of the string
        """
        len_input = len(data)

        if len_input < minimum or maximum != -1 and len_input > maximum:
            return False
        return True
        
    def regexp(self, data, regex, flags=0):
        """
        Validates the data with regexp

        :param regex: The regular expression string to use. 
        :param flags: The regexp flags eg. re.I (case-insensitive)
        """
        regex = re.compile(regex, flags)
        if regex.match(data):
            return True
        return False
    
    def username(self, data):
        """
        Validates the username 

        :param username: The string  
        """
        regex = re.compile(r'^[a-z0-9_]+$', re.I)
        if regex.match(data):
            return True
        return False
    
    def full_name(self, data):
        """
        Validates the full name 

        :param full_name: The string  
        """
        regex = re.compile(r'^[a-z\' ]+$', re.I)
        if regex.match(data):
            return True
        return False
    
    def email(self, data):
        """
        Validates the email 

        :param email: The string  
        """
        regex = re.compile(r'^.+@[^.].*\.[a-z]{2,10}$', re.IGNORECASE)
        if regex.match(data):
            return True
        return False
    
    def url(self, data):
        """
        Validates the url 

        :param url: The string  
        """
        regex = re.compile(ur'^[a-z]+://([^/:]+%s|([0-9]{1,3}\.){3}[0-9]{1,3})(:[0-9]+)?(\/.*)?$', re.IGNORECASE)
        if regex.match(data):
            return True
        return False
        
    def url_two(self, data):
        """
        Validates the url 

        :param url: The string  
        """
        regex = re.compile(r'^[\w\-\.]+[^#?\s]+$', re.IGNORECASE)
        if regex.match(data):
            return True
        return False