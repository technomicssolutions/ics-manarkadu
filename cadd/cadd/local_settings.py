DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cadd',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'krishna',
        'PASSWORD': 'root',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 25
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'testtechnomics06@gmail.com'
EMAIL_HOST_PASSWORD = 'qwertyuiop[]a'
DEFAULT_FROM_EMAIL = 'testtechnomics06@gmail.com'
FOLLOW_UP_MAIL_ID = 'testtechnomics06@gmail.com'