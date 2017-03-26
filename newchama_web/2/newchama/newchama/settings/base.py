"""
Django settings for newchama project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c&55ctl=l_w^^^_$gi*7=45t2h_ki5yhwky0aa(6x)**vzz0^q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    '.newchama.com', # Allow domain and subdomains
    '.newchama.com.', # Also allow FQDN and subdomains
]

IS_PRODUCT_HOST = False

TEST_EMAIL = 'terry@newchama.com'

BD_EMAIL = 'paul@newchama.com'

# Application definition

INSTALLED_APPS = (
    'suit',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'pagination',
    'repository',
    'adminuser',
    'area',
    'industry',
    'member',
    'project',
    'demand',
    'news',
    'deal',
    'member_message',
    'log',
    'recommond',
    'tracking',
    'tools',
    'analysis',
    'alert',
    'subscribe',
    'monitor',
    )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',   #https://pypi.python.org/pypi/django-pagination
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)
#https://code.google.com/p/wadofstuff/wiki/DjangoFullSerializers
# SERIALIZATION_MODULES = {
#     'json': 'wadofstuff.django.serializers.json'
# }

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {messages.DEBUG: 'alert-debug', messages.INFO: 'alert-info', messages.SUCCESS: 'alert-success', messages.WARNING: 'alert-warning', messages.ERROR: 'alert-danger'}

ROOT_URLCONF = 'newchama.urls'

WSGI_APPLICATION = 'newchama.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
     #   'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get("DB_TEST_NAME", ''),
        'HOST': 'newchama.mysql.rds.aliyuncs.com',
        'USER': os.environ.get("DB_TEST_USR", ''),
        'PASSWORD': os.environ.get("DB_TEST_PWD", ''),
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
#STATIC_ROOT = "/var/www/newchama_admin/newchama/static/"
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/').replace('\\', '/'),
)

#MEDIA_ROOT = os.path.join(BASE_DIR, 'upload/').replace('\\', '/')
MEDIA_ROOT = "/var/www/newchama_media"
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qiye.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'newchama@newchama.com'
EMAIL_HOST_PASSWORD = 'newchama@2015'
EMAIL_USE_TLS = False


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'DEBUG',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logsfile/','all.log'),
            'maxBytes': 1024*1024*10,
            'backupCount': 5,
            'formatter':'standard',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logsfile/','request.log'),
            'maxBytes': 1024*1024*10, # 10 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'scripts_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logsfile/','script.log'),
            'maxBytes': 1024*1024*10, # 10 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'member_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logsfile/','member.log'),
            'maxBytes': 1024*1024*10, # 10 MB
            'backupCount': 50,
            'formatter':'standard',
        },
        'project_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logsfile/','project.log'),
            'maxBytes': 1024*1024*10, # 10 MB
            'backupCount': 50,
            'formatter':'standard',
        },
        'demand_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logsfile/','demand.log'),
            'maxBytes': 1024*1024*10, # 10 MB
            'backupCount': 50,
            'formatter':'standard',
        },
        'email_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logsfile/','email.log'),
            'maxBytes': 1024*1024*10, # 10 MB
            'backupCount': 50,
            'formatter':'standard',
        },
        'monitor_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logsfile/','monitor.log'),
            'maxBytes': 1024*1024*10, # 10 MB
            'backupCount': 50,
            'formatter':'standard',
        },
    },
    'loggers': {
         'django': {
             'handlers': ['default','console'],
             'level': 'DEBUG',
             'propagate': True
         },
         'email': {
             'handlers': ['email_handler'],
             'level': 'DEBUG',
             'propagate': True
         },

         'member.views':{
             'handlers': ['member_handler'],
             'level': 'DEBUG',
             'propagate': True
         },
         'project.views':{
             'handlers': ['project_handler'],
             'level': 'DEBUG',
             'propagate': True
         },
         'demand.views':{
             'handlers': ['demand_handler'],
             'level': 'DEBUG',
             'propagate': True
         },
         'django.request': {
             'handlers': ['request_handler'],
             'level': 'DEBUG',
             'propagate': False
         },
         'scripts': { #
             'handlers': ['scripts_handler'],
             'level': 'DEBUG',
             'propagate': False
         },
         'monitor.views': {
             'handlers': ['monitor_handler'],
             'level': 'DEBUG',
             'propagate': True
         },
    }
}

DOMAIN = 'http://test.newchama.com/'
