import time
import streamlit as st
from services.mailer_service import MailerService
from apis.firestore import Firestore
from services.encryption_service import EncryptionService
from exceptions import UserNotFound, UserAlreadyExists
from streamlit_cookies_controller import CookieController
from models.UserCredentials import UserCredentials


st.set_page_config(page_title="Login", initial_sidebar_state='collapsed')

if 'mailer_service' not in st.session_state:
    st.session_state['mailer_service'] = None

if 'firestore' not in st.session_state:
    st.session_state['firestore'] = Firestore()

if 'encryption_service' not in st.session_state:
    st.session_state['encryption_service'] = EncryptionService()

if 'credentials' not in st.session_state:
    st.session_state['credentials'] = None

_, center, _ = st.columns([1,4,1])

def registration_screen():
    with center:
        with st.container(border=True):
            st.header("Mailer Bot Registration")
            
            with st.form(key='registration', border=True):
                name = st.text_input(placeholder='Enter your name here.', label='Name', autocomplete='off')
                user_email = st.text_input(placeholder='Enter email here.', label='Email', autocomplete='off')
                app_pwd = st.text_input(placeholder='Enter GMail app password here.', label='Gmail App Password', autocomplete='off', type='password')

                if st.form_submit_button('Register'):
                    if not name or not user_email or not app_pwd:
                        st.warning('Please fill out all fields.')

                    else:
                        if MailerService.validate_credentials(email=user_email, app_pwd=app_pwd):
                            ms = MailerService(sender_email=user_email, app_password=app_pwd)
                            st.session_state['mailer_service'] = ms
                            app_password_encrypted = encryption_service.encrypt(app_pwd)
                            try:
                                firestore.add_user(email=user_email, name=name, app_password=app_password_encrypted)
                            except UserAlreadyExists:
                                st.error("User already exists.")
                            except Exception as e:
                                st.error(f'Some Error occured: {e}. Try reloading the page.')
                                st.stop()

                            encrypted_email = encryption_service.encrypt(user_email)
                            controller.set('user_email', encrypted_email)

                            st.session_state['credentials'] = UserCredentials(name=name, email=user_email, app_password=app_pwd)

                            st.success('Registration Successful!')
                            time.sleep(1)
                            st.switch_page('pages/0_Upload.py')
                        else:
                            st.error('Invalid Email or App Password.')



controller = CookieController()
encryption_service: EncryptionService = st.session_state['encryption_service']
firestore: Firestore = st.session_state['firestore']

encrypted_email = controller.get('user_email')
if encrypted_email:
    user_email = encryption_service.decrypt(encrypted_email)
    try:
        app_pwd, name = firestore.get_user_app_password_and_name(user_email)
        st.session_state['credentials'] = UserCredentials(name=name, email=user_email, app_password=app_pwd)
        st.success("User Auto Login Successful.")
        time.sleep(1)
        st.switch_page('pages/0_Upload.py')
    except UserNotFound:
        controller.remove('user_email')
        registration_screen()
    except Exception as e:
        st.error(f'Some Error occured: {e}. Try reloading the page.')
        st.stop()

else:
    registration_screen()
    