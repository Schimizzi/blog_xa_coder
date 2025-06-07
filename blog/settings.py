<<<<<<< HEAD


=======
>>>>>>> dev
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


<<<<<<< HEAD
SECRET_KEY = 'django-insecure-your-secret-key-here!' 


DEBUG = True 

ALLOWED_HOSTS = [
]

=======

SECRET_KEY = 'django-xp-coder'

DEBUG = True 

ALLOWED_HOSTS = []
>>>>>>> dev



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
<<<<<<< HEAD
    'ckeditor_uploader', 
=======
    'ckeditor_uploader',
>>>>>>> dev
    'blog_app.apps.BlogAppConfig',
    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'

<<<<<<< HEAD
=======

>>>>>>> dev
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3', 
    }
}


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


<<<<<<< HEAD
LANGUAGE_CODE = 'es-ar' 
=======

LANGUAGE_CODE = 'es-ar'
>>>>>>> dev

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
<<<<<<< HEAD
=======

>>>>>>> dev
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'blog:home' 
LOGOUT_REDIRECT_URL = 'blog:home' 

<<<<<<< HEAD

CKEDITOR_UPLOAD_PATH = "uploads/" 
CKEDITOR_IMAGE_BACKEND = "pillow" 
=======
CKEDITOR_UPLOAD_PATH = "uploads/" 
CKEDITOR_IMAGE_BACKEND = "pillow"
>>>>>>> dev
CKEDITOR_ALLOW_NONIMAGE_FILES = False 

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom', 
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar'],
            '/',
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks'],
            ['Source'], 
        ],
        'height': 300,
<<<<<<< HEAD
        'width': '100%', 
=======
        'width': '100%',
       
>>>>>>> dev
    },
}

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
