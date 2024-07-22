from .base import *


DEBUG = True
ALLOWED_HOSTS = ['localhost','recipe-api-pyjamahr-1.onrender.com']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
