"""
Django settings for upkoding project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import yaml
from pathlib import Path
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'SECRET_KEY', 'b3r95l(hvdtj#ue!0shnj1&5__*+gt=-fr!@3%@&2a0rt0r%#^')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost 127.0.0.1').split()
AUTH_USER_MODEL = 'account.User'
APP_VERSION = os.getenv('APP_VERSION', 'devel')

# Application definition

INSTALLED_APPS = [
    # upkoding apps
    'account.apps.AccountConfig',
    'base.apps.BaseConfig',
    'projects.apps.ProjectsConfig',
    'coders.apps.CodersConfig',
    'codeblocks.apps.CodeblocksConfig',
    'roadmaps.apps.RoadmapsConfig',
    'discord.apps.DiscordConfig',
    # 'forum.apps.ForumConfig',

    # 3rd party apps
    'django_email_verification',
    'whitenoise.runserver_nostatic',
    'social_django',
    'sorl.thumbnail',
    'markdownify.apps.MarkdownifyConfig',
    'mdeditor',
    'anymail',
    'django_ace',
    'stream_django',

    # django contribs
    'django.contrib.postgres',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'account.middleware.SocialLoginExceptionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'upkoding.middlewares.TimezoneMiddleware',
]
if DEBUG:
    MIDDLEWARE = [
        'upkoding.middlewares.QueryCountDebugMiddleware',
    ] + MIDDLEWARE

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'upkoding.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / '_templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'upkoding.context_processors.upkoding',
            ],
        },
    },
]

WSGI_APPLICATION = 'upkoding.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        default='postgres://upkoding:upkoding@localhost:5432/upkoding'
    )
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'id-ID'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# -- Mailer --
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_EMAIL_FROM = os.getenv(
    'DEFAULT_EMAIL_FROM', 'UpKoding <upkoding@example.com>')
SERVER_EMAIL = os.getenv('SERVER_EMAIL', 'upkoding@example.com')
ANYMAIL = {
    'MAILGUN_API_KEY': os.getenv('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': os.getenv('MAILGUN_SENDER_DOMAIN'),
}

# -- Judge0 --
JUDGE0_API_KEY = os.getenv('JUDGE0_API_KEY')

# -- Stream --
STREAM_API_KEY = os.getenv('STREAM_API_KEY', 'key')
STREAM_API_SECRET = os.getenv('STREAM_API_SECRET', 'secret')
# we want to send activity to Stream manually.
STREAM_DISABLE_MODEL_TRACKING = True
STREAM_FEED_MANAGER_CLASS = 'upkoding.activity_feed.FeedManager'

# -- Discord --
DISCORD_APPLICATION_ID = os.getenv('DISCORD_APPLICATION_ID')
DISCORD_PUBLIC_KEY = os.getenv('DISCORD_PUBLIC_KEY')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')
DISCORD_UPKODERS_ROLE_ID = os.getenv('DISCORD_UPKODERS_ROLE_ID')

if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
    AWS_S3_ENDPOINT_URL = 'https://{}.digitaloceanspaces.com'.format(
        AWS_S3_REGION_NAME
    )
    AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_QUERYSTRING_AUTH = False
    AWS_IS_GZIPPED = True

    EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
    PREPEND_WWW = os.getenv('PREPEND_WWW', 'False') == 'True'
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
    if os.getenv('IS_BEHIND_PROXY'):
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[DjangoIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = os.getenv('STATIC_URL', '/static/')
STATICFILES_DIRS = [
    BASE_DIR / '_static/dist',
]

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
THUMBNAIL_FORCE_OVERWRITE = True

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/account/'
LOGIN_ERROR_URL = '/account/login/'
LOGOUT_REDIRECT_URL = '/account/login/'

SOCIAL_AUTH_JSONFIELD_CUSTOM = 'django.db.models.JSONField'
SOCIAL_AUTH_URL_NAMESPACE = 'account:social'
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'account.pipeline.user_details',
)

# Social Auth: Github
SOCIAL_AUTH_GITHUB_KEY = os.getenv('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.getenv('SOCIAL_AUTH_GITHUB_SECRET')
SOCIAL_AUTH_GITHUB_SCOPE = ['read:user', 'user:email']

# Social Auth: Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv(
    'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

# Social Auth: Facebook
SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}
SOCIAL_AUTH_FACEBOOK_API_VERSION = '2.10'

# Site
SITE_DOMAIN = os.getenv('SITE_DOMAIN', 'http://localhost:8000')
POINT_UNIT = 'UP'
DEFAULT_METADATA = {
    'title': 'UpKoding',
    'image': 'assets/img/logo.png',
    'description': 'UpKoding adalah platform belajar pemrograman dengan format bite-sized learning, belajar materi secukupnya, langsung uji dan praktekkan.',
}

GOOGLE_ANALYTICS_TRACKING_ID = os.getenv('GOOGLE_ANALYTICS_TRACKING_ID')
STATUSPAGE_URL = 'https://stats.uptimerobot.com/ElMQmFWXKD'
MAINTENANCE_MODE = os.getenv('MAINTENANCE_MODE', 'False') == 'True'
SHOW_ROADMAPS = os.getenv('SHOW_ROADMAPS', 'False') == 'True'
ENABLE_PAYMENT = os.getenv('ENABLE_PAYMENT', 'False') == 'True'

# Email verification
def email_verified_callback(user):
    user.verified_email = user.email

EMAIL_VERIFIED_CALLBACK = email_verified_callback
EMAIL_FROM_ADDRESS = DEFAULT_EMAIL_FROM
EMAIL_MAIL_SUBJECT = 'Verifikasi Email'
EMAIL_MAIL_HTML = 'email/email_verification.html'
EMAIL_MAIL_PLAIN = 'email/email_verification.txt'
EMAIL_TOKEN_LIFE = 60 * 60 # 1hr
EMAIL_PAGE_TEMPLATE = 'email/email_verification_confirm.html'
EMAIL_PAGE_DOMAIN = SITE_DOMAIN

# MidTrans
MIDTRANS_IS_PRODUCTION = os.getenv('MIDTRANS_IS_PRODUCTION', 'False') == 'True'
MIDTRANS_SERVER_KEY = os.getenv('MIDTRANS_SERVER_KEY')
MIDTRANS_CLIENT_KEY = os.getenv('MIDTRANS_CLIENT_KEY')
MIDTRANS_MERCHANT_ID = os.getenv('MIDTRANS_MERCHANT_ID')

MDEDITOR_CONFIGS = {
    'default': {
        'width': '90% ',  # Custom edit box width
        'heigth': 500,  # Custom edit box height
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "code", "preformatted-text", "code-block", "datetime", "html-entities", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # custom edit box toolbar
        # image upload format type
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
        'image_folder': 'editor',  # image save the folder name
        'theme': 'default',  # edit box theme, dark / default
        'preview_theme': 'default',  # Preview area theme, dark / default
        'editor_theme': 'default',  # edit area theme, pastel-on-dark / default
        'toolbar_autofixed': True,  # Whether the toolbar capitals
        'search_replace': True,  # Whether to open the search for replacement
        'emoji': False,  # whether to open the expression function
        'tex': True,  # whether to open the tex chart function
        'flow_chart': False,  # whether to open the flow chart function
        'sequence': True,  # Whether to open the sequence diagram function
        'watch': True,  # Live preview
        'lineWrapping': False,  # lineWrapping
        'lineNumbers': False,  # lineNumbers
        'language': 'en'  # zh / en / es
    }
}

MARKDOWNIFY = {
    'default': {
        'WHITELIST_TAGS': [
            'b',
            'strong',
            'p'
        ]
    },
    'codes': {
        'WHITELIST_TAGS': [
            'b',
            'strong',
            'p',
            'code',
            'pre',
            'ul',
            'li',
            'ol',
            'hr',
        ],
        'WHITELIST_ATTRS': [
            'class',
        ],
        'MARKDOWN_EXTENSIONS': [
            'markdown.extensions.fenced_code',
            'markdown.extensions.extra',
        ]
    },
    'full': {
        'WHITELIST_TAGS': [
            'a',
            'abbr',
            'acronym',
            'b',
            'blockquote',
            'em',
            'i',
            'li',
            'ol',
            'p',
            'strong',
            'ul',
            'code',
            'pre',
            'hr',
            'h1',
            'h2',
            'h3',
            'h4',
            'h5',
            'h6',
            'img',
        ],
        'WHITELIST_ATTRS': [
            'href',
            'src',
            'alt',
            'class',
        ],
        'MARKDOWN_EXTENSIONS': [
            'markdown.extensions.fenced_code',
            'markdown.extensions.extra',
        ]
    }
}

with open(BASE_DIR / f'upkoding/pricing/v1.yaml') as file:
    PRICING = yaml.load(file, Loader=yaml.FullLoader)

with open(BASE_DIR / f'contributors.yaml') as file:
    CONTRIBUTORS = yaml.load(file, Loader=yaml.FullLoader)
