import streamlit as st

def pending_tab():
    st.subheader("Pending")

    st.file_uploader("Upload new information or data", type=["pdf", "docx", "jpg", "png"])

    if st.button("Request GenAI Re-evaluation"):
        st.write("GenAI Re-evaluation requested.")