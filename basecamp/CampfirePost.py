###################################################
# This program sends a schedule entries message   #
# from every team of the specified account to the # 
# specified campfire.                             #
###################################################

#####################################################################################################################
#                                       EXAMPLE CAMPFIRE URLS                                                       #
# automation for the people campfire: https://3.basecampapi.com/3472161/buckets/6505832/chats/899540284/lines.json  #
# api testing campfire: https://3.basecampapi.com/3472161/buckets/6806445/chats/943497859/lines.json                #
#####################################################################################################################

import requests
import json
import csv
import datetime
import secrets

# manually change depending on which basecamp account desired to be used
global_token = secrets.friendly_access

# manually change depending on which team campfire to message (refer to example urls)
campfire_url="https://3.basecampapi.com/3472161/buckets/6505832/chats/899540284/lines.json"

# refresh url - manually change refresh token based on desired account
refresh_url = "https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token="+secrets.friendly_refresh+"&client_id=c51ec567174bffb69861a58385705a9140f35538&redirect_uri=http://www.townofchapelhill.org&client_secret="+secrets.client_secret

# get json of projects/teams function
def get_projects(token):
    project_url = "https://3.basecampapi.com/3472161/projects.json"
    request = requests.get(project_url, headers={
        "Authorization": "Bearer " + token,
        "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
    })
    return json.loads(request.text)

# send message function
def send_message(message, token,url):
    
    payload = {"content": message}
    headers = {"Authorization": "Bearer " + token,
        "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)",
        "Content-Type":"application/json"}
    
    request = requests.post(url, data=json.dumps(payload), headers=headers)
      
# main function
def main():
    now = datetime.datetime.now()
    
    # print program start timestamp
    print(str(now) + '\n')
    
    # set json file to variable
    projects = get_projects(global_token)
    
    # check if access token has expired
    if 'error' in projects:
        header = {"Content-Type": "application/json"}
        refresh_request = requests.post(refresh_url, headers=header)
        token = json.loads(refresh_request.text)["access_token"]
        projects = get_projects(token)
        
    # create message variable to be sent
    message = "Schedule Entries: \n"
    
    # go through projects and append schedule entries to message
    for i in range(len(projects)):
        
        message += str(i+1) + ". " + projects[i]["name"] + '\n'
        entry_url = projects[i]["dock"][3]["url"][:-5]+"/entries.json"
        request2 = requests.get(entry_url, headers={
            "Authorization": "Bearer " + token,
            "User-Agent": "ToCH Basecamp Integration (snguyen@townofchapelhill.org)"
        })
        
        entries = json.loads(request2.text)
        
        for j in range(len(entries)):
            message += '\t'+ entries[j]["title"] + " - " + entries[j]["starts_at"] + '\n'
    
    # print the message to be sent   
    print(message)
    
    # send message
    send_message(message, token, campfire_url)
    
    print('\n' + str(datetime.datetime.now()))

main()

