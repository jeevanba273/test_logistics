import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'your-password-salt-here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = False

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///logistics.db'

class ProductionConfig(Config):
    DEBUG = False
    # Get DATABASE_URL from environment, fallback to SQLite if not provided or invalid
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Handle PostgreSQL URL format for Railway
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        # Validate the URL format - check if it contains placeholder text
        if 'username:password@host:port' in database_url or ':port/' in database_url:
            # Invalid placeholder URL, fallback to SQLite
            SQLALCHEMY_DATABASE_URI = 'sqlite:///logistics.db'
        else:
            SQLALCHEMY_DATABASE_URI = database_url
    else:
        # No DATABASE_URL provided, use SQLite
        SQLALCHEMY_DATABASE_URI = 'sqlite:///logistics.db'