# -*- coding: utf-8 -*-
"""
unit_test.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
import unittest
import requests
import logging
import sys

from config import PATH
from tests.account import TestAccount, TestAccountByClient, TestAccountAPI
from tests.hash_table import TestHashTable, TestHashTableByClient, TestHashTableAPI
from tests.rank import TestRank, TestRankAPI
from tests.utils import TestUtils

if __name__ == '__main__':
    type_test = None
    if len(sys.argv) > 1:
        type_test = sys.argv[1]

    try:
        requests.get(PATH + '/')
    except:
        logging.critical("Bombolone test can't run because the application is not up.")
        sys.exit(0)

    list_class = []

    if type_test == "unit": 
        list_class += [
            TestAccount,
            TestHashTable,
            TestRank,
            TestUtils
        ]

    if type_test == "app":  
        list_class += [
            TestAccountByClient,
            TestHashTableByClient
        ]

    if type_test == "api":  
        list_class += [
            TestAccountAPI,
            TestHashTableAPI,
            TestRankAPI,
            TestUsersAPI
        ]

    if type_test is None:
        unittest.main()
    else:
        for test_class in list_class:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
            unittest.TextTestRunner(verbosity=2).run(suite)
