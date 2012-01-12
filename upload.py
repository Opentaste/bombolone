# -*- coding: utf-8 -*-
"""
    upload.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
import re, os, time
from werkzeug import secure_filename
from flask import request, session, g, Response, render_template, url_for, redirect, abort 

# Imports inside bombolone
from helpers import allowed_file
from shared import UP_FOLDER   

# Import modules for MongoDB 
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId
			
def upload_file(index, type_upload):
    """
    """ 
    if not 'file_upload_'+index in request.files:
        return ''
    file = request.files['file_upload_'+index]
    if len(file.filename) < 2:
        return ''
    name = file.filename.rsplit('.', 1)[0]
    extension = file.filename.rsplit('.', 1)[1]
    name = str(int(time.time())) + '_' + index + '_' + name + '.' + extension
    name = name.lower()
    
    if file and allowed_file(name):
        path_upload = UP_FOLDER + type_upload + '/'
        file.save(os.path.join(path_upload, name))
        image_path = type_upload + '/' + name	
        return image_path
    else:
        return 'error1'