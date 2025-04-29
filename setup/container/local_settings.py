from os.path import abspath, dirname, join

SITE_ROOT = dirname(dirname(dirname(abspath(__file__))))
STATIC_ROOT = '/veyepar/static/'
STATIC_URL = "/static/"
ADMIN_MEDIA_PREFIX = join(STATIC_URL, "admin/")

ALLOWED_HOSTS = [
    '*',
    ]
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    ]

DATABASES =  {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "veyepar",
        "USER": "veyepar",
        "PASSWORD": "veyepar",
        "HOST": "db",
        "PORT": "5432",
    }
}

UPLOAD_FORMATS = ['mp4', 'webm']

GOOG_CLIENT_SECRET = "/veyepar/config/client_secret.json"
GOOG_TOKEN = ""
GOOG_SCOPES = ""
GOOG_REDIRECT_URL = ""