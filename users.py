# -*- coding: utf-8 -*-
"""
    users.py
    ~~~~~~
    The user module allows administrators to create, modify and delete users.
    The user module supports user rank, which can be set up permissions 
    allowing each rank to do only what the administrator permits. 
    By default there are two users:
      username |  rank  |
    -------------------------------
      admin    |   10   |
      user     |   20   |
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
import re
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

# Imports inside bombolone
from decorators import check_authentication, check_admin, get_hash_users
from helpers import allowed_file, copy_image, create_password, language_check, thumb_image
from not_allowed import NAME_LIST
from validators import email, full_name, length, url, username
    
MODULE_DIR = 'modules/users'
users = Blueprint('users', __name__)
users_permits = ['overview','new','update','remove']

 
@users.route('/admin/users/')
@check_authentication
@get_hash_users
def overview():
    """ The overview shows the list of the users registered, 
    can sort the users depending on the field want. """
    users_list = g.db.users.find()
    return render_template( MODULE_DIR+'/index.html', **locals() )
 
  
@users.route('/admin/users/new/', methods=['POST', 'GET'])
@check_authentication
@check_admin
@get_hash_users
def new():
    """ """       
    language_name = language_check()
    message = None
    
    my = { 
         'username' : '', 
            'email' : '',
         'password' : '', 
             'rank' : 20,
              'lan' : '',
        'time_zone' : 'Europe/London',
             'name' : '',
      'description' : '',
         'location' : '',
              'web' : ''
    }

    if request.method == 'POST':
        form = request.form    
        my = { 
             'username' : form['username'], 
                'email' : form['email'],
             'password' : '', 
                 'rank' : int(form['rank']),
                  'lan' : form['language'],
            'time_zone' : form['time_zone'],
                'image' : '',
                 'name' : form['name'],
          'description' : form['description'],
             'location' : form['location'],
                  'web' : form['web']
        }
        message = request_account_form(my, '', '', '', form['new_password'], form['check_password'])
        if message is None:
            my['password'] = create_password(form['new_password'])
            g.db.users.insert(my)			
            return redirect(url_for('users.overview'))
			
	if not message is None:
	    status = 'mes_red'
        
    return render_template( MODULE_DIR+'/new.html', **locals())
    
 
@users.route('/admin/users/remove/<_id>/')      
@check_authentication 
@check_admin
def remove(_id):
    """

    :param _id: 
    """
    if g.my_id != _id:
        g.db.users.remove({ '_id' : ObjectId(_id) })
        return 'ok'
    return 'nada'


@users.route('/admin/users/<_id>/', methods=['POST', 'GET'])
@check_authentication
@check_admin
@get_hash_users
def update(_id):
    """

    :param _id: 
    """
    language_name = language_check()
    message = None
    
    my = g.db.users.find_one({ '_id' : ObjectId(_id) })

    if request.method == 'POST':
        file = request.files['file']
        form = request.form   
        
        old_username = my['username']
        old_email = my['email']
        
        my['username'] = form['username']
        my['email'] = form['email']
        my['rank'] = int(form['rank'])
        my['lan'] = form['language']
        my['time_zone'] = form['time_zone']
        my['name'] = form['name']
        my['description'] = form['description']
        my['location'] = form['location']
        my['web'] = form['web']

        message = request_account_form(my, old_username, old_email, form['password'], form['password_new'], form['password_check'])
        if message is None:
            
            if len(form['password_new']):
                my['password'] = create_password(form['password_new'])
            
            if file and allowed_file(file.filename):
                my['image'] = upload_avatar(file, my)
            
            g.db.users.update({ '_id' : ObjectId(my['_id']) }, my)			
            return redirect(url_for('users.overview'))
			
	if not message is None:
	    status = 'mes_red'
    
    return render_template( MODULE_DIR+'/update.html', **locals() )
    

def request_account_form(my, old_username, old_email, password, new_password, check_password):
    """ 

    :param my: 
    :param old_username: 
    :param old_email: 
    """
    check_result = check_username(my['username'])
    res_email = None
    message = None
    
    old_username = str.lower(str(old_username))

    # ~~~~~
    if my['email'] != old_email:
        res_email = g.db.users.find_one({"email" : my['email'] })

    # ~~~~~
    if not len(my['username']):
        message = g.users['account_error_1']

    # ~~~~~
    elif not length(my['username'], 2, 20):
        message = g.users['account_error_2']

    # ~~~~~
    elif check_result is not None and my['username'] != old_username:
        message = g.users['account_error_4']

    # ~~~~~
    elif my['username'] in NAME_LIST and my['username'] != old_username:
        message = g.users['account_error_3']

    # ~~~~~
    elif not username(my['username']):
        message = g.users['account_error_7']

    # ~~~~~
    elif not email(my['email']):
        message = g.users['account_error_5']

    # ~~~~~
    elif not check_result is None:
        message = g.users['account_error_6']

    # ~~~~~
    elif not full_name(my['name']) and len(my['name']):
        message = g.users['regex_full_name']

    # ~~~~~
    elif not url(my['web']) and len(my['web']):
        message = g.users['regex_url']

    elif len(new_password) or not 'password' in request.form:
        # ~~~~~
        if not length(new_password, 6, 30):
    		message = g.users['password_error_1']	

    	# ~~~~~
    	elif new_password != check_password:
    		message = g.users['password_error_2']

    	elif len(password):			
            # ~~~~~
            if my['password'] != create_password(password): 
            	message = g.users['password_error_3']	

    # ~~~~~    
    return message


def check_username(new_username):
    """
    """
    new_username = str.lower(str(new_username))
    regx = re.compile('^'+new_username+'$', re.IGNORECASE)
    return g.db.user.find_one({"username" : regx })


def upload_avatar(my):
    """ """
    name = my['username'].lower()
    filename = name + '.' + file.filename.rsplit('.', 1)[1]
    
    # Random num for don't have new image in cache
    num = randint(12, 98) 
    
    filename = str(num) + '_' + filename
    image_path = UPLOAD_FOLDER + 'avatar/' + filename
    image_path_middle = UPLOAD_FOLDER + 'avatar/middle/' + filename
    image_path_small = UPLOAD_FOLDER + 'avatar/small/' + filename
    
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    copy_image(image_path, image_path_middle)
    copy_image(image_path, image_path_small)
    
    # 3 images : profile, post, comment			
    thumb_image((140, 140), image_path)
    thumb_image((60, 60), image_path_middle)
    thumb_image((40, 40), image_path_small)
    
    if my['image'] is not None:
        remove_image(UPLOAD_FOLDER + 'avatar/' + my['image'])
        remove_image(UPLOAD_FOLDER + 'avatar/middle/' + my['image'])
        remove_image(UPLOAD_FOLDER + 'avatar/small/' + my['image'])
		
    return filename