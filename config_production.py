import os

# Debug True/False
DEBUG = False

# Database connection
DATABASE = 'bombolone'

# ~
ENV = "prod"

# ~
PATH = 'http://www.bombolone.com'

# ~
PATH_API = 'http://www.bombolone.com'

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

# ~
JS_FILES_STEP_ONE = ['https://ajax.googleapis.com/ajax/libs/angularjs/1.2.13/angular.min.js',
                     'https://ajax.googleapis.com/ajax/libs/angularjs/1.2.13/angular-route.min.js']

# ~
JS_FILES_STEP_TWO = ['https://ajax.googleapis.com/ajax/libs/angularjs/1.2.13/angular-resource.min.js',
                     '/static/js/lib/angular-ui.min.js']

# ~
CSS_FONT_AWESOME = 'https://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css'
