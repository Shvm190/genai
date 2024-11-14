from openai import AzureOpenAI
import json
import os
import numpy as np
import pandas as pd


INPUT_SCENARIO = 'C:/Users/SSingh/Downloads/scenario1_transactions 3.csv'


def generate_data(scenario_data):
    """ Takes a pandas dataframe formatted scenario data with all columns and performs required formatting to be fed into the Agent"""
    colstokeep = ['transaction_id',
        'transaction_date_time',
        'transaction_amount',
        'description',
        'account_balance',
        'merchant_name',
        'merchant_location',
        'payment_method',
        'payment_channel',
        'geolocation',
        'authentication_method',
        'ip_address',
        'kyc_nationality',
        'kyc_id_type',
        'kyc_address',
        'kyc_occupation',
        'kyc_source_of_funds',
        'kyc_annual_income_range',
        'kyc_pep_status',
        'kyc_customer_since',
        'kyc_frequent_connection_country',
        'customer_id'
        ]

    # colstokeep = ["customer_id", "transaction_amount", "description", "transaction_date_time", "kyc_annual_income_range"]
    colstorename = {
        'description' : 'merchant_category'
        }
    
    scenario_data = scenario_data[colstokeep]
    scenario_data = scenario_data.rename(columns = colstorename)
    
    # Generate Dict in expected format
    dummy_data = {}
    for tran_row in scenario_data.items():
        dummy_data[tran_row[0]] = list(tran_row[1].values)

    # Treat any nans in dict to ensure it can be serialize
    dummy_data = {k: list(map(int, v)) if isinstance(v[0], (np.int64, np.int32)) else v for k, v in dummy_data.items()}  

    return dummy_data


def return_chat_prompt(agent_config, tran_data_dict):

    agent_prompt = [
        {
            'role': 'system',
            'content': f"Role : {agent_config['agent_role']} \n Working principle:  {agent_config['agent_working_principle']}"
        },
        {
            'role': 'user',
            'content': f"Task Requirement: {agent_config['task_requirement']} \n TRANSACTION DATA : \n {tran_data_dict}"
        }
    ]
    return agent_prompt


def invoke_agent(chat_prompt):
    
    print(os.environ)

    # Get Env Variables
    endpoint = os.getenv("AZURE_API_BASE", "https://genai-openai-tmquant.openai.azure.com/")  
    deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "63a57a259faa4a1d972d64a002f59adc")  
    api_version = os.getenv("AZURE_API_VERSION", "2024-02-15-preview")  

    print(f"endpoint {endpoint}, \napi_key={subscription_key}\napi_version={api_version}")

    # Initialize Azure OpenAI client with key-based authentication
    client = AzureOpenAI(  
        azure_endpoint=endpoint,  
        api_key=subscription_key,
        api_version=api_version
    )

    # Generate the completion  
    completion = client.chat.completions.create(  
        model=deployment,  
        messages=chat_prompt,
        max_tokens=800,
        temperature=0,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,  
        stop=None
    )

    return completion


def output_formatting(agent_response):
    resp_imp = agent_response.to_dict()["choices"][0]["message"]["content"]

    try:
        cleaned_json_string = resp_imp.strip('```json\n')
        resp_formatted = json.loads(cleaned_json_string)
        print(resp_formatted)
        flagged_transactions = resp_formatted['flagged_transactions']
        # customer_summary = {i:k for i, k in resp_formatted.items() if i in ['RISK', 'REASON']}
        customer_summary = resp_formatted['summary']
    except:
            print(resp_imp)
    
    return flagged_transactions, customer_summary


if __name__=='__main__':
    # Read Config
    with open("transaction_monitoring_agent/config.json", "r") as infile:
        agent_setup_cnfg = json.load(infile)
    
    # Get Tran Data
    raw_tran_df = pd.read_csv(INPUT_SCENARIO)

    # Get data in required format
    tran_dict = generate_data(raw_tran_df)

    agent_prompt = return_chat_prompt(agent_setup_cnfg, tran_dict)

    tran_agent_response = invoke_agent(agent_prompt)

    flagged_txn, overall_summary = output_formatting(tran_agent_response)
    print(flagged_txn, overall_summary)


