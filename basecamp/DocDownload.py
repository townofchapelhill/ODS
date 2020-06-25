############################################
# This program downloads all documents in  #
# each team of a specified account and     #
# places them in appropriate folders.      #
############################################

import requests
import json
import datetime
import secrets
import os

# manually change depending on which basecamp account desired to be used
global_token = secrets.friendly_access

# refresh url - manually change refresh token based on desired account
refresh_url = "https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token="+secrets.friendly_refresh+"&client_id=c51ec567174bffb69861a58385705a9140f35538&redirect_uri=http://www.townofchapelhill.org&client_secret="+secrets.client_secret

# check vault function 
def check_vault(doc, token, folder):
    
    if doc["uploads_count"] != 0:
        uploads_url = doc["uploads_url"]
        upload_request = requests.get(uploads_url, headers ={
            "Authorization": "Bearer " + token,
            "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
        })
        uploads = json.loads(upload_request.text)
        
        for k in range(len(uploads)):
            download = requests.get(uploads[k]["download_url"], headers={
                "Authorization": "Bearer " + token,
                "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
            })
              
            with open(folder+'/'+uploads[k]["filename"], 'wb') as f:
                f.write(download.content)
        
        
    if doc["vaults_count"] != 0:
        vaults_url = doc["vaults_url"]
        vaults_request = requests.get(vaults_url, headers ={
            "Authorization": "Bearer " + token,
            "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
        })
        vaults = json.loads(vaults_request.text)
        
        for l in range(len(vaults)):
            check_vault(vaults[l], token, folder)

# get json of projects/teams function
def get_projects(token):
    project_url = "https://3.basecampapi.com/3472161/projects.json"
    request = requests.get(project_url, headers={
        "Authorization": "Bearer " + token,
        "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
    })
    return json.loads(request.text)
    
def main():            
    # get current timestamp
    now = datetime.datetime.now()
    
    # print program start timestamp
    print(str(now) + '\n')
    
    projects = get_projects(global_token)
    
    # check if access token has expired
    if 'error' in projects:
        header = {"Content-Type": "application/json"}
        refresh_request = requests.post(refresh_url, headers=header)
        token = json.loads(refresh_request.text)["access_token"]
        projects = get_projects(token)
        
    # loop through projects/teams
    for i in range(len(projects)):
        print(projects[i]["name"])
        project_name = projects[i]["name"]
        
        # make folder for team if it doesn't already exist
        if not os.path.isdir(project_name):
            os.mkdir(project_name)
            
        # access list of documents for account associated with token in team at index i
        doc_url = projects[i]["dock"][5]["url"]
        doc_request = requests.get(doc_url, headers={
            "Authorization": "Bearer " + token,
            "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
        })
        
        # set document json to variable
        documents = json.loads(doc_request.text)
        
        # call function to check vault and download files
        check_vault(documents, token, project_name)

main()
