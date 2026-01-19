import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # Firestore configuration
    FIRESTORE_PROJECT_ID = os.environ.get('FIRESTORE_PROJECT_ID', 'demo-project')
    USE_FIRESTORE_EMULATOR = os.environ.get('USE_FIRESTORE_EMULATOR', 'true').lower() == 'true'
    FIRESTORE_EMULATOR_HOST = os.environ.get('FIRESTORE_EMULATOR_HOST', 'firestore:8080')

    # Google Cloud credentials
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
