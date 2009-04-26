# -*- coding: utf-8 -*-
from ragendja.settings_pre import *
from django.contrib.auth.models import User

# Increase this when you update your media on the production site, so users
# don't have to refresh their cache. By setting this your MEDIA_URL
# automatically becomes /media/MEDIA_VERSION/
MEDIA_VERSION = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = '234879034'

#ENABLE_PROFILER = True
#ONLY_FORCED_PROFILE = True
#PROFILE_PERCENTAGE = 25
#SORT_PROFILE_RESULTS_BY = 'cumulative' # default is 'time'
#PROFILE_PATTERN = 'ext.db..+\((?:get|get_by_key_name|fetch|count|put)\)'

# Enable I18N and set default language to 'en'
USE_I18N = True
LANGUAGE_CODE = 'en'

#Restrict supported languages (and JS media generation)
#LANGUAGES = (
#    ('de', 'German'),
#    ('en', 'English'),
#)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # Django authentication
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	
    # Google authentication
    #'ragendja.auth.middleware.GoogleAuthenticationMiddleware',
    
    # Hybrid Django/Google authentication
    #'ragendja.auth.middleware.HybridAuthenticationMiddleware',
    
    'django.middleware.locale.LocaleMiddleware',
    'ragendja.sites.dynamicsite.DynamicSiteIDMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

# Google authentication
#AUTH_USER_MODULE = 'ragendja.auth.google_models'
#AUTH_ADMIN_MODULE = 'ragendja.auth.google_admin'
# Hybrid Django/Google authentication
#AUTH_USER_MODULE = 'ragendja.auth.hybrid_models'
# Django authentication
AUTH_USER_MODULE = 'delvicious.models' 

GLOBALTAGS = (
	# Add google_login_url and google_logout_url tags
	'ragendja.templatetags.googletags',

    'ragendja.templatetags.ragendjatags',
    'django.templatetags.i18n',
)

#LOGIN_URL = '/account/login/'
LOGIN_URL = '/delvicious/login'
#LOGOUT_URL = '/account/logout/'
LOGOUT_URL = '/delvicious/logout/'
LOGIN_REDIRECT_URL = '/delvicious/add_delicious_account'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.webdesign',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'django.contrib.sites',
    'appenginepatcher',
    'registration',
    'mediautils',
    'delvicious',
)

# List apps which should be left out from app settings and urlsauto loading
IGNORE_APP_SETTINGS = IGNORE_APP_URLSAUTO = (
    # Example:
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'yetanotherapp',
)

# 
# import os
# ROOT_PATH = os.path.dirname(__file__)
# TEMPLATE_DIRS = (
#     # Put strings here, like "/home/html/django_templates" or
#     # "C:/www/django/templates".  Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.
#     ROOT_PATH + '/templates',
# )


from ragendja.settings_post import *
