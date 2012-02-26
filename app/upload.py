# -*- coding: utf-8 -*-
"""
    upload.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside Bombolone
import re, os, time
from random import randint
from flask import request, g, Response, url_for, redirect, abort
from imghdr import what 
from PIL import Image
from werkzeug import secure_filename

# Imports inside Bombolone
from config import (EXTENSIONS, ALLOWED_EXTENSIONS, ALLOWED_ALL_EXTENSIONS, 
                    UP_FOLDER, UP_AVATARS_FOLDER, UP_IMAGE_FOLDER)


class Upload(object):
    
    def __init__(self, username, image):
        self.username  = username.lower()
        self.filename  = secure_filename(image.filename.lower())
        self.extension = self.filename.rsplit('.', 1)[1]
        self.image     = Image.open(image)
        
        self.new_filename = ''
        self.names_list   = []
        self.paths_list   = []
        self.avatar_size  = ['xsmall','small','normal','large']
        
    def allowed_file(self):
        """ """
        self.extension = self.filename.rsplit('.', 1)[1]
        return '.' in self.filename and self.extension in ALLOWED_EXTENSIONS
        
    def avatar_upload(self):
        """ """
        self.__avatar_file()
        
        for path in self.paths_list:
            image_path = os.path.join(UP_AVATARS_FOLDER, path)
            self.image.save(image_path)
        
        self.__avatar_thumbs()
        
        
    def check_aspect_ratio(self, proportion):
        """ The aspect ratio of an image describes the proportional 
        relationship between its width and its height. """
        width, height = self.image.size
        if proportion is 1:
            # 1 square
            if (width / float(height)) == 1:
                return True
        elif proportion is 2:
            # 1.3333:1 (4:3)
            if (round(width / float(height), 4)) is 1.3333:
                return True
        return False
    
    def __avatar_file(self):
        """ """
        if not os.path.exists('static/avatars/%s' % self.username):
            os.mkdir('static/avatars/%s' % self.username)
            
        new_filename = '%s' % self.username
        list_images = os.listdir('static/avatars/%s/' % self.username)
                
        if os.path.exists('static/avatars/%s/%s-normal.%s' % (self.username, new_filename, self.extension)):
            num = randint(12, 98)
            new_filename = '%s-%s' % (self.username, num)
            
        for name in list_images:
            try:
                os.remove('static/avatars/%s/%s' % (self.username, name))
            except:
                print 'Error remove static/avatars/%s/%s ' % (self.username, name)
                
        for size in self.avatar_size:
            name = new_filename + '-' + size  + '.' + self.extension
            path = self.username + '/' + name
            self.paths_list.append(path)
            self.names_list.append(name)
        
    def __avatar_thumbs(self):
        """ """
        self.__thumb((128, 128), os.path.join(UP_AVATARS_FOLDER, self.paths_list[3]))
        self.__thumb((80, 80), os.path.join(UP_AVATARS_FOLDER, self.paths_list[2]))
        self.__thumb((32, 32), os.path.join(UP_AVATARS_FOLDER, self.paths_list[1]))
        self.__thumb((16, 16), os.path.join(UP_AVATARS_FOLDER, self.paths_list[0]))
        
    def __thumb(self, size, image_path):
        """ """
        im = Image.open(image_path)
        im.thumbnail(size, Image.ANTIALIAS)
        extension = EXTENSIONS[what(image_path)]
        try:
            im.save(image_path, extension, quality=92, progressive=1, optimize=True)
        except IOError:
            im.save(image_path, extension, quality=92)
