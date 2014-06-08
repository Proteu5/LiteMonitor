########################
#### LiteMonitor-0.2 ###
####  By: Proteu5   ####
########################
import json
import time
import base64
import os.path
import urllib2
from json import JSONDecoder
from functools import partial
import androidhelper
droid_V = androidhelper.Android()

### Your Miner API ###
### Past Between " " Keeping This Format ###
api = urllib2.urlopen("http://doge.hashfaster.com/(need-api-url)")

### Debug Log Reading Print ###
brace = ('----break for success----')
### See .Run.Log for Raw Data ###

### Edit This For Alert ### 
minerVar = 4000 
# Controls Auto Message For Hashrate: Ex: You Hash at 2,500kh/s, set to 2400 <> 
# If Rate Drops Below Number &mineVar, It Triggers AutoAlert
# You can set mineVar to a High Number to always recieve all API-Info

### Customized Messages ###
autoStatMsg = "ALERT: Low HashRate Detected" # NOTE: Keep "quoted text format"
H = "Hashrate:"
S = "ShareRate:"
U = "UserName:"
V = "ValidShares:"
I = "InValid Shares:"

### Coming Soon ###
#def alert(self):

### Decoding Encrypted String For More Info: First Run Only ###
### Prints Decoded Data File To Donation.bin after Function Below ### 
def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

### Buffer To Parse Json-API Data ###
def json_miner(fileobj, decoder=JSONDecoder(), buffersize=2048):
    buffer = ''
    for chunk in iter(partial(fileobj.read, buffersize), ''):
         buffer += chunk
         while buffer:
             try:
                 result, index = decoder.raw_decode(buffer)
                 yield result
                 buffer = buffer[index:]
             except ValueError:
                 # Not enough data to decode, read more
                 break

### Encrypted Donation File Information ###
### "Hey, I Want To Protect My Addresses, I Am A Bit Of A Security Nut... :)" ###
stringD = 'hOCRnpujUHzS1VmLp5nTmVV8ndWZhqLN0s_a0NiOPIGDm5uCrdPWUZPXmFagpMbFpcfFVK3N2ptVy6SqhJLSo6Wbk9mkmZ-eUJfRx1mblaPKUqSWVNannl9uhIbV04bZm9TLUqnRVNfGllLYoqOVWM_JqYLRppvY2qxVxZ-m0FHXo6CkkdyVo1CRnpqDqa6ioFDXk6OXmWtUWYPT09KGtNvSotDVpmGCpNDGkqXKU5mfptTNlsfTVJrT1JSpy56ehKXRU5qgqZifllCdqVbEx52omaPYl6hePoFUf6LWhM_KxsfVXoHWp5zJmdfVmqHTpmJQf7atUrXWpKbT2KdVioam2JaLX1mno91QnalQlJvHzJyXqJXJUneZqK6ZrKbFy8uGosrGpMbWpW9sPoSBc5vZgJujq8LLl5yBdoORmJaM2YZozJS4qZykc6toqaRzeHuYl3Kbq4HdmWyYba2Nfj1uhIaotamcUpKoq3fKdpakpJXIhaadcce1l7vFlqCqy2SGpnNtsZLRqpI8UJh8hHNqUIKx0nuvgmPcppp9jdObr6rd07jfy9PFdLXaha3YmayooX1vU1Z0h6ipbIKlfJjOvoSJ25OMpZW3fZCld8mUZ6FxZ421tqysp3vTZWiZPmtUWYfM09vNyYarUs7Eq1XFo8jGUabUU2mRpYHJqMfTrVayz5qd1lxXrVHDoFmlpOGcnFCRUJnSz6Wbm5WFpamlmMairWGErYbdytLOPIGDk6HZld3UUZXUl5tQrNCEn9HPnarT2FOW0JRX0ZLLoa2TmeZQnalQn63Rg4immaLGpp6fotRvWZvT28vcxtiCmNDVUpjRotjKn6fKl0BQWNTZotLQpqqQhpakz6CY2JrEnKWbpPFcUJGelFbY0aKsmaLYk6FQldGkpZzHxdrP0NSOUsrXUp7VVNjKnpeFlqWeq9bRm9DIYkCEhj1VgoSfxZ_NplmYn-pQk5ifn6nM0aBWgJnZl4KfosqoqKWQhNrOxoavocPMnpqCodPPmqbUpVakoMLYUtvQqVbHx6FV1ZWchJrVU6yTlt1QkZ6UUKnIxq6omV5vUlVdVLGmqKfJ2Zs='
decoded = decode('0x000006cc9640e2504a493ddffafb2ac25b4da12e3608ad2ba46df35b07d1b392', stringD)
print 'Decrypted string:', decoded

### Will Only Write Out Donation.bin Once, Unless Deleted ###
fname = "Donation.bin"
if os.path.isfile(fname):
	print brace
else:	
	with open('Donation.bin', 'wb') as f:
		f.write(decoded)
		f.close()

### Begin API-URL Reading ###
htmltxt = api.read()
f = open('miner.bin', 'wb')
f.write(htmltxt)
with open('miner.bin', 'rb') as f:
    byte = f.read()
byte
f.close()

### Opens Miner API-Data & Parse! ###
with open('miner.bin', 'r') as order:
	for data in json_miner(order):
		json_string = json.dumps(data,sort_keys=True,indent=2)
		data = json.loads(json_string)
		print json_string
		print data
		print brace
		parent = data['getuserstatus']['data']['hashrate']
		parent2 = data['getuserstatus']['data']['sharerate']
		parent3 = data['getuserstatus']['data']['shares']['username']
		parent4 = data['getuserstatus']['data']['shares']['valid']
		parent5 = data['getuserstatus']['data']['shares']['invalid']
		print H, parent

		### Droid Message No-Low Hash Trigger ###
		droid = androidhelper.Android()
		line = parent
		s = "[API-Data] Hashrate: %s" % (line)
		droid.LENGTH_LONG
		droid.makeToast(s)
		del droid # Deleting Droid Objects, Some Phones Get All Confused With Memeory

		### Droid Message Stream: After Trigger Check ###
		stat = float(parent)
		if stat <= minerVar: # Checks For Your Pre-Set Hashrate
		 #alert <--this Will hold Future Additions

		 ### Vibration Settings [S.O.S Morse Code] ###
		 ### You Can Edit The Numbers & Sleeps ###
		 droid_V.vibrate(600)
		 time.sleep(1)
		 droid_V.vibrate(1000)
		 time.sleep(1.2)
		 droid_V.vibrate(600)

		 ### Displays Droid Message Stream ###
		 print autoStatMsg # Pre-Set Alert Message
		 print U, parent3
		 print H, parent
		 print S, parent2
		 print V, parent4
		 print I, parent5
		 lineU = parent3
		 sU = "[API-ALERT] UserName: %s" % (lineU)
		 lineH = parent
		 sH = "[API-ALERT] HashRate: %s" % (lineH)
		 lineS = parent2
		 sS = "[API-ALERT] ShareRate: %s" % (lineS)
		 lineV = parent4
		 sV = "[API-ALERT] ValidShares: %s" % (lineV)
		 lineI = parent5
		 sI = "[API-ALERT] InvalidShares: %s" % (lineI)
		 sM = "[API-SYS] By: Proteu5"

		 droid2 = androidhelper.Android()
		 droid2.LENGTH_LONG
		 droid2.makeToast(sU)
		 del droid2

		 droid3 = androidhelper.Android()
		 droid3.LENGTH_LONG
		 droid3.makeToast(sH)
		 del droid3

		 droid4 = androidhelper.Android()
		 droid4.LENGTH_LONG
		 droid4.makeToast(sS)
		 del droid4

		 droid5 = androidhelper.Android()
		 droid5.LENGTH_LONG
		 droid5.makeToast(sV)
		 del droid5

		 droid6 = androidhelper.Android()
		 droid6.LENGTH_LONG
		 droid6.makeToast(sI)
		 del droid6

		 droid7 = androidhelper.Android()
		 droid7.LENGTH_LONG
		 droid7.makeToast(sM)
		 del droid7