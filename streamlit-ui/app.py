import streamlit as st
st.set_page_config(layout="wide")
from helpers import colours
from case_summary import case_summary_page
from case_detail import case_detail_page
from PIL import Image

def main():

    st.markdown("""
        <style>
            h1 {
                font-size: 50px;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([6, 1])

    with col1:
        st.title("Empowered Data-Driven GenAI Evaluation (EDGE)")

    with col2:
        st.image(Image.open('static/logo.png'), width=100)

    if 'page' not in st.session_state:
        st.session_state['page'] = 'Case Summary'

    if st.session_state['page'] == 'Case Summary':
        case_summary_page()
    elif st.session_state['page'] == 'Case Detail':
        case_detail_page()

if __name__ == "__main__":
    main()