# -*- coding: utf-8 -*-
"""
tests.utils.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
import unittest

from flask import g

# Imports inside Bombolone
import core.utils

# Fake text to use in tests
TEXT = "This is a test"

class TestUtils(unittest.TestCase):

    def test_get_message(self):
        """should handle valid requests"""

        g.lang = 'en'

        g.test = {'fake_entry': TEXT}
        get_value = core.utils.decorators.GetValue(g.test)
        g.test_msg = get_value.check_key

        message = ('test_msg', 'fake_entry')
        data = dict(success=True, message=message)

        result = core.utils.get_message(data)
        self.assertEqual(True, result[0])
        self.assertEqual(TEXT, result[1])

        errors = [{'code': message}]
        data = dict(success=False, errors=errors)

        result = core.utils.get_message(data)
        self.assertEqual(False, result[0])
        self.assertEqual(TEXT, result[1])

    def test_get_message_invalid(self):
        """should return an empty string on invalid request"""
        message = ()
        data = dict(success=True, message=message)
        result = core.utils.get_message(data)
        self.assertEqual(True, result[0])
        self.assertEqual("", result[1])

        data = dict(success=False, message=message)
        result = core.utils.get_message(data)
        self.assertEqual(False, result[0])
        self.assertEqual("", result[1])

    def test_set_message(self):
        data = {
            "success": ""
        }
        result = core.utils.set_message(data)

    def test_msg_status(self):
        success = ""
        result = core.utils.msg_status(success)

    def test_linkify(self):
        # Test with some random characters
        string = u"fòò bàr !£##“`ñµ@ł€¶ŧ←↓→øæßðđŋħ«»¢“”ñµ"
        result = core.utils.linkify(string)
        self.assertEqual("foo-bar-nn", result)
        # Test with a real string
        string = u"Foo bar... O fuì bar lol Mare!"
        result = core.utils.linkify(string)
        self.assertEqual("foo-bar-o-fui-bar-lol-mare", result)

    def test_ensure_objectid(self):
        item_id = ""
        result = core.utils.ensure_objectid(item_id)
