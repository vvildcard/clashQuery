# python 3.7
# A script to query the Clash Royale API and detect inactive players in your clan. 
# by vvildcard
# 2018/11/01
#
# Notes:
#   You MUST have a worksheet named 'clanDonations.xlsx' in the script's working directory.
#   The script only reads the first worksheet.
#   The first worksheet must be named as the clan's ID.
#
# To Do:
#   User input for clan ID
#   Save clan ID as the worksheet name
#   Handle a missing workbook
#   Handle a worksheet named 'Sheet 1'
#   Add help
#   Add other indicators of activity (war participation, etc)


# -----------------
# Import modules // Define functions // Set variables
# -----------------

import requests, datetime, os
from openpyxl import load_workbook

def getClanID():
    clanID = input("Input your Clan ID: ")
    while True:
        if clanID[0] == "#":  # Remove the #
            clanID = clanID[1:]
        try:
            clanIDSearch = requests.request("GET", url+"clans/%23"+clanID, headers=headers).json()
            break
        except KeyError:
            clanID = input("Clan not found. Try again: ")
    print("Found clan: " + str(clanIDSearch['name']))
    return(clanID)

def getToken():
    tempToken = input("Missing token.\n"
                  "Note: Your token will be stored as plain-text in a token.txt.\n"
                  "If you don't have a token, get one here: developer.clashroyale.com"
                  "Input your token: ")
    while tempToken == '':  # Ask again if the token wasn't given
        input("Input your token: ")
    testToken = tokenTest(tempToken)
    if testToken == True:
        token = tempToken
    tokenFile = open('token.txt', 'w+')  # Create token.txt
    tokenFile.write(token)  # Write the token into the file
    tokenFile.close()
    return(token)

def tokenTest(token):
    tokenTestHeaders = {"Authorization": "Bearer: " + token}
    try:
        tokenTestRequest = requests.get(url+"cards", headers=tokenTestHeaders)  # Test the token
        tokenTestRequest.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error!", err)
    return(True)

date = datetime.datetime.now()
todayDate = date.strftime("%Y"+"-"+"%m"+"-"+"%d")
while True:
    try:
        token = open('token.txt', 'r')
        break
    except FileNotFoundError:
        getToken()
url = "https://api.clashroyale.com/v1/"
headers = {"Authorization": "Bearer: "+token.read()}


# -----------------
# Load the data
# -----------------

# Load the Spreadsheet
while True:
    try:
        wb = load_workbook("clanDonations.xlsx", data_only=True)
        break  # Workbook found
    except FileNotFoundError:
        cwd = os.getcwd()
        print("Missing workbook.\n"
              "If you already have a workbook, place it here:"
              + str(cwd))
        from openpyxl import Workbook
        wb = Workbook()  # Create a workbook
        ws = wb.active  # Set the active sheet
        ws.title = getClanID()  # Set the Sheet name to the Clan ID
        ws['A1'] = "Name"
        ws['B1'] = "Role"
        ws['C1'] = "LastSeen"
        wb.save("clanDonations.xlsx")
clanID = wb.sheetnames[0]
ws = wb[clanID]

# Get clan info from the API
clanMembers = requests.request("GET", url+"clans/%23"+clanID+"/members", headers=headers).json()
# print(clanMembers)


# -----------------
# Parse and prep the data
# -----------------

# Add a new column for today. Skip if today's date is already recorded.
if ws["D1"].value != todayDate:
    ws.insert_cols(4)
    ws["D1"] = todayDate

#  Make a dictionary
#  like this: [{'member1': ['elder', '2018-10-28', '100']}, {'member2': ['member', '2018-10-26', '0']}]
tempDict = {}
for member in clanMembers['items']:
    tempDict[member['name']] = [member['role'], todayDate, member['donations']]
# print(tempDict); print("\n\n")

memberList = []
for i in range(1, ws.max_row):
    memberList.append(str(ws.cell(row=i+1, column=1).value))
# print(memberList)

# Add new members
for member in tempDict:
    # print(member)
    if member not in memberList:
        ws.cell(row=ws.max_row+1, column=1).value = str(member)


# -----------------
# Merge the data
# -----------------

# Search for each member and update their role, last seen date and donations
for member in tempDict:
    # print("member: " + str(member) + "; data: " + str(tempDict[member]))
    for i in range(1, ws.max_row):
        # print("Search: " + str(ws.cell(row=i, column=1).value))
        i += 1
        if str(ws.cell(row=i, column=1).value) == str(member):
            # print(ws.cell(row=i, column=1).value)
            ws.cell(row=i, column=2).value = tempDict[member][0]    # role
            ws.cell(row=i, column=3).value = tempDict[member][1]    # lastSeen
            ws.cell(row=i, column=4).value = tempDict[member][2]    # donations


token.close()
wb.save("clanDonations.xlsx")
wb.close()