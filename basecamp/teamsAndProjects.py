######################################################
##This script extracts all projects/teams in the    ##
##Friendly Robot account and organizes the todos in ##
##each team into a csv file.                        ##
######################################################

import requests
import json
import csv
import datetime
import secrets

now = datetime.datetime.now()

# print program start timestamp
print(str(now) + '\n')

# open csv file
basecamp_bot = open('basecamp_bot.csv', 'w')
writer = csv.writer(basecamp_bot)
writer.writerow(['Team', 'Todo-set', 'To-do'])

# manually change depending on which basecamp account desired to be used
global_token = secrets.friendly_access

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
    
# main function
def main():
    # set json file to variable
    projects = get_projects(global_token)
    
    # check if access token has expired
    if 'error' in projects:
        header = {"Content-Type": "application/json"}
        refresh_request = requests.post(refresh_url, headers=header)
        token = json.loads(refresh_request.text)["access_token"]
        projects = get_projects(token)
    
    row = []
    message = ""
    
    # go through projects
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
        
        # print("Schedule Entries: \n" + message)
        if(projects[i]["purpose"] == "team" or projects[i]["purpose"] == "topic"):
            
            row.append(projects[i]["name"])
            
            # get url for todosets
            todoset_url = projects[i]["dock"][2]["url"][:-5] + "/todolists.json"
            # print(url+"\n")
            request2 = requests.get(todoset_url, headers={
            "Authorization": "Bearer " + token,
            "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
            })
            
            todo_set = json.loads(request2.text)
    
            # go through json todo sets, skipping completed sets
            for j in range(len(todo_set)):
                
                if todo_set[j]["completed"]:
                    continue
                
                # print name of todo set
                if not row:
                    row.append(projects[i]["name"])
                row.append(todo_set[j]["name"])
                
                # use token again to get json todo list of current todo set
                request3 = requests.get(todo_set[j]["todos_url"], headers={
                    "Authorization": "Bearer " + token,
                    "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
                })
                
                # set json todo list to variable
                todo_list = json.loads(request3.text)
                
                if not todo_list:
                    writer.writerow(row)
                    row = []
                    continue
                
                for k in range(len(todo_list)):
                    if not row:
                        row.append(projects[i]["name"])
                        row.append(todo_set[j]["name"])
                    row.append(todo_list[k]["content"])
                    writer.writerow(row)
                    row = []
    
    basecamp_bot.close()
    
    # print program end timestamp
    print('\n' + str(now))

main()