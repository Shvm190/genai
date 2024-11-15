DATA = {
    "Case ID": [1, 2, 3, 4, 5, 6, 7],
    "Customer Name": ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Charlie Davis", "Eva Green", "Frank Harris"],
    "Date Created": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05", "2023-01-06", "2023-01-07"],
    "RAG Status": ["Red", "Amber", "Green", "Red", "Green", "Amber", "Red"],
    "Current Status": ["Open", "Pending", "Closed", "Pending", "Open", "Closed", "Open"],
    "Assigned Operator": ["-", "-", "-", "-", "-", "-", "-"],
    "Priority": [1, 2, 3, 2, 1, 3, 1],
    "Alerts": [
        [
            {
                "alert_id": "A0001",
                "alert_date": "2024-10-05",
                "risk_score": 340,
                "alert_description": "Suspicious large deposit significantly higher than declared income",
                "individual_rules_triggered": ["Large Cross Border Deposits", "Unexplained Source of Funds"]
            },
            {
                "alert_id": "A0002",
                "alert_date": "2024-10-12",
                "risk_score": 250,
                "alert_description": "Large transfer to an unknown recipient",
                "individual_rules_triggered": ["International Transfer Suspicion to Tax Haven", "Sanction List Match"]
            },
            {
                "alert_id": "A0003",
                "alert_date": "2024-10-20",
                "risk_score": 420,
                "alert_description": "Crypto transaction, higher risk",
                "individual_rules_triggered": ["Crypto Transaction Risk", "PEP List Match"]
            },
            {
                "alert_id": "A0004",
                "alert_date": "2024-10-15",
                "risk_score": 380,
                "alert_description": "Frequent small transfers to different accounts",
                "individual_rules_triggered": ["Frequent Small Transfers", "Large Cash Deposit Flag"]
            },
            {
                "alert_id": "A0005",
                "alert_date": "2024-10-03",
                "risk_score": 300,
                "alert_description": "Unexplained deposits from foreign countries",
                "individual_rules_triggered": ["Structuring Transfers Suspicion", "Unexplained Source of Funds"]
            }
        ],
        [], [], [], [], [], []
    ],
    "Case Details": [
        {
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
                        'Type': 'Gift',
                        "Transaction Date": "5/19/2024 8:35",
                    },
                    {
                        "Risk": 5,
                        "Reason for Flagging": "Large money deposit significantly higher than declared income",
                        "Transaction ID": "T170",
                        "Transaction Amount": 250000.0,
                        'Type': 'Crypto',
                        "Transaction Date": "8/29/2024 18:44",
                    },
                    {
                        "Risk": 3,
                        "Reason for Flagging": "Crypto transaction, higher risk",
                        "Transaction ID": "T171",
                        "Transaction Amount": 2922.76,
                        'Type': 'Crypto',
                        "Transaction Date": "9/8/2024 10:44",
                    },
                    {
                        "Risk": 3,
                        "Reason for Flagging": "Crypto transaction, higher risk",
                        "Transaction ID": "T172",
                        "Transaction Amount": 1448.86,
                        'Type': 'Crypto',
                        "Transaction Date": "8/21/2024 17:12",
                    },
                    {
                        "Risk": 3,
                        "Reason for Flagging": "Crypto transaction, higher risk",
                        "Transaction ID": "T173",
                        "Transaction Amount": 2998.37,
                        'Type': 'Crypto',
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
        },
        {"Overall": {'Risk': 4, 'Reason': 'The overall risk assessment is high due to the significant concern raised by the geotag screener. The IP addresses being located in widely dispersed geographical locations (Manchester, UK; Johannesburg, South Africa; and Hanoi, Vietnam) indicate a high risk of fraudulent activity, resulting in a risk score of 5 from the geotag screener. While the transaction screening agent reported a low level of scrutiny with a risk score of 2, and the adverse media screener found no concerning articles with a risk score of 1, the potential for fraud indicated by the geotag screener significantly elevates the overall risk. Therefore, the unified risk score is 4.'}, 'Adverse Media': {'Risk': 5, 'Reason': 'The articles are recent (2024), from reliable sources, and involve serious allegations that suggest suspicious activities with risk level 3.', 'Evidence': [{'date': '', 'source': '', 'headline': '', 'url': ''}]}, 'Geolocation': {'Risk': 5, 'Reason': 'The IP addresses are located in geographies that raise a risk flag with risk level 3.', 'Evidence': ['192.168.1.60', '172.16.0.69']}, 'Transaction Activity': {'Risk': 4, 'Reason': "The customer's transactions suggest possible money laundering or fraud, with a risk level of 3.", 'Evidence': [{'Risk': 3, 'Reason for Flagging': 'Suspicious large deposit significantly higher than declared income', 'Transaction ID': 'T3569', 'Transaction Amount': 28137, 'Transaction Date': '5/19/2024 5:13'}]}, 'KYC': {'Risk': 3, 'Reason': 'The customer exhibits risk factors indicating overall risk level 3 based on KYC information.', 'Evidence': [{'Risk_Factor': 'PEP_Status', 'Status': 'No'}, {'Risk_Factor': 'Sanction_List', 'Status': 'No'}], 'Details': {'Customer_ID': '906875318', 'Full_Name': 'Customer 391', 'Source_of_Funds': 'Salary, Investments', 'Occupation': 'Software Engineer', 'KYC_Review_Date': '2024-09-23'}}},
        {"Overall": {'Risk': 4, 'Reason': 'The overall risk assessment is high due to the significant concern raised by the geotag screener. The IP addresses being located in widely dispersed geographical locations (Manchester, UK; Johannesburg, South Africa; and Hanoi, Vietnam) indicate a high risk of fraudulent activity, resulting in a risk score of 5 from the geotag screener. While the transaction screening agent reported a low level of scrutiny with a risk score of 2, and the adverse media screener found no concerning articles with a risk score of 1, the potential for fraud indicated by the geotag screener significantly elevates the overall risk. Therefore, the unified risk score is 4.'}, 'Adverse Media': {'Risk': 1, 'Reason': 'The articles are recent (2024), from reliable sources, and involve serious allegations that suggest suspicious activities with risk level 2.', 'Evidence': [{'date': '', 'source': '', 'headline': '', 'url': ''}]}, 'Geolocation': {'Risk': 5, 'Reason': 'The IP addresses are located in geographies that raise a risk flag with risk level 2.', 'Evidence': ['192.168.1.248', '172.16.0.213']}, 'Transaction Activity': {'Risk': 2, 'Reason': "The customer's transactions suggest possible money laundering or fraud, with a risk level of 2.", 'Evidence': [{'Risk': 3, 'Reason for Flagging': 'Unexplained deposits from foreign countries', 'Transaction ID': 'T6269', 'Transaction Amount': 1390, 'Transaction Date': '5/19/2024 6:55'}]}, 'KYC': {'Risk': 2, 'Reason': 'The customer exhibits risk factors indicating overall risk level 2 based on KYC information.', 'Evidence': [{'Risk_Factor': 'PEP_Status', 'Status': 'No'}, {'Risk_Factor': 'Sanction_List', 'Status': 'No'}], 'Details': {'Customer_ID': '264618268', 'Full_Name': 'Customer 198', 'Source_of_Funds': 'Salary, Investments', 'Occupation': 'Software Engineer', 'KYC_Review_Date': '2024-09-6'}}},
        {"Overall": {'Risk': 4, 'Reason': 'The overall risk assessment is based on the synthesis of multiple factors. The transaction screening agent identified a low level of scrutiny with a risk score of 2 due to a couple of large transactions, one just below the reporting threshold and another involving a country with moderate risk. The adverse media screener found no articles relating to Shivam Singh, resulting in a low risk score of 1. However, the geotag screener identified a high risk of fraudulent activity with a risk score of 5 due to IP addresses located in widely dispersed geographical locations (Manchester, UK; Johannesburg, South Africa; and Hanoi, Vietnam). The significant discrepancy in geographical locations raises concerns about potential fraudulent behavior, leading to an overall elevated risk score of 4.'}, 'Adverse Media': {'Risk': 5, 'Reason': 'The articles are recent (2024), from reliable sources, and involve serious allegations that suggest suspicious activities with risk level 1.', 'Evidence': [{'date': '', 'source': '', 'headline': '', 'url': ''}]}, 'Geolocation': {'Risk': 1, 'Reason': 'The IP addresses are located in geographies that raise a risk flag with risk level 1.', 'Evidence': ['192.168.1.183', '172.16.0.173']}, 'Transaction Activity': {'Risk': 1, 'Reason': "The customer's transactions suggest possible money laundering or fraud, with a risk level of 1.", 'Evidence': [{'Risk': 4, 'Reason for Flagging': 'Repeated transfers close to the account limit', 'Transaction ID': 'T6791', 'Transaction Amount': 2505, 'Transaction Date': '5/19/2024 6:10'}]}, 'KYC': {'Risk': 1, 'Reason': 'The customer exhibits risk factors indicating overall risk level 1 based on KYC information.', 'Evidence': [{'Risk_Factor': 'PEP_Status', 'Status': 'No'}, {'Risk_Factor': 'Sanction_List', 'Status': 'No'}], 'Details': {'Customer_ID': '628812487', 'Full_Name': 'Customer 125', 'Source_of_Funds': 'Salary, Investments', 'Occupation': 'Software Engineer', 'KYC_Review_Date': '2024-09-22'}}},
        {"Overall": {'Risk': 4, 'Reason': "The overall risk assessment is high due to the following factors:\n  1. Transaction Screening: The customer's transaction history shows a couple of activities that warrant a low level of scrutiny, with two large transactions, one just below the reporting threshold and another involving a country with moderate risk. This results in a low suspicion score of 2.\n  2. Adverse Media Screening: No adverse media articles were found relating to Shivam Singh, resulting in a low risk score of 1.\n  3. Geo-location Risk: The IP addresses are located in widely dispersed geographical locations (Manchester, UK; Johannesburg, South Africa; and Hanoi, Vietnam), indicating a high risk of fraudulent activity, resulting in a high risk score of 5.\n\n  Despite the low risk from transaction and adverse media screening, the high risk from geo-location significantly increases the overall risk score to 4."}, 'Adverse Media': {'Risk': 2, 'Reason': 'The articles are recent (2024), from reliable sources, and involve serious allegations that suggest suspicious activities with risk level 3.', 'Evidence': [{'date': '', 'source': '', 'headline': '', 'url': ''}]}, 'Geolocation': {'Risk': 3, 'Reason': 'The IP addresses are located in geographies that raise a risk flag with risk level 3.', 'Evidence': ['192.168.1.159', '172.16.0.159']}, 'Transaction Activity': {'Risk': 4, 'Reason': "The customer's transactions suggest possible money laundering or fraud, with a risk level of 3.", 'Evidence': [{'Risk': 1, 'Reason for Flagging': 'Frequent international transfers without business justification', 'Transaction ID': 'T3202', 'Transaction Amount': 13762, 'Transaction Date': '5/19/2024 10:28'}]}, 'KYC': {'Risk': 3, 'Reason': 'The customer exhibits risk factors indicating overall risk level 3 based on KYC information.', 'Evidence': [{'Risk_Factor': 'PEP_Status', 'Status': 'No'}, {'Risk_Factor': 'Sanction_List', 'Status': 'No'}], 'Details': {'Customer_ID': '398553267', 'Full_Name': 'Customer 411', 'Source_of_Funds': 'Salary, Investments', 'Occupation': 'Software Engineer', 'KYC_Review_Date': '2024-09-30'}}},
        {"Overall": {'Risk': 4, 'Reason': "The overall risk assessment is high due to the following factors:\n  1. Transaction Screening: The customer's transaction history shows a couple of activities that warrant a low level of scrutiny, with two large transactions, one just below the reporting threshold and another involving a country with moderate risk. This results in a low suspicion score of 2.\n  2. Adverse Media Screening: No adverse media articles were found relating to Shivam Singh, resulting in a low risk score of 1.\n  3. Geo-location Risk: The IP addresses are located in widely dispersed geographical locations (Manchester, UK; Johannesburg, South Africa; and Hanoi, Vietnam), indicating a high risk of fraudulent activity, resulting in a high risk score of 5.\n\nThe high risk score from the geo-location screener significantly impacts the overall risk assessment, leading to a unified risk score of 4."}, 'Adverse Media': {'Risk': 1, 'Reason': 'The articles are recent (2024), from reliable sources, and involve serious allegations that suggest suspicious activities with risk level 1.', 'Evidence': [{'date': '', 'source': '', 'headline': '', 'url': ''}]}, 'Geolocation': {'Risk': 5, 'Reason': 'The IP addresses are located in geographies that raise a risk flag with risk level 1.', 'Evidence': ['192.168.1.207', '172.16.0.209']}, 'Transaction Activity': {'Risk': 2, 'Reason': "The customer's transactions suggest possible money laundering or fraud, with a risk level of 1.", 'Evidence': [{'Risk': 4, 'Reason for Flagging': 'Suspicious large deposit significantly higher than declared income', 'Transaction ID': 'T4207', 'Transaction Amount': 30546, 'Transaction Date': '5/19/2024 4:12'}]}, 'KYC': {'Risk': 1, 'Reason': 'The customer exhibits risk factors indicating overall risk level 1 based on KYC information.', 'Evidence': [{'Risk_Factor': 'PEP_Status', 'Status': 'No'}, {'Risk_Factor': 'Sanction_List', 'Status': 'No'}], 'Details': {'Customer_ID': '527410511', 'Full_Name': 'Customer 699', 'Source_of_Funds': 'Salary, Investments', 'Occupation': 'Software Engineer', 'KYC_Review_Date': '2024-09-12'}}},
        {"Overall": {'Risk': 4, 'Reason': 'The overall risk assessment is high due to the significant concern raised by the geotag screener. The IP addresses associated with the customer are located in widely dispersed geographical locations (Manchester, UK; Johannesburg, South Africa; and Hanoi, Vietnam), which is indicative of a high risk of fraudulent activity. While the transaction screening agent reported a low level of scrutiny with a risk score of 2, and the adverse media screener found no negative articles related to the customer, the high risk from the geotag screener significantly elevates the overall risk score.'}, 'Adverse Media': {'Risk': 4, 'Reason': 'The articles are recent (2024), from reliable sources, and involve serious allegations that suggest suspicious activities with risk level 3.', 'Evidence': [{'date': '', 'source': '', 'headline': '', 'url': ''}]}, 'Geolocation': {'Risk': 2, 'Reason': 'The IP addresses are located in geographies that raise a risk flag with risk level 3.', 'Evidence': ['192.168.1.165', '172.16.0.56']}, 'Transaction Activity': {'Risk': 3, 'Reason': "The customer's transactions suggest possible money laundering or fraud, with a risk level of 3.", 'Evidence': [{'Risk': 2, 'Reason for Flagging': 'Frequent small transfers to different accounts', 'Transaction ID': 'T6432', 'Transaction Amount': 26518, 'Transaction Date': '5/19/2024 8:19'}]}, 'KYC': {'Risk': 3, 'Reason': 'The customer exhibits risk factors indicating overall risk level 3 based on KYC information.', 'Evidence': [{'Risk_Factor': 'PEP_Status', 'Status': 'No'}, {'Risk_Factor': 'Sanction_List', 'Status': 'No'}], 'Details': {'Customer_ID': '366733522', 'Full_Name': 'Customer 844', 'Source_of_Funds': 'Salary, Investments', 'Occupation': 'Software Engineer', 'KYC_Review_Date': '2024-09-12'}}},
    ],
}