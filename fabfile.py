# -*- coding: utf-8 -*-
"""
    fabfile.py
    ~~~~~~
    It provides a basic suite of operations for executing local or remote shell commands, 
    as well as auxiliary functionality such as prompting the running user for input, 
    or aborting execution.
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
from init import clean_database, init_mongodb


def init(all_item=True):
    """ Initialize the database MongoDB of Bombolone. """
    print 'Initialization Bombolone'
    print '##########################\n'

    init_mongodb(all_item)
    print ' * Start Database\n'
   
    
def clean(all_item=True):
    """ Clean and Initialize the database MongoDB of Bombolone. """
    print 'Clean database'
    print '##########################\n'

    clean_database(all)
    print ' * Clean Database\n'

    
def restore(all_item=True):
    """ Clean and Initialize the database MongoDB of Bombolone. """
    print 'Restore database'
    print '##########################\n'

    clean_database(all_item)
    print ' * Clean Database\n'

    init_mongodb(all_item)
    print ' * Start Database\n'