import os

# Debug True/False
DEBUG = True

# Title of this weblog instance
TITLE = 'Bombolone'

# Description of this weblog instance
DESCRIPTION = 'Bombolone description'

# Database connection
DATABASE = 'bombolone'

# ~
ENV = "home"

# ~
PATH = 'http://0.0.0.0:5000'

# ~
PATH_API = 'http://0.0.0.0:5000/api'

# ~
PATH_LAYOUT = 'http://0.0.0.0:5000/static/layout/'

# ~
PROJECT_DIR = os.path.dirname(__file__)

# ~
STATIC = os.path.join(PROJECT_DIR,'./static')

# ~
TEMPLATES = os.path.join(PROJECT_DIR,'./templates')

# ~
STATIC_FOLDER = os.path.join(PROJECT_DIR,'./static')

# ~
PROJECT_STATIC_FILES = 'data/upload'

# ~
UP_FOLDER = os.path.join(PROJECT_DIR,'../{}/'.format(PROJECT_STATIC_FILES))

# ~
UP_AVATARS_FOLDER = os.path.join(PROJECT_DIR,'../{}/avatars/'.format(PROJECT_STATIC_FILES))

# ~
UP_AVATARS_TMP_FOLDER = os.path.join(PROJECT_DIR,'../{}/avatars/tmp/'.format(PROJECT_STATIC_FILES))

# ~
UP_IMAGE_FOLDER = os.path.join(PROJECT_DIR,'../{}/images/'.format(PROJECT_STATIC_FILES))

# ~
UP_IMAGE_TMP_FOLDER = os.path.join(PROJECT_DIR,'../{}/images/tmp/'.format(PROJECT_STATIC_FILES))

# ~
PORT = 5000

# ~
SECRET_KEY = '\x9e\xec\x91\x0e\xa4\x00\xbb\x199\t\xe1\xe3\xd2\xa7\xb4\xf7\tP_\x9e\x8f\xf4\x06\x08'

# ~
PORT_DATABASE = None

# ~
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# ~
ALLOWED_ALL_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# ~
EXTENSIONS = {'png' : 'PNG', 'jpg' : 'JPEG', 'jpeg' : 'JPEG', 'gif' : 'GIF'}

# ~
EXTENSIONS_REQUEST = {'png', 'jpg', 'jpeg', 'gif', 'css', 'js'}

# ~
LIST_LANGUAGES = ['ar','cn','de','en','es','fr','gr','it','jp','pt','ru','tr']

# List js local files
JS_FILES = ['/static/js/lib/angular.min.js', '/static/js/lib/angular-resource.min.js', '/static/js/lib/jquery.min.js']

