# import os
# from pathlib import Path
# import dj_database_url
# from decouple import config

# # ----------------------------- 
# # Base Directory
# # ----------------------------- 
# BASE_DIR = Path(__file__).resolve().parent.parent

# # ----------------------------- 
# # Security
# # ----------------------------- 
# SECRET_KEY = config("SECRET_KEY", default="fallback-secret-key-change-in-production")
# DEBUG = config("DEBUG", default=False, cast=bool)

# ALLOWED_HOSTS = config(
#     "ALLOWED_HOSTS", 
#     default="localhost,127.0.0.1,.onrender.com,.herokuapp.com,.railway.app", 
#     cast=lambda x: [host.strip() for host in x.split(',')]
# )

# # ----------------------------- 
# # Applications
# # ----------------------------- 
# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth", 
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     "portfolio",  # Your portfolio app
# ]

# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "whitenoise.middleware.WhiteNoiseMiddleware",  # For static files in production
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware", 
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "sartaj_portfolio.urls"

# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [BASE_DIR / "templates"],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.debug",
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = "sartaj_portfolio.wsgi.application"

# # ----------------------------- 
# # Database Configuration
# # ----------------------------- 
# DATABASE_URL = config("DATABASE_URL", default=None)

# if DATABASE_URL:
#     # PostgreSQL (Render/Production)
#     DATABASES = {
#         "default": dj_database_url.config(
#             default=DATABASE_URL,
#             conn_max_age=600,
#             conn_health_checks=True,
#             ssl_require=not DEBUG
#         )
#     }
# else:
#     # SQLite (Local Development)
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": BASE_DIR / "db.sqlite3",
#         }
#     }

# # ----------------------------- 
# # Password Validators
# # ----------------------------- 
# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]

# # ----------------------------- 
# # Internationalization
# # ----------------------------- 
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = config("TIME_ZONE", default="UTC")
# USE_I18N = True
# USE_TZ = True

# # ----------------------------- 
# # Static files
# # ----------------------------- 
# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"

# if DEBUG:
#     STATICFILES_DIRS = [BASE_DIR / "static"]

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# # ----------------------------- 
# # Media files
# # ----------------------------- 
# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"

# # ----------------------------- 
# # Default primary key field type
# # ----------------------------- 
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# # ----------------------------- 
# # Security Settings for Production
# # ----------------------------- 
# if not DEBUG:
#     SECURE_BROWSER_XSS_FILTER = True
#     SECURE_CONTENT_TYPE_NOSNIFF = True
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_SECONDS = 31536000
#     SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     X_FRAME_OPTIONS = 'DENY'

# # ----------------------------- 
# # Caching (optional - Redis)
# # ----------------------------- 
# REDIS_URL = config("REDIS_URL", default=None)
# if REDIS_URL and not DEBUG:
#     CACHES = {
#         "default": {
#             "BACKEND": "django_redis.cache.RedisCache",
#             "LOCATION": REDIS_URL,
#             "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
#         }
#     }
# else:
#     CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

# # ----------------------------- 
# # Email
# # ----------------------------- 
# if DEBUG:
#     EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# else:
#     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#     EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
#     EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
#     EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
#     EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
#     EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
#     DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@yourdomain.com')

# # ----------------------------- 
# # Logging
# # ----------------------------- 
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {'format': '{levelname} {asctime} {module} {message}', 'style': '{'},
#         'simple': {'format': '{levelname} {message}', 'style': '{'},
#     },
#     'handlers': {
#         'console': {'class': 'logging.StreamHandler', 'formatter': 'simple' if DEBUG else 'verbose'},
#     },
#     'root': {'handlers': ['console'], 'level': 'INFO'},
#     'loggers': {
#         'django': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
#         'portfolio': {'handlers': ['console'], 'level': 'DEBUG' if DEBUG else 'INFO', 'propagate': False},
#     },
# }
import os
from pathlib import Path
import dj_database_url
from decouple import config

# -----------------------------
# Base Directory
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Security
# -----------------------------
SECRET_KEY = config("SECRET_KEY", default="fallback-secret-key")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com"]

# -----------------------------
# Installed Apps
# -----------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "portfolio",  # your app
]

# -----------------------------
# Middleware
# -----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # For static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------
# Root URL / WSGI
# -----------------------------
ROOT_URLCONF = "sartaj_portfolio.urls"       # ✅ project folder
WSGI_APPLICATION = "sartaj_portfolio.wsgi.application"  # ✅ project folder

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Custom templates directory
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# -----------------------------
# Database
# -----------------------------
ENVIRONMENT = config("ENV", default="development")

if ENVIRONMENT == "production":
    DATABASES = {
        "default": dj_database_url.config(
            default=config("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:  # Development → use SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -----------------------------
# Password Validation
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------
# Internationalization
# -----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -----------------------------
# Static & Media Files
# -----------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # Your static folder
STATIC_ROOT = BASE_DIR / "staticfiles"    # For collectstatic
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# -----------------------------
# Default Auto Field
# -----------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
