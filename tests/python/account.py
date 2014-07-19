# -*- coding: utf-8 -*-
"""
tests.account.py
~~~~~~

The TestCase class provides a number of methods to 
check for and report failures, such as:

assertEqual(a, b)           a == b   
assertNotEqual(a, b)        a != b   
assertTrue(x)               bool(x) is True  
assertFalse(x)              bool(x) is False     
assertIs(a, b)              a is b  
assertIsNot(a, b)           a is not b  
assertIsNone(x)             x is None   
assertIsNotNone(x)          x is not None   
assertIn(a, b)              a in b  
assertNotIn(a, b)           a not in b  
assertIsInstance(a, b)      isinstance(a, b)    
assertNotIsInstance(a, b)   not isinstance(a, b) 

Requests: HTTP for Humans
>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
u'{"type":"User"...'
>>> r.json()
{u'private_gists': 419, u'total_private_repos': 77, ...}  

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
import unittest
import requests

from config import PATH, PATH_API

headers = {'Accept': 'text/html'}

class TestAccount(unittest.TestCase):
    pass

class TestAccountAPI(unittest.TestCase):

    def test_account_update(self):
        r = requests.get(PATH_API + "/account/update.json", headers=headers)
        self.assertEqual(404, r.status_code) 
        self.assertIsNot('errors', r.json())

        r = requests.post(PATH_API + "/account/update.json", headers=headers)
        self.assertEqual(401, r.status_code) 
        self.assertIsNot('errors', r.json())

    def test_account_update_profile(self):
        r = requests.get(PATH_API + "/account/update_profile.json", headers=headers)
        self.assertEqual(404, r.status_code) 
        self.assertIsNot('errors', r.json())

        r = requests.post(PATH_API + "/account/update_profile.json", headers=headers)
        self.assertEqual(401, r.status_code) 
        self.assertIsNot('errors', r.json())

    def test_account_update_account(self):
        r = requests.get(PATH_API + "/account/update_account.json", headers=headers)
        self.assertEqual(404, r.status_code) 
        self.assertIsNot('errors', r.json())

        r = requests.post(PATH_API + "/account/update_account.json", headers=headers)
        self.assertEqual(401, r.status_code) 
        self.assertIsNot('errors', r.json())

    def test_account_update_password(self):
        r = requests.get(PATH_API + "/account/update_password.json", headers=headers)
        self.assertEqual(404, r.status_code) 
        self.assertIsNot('errors', r.json())

        r = requests.post(PATH_API + "/account/update_password.json", headers=headers)
        self.assertEqual(401, r.status_code) 
        self.assertIsNot('errors', r.json())

    def test_account_upload_avatar(self):
        r = requests.get(PATH_API + "/account/upload_avatar.json", headers=headers)
        self.assertEqual(404, r.status_code) 
        self.assertIsNot('errors', r.json())

        r = requests.post(PATH_API + "/account/upload_avatar.json", headers=headers)
        self.assertEqual(401, r.status_code) 
        self.assertIsNot('errors', r.json())










