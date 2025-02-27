# noqa: E800
"""
Django settings for MobSF project.

MobSF and Django settings
"""

import imp
import logging
import os

from MobSF.utils import (find_java_binary, find_vboxmange_binary, first_run,
                         get_mobsf_home)

logger = logging.getLogger(__name__)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#       MOBSF CONFIGURATIONS
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

MOBSF_VER = 'v1.1.4 Beta'
BANNER = """
  __  __       _    ____  _____           _   _   
 |  \/  | ___ | |__/ ___||  ___| __   __ / | / |
 | |\/| |/ _ \| '_ \___ \| |_    \ \ / / | | | |
 | |  | | (_) | |_) |__) |  _|    \ V /  | |_| |
 |_|  |_|\___/|_.__/____/|_|       \_/   |_(_)_|

"""  # noqa: W291
# ASCII Standard
# ==============================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ==========MobSF Home Directory=================
USE_HOME = False

# True : All Uploads/Downloads will be stored in user's home directory
# False : All Uploads/Downloads will be stored in MobSF root directory
# If you need multiple users to share the scan results set this to False
# ===============================================

MobSF_HOME = get_mobsf_home(USE_HOME)
# Logs Directory
LOG_DIR = os.path.join(MobSF_HOME, 'logs/')
# Download Directory
DWD_DIR = os.path.join(MobSF_HOME, 'downloads/')
# Screenshot Directory
SCREEN_DIR = os.path.join(MobSF_HOME, 'downloads/screen/')
# Upload Directory
UPLD_DIR = os.path.join(MobSF_HOME, 'uploads/')
# Database Directory
DB_DIR = os.path.join(MobSF_HOME, 'db.sqlite3')
# Tools Directory
TOOLS_DIR = os.path.join(BASE_DIR, 'DynamicAnalyzer/tools/')
# Secret File
SECRET_FILE = os.path.join(MobSF_HOME, 'secret')

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# Sqlite3 suport

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_DIR,
    },
}
# End Sqlite3 support

# Postgres DB - Install psycopg2
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mobsf',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
# End Postgres support
"""
# ===============================================

# ==========LOAD CONFIG FROM MobSF HOME==========
try:
    # Update Config from MobSF Home Directory
    if USE_HOME:
        USER_CONFIG = os.path.join(MobSF_HOME, 'config.py')
        sett = imp.load_source('user_settings', USER_CONFIG)
        locals().update(
            {k: v for k, v in list(sett.__dict__.items())
                if not k.startswith('__')})
        CONFIG_HOME = True
    else:
        CONFIG_HOME = False
except Exception:
    logger.exception('Reading Config')
    CONFIG_HOME = False
# ===============================================

# ===MOBSF SECRET GENERATION AND DB MIGRATION====
SECRET_KEY = first_run(SECRET_FILE, BASE_DIR, MobSF_HOME)

# =============================================

# =============ALLOWED EXTENSIONS================
ALLOWED_EXTENSIONS = {
    '.txt': 'text/plain',
    '.png': 'image/png',
    '.zip': 'application/zip',
    '.tar': 'application/x-tar',
}
# ===============================================

# =============ALLOWED MIMETYPES=================

APK_MIME = [
    'application/octet-stream',
    'application/vnd.android.package-archive',
    'application/x-zip-compressed',
    'binary/octet-stream',
]
IPA_MIME = [
    'application/iphone',
    'application/octet-stream',
    'application/x-itunes-ipa',
    'application/x-zip-compressed',
    'binary/octet-stream',
]
ZIP_MIME = [
    'application/zip',
    'application/octet-stream',
    'application/x-zip-compressed',
    'binary/octet-stream',
]
APPX_MIME = [
    'application/octet-stream',
    'application/vns.ms-appx',
    'application/x-zip-compressed',
]

# ===============================================

# ============DJANGO SETTINGS =================
DEBUG = True
DJANGO_LOG_LEVEL = DEBUG
ALLOWED_HOSTS = ['127.0.0.1', 'mobsf', '*']
# Application definition
INSTALLED_APPS = (
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'StaticAnalyzer',
    'DynamicAnalyzer',
    'MobSF',
    'MalwareAnalyzer',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

MIDDLEWARE = (
    'MobSF.views.api.rest_api_middleware.RestApiAuthMiddleware',
)
ROOT_URLCONF = 'MobSF.urls'
WSGI_APPLICATION = 'MobSF.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS':
            [
                os.path.join(BASE_DIR, 'templates'),
            ],
        'OPTIONS':
            {
                'debug': True,
            },
    },
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# 256MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 268435456

# ===================
# USER CONFIGURATION
# ===================

if CONFIG_HOME:
    logger.info('Loading User config from: %s', USER_CONFIG)
else:
    """
    IMPORTANT
    If 'USE_HOME' is set to True,
    then below user configuration settings are not considered.
    The user configuration will be loaded from
    config.py in MobSF Home directory.
    """
    # ^CONFIG-START^: Do not edit this line
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #          MOBSF USER CONFIGURATIONS
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # -------------------------
    # STATIC ANALYZER SETTINGS
    # -------------------------

    # ==========ANDROID SKIP CLASSES==========================
    # Common third party classes that will be skipped during static analysis
    SKIP_CLASSES = [
        r'com[\\\/]{1}google[\\\/]{1}',
        r'com[\\\/]{1}android[\\\/]{1}',
        r'android[\\\/]{1}content[\\\/]{1}',
        r'android[\\\/]{1}support[\\\/]{1}',
        r'android[\\\/]{1}arch[\\\/]{1}',
        r'kotlin[\\\/]{1}',

        r'okhttp2[\\\/]{1}', r'okhttp3[\\\/]{1}',
        r'com[\\\/]{1}squareup[\\\/]{1}okhttp[\\\/]{1}',
        r'com[\\\/]{1}twitter[\\\/]{1}',
        r'twitter4j[\\\/]{1}',
        r'org[\\\/]{1}apache[\\\/]{1}',
        r'oauth[\\\/]{1}signpost[\\\/]{1}',
        r'org[\\\/]{1}chromium[\\\/]{1}',
        r'com[\\\/]{1}facebook[\\\/]{1}',
    ]

    # ==========DECOMPILER SETTINGS=================

    DECOMPILER = 'cfr'

    # Three Decompilers are available
    # 1. jd-core
    # 2. cfr
    # 3. procyon

    # ==============================================

    # ==========Dex to Jar Converter================
    JAR_CONVERTER = 'd2j'

    # Two Dex to Jar converters are available
    # 1. d2j
    # 2. enjarify
    # ==============================================

    # ======WINDOWS STATIC ANALYSIS SETTINGS ===========

    # Private key
    WINDOWS_VM_SECRET = 'MobSF/windows_vm_priv_key.asc'
    # IP and Port of the MobSF Windows VM
    # example: WINDOWS_VM_IP = '127.0.0.1'   ;noqa E800
    WINDOWS_VM_IP = None
    WINDOWS_VM_PORT = '8000'
    # ==================================================

    # ==============3rd Party Tools=================
    """
    If you want to use a different version of 3rd party tools used by MobSF.
    You can do that by specifying the path here. If specified, MobSF will run
    the tool from this location.
    """

    # Android 3P Tools
    DEX2JAR_BINARY = ''
    BACKSMALI_BINARY = ''
    CFR_DECOMPILER_BINARY = ''
    JD_CORE_DECOMPILER_BINARY = ''
    PROCYON_DECOMPILER_BINARY = ''
    APKTOOL_BINARY = ''
    ADB_BINARY = ''
    ENJARIFY_DIRECTORY = ''

    # iOS 3P Tools
    OTOOL_BINARY = ''
    JTOOL_BINARY = ''
    CLASSDUMPZ_BINARY = ''
    CLASSDUMP_SWIFT_BINARY = ''

    # COMMON
    JAVA_DIRECTORY = ''
    VBOXMANAGE_BINARY = ''
    PYTHON3_PATH = ''

    """
    Examples:
    JAVA_DIRECTORY = 'C:/Program Files/Java/jdk1.7.0_17/bin/'
    JAVA_DIRECTORY = '/usr/bin/'
    DEX2JAR_BINARY = '/Users/ajin/dex2jar/d2j-dex2jar.sh'
    ENJARIFY_DIRECTORY = 'D:/enjarify/'
    VBOXMANAGE_BINARY = '/usr/bin/VBoxManage'
    CFR_DECOMPILER_BINARY = '/home/ajin/tools/cfr.jar'
    PYTHON3_PATH = 'C:/Users/Ajin/AppData/Local/Programs/Python/Python35-32/'
    """
    # ===============================================

    # -------------------------
    # DYNAMIC ANALYZER SETTINGS
    # -------------------------

    # ========ANDROID DYNAMIC ANALYSIS SETTINGS================================

    ANDROID_DYNAMIC_ANALYZER = 'MobSF_VM'

    # You can choose any of the below
    # 1. MobSF_VM
    # 2. MobSF_REAL_DEVICE

    """
    MobSF_VM x86 Android 4.4.2 running on VirtualBox(Fast, not all Apps work)
    MobSF_REAL_DEVICE - Rooted Android 4.03 4.4 Device
    (Very Fast, All Apps work)
    Supports Android 5+ for real device. Not tested!
    """

    # =========================================================================

    # =======ANDROID REAL DEVICE SETTINGS===========
    DEVICE_IP = '192.168.1.18'
    DEVICE_ADB_PORT = 5555
    DEVICE_TIMEOUT = 300
    # ==============================================

    # ====ANDROID MOBSF VIRTUALBOX VM SETTINGS =====
    # VM UUID
    UUID = '408e1874-759f-4417-9453-53ef21dc2ade'
    # Snapshot UUID
    SUUID = '5c9deb28-def6-49c0-9233-b5e03edd85c6'
    # IP of the MobSF VM
    VM_IP = '192.168.56.101'
    VM_ADB_PORT = 5555
    VM_TIMEOUT = 100
    VBOX_HEADLESS = False
    # ==============================================

    # --------------------------
    # MobSF MITM PROXY SETTINGS
    # --------------------------

    # ================HOST/PROXY SETTINGS ===============
    PROXY_IP = '192.168.56.1'  # Host/Server/Proxy IP
    PORT = 1337  # Proxy Port
    ROOT_CA = '0026aabb.0'
    SCREEN_IP = PROXY_IP  # ScreenCast IP
    SCREEN_PORT = 9339  # ScreenCast Port(Do not Change)
    # ===================================================

    # ========UPSTREAM PROXY SETTINGS ==============
    # If you are behind a Proxy
    UPSTREAM_PROXY_ENABLED = False
    UPSTREAM_PROXY_SSL_VERIFY = True
    UPSTREAM_PROXY_TYPE = 'http'
    UPSTREAM_PROXY_IP = '127.0.0.1'
    UPSTREAM_PROXY_PORT = 3128
    UPSTREAM_PROXY_USERNAME = ''
    UPSTREAM_PROXY_PASSWORD = ''
    # ==============================================

    # --------------------------
    # MALWARE ANALYZER SETTINGS
    # --------------------------

    DOMAIN_MALWARE_SCAN = True

    # ----------APKiD-------------------------------
    APKID_ENABLED = True
    # ==============================================

    # ========DISABLED COMPONENTS===================

    # ----------VirusTotal--------------------------
    VT_ENABLED = False
    VT_API_KEY = 'XXXXXXXXXXXXXX'
    VT_UPLOAD = False
    # Before setting VT_ENABLED to True,
    # Make sure VT_API_KEY is set to your VirusTotal API key
    # register at: https://www.virustotal.com/#/join-us
    # You can get your API KEY from:
    # https://www.virustotal.com/en/user/<username>/apikey/
    # Files will be uploaded to VirusTotal
    # if VT_UPLOAD is set to True.
    # ==============================================

    # -----External URLS--------------------------
    MALWARE_DB_URL = 'http://www.malwaredomainlist.com/mdlcsv.php'
    VIRUS_TOTAL_BASE_URL = 'https://www.virustotal.com/vtapi/v2/file/'
    TRACKERS_DB_URL = 'https://reports.exodus-privacy.eu.org/api/trackers'

    # ^CONFIG-END^: Do not edit this line

# The below code should be loaded last.
# ============JAVA SETTINGS======================
JAVA_BINARY = find_java_binary()
# ===============================================

# ================VirtualBox Settings============
VBOX = find_vboxmange_binary(False)
# ===============================================

# Better logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] %(asctime)-15s - %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
        'color': {
            '()': 'colorlog.ColoredFormatter',
            'format':
                '%(log_color)s[%(levelname)s] %(asctime)-15s - %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(MobSF_HOME, 'logs', 'debug.log'),
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console', 'logfile'],
            # DEBUG will log all queries, so change it to WARNING.
            'level': 'INFO',
            'propagate': False,   # Don't propagate to other handlers
        },
        'MobSF': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'StaticAnalyzer': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'MalwareAnalyzer': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'DynamicAnalyzer': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
