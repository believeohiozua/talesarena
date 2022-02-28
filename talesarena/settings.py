import os
from decouple import config
import django_heroku
import dj_database_url
import psycopg2
from djangoeditorwidgets.config import *



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!


DEBUG=config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ["www.talesarena.com", "127.0.0.1", "talesarena.herokuapp.com", "localhost"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tales.apps.TalesConfig',
    'services.apps.ServicesConfig',
    'adverts.apps.AdvertsConfig',      
    'tinymce',
    # 'filebrowser',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'bootstrap_pagination',
    'django_social_share',
    'social_django',
    'storages',   
    'djangosecure',
    'favicon',
    "sslserver",    
#     'sorl.thumbnail',
#    'easy_thumbnails',
    # 'image_cropping',  
    # 'filer',
    # 'mptt', 
    'widget_tweaks',  
    'crispy_forms', 
    'djangoeditorwidgets',
] 



AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',    
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
    "allauth.account.auth_backends.AuthenticationBackend",

]



# THUMBNAIL_PROCESSORS = (
#     'image_cropping.thumbnail_processors.crop_corners',
# ) + thumbnail_settings.THUMBNAIL_PROCESSORS
# # size is "width x height"
# IMAGE_CROPPING_THUMB_SIZE = (500, 500)
# THUMBNAIL_HIGH_RESOLUTION = True
# IMAGE_CROPPING_BACKEND = 'image_cropping.backends.easy_thumbs.EasyThumbnailsBackend'
# IMAGE_CROPPING_BACKEND_PARAMS = {}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    
]
# SECURE_SSL_REDIRECT=True
# SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https") #or None
# SESSION_COOKIE_SECURE=True
# CSRF_COOKIE_SECURE=True
# SECURE_HSTS_SECONDS=None
# SECURE_HSTS_INCLUDE_SUBDOMAINS=True
# SECURE_FRAME_DENY=True
# CORS_REPLACE_HTTPS_REFERER      = False
# HOST_SCHEME                     = "http://"





ROOT_URLCONF = 'talesarena.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'talesarena.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True




SITE_ID = 1
LOGIN_URL='/account/login/'
LOGIN_REDIRECT_URL='/'
ACCOUNT_AUTHENTICATION_METHOD="username_email"
ACOUNT_CONFIRM_EMAIL_ON_GET=False
ACOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL=LOGIN_URL
ACOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL='/'
ACOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=3
ACOUNT_EMAIL_REQUIRED=True
ACOUNT_EMAIL_VERIFIATION="optional"
ACOUNT_EMAIL_SUBJECT_PREFIX="[Site]"
ACOUNT_DEFAULT_HTTP_PROTOCOL="http"
ACOUNT_LOGOUT_ON_GET=False
ACOUNT_LOGOUT_REDIRECT_URL="/"
ACOUNT_SIGNUP_FORM_CLASS= None
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION=True
ACCOUNT_UNIQUE_EMAIL=True
ACOUNT_USER_MODEL_USERNAME_FIELD="username"
ACOUNT_USER_MODEL_EMAIL_FIELD="email"
ACOUNT_USERNAME_MIN_LENGTH=5
ACOUNT_USERNAME_BLACKLIST=['Ehaioleudu']
ACOUNT_USERNAME_REQUIRED=True
ACOUNT_PASSWORD_INPUT_RENDER_VALUE=True
ACOUNT_PASSWORD_MIN_LENGTH=6
ACOUNT_LOGIN_ON_EMAIL_CONFIRMATION=True
ACOUNT_LOGIN_ON_EMAIL_CONFIRMATION=True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED =True
# ACCOUNT_SESSION_REMEMBER =True comment this out so it can show Remember me field
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30 # One month
ACCOUNT_FORMS = {
'signup': 'tales.forms.CustomSignupForm',
}

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
    }



SOCIAL_AUTH_GOOGLE_OAUTH2_KEY= config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY') 
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET= config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET') 

MAILCHIMP_API_KEY = ''
MAILCHIMP_DATA_CENTER = ''
MAILCHIMP_EMAIL_LIST_ID = ''


if DEBUG == False:  
    EMAIL_USE_TLS =True
    EMAIL_HOST = 'smtp.mailgun.org'
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587
    SERVER_EMAIL = EMAIL_HOST_USER
    DEFAULT_FROM_EMAIL ='info@talesarena.com'

    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID') 
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY') 
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')  
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    CRISPY_TEMPLATE_PACK = 'bootstrap4'

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = '/static/'
    FAVICON_PATH = STATIC_URL + 'images/badge.png'

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'   
    django_heroku.settings(locals(), staticfiles=False)
else:    
    EMAIL_HOST = 'smtp.gmail.com'    
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    STATICFILES_DIRS = [os.path.join(BASE_DIR,'staticfiles')]
    VENV_PATH = os.path.dirname(BASE_DIR)

    STATIC_ROOT = os.path.join(VENV_PATH,'static_root')   
    STATIC_URL = '/static/'

    MEDIA_ROOT = os.path.join(VENV_PATH, 'media')
    MEDIA_URL = '/media/' 
    CRISPY_TEMPLATE_PACK = 'bootstrap4'

DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True