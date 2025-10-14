import streamlit as st

_, center, _ = st.columns([1,4,1])

with center:
    st.header("Thanks for using Mailer Bot!")
    st.success('Logged out successfully!')
    if st.button('Log in'):
        st.switch_page('app.py')