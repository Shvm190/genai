
import os  
from openai import AzureOpenAI  
from azure.identity import DefaultAzureCredential, get_bearer_token_provider  

endpoint = os.getenv("ENDPOINT_URL", "https://genai-openai-tmquant.openai.azure.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")  

# Initialize Azure OpenAI client with Entra ID authentication
token_provider = get_bearer_token_provider(  
    DefaultAzureCredential(),  
    "https://cognitiveservices.azure.com/.default"  
)  

client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    azure_ad_token_provider=token_provider,  
    api_version="2024-05-01-preview",  
)  

completion = client.chat.completions.create(  
    model=deployment,  
    messages=[
{
"role": "system",
"content": "You are an AI assistant that helps people find information."
}
],  
    past_messages=10,  
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,  
    stop=None,  
    stream=False  
)  

print(completion.to_json())  
