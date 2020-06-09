################################################
# This program prints all the todos/todosets   #
# for a specified team for a specified account #
################################################

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

# url is for CHOD team (manually change for desired team)
project_url = "https://3.basecampapi.com/3472161/buckets/2528552/todosets/365963496/todolists.json"

# get json of projects/teams function
def get_todos(token):
    request = requests.get(project_url, headers={
        "Authorization": "Bearer " + token,
        "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
    })
    return json.loads(request.text)

# main function
def main():
    # set json file to variable
    todo_set = get_todos(global_token)
    
    # check if access token has expired
    if 'error' in todo_set:
        refresh_url = "https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token="+secrets.test_refresh+"&client_id=c51ec567174bffb69861a58385705a9140f35538&redirect_uri=http://www.townofchapelhill.org&client_secret="+secrets.client_secret
        header = {"Content-Type": "application/json"}
        refresh_request = requests.post(refresh_url, headers=header)
        token = json.loads(refresh_request.text)["access_token"]
        todo_set = get_todos(token)
    
    # go through json todo sets, skipping completed sets
    for i in range(len(todo_set)):
        
        if todo_set[i]["completed"]:
            continue
        
        # print name of todo set
        print(todo_set[i]["name"])
        
        # use token again to get json todo list of current todo set
        request = requests.get(todo_set[i]["todos_url"], headers={
            "Authorization": "Bearer " + token,
            "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
        })
        
        # set json todo list to variable
        todo_list = json.loads(request.text)
        
        # print todo lists
        for i in range(len(todo_list)):
            print("---> " + todo_list[i]["content"])
        
        print('\n')
    
    print(str(now))

main()