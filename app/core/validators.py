# -*- coding: utf-8 -*-
"""
validators.py
~~~~~~
    
:copyright: (c) 2013 by Bombolone
""" 
# Imports outside Bombolone
import re

# Thanks http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
URL_TWO_REGEX = re.compile(r'^[A-Za-z0-9_\/]+$', re.IGNORECASE)
USERNAME_REGEX = re.compile(r'^[a-z0-9_]+$', re.I)
FULLNAME_REGEX = re.compile(r'^[^\W0-9_]+([ \-\'][^\W0-9_]+)*?$', re.U)
EMAIL_REGEX = re.compile(r'^.+@[^.].*\.[a-z]{2,10}$', re.IGNORECASE)
             
class CheckValue(object):
    
    def __init__(self):
        pass
        
    def length(self, data, minimum=-1, maximum=-1):
        """ Validates the length of a string
        :param min: The minimum required length of the string. 
        :param max: The maximum length of the string """
        len_input = len(data)
        
        if len_input < minimum or maximum != -1 and len_input > maximum:
            return False
        return True
        
    def regexp(self, data, regex, flags=0):
        """ Validates the data with regexp
        :param regex: The regular expression string to use. 
        :param flags: The regexp flags eg. re.I (case-insensitive) """
        regex = re.compile(regex, flags)
        if regex.match(data):
            return True
        return False
    
    def username(self, data):
        """ Validates the username 
        :param username: The string """
        if USERNAME_REGEX.match(data):
            return True
        return False
    
    def full_name(self, data):
        """ Validates the full name 
        :param full_name: The string """
        if FULLNAME_REGEX.match(data):
            return True
        return False
    
    def email(self, data):
        """ Validates the email 
        :param email: The string """
        if EMAIL_REGEX.match(data):
            return True
        return False
    
    def url(self, data):
        """ Validates the url 
        :param url: The string """
        if URL_REGEX.match(data):
            return True
        return False

    def url_two(self, data):
        """ Validates the url 
        :param url: The string """
        if URL_TWO_REGEX.match(data):
            return True
        return False
        
    def integer(self, data):
        """ """
        try:
            tmp = int(data)
            return True
        except:
            return False
    
    def float(self, data):
        """ """
        try:
            tmp = float(data)
            return True
        except:
            return False