import streamlit as st
import pandas as pd
from helpers import colours
from data import DATA

def button_callback(df, index):
    st.session_state["selected_case_data"] = df.iloc[index]
    st.session_state["selected_evidence"] = []
    st.session_state["page"] = "Case Detail"

def case_summary_page():
    st.title("Case Summary")

    df = pd.DataFrame(DATA)

    # Filters
    status_filter = st.selectbox("Filter by Status", ["All", "Open", "Pending", "Closed"])
    if status_filter != "All":
        df = df[df["Current Status"] == status_filter]

    rag_filter = st.selectbox("Filter by RAG Status", ["All", "Red", "Amber", "Green"])
    if rag_filter != "All":
        df = df[df["RAG Status"] == rag_filter]

    # CSS for scrollable table
    st.markdown(f"""
        <style>
        .reportview-container .main .block-container{{
            padding-top: 0rem;
        }}
        .stButton button {{
            background-color: {colours["barclays_blue"]} !important;
            color: {colours["barclays_white"]} !important;
            border: none;
            padding: 5px 10px;
            cursor: pointer;
            width: 100%;
        }}
        .stButton button:hover {{
            background-color: {colours["barclays_light_blue"]} !important;
        }}
        body {{
            overflow-y: hidden;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Encapsulate the table inside the scrollable div
    st.markdown('<div class="scrollable-table">', unsafe_allow_html=True)

    summary_df = df.drop(columns=['Alerts', 'Case Details']).copy()

    # Header row
    cols = st.columns(len(summary_df.columns) + 1)
    for col_index, col_name in enumerate(summary_df.columns):
        cols[col_index].markdown(f"<div style='font-weight: bold; background-color: {colours['barclays_blue']}; color: {colours['barclays_white']}; padding: 8px;'>{col_name}</div>", unsafe_allow_html=True)

    # Construct the table with buttons
    for index, row in summary_df.iterrows():
        cols = st.columns(len(row) + 1)
        for col_index, value in enumerate(row):
            cols[col_index].markdown(f"<div style='padding: 8px;'>{value}</div>", unsafe_allow_html=True)
        if cols[len(row)].button("Assign", key=index):
            button_callback(df, index)

    st.markdown('</div>', unsafe_allow_html=True)