import streamlit as st
import pandas as pd
from pending_tab import pending_tab
from helpers import colours, create_geolocation_map
from PIL import Image

def add_evidence(evidence_type, evidence):
    st.session_state["selected_evidence"].append([evidence_type, evidence])

def case_detail_page():
    if "selected_case_data" not in st.session_state:
        st.warning("Please assign a case from the Case Summary page.")
        return

    case_data = st.session_state["selected_case_data"]

    case_data["agent_outputs"] = {
        "Overall": {
            "Risk": 5,
            "Reason": "The overall risk is assessed as high due to multiple factors indicating suspicious and potentially illegal activities. Adverse media reports from reliable sources in 2024 allege serious crimes such as human trafficking and illegal transport of individuals. Geolocation data shows IP addresses from widely dispersed locations within short time intervals, suggesting possible fraudulent activity. Additionally, the transaction activity includes extremely large deposits significantly higher than the declared annual income and multiple high-value cryptocurrency transactions, which are considered higher risk. The combination of these factors strongly indicates suspicious behavior.",
        },
        "Adverse Media": {
            "Risk": 5,
            "Reason": "The articles are recent (2024), from reliable sources, and involve serious allegations such as human trafficking and illegal transport of individuals, which are highly suspicious activities.",
            "Evidence": [
                {
                    "date": "14/10/2024",
                    "source": "The Washington Post",
                    "headline": "John Doe is a Human Trafficker",
                    "url": "https://www.washingtonpost.com/cvhjbnkl/",
                },
                {
                    "date": "27/10/2024",
                    "source": "BBC News",
                    "headline": "John Doe is a Bad Person",
                    "url": "https://www.bbc.co.uk/news/articles/c4gve4dcrdyvubu8jljo",
                }
            ]
        },
        "Geolocation": {
            "Risk": "5",
            "Reason": "The IP addresses are located in widely dispersed geographical locations (Marseille, France; Fortaleza, Brazil; and Newark, USA) within short time intervals, indicating a high risk of fraudulent activity.",
            "Evidence": [
                {"ip": "54.192.111.6", "datetime": "2024-10-06 06:49:03", "latitude": 43.29695, "longitude": 5.38107},
                {"ip": "179.224.188.48", "datetime": "2024-10-06 13:23:58",  "latitude": -3.71716, "longitude": -38.54308},
                {"ip": "97.37.242.205", "datetime": "2024-10-06 15:09:34",  "latitude": 40.73228, "longitude": -74.17358},
            ]
        },
        "Transaction Activity": {
            "Risk": 5,
            "Reason": "The customer has made two extremely large deposits (560,000 and 250,000) which are significantly higher than their declared annual income of less than 20k. Additionally, there are multiple high-value cryptocurrency transactions, which are considered higher risk. The combination of these factors indicates strong suspicious behavior.",
            "Evidence": [
                {
                    "Risk": 5,
                    "Reason for Flagging": "Large money deposit significantly higher than declared income",
                    "Transaction ID": "T169",
                    "Transaction Amount": 560000.0,
                    "Transaction Date": "5/19/2024 8:35",
                },
                {
                    "Risk": 5,
                    "Reason for Flagging": "Large money deposit significantly higher than declared income",
                    "Transaction ID": "T170",
                    "Transaction Amount": 250000.0,
                    "Transaction Date": "8/29/2024 18:44",
                },
                {
                    "Risk": 3,
                    "Reason for Flagging": "Crypto transaction, higher risk",
                    "Transaction ID": "T171",
                    "Transaction Amount": 2922.76,
                    "Transaction Date": "9/8/2024 10:44",
                },
                {
                    "Risk": 3,
                    "Reason for Flagging": "Crypto transaction, higher risk",
                    "Transaction ID": "T172",
                    "Transaction Amount": 1448.86,
                    "Transaction Date": "8/21/2024 17:12",
                },
                {
                    "Risk": 3,
                    "Reason for Flagging": "Crypto transaction, higher risk",
                    "Transaction ID": "T173",
                    "Transaction Amount": 2998.37,
                    "Transaction Date": "8/21/2024 16:34",
                }
            ],
        },
        "KYC": {
            "Risk": 4,
            "Reason": "The customer has a high risk due to facial recognition alerts from a sanctioned person",
            "Evidence": [
                (0.74, "static/human_1.jpg", "static/human_2.jpg")
            ]
        },
    }


    # Custom CSS for styling
    st.markdown(f"""
        <style>
        .reportview-container .main .block-container{{
            padding-top: 0rem;
        }}
        .stHeader {{
            color: {colours['barclays_white']};
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }}
        .stSummary {{
            background-color: {colours['barclays_light_blue']};
            padding: 10px;
            border: 1px solid #003087;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .stRiskTable {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            table-layout: fixed; /* Ensures fixed layout for equal column width */
        }}
        .stRiskTable th, .stRiskTable td {{
            border: 1px solid #003087;
            padding: 10px;
            text-align: center;
            width: 50%; /* Ensure columns have the same width */
        }}
        .stRiskTable th {{
            background-color: #005EB8;
            color: white;
            font-weight: bold;
        }}
        .caseDetailsTable {{
            width: 100%;
            border-collapse: collapse;
        }}
        .caseDetailsTable th, .caseDetailsTable td {{
            border: 1px solid #003087;
            padding: 8px;
            text-align: left;
        }}
        .caseDetailsTable th {{
            background-color: {colours['barclays_light_blue']};
            color: white;
        }}
        .caseDetailsTable td {{
            background-color: {colours['barclays_medium_blue']};
        }}
        .stRiskScore {{
            color: white;
            padding: 15px;
            border: 1px solid #003087;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
        }}
        .stRiskScore-5 {{
            background-color: #D9534F; /* Subdued red color for risk score 5 */
        }}
        .stRiskScore-4 {{
            background-color: #E67E22; /* Subdued orange color for risk score 4 */
        }}
        .stRiskScore-3 {{
            background-color: #F0AD4E; /* Subdued yellow-orange color for risk score 3 */
        }}
        .stRiskScore-2 {{
            background-color: #FFC107; /* Subdued yellow-orange-greenish color for risk score 2 */
        }}
        .stRiskScore-1 {{
            background-color: #5CB85C; /* Subdued green color for risk score 1 */
        }}
        .stSubHeader {{
            color: {colours['barclays_white']};
            font-size: 20px;
            font-weight: bold;
            margin-top: 20px;
        }}
        .stRiskyMediaTable {{
            display: flex;
            flex-direction: column;
            width: 100%;
            border: 1px solid #003087;
            border-radius: 5px;
            overflow: hidden;
        }}
        .stRiskyMediaRow {{
            display: flex;
            width: 100%;
            border-bottom: 1px solid #003087;
        }}
        .stRiskyMediaCell {{
            flex: 1;
            padding: 10px;
            border-right: 1px solid #003087;
            word-wrap: break-word;
            white-space: normal;
        }}
        .stRiskyMediaCell:last-child {{
            border-right: none;
        }}
        .stRiskyMediaHeader {{
            background-color: #005EB8;
            color: white;
            font-weight: bold;
        }}
        .stRiskyMediaBody {{
            background-color: #f2f2f2;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Header showing the current status of the case
    st.markdown(f'<div class="stHeader">Case Status: {case_data["Current Status"]}</div>', unsafe_allow_html=True)

    # Display case details in a table format with two rows of 3 columns each
    st.markdown(f"""
        <table class="caseDetailsTable">
            <tr>
                <th>Case ID</th>
                <th>Customer Name</th>
                <th>Date Created</th>
            </tr>
            <tr>
                <td>{case_data["Case ID"]}</td>
                <td>{case_data["Customer Name"]}</td>
                <td>{case_data["Date Created"]}</td>
            </tr>
            <tr>
                <th>RAG Status</th>
                <th>Priority</th>
                <th>Assigned Operator</th>
            </tr>
            <tr>
                <td>{case_data["RAG Status"]}</td>
                <td>{case_data["Priority"]}</td>
                <td>{case_data["Assigned Operator"]}</td>
            </tr>
        </table>
    """, unsafe_allow_html=True)

    # Creating the tabs
    tabs = ["Final Summary", "Alerts", "Adverse Media", "KYC", "Transaction Activity", "Geolocation", "Evidence"]
    if case_data["Current Status"] == "Pending":
        tabs.append("Upload New Information")

    selected_tab = st.tabs(tabs)

    with selected_tab[0]:
        overall_data = case_data["agent_outputs"]["Overall"]
        st.markdown('<div class="stSubHeader">Case Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stSummary">{overall_data["Reason"]}</div>', unsafe_allow_html=True)

        st.markdown('<div class="stSubHeader">GenAI Agent Risk Scores</div>', unsafe_allow_html=True)
        genai_risk_scores = [(x, case_data["agent_outputs"][x]["Risk"]) for x in case_data["agent_outputs"] if x != 'Overall']

        # Create a DataFrame from the sample data
        agents, scores = [x[0] for x in genai_risk_scores], [int(x[1]) for x in genai_risk_scores]
        genai_risk_scores_df = pd.DataFrame({'Agent': agents, 'Risk Score': scores})

        # Function to color the risk score cells
        def color_risk(val):
            color = ""
            if val == 5:
                color = "#D9534F"  # Subdued red color for risk score 5
            elif val == 4:
                color = "#E67E22"  # Subdued orange color for risk score 4
            elif val == 3:
                color = "#F0AD4E"  # Subdued yellow-orange color for risk score 3
            elif val == 2:
                color = "#FFC107"  # Subdued yellow-orange-greenish color for risk score 2
            elif val == 1:
                color = "#5CB85C"  # Subdued green color for risk score 1
            return f'background-color: {color}; color: white;'

        # Apply the color function to the DataFrame
        styled_df = genai_risk_scores_df.style.map(color_risk, subset=["Risk Score"])

        # Display the styled DataFrame as a table
        a = st.dataframe(styled_df, use_container_width=True, hide_index=True, column_config=None)
        a.disabled=[]
        #a = st.table(styled_df)
        #a.disabled=[]

        # Displaying the risk score
        risk_score = overall_data["Risk"]
        risk_class = f"stRiskScore stRiskScore-{risk_score}"

        st.markdown(f'<div class="{risk_class}">Risk Score: {risk_score} out of 5</div>', unsafe_allow_html=True)

    with selected_tab[1]:
        st.markdown('<div class="stSubHeader">Case Alerts</div>', unsafe_allow_html=True)

        case_alerts = case_data["Alerts"]

        # Table header
        st.markdown('<div class="stRiskyMediaRow stRiskyMediaHeader">', unsafe_allow_html=True)
        columns = st.columns([1, 1, 1, 2])
        with columns[0]:
            st.markdown("Alert ID")
        with columns[1]:
            st.markdown("Date")
        with columns[2]:
            st.markdown("Risk Score")
        with columns[3]:
            st.markdown("Description")
        st.markdown('</div>', unsafe_allow_html=True)

        # Table body
        for i, alert in enumerate(case_alerts):
            st.markdown('<div class="stRiskyMediaRow stRiskyMediaBody">', unsafe_allow_html=True)
            columns = st.columns([1, 1, 1, 2])
            with columns[0]:
                st.markdown(alert["alert_id"])
            with columns[1]:
                st.markdown(alert["alert_date"])
            with columns[2]:
                st.markdown(alert["risk_score"])
            with columns[3]:
                st.markdown(alert["alert_description"])
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with selected_tab[2]:

        adverse_media_data = case_data["agent_outputs"]["Adverse Media"]

        # Displaying the descriptive summary
        st.markdown('<div class="stSubHeader">Adverse Media Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stSummary">{adverse_media_data["Reason"]}</div>', unsafe_allow_html=True)

        # Displaying the risky media information in a table using st.columns
        st.markdown('<div class="stSubHeader">Risky Media</div>', unsafe_allow_html=True)
        st.markdown('<div class="stRiskyMediaTable">', unsafe_allow_html=True)

        # Table header
        st.markdown('<div class="stRiskyMediaRow stRiskyMediaHeader">', unsafe_allow_html=True)
        columns = st.columns([1, 1, 2, 1, 1])
        with columns[0]:
            st.markdown("Date")
        with columns[1]:
            st.markdown("Source")
        with columns[2]:
            st.markdown("Headline")
        with columns[3]:
            st.markdown("URL")
        with columns[4]:
            st.markdown("Action")
        st.markdown('</div>', unsafe_allow_html=True)

        # Table body
        for i, media in enumerate(adverse_media_data["Evidence"]):
            st.markdown('<div class="stRiskyMediaRow stRiskyMediaBody">', unsafe_allow_html=True)
            columns = st.columns([1, 1, 2, 1, 1])
            with columns[0]:
                st.markdown(media["date"])
            with columns[1]:
                st.markdown(media["source"])
            with columns[2]:
                st.markdown(media["headline"])
            with columns[3]:
                st.markdown(f'<a href="{media["url"]}" target="_blank">{media["url"]}</a>', unsafe_allow_html=True)
            with columns[4]:
                if st.button("Add to Case", key=f'add_media_evidence_{i}'):
                    add_evidence("Adverse Media", media["headline"])

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Displaying the risk score
        risk_score = adverse_media_data["Risk"]
        risk_class = f"stRiskScore stRiskScore-{risk_score}"

        st.markdown(f'<div class="{risk_class}">Risk Score: {risk_score} out of 5</div>', unsafe_allow_html=True)

    with selected_tab[3]:
        kyc_data = case_data["agent_outputs"]["KYC"]

        # Displaying the descriptive summary
        st.markdown('<div class="stSubHeader">KYC Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stSummary">{kyc_data["Reason"]}</div>', unsafe_allow_html=True)

        customer_images = []
        sanctioned_images = []
        for score, face1, face2 in kyc_data['Evidence']:
            st.markdown(f'<div class="stSubHeader">Facial Recognition Score: {score*100}%</div>', unsafe_allow_html=True)
            customer_images.append(Image.open(face1))
            sanctioned_images.append(Image.open(face2))

        col1, col2 = st.columns(2)

        with col1:
            for customer_image in customer_images:
                st.image(customer_image, caption='Customer Image', width=300)

        with col2:
            for sanctioned_image in sanctioned_images:
                st.image(sanctioned_image, caption='Similar Sanctioned Person', width=300)

    with selected_tab[4]:
        transaction_activity_data = case_data["agent_outputs"]["Transaction Activity"]

        # Displaying the descriptive summary
        st.markdown('<div class="stSubHeader">Transaction Activity Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stSummary">{transaction_activity_data["Reason"]}</div>', unsafe_allow_html=True)

        # Displaying the risky media information in a table using st.columns
        st.markdown('<div class="stSubHeader">Risky Transactions</div>', unsafe_allow_html=True)
        st.markdown('<div class="stRiskyMediaTable">', unsafe_allow_html=True)

        # Table header
        st.markdown('<div class="stRiskyMediaRow stRiskyMediaHeader">', unsafe_allow_html=True)
        columns = st.columns([1, 1, 2, 1])
        with columns[0]:
            st.markdown("ID")
        with columns[1]:
            st.markdown("Date")
        with columns[2]:
            st.markdown("Amount")
        with columns[3]:
            st.markdown("Action")
        st.markdown('</div>', unsafe_allow_html=True)

        # Table body
        for i, transaction in enumerate(transaction_activity_data["Evidence"]):
            st.markdown('<div class="stRiskyMediaRow stRiskyMediaBody">', unsafe_allow_html=True)
            columns = st.columns([1, 1, 2, 1])
            with columns[0]:
                st.markdown(transaction["Transaction ID"])
            with columns[1]:
                st.markdown(transaction["Transaction Date"])
            with columns[2]:
                st.markdown(transaction["Transaction Amount"])
            with columns[3]:
                if st.button("Add to Case", key=f'add_txn_evidence_{i}'):
                    add_evidence("Transaction Activity", f'{transaction["Transaction Amount"]} on {transaction["Transaction Date"]}')
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Displaying the risk score
        risk_score = adverse_media_data["Risk"]
        risk_class = f"stRiskScore stRiskScore-{risk_score}"

        st.markdown(f'<div class="{risk_class}">Risk Score: {risk_score} out of 5</div>', unsafe_allow_html=True)

    with selected_tab[5]:
        geolocation_data = case_data["agent_outputs"]["Geolocation"]
        # Displaying the descriptive summary
        st.markdown('<div class="stSubHeader">Geolocation Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stSummary">{geolocation_data["Reason"]}</div>', unsafe_allow_html=True)
        heat_map = create_geolocation_map([[evidence["datetime"], evidence["latitude"], evidence["longitude"]] for evidence in geolocation_data["Evidence"]])
        # Displaying the risk score
        risk_score = geolocation_data["Risk"]
        risk_class = f"stRiskScore stRiskScore-{risk_score}"
        st.markdown(f'<div class="{risk_class}">Risk Score: {risk_score} out of 5</div>', unsafe_allow_html=True)

    with selected_tab[6]:
        st.markdown('<div class="stSubHeader">Evidence</div>', unsafe_allow_html=True)

        # Table header
        st.markdown('<div class="stRiskyMediaRow stRiskyMediaHeader">', unsafe_allow_html=True)
        columns = st.columns([2, 2, 1])
        with columns[0]:
            st.markdown("Evidence Type")
        with columns[1]:
            st.markdown("Evidence ID")
        with columns[2]:
            st.markdown("Action")
        st.markdown('</div>', unsafe_allow_html=True)

        # Table body
        for i, (evidence_type, evidence_id) in enumerate(st.session_state["selected_evidence"]):
            st.markdown('<div class="stRiskyMediaRow stRiskyMediaBody">', unsafe_allow_html=True)
            columns = st.columns([1, 1, 2, 1])
            with columns[0]:
                st.markdown(evidence_type)
            with columns[1]:
                st.markdown(evidence_id)
            with columns[3]:
                st.button("Remove from Case", key=f'remove_evidence_{i}')
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    if case_data["Current Status"] == "Pending":
        with selected_tab[7]:
            st.markdown('<div class="stSubHeader">Upload New Information</div>', unsafe_allow_html=True)
            uploaded_files = st.file_uploader("Upload files for new information or data", accept_multiple_files=True)
            if st.button("Re-evaluate GenAI Agents"):
                st.write("Re-run the GenAI agents with the uploaded files.")
