from .settings import *

DEBUG = False

INSTALLED_APPS += ['storages']


# AWS and S3 Settings
AWS_S3_ADDRESSING_STYLE = 'virtual'
AWS_IS_GZIPPED = True
AWS_S3_SECURE_URLS = True

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

# Static and Media files configuration for S3
STATICFILES_STORAGE = 'portfolio.custom_storage.StaticStorage'
DEFAULT_FILE_STORAGE = 'portfolio.custom_storage.MediaStorage'

# This will be used when DEBUG is False
STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/' if not DEBUG else '/static/'
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'

# Disable django-heroku's static files handling
django_heroku.settings(locals(), staticfiles=False)