# -*- coding: utf-8 -*- 
"""
Django settings for newchama project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

NUM=1
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yu%a%*c@hp&_*yavx3g9&^kly4aad#do=+)rl-@fangh+fio-0'
SECRET_SALT = 'newchama'
# SECURITY WARNING: don't run with debug turned on in production!
#APPEND_SLASH=True
DEBUG = True
IS_PRODUCT_HOST=False


ALLOWED_HOSTS = [
    '.newchama.com', # Allow domain and subdomains
    '.newchama.com.', # Also allow FQDN and subdomains
  #  '127.0.0.1'
  #  '172.16.0.73'
]

TEMPLATE_DEBUG = True

#ALLOWED_HOSTS = ['localhost']

#SESSION_SAVE_EVERY_REQUEST=True

# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'home',
    'account',
    'purchase',
    'sales',
    'pagination',
    'services',
    'news',
    'deal',
    'api',
    'rest_framework',
   # 'corsheaders',
    'subscribe',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'PAGE_SIZE': 10
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'newchama.middleware.LangChoiceMiddleware',
    'pagination.middleware.PaginationMiddleware',
    #'corsheaders.middleware.CorsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    'django.contrib.messages.context_processors.messages',
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qiye.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'newchama@newchama.com'
EMAIL_HOST_PASSWORD = 'newchama@2015'
EMAIL_USE_TLS = False
EMAIL_CVSOURCE = 'newchama@newchama.com'


ROOT_URLCONF = 'newchama.urls'

WSGI_APPLICATION = 'newchama.wsgi.application'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

#from django.contrib.messages import constants as message_constants

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {messages.DEBUG: 'alert-debug',
messages.INFO: 'alert-info',
messages.SUCCESS: 'alert-success',
messages.WARNING: 'alert-warning',
messages.ERROR: 'alert-danger',}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    # 'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newchama',
        'HOST': 'newchama.mysql.rds.aliyuncs.com',
        'USER': 'newchama',
        'PASSWORD': 'newchama1234',
        'PORT': '3306',
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

LANGUAGE_COOKIE_NAME = 'language'
CHINESE_STRING='zh-cn'
ENGLISH_STRING='zh-cn'
#ENGLISH_STRING='en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

#MEDIA_ROOT = os.path.join( BASE_DIR ,'media').replace('\\','/')
MEDIA_ROOT = "/var/www/newchama_media"
MEDIA_URL = '/media/' 

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static/').replace('\\','/'), 
)

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1',
    '192.168.3.18'
)
CORS_ALLOW_CREDENTIALS = True

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
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logs/','all.log'), #或者直接写路径：'c:\logs\all.log',
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
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logs/','request.log'), #或者直接写路径：'filename':'c:\logs\request.log''  
            'maxBytes': 1024*1024*10, # 10 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'scprits_handler': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logs/','script.log'), #或者直接写路径：'filename':'c:\logs\script.log'
            'maxBytes': 1024*1024*10, # 10 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default','console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'api.views':{
            'handlers': ['default','console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'account.views':{
            'handlers': ['default','console'],
            'level': 'ERROR',
            'propagate': True         
        },
       'sales.views':{
            'handlers': ['default','console'],
            'level': 'ERROR',
            'propagate': True
        },
        'purchase.views':{
                'handlers': ['default','console'],
                'level': 'DEBUG',
                'propagate': True
        },
        'news.views':{
                'handlers': ['default','console'],
                'level': 'ERROR',
                'propagate': True
        },
        'deal.views':{
                'handlers': ['default','console'],
                'level': 'ERROR',
                'propagate': True
        },
        'newchama.helper':{
                'handlers': ['default','console'],
                'level': 'ERROR',
                'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'ERROR',
            'propagate': False
        },
        'scripts': { # 脚本专用日志
            'handlers': ['scprits_handler'],
            'level': 'ERROR',
            'propagate': False
        },
        'subscribe.views':{
                'handlers': ['default','console'],
                'level': 'ERROR',
                'propagate': True
        },
        'other_login.views':{
                'handlers': ['default','console'],
                'level': 'ERROR',
                'propagate': True
        },
    }
}          
