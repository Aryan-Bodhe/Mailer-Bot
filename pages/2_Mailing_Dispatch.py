import streamlit as st
from services.mailer_service import MailerService

# Page config
st.set_page_config(page_title='Mail Dispatch Results', layout='wide', initial_sidebar_state='collapsed')

# Load session variables
ms: MailerService = st.session_state['mailer_service']
student_exam_data = st.session_state['student_exam_data']
course_name = st.session_state['course_name']
exam_name = st.session_state['exam_name'] 
professor_name = st.session_state['professor_name']

# Run send_bulk only once
if "mail_sent" not in st.session_state:
    with st.container(horizontal_alignment='center', vertical_alignment='center'):
        with st.spinner("Sending mails...", width=300):
            success, total, failed_mails = ms.send_bulk(
                student_exam_data, course_name, exam_name, professor_name
            )
            # store results in session
            st.session_state["mail_sent"] = True
            st.session_state["success"] = success
            st.session_state["total"] = total
            st.session_state["failed_mails"] = failed_mails

        
    # Layout
    left_col, right_col = st.columns([2, 4])

    with left_col:
        st.header('Mail Dispatcher Summary')
        st.text(f"Total mails sent: {success}/{total}.")


    with right_col:
        st.header('Failed to send')
        st.text('Following emails could not be sent due to missing data or internal errors.')
        st.dataframe(failed_mails)

else:
    success = st.session_state["success"]
    total = st.session_state["total"]
    failed_mails = st.session_state["failed_mails"]

if st.button("Send More Mails"):
    creds = st.session_state['credentials']
    st.session_state.clear()
    st.session_state['credentials'] = creds
    st.switch_page("pages/0_Upload.py")

# clear everything and go to home page
if st.button("Logout"):
    st.session_state.clear()
    st.switch_page('pages/3_Logout_Screen.py')