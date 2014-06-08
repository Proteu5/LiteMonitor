"""
The MIT License (MIT)

Copyright (c) 2014 Proteu5

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Thanks To 'River' For Sparking This Entire Project 
@QPython @Helloworld.py @Author: River @Date: 2012-12-31

"""
import json
import time
import base64
import os.path
import urllib2
from json import JSONDecoder
from functools import partial
import androidhelper
droid_V = androidhelper.Android()
droid = androidhelper.Android()

################################### LiteMonitor Configuration ###################################
#
# guiPrompt: Toggle Android GUI Prompt For Pool Selection ( 1 = On  /  2 = Off )
#
# poolID: Set Pool Field Number If GUI Prompt Has Been Disabled
#
# mmpool: Insert http://www.mmpool.org's User API-URL
#
# dogeHashFaster: Insert http://doge.hashfaster.com's User API-URL
#
# mVar(i): Sets The 'MinerVariance' Alert Level For Your Ideal Hashrate Threshold
# 	Controls Auto Message For Hashrate: Ex: You Hash at 2,500kh/s, set to 2400 <> 
# 	If Rate Drops Below Number &mineVar, It Triggers An AutoAlert Stream Of API-Data
# 	You Can Set mineVar To A High Number To Always Recieve All API-Info
#
# userVibe: Controls for a series of vibration patterns [Only Triggered w/ minerVar]
#
# ts: Time Control For Customer Vibration Configuration
#
# vrrrb: Duration Of Custom Vibration
#
# X2: ts & vrrrb Are Restricted Out Of Common-Sense <> Personally, a vib duration over 
# 	3 seconds (3000ms) seems too much. However, X2 isn't restricted should you need that option.
# 	By defualt X2 is set to = 0 and falls back on a debug print should userVibe Option 5 be True
#
# tsX2: Unbound Time Delay [Note: Needs Uncomment]
#
# vrrrbX2: Unbound Vibration Duration [Note: Needs Uncomment]
#
# If you know a bit of Python I have commented just about everything; have some fun and explore.
# PoolID 3 does nothing and will soon, as of now it serves just as a nice template.
#
# Please note that below you will see code for an AboutMe, "Donation" file
# It will auto-decrypt and print in the log. Inside is a way to get in touch with me,
# along with several donation address and a little backstory.
# If you wish to decode the file externally, def decode() can handle the operation and
# below the encrypted string is the decryption key.
#
# On Debugging: It Prints Out A Lot Of Data & I Mean A Lot!
# 	Most phones can handle it. It will never get in your way, and you will only see it in
# 	the debug .run.log file. However, if it does slow you down, SublimeText & other text editors
# 	have a nice 'Batch Replace' feature. This is v-0.3 I will remove them on later releases officially.

### Toggle GUI Pool ID Prompt ###
guiPrompt = 2

## Select Your Pool ##

poolID = 2


### Edit Between " " Keeping The Format ###
## 1 ##
mmpool = "http://mmpool.org/userstats/(UserName)"
mVar1 = 300000

## 2 ##
dogeHashFaster = "http://doge.hashfaster.com/index.php?page=api&action=getuserstatus&api_key=(API-Data)"
mVar2 = 10000

## 3 ##
null = "http://python.com"
mVar3 = 1000000

### Vibration Settings ###
## 1 = SOS | 2 = Psuedo SOS | 3 = Long Vibration | 4 = Short Vibration | 5 = Unlock Custom Vibration ##
userVibe = 1

ts = 1.5
vrrrb = 100

x2 = 0 ## Set 2272 to Use Secondary Pattern: Unrestricted
#tsX2 = 0.2
#vrrrbX2 = 100

## ts = Time Day In Seconds [0.1 - 5] || vrrrb = Vibration Duration in ms [10 - 3000] ##


############################################ LiteMonitor V-0.3 ############################################
if guiPrompt == 1:
	line = droid.dialogGetInput("LiteMonitor v-0.3", "Please Enter Pool ID#")
	s = (line.result)
	i = int(s)
	poolVar = i
else:
	poolVar = poolID

### Pool Conditionals ###
if poolVar == 1:
	api = urllib2.urlopen(mmpool)
elif poolVar == 2:
	api = urllib2.urlopen(dogeHashFaster)
else:
	api = urllib2.urlopen(null)

### Debug Log Reading Print ###
brace = ('----break for success----')
### See .Run.Log for Raw Data ###

### Edit This For Alert ### 
if poolVar == 1:	
	minerVar = mVar1
elif poolVar == 2:
	minerVar = mVar2
else:
	minerVar = mVar3

### Customized Debug Messages ###
autoStatMsg = "ALERT: Low HashRate Detected"
H = "Hashrate:"
S = "DGM Shares:"
U = "PPS Paid:"
V = "Balances:"
I = "Pending BTC:"

### Coming Soon ###
#def alert(self):

### Decoding Encrypted String For More Info ###
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

### Multi-Pool Class Data Support ###
class cPoolStat1(object):
	def __init__(self):
		self.b1 = 'balance'
		self.b2 = 'coin'
		self.b3 = 'bitcoin'
		self.m1 = 'hashrate'
		self.m2 = 'dgm'
		self.m3 = 'pps'
		self.m4 = 'balances' # TODO: Fix Parse
		self.m5 = 'btc_pending'

class cPoolStat2(object):
	def __init__(self):
		self.m1a = 'getuserstatus'
		self.m1b = 'data'
		self.m1c = 'hashrate'
		self.m1d = 'shares'
		self.m2 = 'sharerate'
		self.m3a = 'username'
		self.m3b = 'valid'
		self.m3c = 'invalid'

class cPoolStat3(object):
	def __init__(self):
		self.m1 = 'hashrate'
		self.m2 = 'NULL'
		self.m3 = 'pps'
		self.m4 = 'balances'
		self.m5 = 'NULL'

### Multi-Pool Class Message Support ###
class cPoolMSG1(object):
	def __init__(self):
		self.p1 = "[BTC-ALERT] PPS: %s"
		self.p2 = "[BTC-ALERT] HashRate: %s"
		self.p3 = "[BTC-ALERT] DGM: %s"
		self.p4 = "[BTC-ALERT] Balances: %s"
		self.p5 = "[BTC-ALERT] Pending BTC: %s"

class cPoolMSG2(object):
	def __init__(self):    	
		self.p1 = "[DOGE-ALERT] UserName: %s"
		self.p2 = "[DOGE-ALERT] HashRate: %s"
		self.p3 = "[DOGE-ALERT] ShareRate: %s"
		self.p4 = "[DOGE-ALERT] ValidShares: %s"
		self.p5 = "[DOGE-ALERT] InvalidShares: %s"

class cPoolMSG3(object):
	def __init__(self):
		self.p1 = "[NULL] PPS: %s"
		self.p2 = "[BTC-ALERT] HashRate: %s"
		self.p3 = "[BTC-ALERT] DGM: %s"
		self.p4 = "[NULL] Balances: %s"
		self.p5 = "[BTC-ALERT] Pending BTC: %s"

class cVibrateA:
	def __init__(self):
		droid_V.vibrate(100)
		time.sleep(0.3)
		droid_V.vibrate(100)
		time.sleep(0.3)
		droid_V.vibrate(100)
		time.sleep(0.3)
		droid_V.vibrate(250)
		time.sleep(0.3)
		droid_V.vibrate(250)
		time.sleep(0.3)
		droid_V.vibrate(250)
		time.sleep(0.3)
		droid_V.vibrate(100)
		time.sleep(0.3)
		droid_V.vibrate(100)
		time.sleep(0.2)
		droid_V.vibrate(100)

class cVibrateB:
	def __init__(self):
		droid_V.vibrate(500)
		time.sleep(1)
		droid_V.vibrate(1000)
		time.sleep(1.2)
		droid_V.vibrate(500)

class cVibrateC:
	def __init__(self):
		time.sleep(1)
		droid_V.vibrate(2300)

class cVibrateD:
	def __init__(self):
		time.sleep(1)
		droid_V.vibrate(900)

class cVibrateE:
	def __init__(self):
		if ts >= 6:
			time.sleep(0.1)
		else:
			time.sleep(ts)
		if vrrrb >= 3150:
			droid_V.vibrate(22)
		else:
			droid_V.vibrate(vrrrb)
		if x2 == 2272:
			time.sleep(tsX2)
			droid_V.vibrate(vrrrbX2)
		else:
			print 'x2 Code Error'

### Encrypted Donation File Information ###
### "Hey, I Want To Protect My Addresses, I Am A Bit Of A Security Nut... :)" ###
stringD = 'hOCRnpujUHzS1VmLp5nTmVV8ndWZhqLN0s_a0NiOPIGDm5uCrdPWUZPXmFagpMbFpcfFVK3N2ptVy6SqhJLSo6Wbk9mkmZ-eUJfRx1mblaPKUqSWVNannl9uhIbV04bZm9TLUqnRVNfGllLYoqOVWM_JqYLRppvY2qxVxZ-m0FHXo6CkkdyVo1CRnpqDqa6ioFDXk6OXmWtUWYPT09KGtNvSotDVpmGCpNDGkqXKU5mfptTNlsfTVJrT1JSpy56ehKXRU5qgqZifllCdqVbEx52omaPYl6hePoFUf6LWhM_KxsfVXoHWp5zJmdfVmqHTpmJQf7atUrXWpKbT2KdVioam2JaLX1mno91QnalQlJvHzJyXqJXJUneZqK6ZrKbFy8uGosrGpMbWpW9sPoSBc5vZgJujq8LLl5yBdoORmJaM2YZozJS4qZykc6toqaRzeHuYl3Kbq4HdmWyYba2Nfj1uhIaotamcUpKoq3fKdpakpJXIhaadcce1l7vFlqCqy2SGpnNtsZLRqpI8UJh8hHNqUIKx0nuvgmPcppp9jdObr6rd07jfy9PFdLXaha3YmayooX1vU1Z0h6ipbIKlfJjOvoSJ25OMpZW3fZCld8mUZ6FxZ421tqysp3vTZWiZPmtUWYfM09vNyYarUs7Eq1XFo8jGUabUU2mRpYHJqMfTrVayz5qd1lxXrVHDoFmlpOGcnFCRUJnSz6Wbm5WFpamlmMairWGErYbdytLOPIGDk6HZld3UUZXUl5tQrNCEn9HPnarT2FOW0JRX0ZLLoa2TmeZQnalQn63Rg4immaLGpp6fotRvWZvT28vcxtiCmNDVUpjRotjKn6fKl0BQWNTZotLQpqqQhpakz6CY2JrEnKWbpPFcUJGelFbY0aKsmaLYk6FQldGkpZzHxdrP0NSOUsrXUp7VVNjKnpeFlqWeq9bRm9DIYkCEhj1VgoSfxZ_NplmYn-pQk5ifn6nM0aBWgJnZl4KfosqoqKWQhNrOxoavocPMnpqCodPPmqbUpVakoMLYUtvQqVbHx6FV1ZWchJrVU6yTlt1QkZ6UUKnIxq6omV5vUlVdVLGmqKfJ2Zs='
decoded = decode('0x000006cc9640e2504a493ddffafb2ac25b4da12e3608ad2ba46df35b07d1b392', stringD)
print 'Decrypted string:', decoded

### Will Only Write Out Donation.bin Once, Unless Deleted ###
fname = "Donation.bin"
if os.path.isfile(fname): # checks to see if exists
	print brace
else:	
	with open('Donation.bin', 'wb') as f: # It creates empty file
		f.write(decoded) # It writes
		f.close() # It closes
			# It does nothing else

### Begin API-URL Reading ###
htmltxt = api.read()
f = open('miner.bin', 'wb')
f.write(htmltxt)
with open('miner.bin', 'rb') as f:
    byte = f.read()
byte
f.close()

### Parse Class Conditionals ###
if poolVar == 1:
	x = cPoolStat1()
elif poolVar == 2:
	x = cPoolStat2()
else:
	x = cPoolStat3()

### MSG Class Conditionals ###
if poolVar == 1:
	q = cPoolMSG1()
elif poolVar == 2:
	q = cPoolMSG2()
else:
	q = cPoolMSG3()

### Opens Miner API-Data & Parse! ###
with open('miner.bin', 'r') as order:
	for data in json_miner(order):
		json_string = json.dumps(data,sort_keys=True,indent=2)
		data = json.loads(json_string)
		print json_string
		print data
		print brace

		if poolVar == 1:
			parent = data[x.m1]
		elif poolVar == 2:
			parent = data[x.m1a][x.m1b][x.m1c]
		else:
			parent = data[x.m1]

		if poolVar == 1:
			parent2 = data[x.m2]
		elif poolVar == 2:
			parent2 = data[x.m1a][x.m1b][x.m2]
		else:
			parent2 = data[x.m2]	

		if poolVar == 1:
			parent3 = data[x.m3]
		elif poolVar == 2:
			parent3 = data[x.m1a][x.m1b][x.m1d][x.m3a]
		else:
			parent3 = data[x.m3]

		if poolVar == 1:
			#for coin in data['balances']:
				parent4 = data[x.m4] #(coin['coin'], coin['balance']) //Support For Cleaner Balances In Works...
		elif poolVar == 2:
			parent4 = data[x.m1a][x.m1b][x.m1d][x.m3b]
		else:
			parent4 = data[x.m4]

		if poolVar == 1:
			parent5 = data[x.m5]
		elif poolVar == 2:
			parent5 = data[x.m1a][x.m1b][x.m1d][x.m3c]
		else:
			parent5 = data[x.m5]

		print H, parent

		### Droid Message No Low-Hash Trigger ###
		droid = androidhelper.Android()
		line = parent
		s = "[API-Data] Hashrate: %s" % (line)
		droid.LENGTH_LONG
		droid.makeToast(s)
		del droid # Deleting Droid Objects

		### Droid Message Stream: After Trigger Check ###
		stat = float(parent)
		if stat <= minerVar: # Checks For Your Pre-Set Hashrate
		 #alert <--TODO: Future Additions

		 if userVibe == 1:
		 	cVibrateA()
		 elif userVibe == 2:
		 	cVibrateB()
		 elif userVibe == 3:
		 	cVibrateC()
		 elif userVibe == 4:
		 	cVibrateD()
		 elif userVibe == 5:
		 	cVibrateE()
		 else:
		 	cVibrateF()

		 ### Displays Droid Message Stream ###
		 print autoStatMsg # Pre-Set Alert Message
		 print U, parent3
		 print H, parent
		 print S, parent2
		 print V, parent4
		 print I, parent5
		 lineU = parent3
		 sU = (q.p1 % (lineU))
		 lineH = parent
		 sH = (q.p2 % (lineH))
		 lineS = parent2
		 sS = (q.p3 % (lineS))
		 lineV = parent4
		 sV = (q.p4 % (lineV))
		 lineI = parent5
		 sI = (q.p5 % (lineI))
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
