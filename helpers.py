# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
import os
from flask import g
from hashlib import md5, sha1
from imghdr import what
from PIL import Image 
from shutil import copyfile

from shared import db, ALLOWED_EXTENSIONS
    
        
def allowed_file(filename):
    """Check if the file has correct extension.
    Return True or False"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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
         
    
def get_hash_map(module):
    """
    """
    module_map = g.db.hash_table.find_one({ 'name' : module })
    return { x : y[g.lan] for x, y in module_map['value'].iteritems() }
    
    
def language_check():
    """ Finding the available languages """
    language_name = g.db.languages.find_one({ 'code' : g.lan })
    return [ (x , y) for x, y in sorted(language_name['value'].iteritems()) if x in g.languages ]


def remove_image(path):
	try:
		os.remove(path)
	except:
		print 'nada ',path
    		   
    
def thumb_image(size, image_path):
    """ """
    im = Image.open(image_path)
    im.thumbnail(size, Image.ANTIALIAS)
    extension = EXTENSIONS[what(image_path)]
    try:
        im.save(image_path, extension, quality=92, progressive=1, optimize=True)
    except IOError:
        im.save(image_path, extension, quality=92)    
