######################################################
##This script posts all schedule entries in the     ##
##Friendly Robot account's teams into the Automation##
##for the people's schedule                         ##
######################################################

import requests
import json
import csv
import datetime
import secrets

now = datetime.datetime.now()

# print program start timestamp
print(str(now) + '\n')

# manually change depending on which basecamp account desired to be used
global_token = secrets.friendly_access

# refresh url - manually change refresh token based on desired account
refresh_url = "https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token="+secrets.friendly_refresh+"&client_id=c51ec567174bffb69861a58385705a9140f35538&redirect_uri=http://www.townofchapelhill.org&client_secret="+secrets.client_secret

# schedule url - manually change depending on which team you want to post to
schedule_url = "https://3.basecampapi.com/3472161/buckets/6505832/schedules/899540291/entries.json"

# get json of projects/teams function
def get_projects(token):
    project_url = "https://3.basecampapi.com/3472161/projects.json"
    request = requests.get(project_url, headers={
        "Authorization": "Bearer " + token,
        "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
    })
    return json.loads(request.text)
 
def main(): 
    # set json file to variable
    projects = get_projects(global_token)
    
    # check if access token has expired
    if 'error' in projects:
        header = {"Content-Type": "application/json"}
        refresh_request = requests.post(refresh_url, headers=header)
        token = json.loads(refresh_request.text)["access_token"]
        projects = get_projects(token)
        
    # go through projects
    for i in range(len(projects)):
        print(projects[i]["name"])
        # exclude this team's entries
        if projects[i]["name"] == "Automation For The People":
            continue
        
        # get the entries
        entry_url = projects[i]["dock"][3]["url"][:-5]+"/entries.json"
        request2 = requests.get(entry_url, headers={
            "Authorization": "Bearer " + token,
            "User-Agent": "ToCH Basecamp Integration (snguyen@townofchapelhill.org)"
        })
    
        entries = json.loads(request2.text)
        
        # post each entry
        for j in range(len(entries)):
            print('\t' + entries[j]["title"])
            
            payload = {
              "summary" : entries[j]["summary"],
              "starts_at": entries[j]["starts_at"],
              "ends_at": entries[j]["ends_at"],
              "description": entries[j]["description"],
              "all_day": entries[j]["all_day"],
            }
            headers = {"Authorization": "Bearer " + token,
                "User-Agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)",
                "Content-Type":"application/json"}
            
            request = requests.post(schedule_url, data=json.dumps(payload), headers=headers)
      
    print('\n' + str(datetime.datetime.now()))
    
main()

