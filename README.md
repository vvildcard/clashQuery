# clashQuery
Scripts to query the Clash Royale API

## clanDonations
### Usage
You should be able to just run the script and provide info, as requested. 

#### Tokens
1. Register or Login: https://developer.clashroyale.com
2. Open your accounts page: https://developer.clashroyale.com/#/account
3. Create a Key. 
4. Give it a name and description. 
5. Use your _external_ IP address (www.whatismyip.com)
6. Copy the _entire_ text of your key into the token.txt, or delete token.txt 
and input the key when your key when prompted. 

### Scheduling
You'll probably want to get data on a regular basis. Donations are reset for all
 clan members on Sunday's at 8pm EST (5pm PST). 

#### Windows: Task Scheduler
1. Run Task Scheduler
2. Right-click 'Task Scheduler Library' > New Folder > Call it ClashRoyale (or whatever)
3. Select your new folder and click 'Create Basic Task...' (right-side pane)
4. Give it a name. 
5. Set a desirable time (donations reset at 8pm EST/5pm PST). 
6. Set the Action to 'Start a Program'. 
7. Set the program to your python.exe (probably here:
 `C:\Users\username\AppData\Local\Programs\Python\Python37-32\python.exe`)
8. In 'Add arguments', add the path to your script (in " if there are any spaces
 in your path)
9. In 'Start in', add the path to the place where want to save your token.txt
 and workbook. 

#### Linux: cron
1. Run this in terminal: `crontab -e`
2. This probably opens the cron config in vim, so push `i` to edit. 
3. Move the cursor to a blank line and paste `55 16 * * 0 path/to/your/clanDonations.py`
4. Adjust the time, if needed... the example is set to 4:55pm on Sundays, which
 will catch all US time zones. If you're in EST, you could set it to `55 19 * * 0`,
 for example. 
If you want to collect daily, use `55 16 * * *`
5. The token.txt and workbook are created in working directory, which may not be the
 location of your clanDonations.py. 

#### Mac: cron
1. Google it. :)
