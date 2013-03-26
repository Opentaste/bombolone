# -*- coding: utf-8 -*-
"""
test.py
~~~~~~

:copyright: (c) 2013 by Bombolone
""" 
import unittest
import time
from datetime import datetime 
from flask import g, Blueprint, render_template, request
from pymongo import ASCENDING, DESCENDING
from xml.dom.minidom import parseString

# Imports inside Bombolone
from shared import app
from decorators import check_rank

# Imports from Bombolone's Core
from core.utils import ensure_objectid

test = Blueprint('test', __name__)

@test.route('/admin/test/scenario/')
@check_rank(30)
def scenario():
    """ Generate the sitemap """
    timestamp = int(time.time()*0.01)
    return render_template('admin/test/scenario.html', timestamp=timestamp)

@test.route('/admin/test/admin/')
@check_rank(30)
def admin():
    """ Generate the sitemap """
    timestamp = int(time.time()*0.01)
    return render_template('admin/test/scenario_admin.html', timestamp=timestamp)

@test.route('/admin/test/basic/')
@check_rank(30)
def basic():
    """ Generate the sitemap's tests """
    errors = ['Zona 1 out: <b style="color:green">ok</b>',
            'Zona recipe out: <b style="color:green">ok</b>',
            'Zona user out: <b style="color:green">ok</b>',
            'Zona 1 in: <b style="color:green">ok</b>',
            'Zona recipe in: <b style="color:green">ok</b>',
            'Zona user in: <b style="color:green">ok</b>',
            'Zona write recipe in: <b style="color:green">ok</b>',
            'Zona update recipe in: <b style="color:green">ok</b>',
            'Zona draft recipe list in: <b style="color:green">ok</b>',
            'Zona favorite recipe list in: <b style="color:green">ok</b>',
            'Zona admin: <b style="color:green">ok</b>']
    
    def check_404_500(client, list_urls, message, index_error, ot_name=None, password=None):
        """ """
        if ot_name:
            rv = client.post('/login/', data={
                "ot_name" : ot_name,
                "pass" : password
            }, follow_redirects=True)
        for url in list_urls:
            try:
                rv = client.get(url)
            except BaseException, e:
                errors[index_error] = '<b style="color:red">{2}: down</b><br />Error {0} at {1}'.format(e, url, message)
            else:
                if 'Not found' in rv.data:
                    errors[index_error] = '<b style="color:red">{1}: down</b><br />Page Not found at {0}'.format(url, message)
                elif 'Error 500' in rv.data:
                    errors[index_error] = '<b style="color:red">{1}: down</b><br />Error 500 at {0}'.format(url, message)
        return None, None
            
    test_draft_recipe = {
        'name_it': '',
        'name_en': '',
        'description_it': '',
        'description_en': '',
        'ingr_for': '',
        'time_hours': '',
        'time_minutes': '',
        'prepare_it_0': '',
        'prepare_en_0': '',
        'num_pre': '1',
        'name_tags': '',
        'num_list_tag': '0',
        'num_file': '0',
        'language_showed': 'en',
        'recipe_id': '',
        'save': 'Save draft'
    }
    
    test_add_ingredient = {
        'name_it': '',
        'name_en': '',
        'description_it': '',
        'description_en': '',
        'ingr_for': '',
        'ingredient_add': '4e3748ee917769cc7b9599c4', # tomato
        'time_hours': '',
        'time_minutes': '',
        'position_add': '0',
        'prepare_it_0': '',
        'prepare_en_0': '',
        'num_pre': '1',
        'name_tags': '',
        'num_list_tag': '0',
        'num_file': '0',
        'language_showed': 'en',
        'recipe_id': '',
        'save': 'Save draft'
    }
    
    # Zona 1 out ======================================================
    list_urls = [
        '/',
        '/remember/',
        '/remember/asdf/',
        '/about/contact/',
        '/login/'
    ]
    with app.test_client() as c:
        check_404_500(c, list_urls, 'Zona 1 out', 0)
    
    # Zona recipe out =================================================
    try:
        with app.test_client() as c:
            lista_recipe = g.db.recipes.find({'draft': False}).sort("created", DESCENDING)
            last_url = ''
            last_recipe_id = ''
            for recipe in lista_recipe:
                last_recipe_id =  str(recipe['_id'])
                if len(recipe['url']['it']):
                    last_url = '/{0}/{1}/'.format(recipe['ot_name'], recipe['url']['it']) 
                    c.get(last_url)
                if len(recipe['url']['en']):
                    last_url = '/{0}/{1}/'.format(recipe['ot_name'], recipe['url']['en'])
                    c.get(last_url)
    except BaseException, e:
        errors[1] = '<b style="color:red">Zona recipe out: down</b><br />Error {0} at {1} (recipe _id is {2})'.format(e, last_url, last_recipe_id)
    
    # Zona user out ===================================================
    with app.test_client() as c:
        list_urls = ['/{}/'.format(user['ot_name']) for user in g.db.users.find()]
        check_404_500(c, list_urls, 'Zona user out', 2)
    
    # Zona 1 in =======================================================
    list_urls = [
        '/',
        '/remember/',
        '/remember/asdf/',
        '/about/contact/',
        '/login/',
        'notification',
        '/settings/profile/',
        '/settings/account/',
        '/settings/password/',
        '/change_email/asdf/',
        '/settings/social/'
    ]
    with app.test_client() as c:
        check_404_500(c, list_urls, 'Zona 1 in', 3, ot_name='user_for_test', password='1234user_for_test567')
    
    # Zona recipe in ==================================================
    try:
        with app.test_client() as c:
            last_url = '/login/'
            rv = c.post(last_url, data={
                "ot_name" : 'user_for_test',
                "pass" : '1234user_for_test567'
            }, follow_redirects=True)
            lista_recipe = g.db.recipes.find({'draft': False}).sort("created", DESCENDING)
            last_url = ''
            last_recipe_id = ''
            for recipe in lista_recipe:
                last_recipe_id =  str(recipe['_id'])
                if len(recipe['name']['it']) > 2:
                    last_url = '/{0}/{1}/'.format(recipe['ot_name'], recipe['url']['it'])
                    c.get(last_url)
                if len(recipe['name']['en']) > 2:
                    last_url = '/{0}/{1}/'.format(recipe['ot_name'], recipe['url']['en'])
                    c.get(last_url)
    except BaseException, e:
        errors[4] = '<b style="color:red">Zona recipe in: down</b><br />Error {0} at {1} (recipe _id is {2})'.format(e, last_url, last_recipe_id)
    
    # Zona user in ====================================================
    with app.test_client() as c:
        list_urls = ['/{}/'.format(user['ot_name']) for user in g.db.users.find()]
        check_404_500(c, list_urls, 'Zona user in', 5, ot_name='user_for_test', password='1234user_for_test567')
    
    # Zona write recipe in ============================================
    with app.test_client() as c:
        check_404_500(c, ['write_recipe'], 'Zona write recipe in', 6, ot_name='user_for_test', password='1234user_for_test567')
    
    # Zona update recipe in ===========================================
    with app.test_client() as c:
        lista_recipe = g.db.recipes.find().sort("created", DESCENDING)
        list_urls = ['/write_recipe/'+str(recipe['_id'])+'/' for recipe in lista_recipe]
        check_404_500(c, list_urls, 'Zona update recipe in', 7, ot_name='user_for_test', password='1234user_for_test567')
    
    # Zona draft recipe list in =======================================
    try:
        with app.test_client() as c:
            check_404_500(c, ['draft'], 'Zona draft recipe list in', 8, ot_name='user_for_test', password='1234user_for_test567')
    except BaseException, e:
        errors[8] = '<b style="color:red">Zona draft recipe list in: down</b><br />Error {0}'.format(e)
    
    # Zona favorites recipe list in ===================================
    try:
        with app.test_client() as c:
            check_404_500(c, ['favorites'], 'Zona favorites recipe list in', 9, ot_name='user_for_test', password='1234user_for_test567')
    except BaseException, e:
        errors[9] = '<b style="color:red">Zona favorites recipe list in: down</b><br />Error {0}'.format(e)
    
    # Zona admin ======================================================
    list_urls = [
        '/admin/',
        '/admin/crew/',
        '/admin/hash_table/',
        '/admin/languages/',
        '/admin/logs/errors/',
        '/admin/matrix/',
        '/admin/matrix_ingredients/',
        '/admin/rank/',
        '/admin/recipes/',
        '/admin/tags/',
        '/admin/new_tags/',
        '/admin/ingredients/',
        '/admin/new_ingredients/',
        '/admin/users/'
    ]
    with app.test_client() as c:
        check_404_500(c, list_urls, 'Zona 1 out', 10, ot_name='manager_for_test', password='manager_for_test890')
    
    return render_template('admin/test/basic.html', **locals())
