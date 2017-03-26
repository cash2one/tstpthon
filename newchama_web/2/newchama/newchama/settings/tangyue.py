# -*- coding: utf-8 -*-

from newchama.settings.base import *

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'test',
#        'HOST': 'localhost',
#        'USER': 'root',
#        'PASSWORD': '',
#        'PORT': '3306',
#    }
#}

DOMAIN = 'http://127.0.0.1:8000/'
#COMPRESS_ENABLED = True
#COMPRESS_OFFLINE = True

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'sass --scss --compass --sourcemap=none {infile} {outfile}'),
)

ADMINS = (
    ('tangyue', 'tangyue@newchama.com'),
)

TEST_EMAIL = 'tangyue@newchama.com'
