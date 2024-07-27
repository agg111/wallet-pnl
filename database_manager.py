from firebase_admin import credentials, firestore, initialize_app
import os
import logging

# Suppress gRPC logs
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GRPC_TRACE'] = ''

FIREBASE_CREDS = os.getenv('FIREBASE_CREDS')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_firebase():
    cred = credentials.Certificate("cryptowallet-58c08-firebase-adminsdk-njv87-3c9594e4db.json")
    initialize_app(cred)
    return firestore.client()

def save(db, collection, records): 
    try:
        for record in records:
            db.collection(collection).document(record['id']).set(record)
        logging.info(f"Data successfully stored in Firebase collection: {collection}")
    except Exception as e:
        logging.error(f"An error occurred while writing to Firebase: {e}")

def get_collection(db, collection):
    data = db.collection(collection).stream()
    return data

def get_hourly_data(db, collection, id):
    hourly_data = db.collection(collection).document(id)
    return hourly_data.get().to_dict()


    