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


def clean_database(all_item=1):
    """ Removes all the collections in the database. """
    
    if int(all_item):
        db.users.remove()
        
    db.languages.remove()
    db.hash_table.remove()
    db.pages.remove()
    
    
def init_mongodb(all_item=1):
    """ Initialize the database MongoDB of Bombolone. """

    if int(all_item):
        init_users()

    init_languages()
    init_hash_table()
    init_pages()


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
                'email' : '',
             'password' : create_password('admin'), # Create passwords in md5 and sha1
                 'rank' : 10,
             'language' : 'English',
                  'lan' : 'en',
            'time_zone' : 'Europe/London',
                'image' : '',
                 'name' : '',
          'description' : '',
             'location' : '',
                  'web' : ''
        },
        {
             'username' : 'user', 
                'email' : '',
             'password' : create_password('user'), 
                 'rank' : 20,
             'language' : 'English',
                  'lan' : 'en',
            'time_zone' : 'Europe/London',
                'image' : '',
                 'name' : '',
          'description' : '',
             'location' : '',
                  'web' : ''
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
        'module' : True, 
        'value': {
            'name': {
    		    'it' : 'Bombolone',
    		    'en' : 'Bombolone',
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
    		    'it' : 'Bombolone |',
    		    'en' : 'Bombolone |',
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
    		    'it' : 'Logout',
    		    'en' : 'Logout',
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
    		    'it' : 'Sito web',
    		    'en' : 'Web site',
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
    		    'it' : 'Profilo',
    		    'en' : 'Profile',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'settings': {
    		    'it' : 'Impostazioni',
    		    'en' : 'Settings',
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
                'ar' : '' },
            'name_val': {
    		    'it': 'Nome',
    		    'en': 'Name',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'number': {
    		    'it': 'Numero',
    		    'en': 'Number',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'remove': {
    		    'it': 'Rimuovi',
    		    'en': 'Remove',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'remove_item': {
    		    'it': 'Rimuovi elemento',
    		    'en': 'Remove item',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'add_field': {
    		    'it': '+ Aggiungi campo',
    		    'en': '+ Add field',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'remove_field': {
    		    'it': '- Rimuovi campo',
    		    'en': '- Remove field',
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
        'module' : True, 
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
    
    dict_hash_table = { 
        'name' : 'hash_table',
        'module' : True,  
        'value': {
            'name': {
    		    'it' : 'Hash Table',
    		    'en' : 'Hash Table',
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
    		    'it' : 'Hash Table',
    		    'en' : 'Hash Table',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'add_new_hash_map': {
    		    'it' : 'Aggiungi nuova hash map',
    		    'en' : 'Add new hash map',
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
    
    dict_users = { 
        'name' : 'users', 
        'module' : True, 
        'value': {
            'name': {
    		    'it' : 'Utenti',
    		    'en' : 'Users',
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
    		    'it' : 'Amministrazione utenti',
    		    'en' : 'Admin users',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'descritpion': {
    		    'it' : '',
    		    'en' : ' ',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'rank' : {
    		    'it' : 'Rango',
    		    'en' : 'Rank',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'language' : {
    		    'it' : 'Lingua',
    		    'en' : 'Language',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'time_zone' : {
    		    'it' : 'Fuso orario',
    		    'en' : 'Time zone',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'time_zone_end_1' : {
    		    'it' : u'Fine fuso orario USA & Canada',
    		    'en' : u'End Time Zone Usa & Canada',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'picture' : {
    		    'it' : 'Immagine',
    		    'en' : 'Picture',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },   
            'setting_name' : {
    		    'it' : 'Nome',
    		    'en' : 'Name',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },       
            'location' : {
    		    'it' : 'Posizione',
    		    'en' : 'Location',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },  
            'web' : {
    		    'it' : 'Web',
    		    'en' : 'Web',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'description' : {
    		    'it' : 'Descrizione',
    		    'en' : 'Description',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'check_password' : {
    		    'it' : 'Verifica password',
    		    'en' : 'Check password',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'add_user': {
    		    'it' : 'Aggiungi utente',
    		    'en' : 'Add user',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'create_user': {
    		    'it' : 'Crea utente',
    		    'en' : 'Create user',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
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
                'ar' : ''},
            'regex_full_name': {
				'it' : 'Il nome deve essere composto da sole lettere e spazi.',
				'en' : 'The name must consist of only letters and spaces.',
                'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : ''},
	        'regex_url': {
				'it' : u'L\'url inserito non è scritto correttamente',
				'en' : u'The url you entered is spelled incorrectly',
                'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : ''}
        }
    }
    
    dict_pages = { 
        'name' : 'pages', 
        'module' : True, 
        'value': {
            'name': {
    		    'it' : 'Pagine',
    		    'en' : 'Pages',
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
    		    'it' : 'Amministrazione pagine',
    		    'en' : 'Admin pages',
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
    
    dict_login = { 
        'name' : 'login', 
        'module' : True, 
        'value': {
            'name': {
    		    'it' : 'Utenti',
    		    'en' : 'Users',
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
    		    'it' : 'Amministrazione utenti',
    		    'en' : 'Admin users',
    		    'pt' : '',
                'fr' : '',
                'de' : '',
                'jp' : '',
                'cn' : '',
                'ru' : '',
                'tr' : '',
                'gr' : '',
                'ar' : '' },
            'error_1' : {
                'it' : 'Devi completare tutti i campi',
                'en' : 'You must complete every field',
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
                'it' : u'L\'username o l\'email è errata',
                'en' : 'Wrong Username/Email and password combination.',
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
            'send': {
				'it': 'Email inviata al tuo indirizzo di posta',
				'en': 'Email sent to your email address',
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
    db.hash_table.insert( dict_hash_table )
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
         