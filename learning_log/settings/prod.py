from .base import *
import os
from decouple import config

DEBUG = False

ADMIN = config('ADMIN').split(',')

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')


DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME_PROD'),
        'USER': config('DB_USER_PROD'),
        'PASSWORD': config('DB_PASSWORD_PROD'),
        'HOST': config('DB_HOST_PROD'),
        'PORT': config('DB_PORT_PROD'),
    }
}


AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = config('AWS_S3_FILE_OVERWRITE')
# AWS_DEFAULT_ACL = config('AWS_DEFAULT_ACL')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')

STATICFILES_STORAGE = config('STATICFILES_STORAGE')
DEFAULT_FILE_STORAGE = config('DEFAULT_FILE_STORAGE')
AWS_S3_CUSTOM_DOMAIN_MEDIA = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN_MEDIA}/media/'

