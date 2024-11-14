from openai import AzureOpenAI
import json
import os
import numpy as np
import pandas as pd


INPUTS = 'aggregator_agent/input_example.json'


def return_chat_prompt(agent_config, feeder_resp_dict):

    agent_prompt = [
        {
            'role': 'system',
            'content': f"Role : {agent_config['agent_role']} \n Working principle:  {agent_config['agent_working_principle']}"
        },
        {
            'role': 'user',
            'content': f"Task Requirement: {agent_config['task_requirement']} \n Feeder Agent Responses : \n {feeder_resp_dict}"
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
    
    return resp_imp


if __name__=='__main__':
    # Read Config
    with open("aggregator_agent/config.json", "r") as infile:
        agent_setup_cnfg = json.load(infile)

    # Get Response from feeder AI Agents
    with open(INPUTS, "r") as infile:
        feeder_agent_response = json.load(infile)

    agent_prompt = return_chat_prompt(agent_setup_cnfg, feeder_agent_response)

    aggregator_agent_response = invoke_agent(agent_prompt)

    aggregator_agent_response_f = output_formatting(aggregator_agent_response)
    print(aggregator_agent_response_f)


