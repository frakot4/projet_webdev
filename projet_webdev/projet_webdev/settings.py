import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# On charge le fichier .env créé par Dokploy au moment du build
load_dotenv(BASE_DIR.parent / '.env')


# --- CONFIGURATION DÉPLOIEMENT (SÉCURISÉE) ---

# On récupère la SECRET_KEY depuis Dokploy, sinon clé de secours
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-3yg!m&*g6@jys#essj@1rklz)^-e7c$h5i*3g)l4s-7d^gfyy%')

# DEBUG lit la variable 'False' de Dokploy
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# On récupère les domaines autorisés configurés dans Dokploy
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Indispensable pour autoriser la connexion admin en HTTPS derrière Dokploy
CSRF_TRUSTED_ORIGINS = ['https://rakotomavofanatitra.dev']


# --- APPLICATION DEFINITION ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # Gère les fichiers statiques en prod
    'django.contrib.staticfiles',
    'internship_projet',
    'internship_projet_comptes', 
    'internship_projet_gestion_profs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Indispensable pour le CSS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projet_webdev.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'projet_webdev.wsgi.application'


# --- DATABASE (SQLite + PVC Dokploy) ---

# 1. On définit un dossier 'data' à la racine du projet
DATA_DIR = BASE_DIR / 'data'

# 2. On demande à Python de créer ce dossier s'il n'existe pas encore
os.makedirs(DATA_DIR, exist_ok=True)

# 3. On range le fichier SQLite à l'intérieur
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATA_DIR / 'db.sqlite3',
    }
}


# --- PASSWORD VALIDATION ---

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- INTERNATIONALIZATION ---

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- STATIC FILES (CSS, JavaScript, Images) ---

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- MEDIA FILES (Images uploadées) ---

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- REDIRECTIONS ---

LOGIN_REDIRECT_URL = 'dispatch_login' 
LOGOUT_REDIRECT_URL = 'login'