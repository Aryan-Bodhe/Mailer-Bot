import streamlit as st
from services.mailer_service import MailerService
from services.dataloader import DataLoader
from models.UserCredentials import UserCredentials
from services.encryption_service import EncryptionService

st.set_page_config(page_title='Mail Preview', initial_sidebar_state='collapsed', layout='wide')

st.title("📧 Mailing Service")

if "credentials" not in st.session_state:
    st.switch_page('app.py')

# Check if file was uploaded
if "dataloader_instance" not in st.session_state:
    st.warning("⚠️ Please upload a file on the upload page first.")
    if st.button("Upload File"):
        st.switch_page("pages/0_Upload.py")
    st.stop()

if 'encryption_service' not in st.session_state:
    st.session_state['encryption_service'] = EncryptionService()

creds: UserCredentials = st.session_state['credentials']
encryption_service: EncryptionService = st.session_state['encryption_service']
left_col, center_col, right_col = st.columns([1,4,2])
dl: DataLoader = st.session_state['dataloader_instance']

if 'mailer_service' not in st.session_state or st.session_state['mailer_service'] is None:
    ms: MailerService = MailerService(sender_email=creds.email, app_password=encryption_service.decrypt(creds.app_password))
    st.session_state['mailer_service'] = ms
else: 
    ms: MailerService = st.session_state['mailer_service']


with left_col:
    st.session_state['course_name'] = course_name = st.text_input("Course Name", "Real Analysis")
    st.session_state['professor_name'] = professor_name = st.text_input("Professor Name", creds.name)
    st.session_state['exam_name'] = exam_name = st.selectbox("Examination", options=dl.get_exam_names())

with center_col:
    st.text("Student Exam Data", )
    student_data = dl.get_student_exam_data(exam_name)
    st.session_state['student_exam_data'] = student_data
    st.session_state['mailer_service'] = ms
    st.dataframe(student_data)

with right_col:
    preview_data = student_data.iloc[0]
    preview_subject, preview_body = ms.prepare_mail_content(getattr(preview_data, "Name"), getattr(preview_data, exam_name), course_name, exam_name, professor_name)
    with st.container(border=True):
        st.text(preview_subject)
    with st.container(border=True):
        st.text(preview_body)

with st.container(width=300, horizontal_alignment='center'):
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Back"):
            # clear all page specific data
            keys_to_delete = {'course_name', 'professor_name', 'exam_name', 'student_exam_data', 'mailer_service'}
            for key in keys_to_delete:
                if key in st.session_state:
                    del st.session_state[key]
            st.switch_page(page='app.py')

    with col2:    
        if st.button("Send All Mails"):
            st.switch_page(page='pages/2_Mailing_Dispatch.py')