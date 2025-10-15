import os
import json
import tempfile
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from firebase_admin import credentials, firestore, initialize_app, get_app

from exceptions import UserAlreadyExists, UserNotFound

load_dotenv(override=True)

IST = ZoneInfo('Asia/Kolkata')

class Firestore:
    def __init__(self):
        temp_path = None
        try:
            get_app()
        except Exception:
            # creds = credentials.Certificate(os.environ.get("SERVICE_ACCOUNT_KEY_FILE"))
            service_account_key_info = json.loads(st.secrets['firebase']['serviceAccountKey'])
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json") as f:
                json.dump(service_account_key_info, f)
                temp_path = f.name

            creds = credentials.Certificate(temp_path)
            initialize_app(creds)
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
        self.db = firestore.client()

    def add_user(self, email: str, name: str, app_password: str):
        doc_ref = self.db.collection('gmail_credentials').document(email)
        doc = doc_ref.get()

        if not doc.exists:
            doc_ref.set({
                'email': email,
                'name': name,
                'app_password': app_password,
                'last_accessed': datetime.now(tz=IST),
                'created': datetime.now(tz=IST)
            })
            return 
        else:
            raise UserAlreadyExists(email)


    def get_user_app_password_and_name(self, email: str):
        doc_ref = self.db.collection('gmail_credentials').document(email)
        doc = doc_ref.get()

        if doc.exists:
            doc_ref.update({
                'last_accessed': datetime.now(tz=IST)
            })
            data = doc.to_dict()
            return data.get('app_password'), data.get('name')
        
        else:
            raise UserNotFound(email)
        
        

# fs = Firestore()
# token = fs.get_user_refresh_token('aryan@gmail.com')
# print(token)