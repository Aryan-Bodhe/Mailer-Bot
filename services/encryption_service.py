import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

class EncryptionService:
    def __init__(self):
        # self.fernet = Fernet(os.environ.get('FERNET_KEY').encode())
        self.fernet = Fernet(st.secrets['fernet']['fernetKey'].encode())

    def encrypt(self, data: str):
        encrypted_data = self.fernet.encrypt(data.encode()).decode()
        return encrypted_data
    
    def decrypt(self, data: str):
        decrypted_data = self.fernet.decrypt(data.encode()).decode()
        return decrypted_data
