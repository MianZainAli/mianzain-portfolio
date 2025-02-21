from .base import *

import dj_database_url
import django_heroku

DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS',default=[''])
CSRF_TRUSTED_ORIGINS = [
    f'http://{host}' for host in ALLOWED_HOSTS if host
] + [
    f'https://{host}' for host in ALLOWED_HOSTS if host
]


DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# AWS SETTINGS
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')

# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# AWS_DEFAULT_ACL = 'public-read'
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }

# AWS_LOCATION = 'static'

# AWS_QUERYSTRING_AUTH = False
# AWS_HEADERS = {
#     'Access-Control-Allow-Origin': '*'
# }

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

django_heroku.settings(locals(), staticfiles=False)