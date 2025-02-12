from .base import *

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOST', default=[])

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

INSTALLED_APPS += [
    'storages',
]

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_VERIFY = True
AWS_QUERYSTRING_AUTH = False

django_heroku.settings(locals()) 
