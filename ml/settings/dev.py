from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q%@4+a_(vdw^ap_c*sbnu76aydeutxf%l7rm!nydo4@7-8*75s'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

LOCAL_ENV = None

if 'EMAIL_BACKEND' in os.environ:
    EMAIL_BACKEND = os.environ['EMAIL_BACKEND']
    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    SERVER_EMAIL = EMAIL_HOST_USER
    DEFAULT_CONTACT_US_EMAIL = EMAIL_HOST_USER

try:
    from .local import *
except ImportError:
    pass
