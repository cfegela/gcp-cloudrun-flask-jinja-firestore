import os
from google.cloud import firestore
from config import Config

def get_db():
    """Initialize and return Firestore client."""
    if Config.USE_FIRESTORE_EMULATOR:
        os.environ['FIRESTORE_EMULATOR_HOST'] = Config.FIRESTORE_EMULATOR_HOST

    db = firestore.Client(project=Config.FIRESTORE_PROJECT_ID)
    return db

# Initialize database
db = get_db()
