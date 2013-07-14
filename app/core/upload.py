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
    """ """
    
    name      = ""
    filename  = ""
    extension = ""
    _id       = None
    num_image = None
    
    def __init__(self, name, image):
        self.name      = secure_filename(name.lower())
        self.filename  = secure_filename(image.filename.lower())
        self.extension = self.filename.rsplit('.', 1)[1]
        self.image     = Image.open(image)
        
        self.new_filename  = ''
        self.names_list    = []
        self.paths_list    = []
        self.avatar_size   = ['xsmall','small','normal','large']
    
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
        avatars_path = '{}{}'.format(UP_AVATARS_FOLDER, self.name)
        # If not exists the user avatars folder create a new one
        if not os.path.exists(avatars_path):
            os.mkdir(avatars_path)
        
        new_filename = self.name
        
        # Gets all the images name inside user avatars folder
        list_images = os.listdir(avatars_path+'/')
        
        # In case we upload an image with the same name of the old one, we add an random number
        if os.path.exists('{}/{}-normal.{}'.format(avatars_path, new_filename, self.extension)):
            random_number = randint(12, 98)
            new_filename = '{}-{}'.format(self.name, random_number)
        
        # Remove all the old images
        for name in list_images:
            try:
                os.remove('{}/{}'.format(avatars_path, name))
            except:
                print 'Error remove {}/{} '.format(avatars_path, name)
        
        # Create different name for any size
        for size in self.avatar_size:
            name = new_filename + '-' + size  + '.' + self.extension
            path = self.name + '/' + name
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
