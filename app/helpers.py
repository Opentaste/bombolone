# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
# Imports outside Bombolone
import os
from flask import g
from hashlib import md5, sha1
from shutil import copyfile

def copy_image(src,dst):
	""" If src and dst are the same files, Error is raised."""
	try:
		copyfile(src, dst)
	except:
		print 'sto spostando nella stessa destinazione o src non esiste'   
	
		  
def create_password(word):
    """
    """
    new_pass_left = md5() 
    new_pass_right = sha1()
    new_pass_left.update(word)
    new_pass_right.update(word + 'magic_string')
    new_pass = new_pass_right.hexdigest() + 'f9eAf$2' + new_pass_left.hexdigest() + 'dY!sFd'
    return new_pass
