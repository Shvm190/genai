
import os, sys

os.environ["AZURE_API_KEY"] = "KEY"
os.environ["AZURE_API_BASE"] = "https://genai-openai-tmquant.openai.azure.com/"
os.environ["AZURE_API_VERSION"] = "2024-02-15-preview"

from dotenv import dotenv_values, load_dotenv
from ast import literal_eval
import json

load_dotenv()

config=dotenv_values(".env")
azure_endpoint = os.environ.get("AZURE_API_BASE")
openai_api_key = os.environ.get("AZURE_API_KEY")
openai_api_version = os.environ.get("AZURE_API_VERSION")
model_name="azure/gpt-4o"

import dspy

lm = dspy.LM('azure/gpt-4o')
dspy.configure(lm=lm)

IP_MAPPING = {
    "54.192.111.6": "Manchester, UK",
    "218.145.0.59": "Manchester, UK",
    "195.184.190.13": "London, UK",
    "222.181.250.193": "Paris, France",
    "227.167.54.159": "Budapest, Hungary",
    "15.127.207.249": "La Paz, Bolivia",
    "44.20.172.143": "Chicago, United States",
    "97.37.242.205": "Hanoi, Vietnam",
    "179.224.188.48": "Johanessburg, South Africa",
    "76.67.210.14": "Gabadone, Botswana",
}

class GetIP:
    name = "GetIP"
    input_variable = "ip"
    desc = "takes an ip and returns location"

    def __init__(self):
        pass
   
    def __call__(self, ip):
        return IP_MAPPING[ip]
    

mytool = GetIP()


class BasicQA(dspy.Signature):
    """
   Given a list of ip addresses check if their locations are suspicious or not based on 
    the clustering of their locations. Return a risk rating of these transactions being fraudlent as follows:
    - 5: High Risk - locations are very widely spready across the globe, and unlikely to be possible in a short space of time.
    - 4: Medium Risk - locations are spread across a number of different countries, but those countries are in the same wider region.
    - 3: Medium Risk - locations are spread across a number of different countries, but those countries border each other.
    - 2: Low Risk - locations all originate from the same country, but different regions or cities.
    - 1: No Risk - locations all originate from the same city in the same country.
    """
    question = dspy.InputField()
    answer = dspy.OutputField(desc="in JSON format: {'Risk': '1-5', 'Reason':'xxx'}")


react_module = dspy.ReAct(BasicQA, tools=[mytool])


if __name__ == "__main__":
    
    ip_list = sys.argv[1:]
    p = react_module(question=", ".join(ip_list))

    print(json.dumps(literal_eval(p.answer), indent=True))
