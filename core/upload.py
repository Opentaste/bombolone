# -*- coding: utf-8 -*-
"""
upload.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
import cStringIO
import os
import werkzeug
import time
from random import randint
from flask import request
from imghdr import what
from PIL import Image

# Imports inside Bombolone
from config import (EXTENSIONS, ALLOWED_EXTENSIONS, ALLOWED_ALL_EXTENSIONS,
                    UP_AVATARS_FOLDER)
from core.utils import get_extension, linkify

AVATAR_IMAGE_SIZE = {
    "xsmall": (40, 40),
    "small": (128, 128),
    "normal": (260, 260),
    "large": (346, 346)
}

class GenericUpload(object):
    """ """

    def __init__(self):
        """ """
        self.name = ""
        self.filename = ""
        self.extension = ""
        self._id = None
        self.num_image = None
        self.new_filename = ''
        self.names_list = []
        self.paths_list = []

    def _open_image_by_network_object(self, network_object=None):
        """ 
        constructs a StringIO holding the image
        """
        image = cStringIO.StringIO(network_object.read())
        self.image = Image.open(image)

    def allowed_file(self):
        """ """
        self.extension = get_extension(self.filename)
        return '.' in self.filename and self.extension in ALLOWED_EXTENSIONS

    def ajax_upload(self, path, extension):
        """ """
        file = werkzeug.FileStorage(stream=request.stream)
        timestamp = str(int(time.time() * 1000000000))
        self.filename = timestamp + '.' + extension
        image_path = os.path.join(path, self.filename)
        file.save(image_path)
        self.image = Image.open(image_path)
        self.extension = self.image.format.lower()
        return self.filename

    def iframe_upload(self, path, extension):
        """ """
        try:
            timestamp = str(int(time.time() * 1000000000))
            image_name = timestamp + '.' + extension
            image_path = os.path.join(path, image_name)
            self.image.save(image_path)
            return image_name
        except BaseException, e:
            print 'Error caught in Upload.iframe_upload : {0}'.format(e)
            return '[ error upload ] - Error in upload image'

    def check_aspect_ratio(self, proportion):
        """ The aspect ratio of an image describes the proportional
        relationship between its width and its height. 

        """
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

    def thumb(self, size, image_path):
        """ """
        im = Image.open(image_path)
        width, height = im.size
        im.thumbnail(size, Image.ANTIALIAS)
        extension = EXTENSIONS[what(image_path)]
        width_proportion = float(width) / im.size[0]
        height_proportion = float(height) / im.size[1]
        quality = 92
        if width_proportion < 4 and height_proportion < 4:
            quality = 94
        try:
            im.save(image_path, extension, quality=quality, optimize=True)
        except IOError:
            im.save(image_path, extension, quality=quality)

class UploadAvatar(GenericUpload):
    """ Upload Avatars
    L'utente seleziona l'immagine che in automatico viene caricata online e salvata
    sulla cartella /avatars/tmp/time_stamp.estensione nella dimensione large.
    Se l'utente salva il profilo allora viene usata tale immagine per creare le
    4 immagini dell'avatar.

    """
    avatar_size = ['xsmall','small','normal','large']

    def _set_filename(self):
        """ """
        self.extension = self.image.format.lower()
        random_number = randint(12, 98)
        self.new_filename = '{}-{}'.format(self.name, random_number)

    def _avatar_thumbs(self):
        """ """
        self.thumb(AVATAR_IMAGE_SIZE['large'], os.path.join(UP_AVATARS_FOLDER, self.paths_list[3]))
        self.thumb(AVATAR_IMAGE_SIZE['normal'], os.path.join(UP_AVATARS_FOLDER, self.paths_list[2]))
        self.thumb(AVATAR_IMAGE_SIZE['small'], os.path.join(UP_AVATARS_FOLDER, self.paths_list[1]))
        self.thumb(AVATAR_IMAGE_SIZE['xsmall'], os.path.join(UP_AVATARS_FOLDER, self.paths_list[0]))

    def _crop_avatar(self, coords, image_path):
        """ The method will recieve the image_path and the coords, like: (x1,y1,x2,y2)
        that probably will come from the crop.html 

        """
        im = Image.open(image_path)
        region_crop = im.crop(coords, Image.ANTIALIAS)
        extension = EXTENSIONS[what(image_path)]
        try:
            region_crop.save(image_path, extension, quality=92, progressive=1, optimize=True)
        except IOError:
            region_crop.save(image_path, extension, quality=92)

    def _avatar_file(self):
        """ """
        avatars_path = '{}/{}'.format(UP_AVATARS_FOLDER, self._id)
        # If not exists the user avatars folder create a new one
        if not os.path.exists(avatars_path):
            os.mkdir(avatars_path)

        # Gets all the images name inside user avatars folder
        list_images = os.listdir(avatars_path+'/')

        # In case we upload an image with the same name of the old one, we add an random number
        if os.path.exists('{}/{}-normal.{}'.format(avatars_path, self.new_filename, self.extension)):
            random_number = randint(12, 98)
            self.new_filename = '{}-{}'.format(self.name, random_number)

        # Remove all the old images
        for name in list_images:
            try:
                os.remove('{}/{}'.format(avatars_path, name))
            except BaseException, e:
                print 'Error caught in Upload._avatar_file {1}/{2} : {0}'.format(e, avatars_path, name)

        # Create different name for any size
        for size in self.avatar_size:
            name = self.new_filename + '-' + size  + '.' + self.extension
            path = self._id + '/' + name
            self.paths_list.append(path)
            self.names_list.append(name)

    def upload(self, image=None, network_object=None, user=None):
        """ """
        self._id = str(user['_id'])
        unicode_username = unicode(user['username'])
        self.name = linkify(unicode_username)
        if network_object:
            self._open_image_by_network_object(network_object=network_object)
        if image:
            self.image = Image.open(image)
        self._set_filename()
        self._avatar_file()
        for path in self.paths_list:
            image_path = os.path.join(UP_AVATARS_FOLDER, path)
            self.image.save(image_path)
        self._avatar_thumbs()
