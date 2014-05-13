import os

# Debug True/False
DEBUG = True

# Database connection
DATABASE = 'bombolone'

# ~
ENV = "home"

# ~
PATH = 'http://0.0.0.0:5000'

# ~
PATH_API = 'http://0.0.0.0:5000/api/1.0'

# ~
PATH_LAYOUT = 'http://0.0.0.0:5000/static/layout/'

# ~
PROJECT_DIR = os.path.dirname(__file__)

# ~
STATIC = os.path.join(PROJECT_DIR,'./static')

# ~
TEMPLATES = os.path.join(PROJECT_DIR,'./templates')

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
SECRET_KEY = 'secret_key'

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

# activate user status
ACTIVATED = 1

# not activate user status
NOTACTIVATED = 0

# List js local files
JS_FILES_STEP_ONE = ['/static/js/lib/angular.min.js',
                     '/static/js/lib/angular-route.min.js']

# List js local files
JS_FILES_STEP_TWO = ['/static/js/lib/angular-resource.min.js',
                     '/static/js/lib/angular-ui.min.js']

# ~
CSS_FONT_AWESOME = '/static/css/font-awesome/font-awesome.min.css'
