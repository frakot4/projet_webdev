import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURATION DÉPLOIEMENT (DOKPLOY) ---

# On récupère la SECRET_KEY depuis Dokploy, sinon on utilise une clé de secours locale
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-iyfpw$qiurz&7gwczv+t1x72dcl+3p#6e5n+=w+!y2!&41qzvt')

# DEBUG est True sur ton PC, mais devient False sur le serveur (via la variable DEBUG dans Dokploy)
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# On récupère les domaines autorisés (IP + Nom de domaine) configurés dans Dokploy
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# --- APPLICATION DEFINITION ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # Ajouté pour gérer les fichiers statiques (CSS/JS)
    'django.contrib.staticfiles',
    'internship_projet',
    'internship_projet_comptes', 
    'internship_projet_gestion_profs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Ajouté : Indispensable pour le CSS en production
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


# --- DATABASE ---
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

# Dossier où Django va rassembler tous les fichiers statiques pour la production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuration WhiteNoise pour servir les fichiers compressés (plus rapide)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- MEDIA FILES (Images uploadées) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- REDIRECTIONS ---
LOGIN_REDIRECT_URL = 'dispatch_login' 
LOGOUT_REDIRECT_URL = 'login'
