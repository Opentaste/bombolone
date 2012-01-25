# -*- coding: utf-8 -*-
"""
    init.py
    ~~~~~~
    Implements several functions to populate the database startup Bombolone.
    
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
"""
from helpers import create_password
from shared import db


def clean_database():
    """ Removes all the collections in the database. """
    db.languages.remove()
    db.hash_table.remove()
    db.pages.remove()
    db.users.remove()


def init_languages():
    """ Initializes the base 8 languages, 
    and in any language is written the name of the other.
    """
    
    dict_languages = {
        'it' : {
            'it' : 'Italiano',
            'en' : 'Inglese',
            'es' : 'Spagnolo',
            'pt' : 'Portoghese',
            'fr' : 'Francese',
            'de' : 'Tedesco',
            'jp' : 'Giapponese',
            'cn' : 'Cinese',
            'ru' : 'Russo',
            'tr' : 'Turco',
            'gr' : 'Greco',
            'ar' : 'Arabo' },
        'en' : {
            'it' : 'Italian',
            'en' : 'English',
            'es' : 'Spanish',
            'pt' : 'Portuguese',
            'fr' : 'French',
            'de' : 'German',
            'jp' : 'Japanese',
            'cn' : 'Chinese',
            'ru' : 'Russian',
            'tr' : 'Turkish',
            'gr' : 'Greek',
            'ar' : 'Arabic' },
        'es' : {
            'it' : 'Italiano',
            'en' : 'Inglés',
            'es' : '',
            'pt' : 'Portugués',
            'fr' : 'Francés',
            'de' : 'Alemán',
            'jp' : 'Japonés',
            'cn' : 'Chino',
            'ru' : 'Ruso',
            'tr' : 'Turco',
            'gr' : 'Griego',
            'ar' : '' },
        'pt' : {
            'it' : 'Italiano',
            'en' : 'Inglês',
            'es' : '',
            'pt' : 'Português',
            'fr' : 'Francês',
            'de' : 'Alemão',
            'jp' : 'Japonês',
            'cn' : 'Chinês',
            'ru' : 'Russo',
            'tr' : 'Turco',
            'gr' : 'Grego',
            'ar' : '' },
        'fr' : {
            'it' : 'Italienne',
            'en' : 'Anglaise',
            'es' : '',
            'pt' : 'Portugaise',
            'fr' : 'Française',
            'de' : 'Allemande',
            'jp' : 'Japonaise',
            'cn' : 'Chinoise',
            'ru' : 'Russes',
            'tr' : 'Turque',
            'gr' : 'Grecs',
            'ar' : '' },
        'de' : {
            'it' : 'Italienisch',
            'en' : 'Englisch',
            'es' : '',
            'pt' : 'Portugiesisch',
            'fr' : 'Französisch',
            'de' : 'Deutsch',
            'jp' : 'Japanisch',
            'cn' : 'Chinesisch',
            'ru' : 'Russisch',
            'tr' : 'Türkisch',
            'gr' : 'Griechisch',
            'ar' : 'Arabisch' },
        'jp' : {
            'it' : 'イタリア',
            'en' : 'スペイン',
            'es' : '',
            'pt' : 'ポルトガル',
            'fr' : 'フランス',
            'de' : 'ドイツ',
            'jp' : '日本',
            'cn' : '中国',
            'ru' : 'ロシア語',
            'tr' : 'トルコ',
            'gr' : 'ギリシャ',
            'ar' : '' },
        'cn' : {
            'it' : '意大利',
            'en' : '西班牙',
            'es' : '',
            'pt' : '葡萄牙文',
            'fr' : '法国',
            'de' : '德国',
            'jp' : '日语',
            'cn' : '中国',
            'ru' : '俄罗斯',
            'tr' : '土耳其',
            'gr' : '希腊',
            'ar' : '' },
        'ru' : {
            'it' : 'итальянский',
            'en' : 'испанский',
            'es' : '',
            'pt' : 'португальский',
            'fr' : 'французский',
            'de' : 'немецкий',
            'jp' : 'японский',
            'cn' : 'китайский',
            'ru' : 'русский',
            'tr' : 'турецкий',
            'gr' : 'греческий',
            'ar' : '' },
        'tr' : {
            'it' : 'İtalyan',
            'en' : 'İngilizce',
            'es' : '',
            'pt' : 'Portekizce',
            'fr' : 'Fransız',
            'de' : 'Alman',
            'jp' : 'Japon',
            'cn' : 'Çin',
            'ru' : 'Rus',
            'tr' : 'Türk',
            'gr' : 'Yunan',
            'ar' : '' },
        'gr' : {
            'it' : 'ιταλικά',
            'en' : 'ισπανικά',
            'es' : '',
            'pt' : 'Πορτογαλικά',
            'fr' : 'γαλλικά',
            'de' : 'γερμανικά',
            'jp' : 'Ιαπωνικά',
            'cn' : 'κινέζικα',
            'ru' : 'Ρωσική',
            'tr' : 'Τουρκικά',
            'gr' : 'ελληνικά',
            'ar' : '' },
        'ar' : {
            'it' : 'إيطالي',
            'en' : 'الأسبانية',
            'es' : '',
            'pt' : 'البرتغالية',
            'fr' : 'فرنسي',
            'de' : 'ألماني',
            'jp' : 'اليابانية',
            'cn' : 'الصينية',
            'ru' : 'الروسية',
            'tr' : 'تركي',
            'gr' : 'يوناني',
            'ar' : 'العربية'
        }
    }
    
    # Insert the languages dictionaries 
    for lan in dict_languages:
        db.languages.insert( { 'code' : lan, 'value' : dict_languages[lan], 'check' : True })


def init_users():
    """ Initializes the base two users: Admin and Users """
    
    list_users = [
        {
            'username' : 'admin', 
            'password' : create_password('admin'), # Create passwords in md5 and sha1
            'rank' : 10 
        },
        {
            'username' : 'admin', 
            'password' : create_password('user'), 
            'rank' : 10 
        }
    ]
    
    # Insert the users list 
    for user in list_users:
        db.users.insert( user )
   
def init_hash_table():
    """ Initialize a document for each module within the MongoDB
    hash_table collection, each document contains a dictionary like hash map. """
    
    dict_admin = { 
        'name' : 'admin', 
        'value': {
            'name': {
    		    'it': 'Bombolone',
    		    'en': 'Bombolone',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'title': {
    		    'it': 'Bombolone |',
    		    'en': 'Bombolone |',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'logout': {
    		    'it': 'Logout',
    		    'en': 'Logout',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'web_site': {
    		    'it': 'Sito web',
    		    'en': 'Web site',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'profile': {
    		    'it': 'Profilo',
    		    'en': 'Profile',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'save': {
    		    'it': 'Salva',
    		    'en': 'Save',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' }
        }
    }
    
    dict_languages = { 
        'name' : 'languages', 
        'value': {
            'name': {
    		    'it' : 'Lingue',
    		    'en' : 'Languages',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'title': {
    		    'it' : 'Lingue',
    		    'en' : 'Languages',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'code': {
    		    'it' : 'codice',
    		    'en' : 'code',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'language': {
    		    'it' : 'lingua',
    		    'en' : 'language',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'update_ok': {
    		    'it' : 'Salvataggio delle lingue riuscito.',
    		    'en' : 'Languages saved successfully.',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'update_no': {
    		    'it' : 'Si è verificato un errore durante il salvataggio delle lingue.',
    		    'en' : 'There was an error while saving languages.',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' }       
        }
    }
    
    dict_hash_map = { 
        'name' : 'hash_map', 
        'value': {}
    }
    
    dict_users = { 
        'name' : 'users', 
        'value': {
            'account_error_1': {
    		    'it' : 'Devi inserire l\'username',
    		    'en' : 'You must enter the username',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'account_error_2': {
    		    'it' : 'L\'username inserito deve essere almeno di due caratteri',
    			'en' : 'The username entered must be at least two characters',
    			'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'account_error_3': {
    		    'it' : u'L\'username inserito non è disponibile',
    			'en' : 'The entered username is not available',
    			'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'account_error_4': {
    		    'it' : u'L\'username inserito non è disponibile',
    			'en' : 'The entered username is not available',
    			'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'account_error_5': {
    		    'it' : u'Il formato dell\'email non è corretto',
    			'en' : 'The format of the email is incorrect',
    			'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'account_error_6': {
    		    'it' : u'L\'email scritta è già utilizzata da un altro account',
    		    'en' : 'The email written is already used by another account',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'account_error_7': {
    		    'it' : u'L\'username deve essere alfanumerico senza spazi',
    		    'en' : u'The username must be alphanumeric with no spaces',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'account_ok': {
    		    'it' : 'Account modificato correttamente',
    		    'en' : 'Account changed successfully',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'password_error_1': {
    		    'it' : 'La nuova password inserita deve essere almeno di 6 caratteri',
    			'en' : 'The new password entered must be at least 6 characters',
    			'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'password_error_2': {
    		    'it' : 'Le nuove password inserite non sono uguali',
    			'en' : 'The new passwords entered do not match',
    			'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : ''
            }
        }
    }
    
    dict_pages = { 
        'name' : 'pages', 
        'value': {}
    }
    
    dict_login = { 
        'name' : 'login', 
        'value': {
            'error_1' : {
                'it' : 'errore 1',
                'en' : 'error 1',
                'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : ''
            },
            'error_2' : {
                'it' : 'errore 2',
                'en' : 'error 2',
                'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : ''      
            }
        }
    }
    
    # Insert 
    db.hash_table.insert( dict_admin )
    db.hash_table.insert( dict_languages )
    db.hash_table.insert( dict_hash_map )
    db.hash_table.insert( dict_users )
    db.hash_table.insert( dict_pages )
    db.hash_table.insert( dict_login )
    
    
def init_pages():
    """ fixtures MongoDB """   
    for num in range(1,6):
        page = {
            'name' : 'page_'+str(num),
            'file' : 'page_'+str(num),
            'title': {
                'en' : 'Title '+str(num),
                'it' : 'Titolo '+str(num)
            },
            'description': {
                'en' : 'Description '+str(num),
                'it' : 'Descrizione '+str(num)
            },
            'url': {
                'en' : 'page_'+str(num),
                'it' : 'pagina_'+str(num)
            },
            'content' : {
                'en' : [
                    { 'label' : 'label_1' , 'alias' : 'Label 1', 'value' : '1', 'type' : 0 },
                    { 'label' : 'label_2' , 'alias' : 'Label 2', 'value' : '2', 'type' : 0 },
                    { 'label' : 'label_3' , 'alias' : 'Label 3', 'value' : '3', 'type' : 0 },
                    { 'label' : 'label_4' , 'alias' : 'Label 4', 'value' : '4', 'type' : 0 },
                    { 'label' : 'label_5' , 'alias' : 'Label 5', 'value' : '5', 'type' : 0 }],
                'it' : [
                    { 'label' : 'label_1' , 'alias' : 'Campo 1', 'value' : '1', 'type' : 0 },
                    { 'label' : 'label_2' , 'alias' : 'Campo 2', 'value' : '2', 'type' : 0 },
                    { 'label' : 'label_3' , 'alias' : 'Campo 3', 'value' : '3', 'type' : 0 },
                    { 'label' : 'label_4' , 'alias' : 'Campo 4', 'value' : '4', 'type' : 0 },
                    { 'label' : 'label_5' , 'alias' : 'Campo 5', 'value' : '5', 'type' : 0 }]
            },
            'input_label': [ 1, 1, 1, 1, 1 ]
        }

        if num == 1:
            page['name'] = 'home_page'
            page['file'] = 'home'
            page['title'] = { 'en' : 'Home Page', 'it' : 'Home' }
            page['url'] = None
            db.pages.update( { 'name' : 'home_page' }, page, True)
        else:
            db.pages.update( { 'name' : 'page_'+str(num) }, page, True)
         

def init_mongodb():
    """ Initialize the database MongoDB of Bombolone. """
    init_languages()
    init_users()
    init_hash_table()
    init_pages()
        