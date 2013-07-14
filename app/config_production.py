import os

# Debug True/False
DEBUG = False

# Title of this weblog instance
TITLE = 'Bombolone'

# Description of this weblog instance
DESCRIPTION = 'Bombolone description'

# Database connection
DATABASE = 'bombolone'

# ~
ENV = "prod"

# ~
PATH = 'http://www.bombolone.com'

# ~
PATH_LAYOUT = 'http://www.bombolone.com/static/layout/'

# ~
PROJECT_DIR = os.path.dirname(__file__)

# ~
PROJECT_STATIC_FILES = 'data/upload'

# ~
UP_FOLDER = os.path.join(PROJECT_DIR,'../../%s/' % PROJECT_STATIC_FILES)

# ~
UP_AVATARS_FOLDER = os.path.join(PROJECT_DIR,'../../%s/avatars/' % PROJECT_STATIC_FILES)

# ~
UP_IMAGE_FOLDER = os.path.join(PROJECT_DIR,'../../%s/images/' % PROJECT_STATIC_FILES)

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
JS_FILES = ['https://ajax.googleapis.com/ajax/libs/angularjs/1.1.5/angular.min.js', 
			'https://ajax.googleapis.com/ajax/libs/angularjs/1.1.5/angular-resource.min.js',
			'//ajax.googleapis.com/ajax/libs/jquery/2.0.2/jquery.min.js']