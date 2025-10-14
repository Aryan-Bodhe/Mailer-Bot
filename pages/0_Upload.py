import streamlit as st
from services.dataloader import DataLoader

if 'credentials' not in st.session_state:
    st.switch_page('app.py')

st.set_page_config(page_title="Marks Mailer Bot", page_icon="📧", initial_sidebar_state='collapsed', layout='wide')
_, center_col, _ = st.columns([1,4,1])

with center_col:
    with st.container(border=True):
        st.title("Mailer Bot")

        uploaded_file = st.file_uploader(
            "Upload Excel file containing student exam marks.", 
            type=[".xlsx", ".xls"],
        )

        if uploaded_file:
            st.success("File upload successful!")
            dl = DataLoader(uploaded_file)
            st.session_state["dataloader_instance"] = dl

            if st.button("Proceed"):
                st.switch_page(page="pages/1_Mailing_Preview.py") 
            
            st.dataframe(dl.get_head())
        else:
            st.warning("Please upload a valid excel file to continue.")

