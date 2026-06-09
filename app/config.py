import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    
    # Company configuration
    COMPANY_NAME = 'Medical Store Management System'
    COMPANY_ADDRESS = 'Your Store Address'
    COMPANY_PHONE = '+1-XXX-XXX-XXXX'
    COMPANY_EMAIL = 'info@medicalstore.com'
    COMPANY_GST = 'GST Number'
    
    # PDF configuration
    PDF_MARGIN_TOP = 0.5
    PDF_MARGIN_BOTTOM = 0.5
    PDF_MARGIN_LEFT = 0.5
    PDF_MARGIN_RIGHT = 0.5
    
    # File upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    
    # Reports
    REPORTS_FOLDER = 'reports'
    BACKUP_FOLDER = 'backups'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///medical_store.db'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///medical_store.db'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
