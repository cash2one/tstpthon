# -*- coding: utf-8 -*-

from newchama.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get("DB_STAGE_NAME", ''),
        'HOST': 'rdsyjvqqiyjvqqi.mysql.rds.aliyuncs.com',
        'USER': os.environ.get("DB_STAGE_USR", ''),
        'PASSWORD': os.environ.get("DB_STAGE_PWD", ''),
        'PORT': '3306',
    }
}

IS_PRODUCT_HOST=True
DEBUG = False
TEMPLATE_DEBUG = False

DOMAIN = 'http://stagingcms.newchama.com/'
MEDIA_ROOT = "/var/www/newchama_media"
