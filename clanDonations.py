# python 3.7
# A script to query the Clash Royale API and detect inactive players in your clan. 
# by vvildcard
# 2018/11/01
#
# Notes:
#   You MUST have a worksheet named 'memberDonations.xlsx' in the script's working directory.
#   You MUST have a file named 'token.txt' in the script's working directory.
#   The script only reads the first worksheet.
#   The first worksheet must be named as the clan's ID.
#
# To Do:
#   User input for clan ID
#   Save clan ID as the worksheet name
#   Handle a missing workbook
#   Handle a worksheet named 'Sheet 1'
#   Add help

# -----------------
# Import modules // Define Functions // Set some variables
# -----------------

import requests, datetime, openpyxl, string
from openpyxl import load_workbook

def index_to_col(index):
    return string.ascii_uppercase[index]

def excel_to_dict(excel_path, headers=[]):
    wb = openpyxl.load_workbook(excel_path)
    ws = wb["Sheet1"]
    result_dict = []
    for row in range(2, ws.max_row+1):
        line = dict()
        for header in headers:
            cell_value = ws[index_to_col(headers.index(header)) + str(row)].value
            if type(cell_value) is int:
                cell_value = str(cell_value)
            elif cell_value is None:
                cell_value = ''
            line[header] = cell_value
        result_dict.append(line)
    return result_dict

date = datetime.datetime.now()
todayDate = date.strftime("%Y"+"-"+"%m"+"-"+"%d")
token = open('token.txt', 'r')
url = "https://api.clashroyale.com/v1/"
headers = {"Authorization": "Bearer: "+token.read()}


# -----------------
# Load the data
# -----------------
wb = load_workbook("memberDonations.xlsx", data_only=True)
clan = wb.sheetnames[0]
ws = wb[clan]
clanMembers = requests.request("GET", url+"clans/%23"+clan+"/members", headers=headers).json()
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


#   	str(todayDate)
#   	str(member['name'].encode('utf-8'))
#   	member['role']
#   	str(member['donations']

#   If a member isn't found, add them to a new row
#

wb.save("memberDonations.xlsx")