### functions for accessing Sierra resources

import secrets
import requests
import json

def get_token():
    url = "https://catalog.chapelhillpubliclibrary.org/iii/sierra-api/v5/token"

    # Get the API key from secrets file
    header = {"Authorization": "Basic " + str(secrets.sierra_api), "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, headers=header)
    if response.status_code != 200:
        print(f'get Sierra Token failed with code {response.status_code} ')
        exit(1)
    json_response = json.loads(response.text)
    return json_response["access_token"]

# Function to get the API token
def get_sierra_token():
    url = "https://catalog.chapelhillpubliclibrary.org/iii/sierra-api/v5/token"
    # Get the API key from secrets.py
    header = {"Authorization": "Basic " + str(secrets.sierra_api), "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, headers=header)
    if response.status_code != 200:
        print(f'get Sierra Token failed with code {response.status_code} ')
        exit(1)
    json_response = json.loads(response.text)
    return json_response["access_token"]