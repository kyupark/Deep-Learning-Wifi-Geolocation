import subprocess
import plistlib
import pprint
import os
import math
from operator import itemgetter

roomdict = {
'WENTW305': (26,16),
'WENTW306': (32, 4),
'WENTW307': (20,16),
'WENTW310': (20, 4),
'WENTW312': (12, 4),
'WENTW314': ( 4, 4),
}

signaldict = {
'46': 5.0,
'47': 5.2,
'48': 5.4,
'49': 5.6,
'50': 5.8,
'51': 6.0,
'52': 6.3,
'53': 6.6,
'54': 6.9,
'55': 7.2,
'56': 7.6,
'57': 8.0,
'58': 8.4,
'59': 8.9,
'60': 9.4,
'61': 10.0,
'62': 10.7,
'63': 12.5,
'64': 12.4,
'65': 13.4,
}

routerdict = {
'04:bd:88:1e:b9:60': 'WENTW305',
'04:bd:88:1e:b9:61': 'WENTW305',
'04:bd:88:1e:b9:70': 'WENTW305',
'04:bd:88:1e:b9:71': 'WENTW305',

'04:bd:88:3b:7c:80': 'WENTW306',
'04:bd:88:3b:7c:82': 'WENTW306',
'04:bd:88:3b:7c:90': 'WENTW306',
'04:bd:88:3b:7c:92': 'WENTW306',

'04:bd:88:3b:73:c0': 'WENTW307',
'04:bd:88:3b:73:c1': 'WENTW307',

'04:bd:88:1e:b8:e0': 'WENTW310',
'04:bd:88:1e:b8:e1': 'WENTW310',

'04:bd:88:3b:77:a0': 'WENTW312',
'04:bd:88:3b:77:a1': 'WENTW312',
'04:bd:88:3b:77:b0': 'WENTW312',
'04:bd:88:3b:77:b1': 'WENTW312',

'04:bd:88:1e:b9:b0': 'WENTW314',
'04:bd:88:1e:b9:b2': 'WENTW314',
'04:bd:88:1e:b9:c0': 'WENTW314',
'04:bd:88:1e:b9:c1': 'WENTW314',

'00:18:0a:d1:0e:e0': 'Caffe Nero Downtown 1', # Add some test wifi router around you like this, when testing
'00:18:0a:d1:6f:90': 'Caffe Nero Downtown 2',
}

pp = pprint.PrettyPrinter(indent=4) # PrettyPrint print pretty :)

for count in range(0, 1000): # 1000 repetition instead of infinite
	airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s -x > airport.plist" # command to run
	subprocess.check_output(airport, shell=True) # running the command in subprocess to 
	# os.system("clear") # not clearing the result screen for test, to see the all history, 

	pl = plistlib.readPlist('airport.plist') # reading plist which is based on XML, plist is used only on Mac OS X

	routers = [] # making a empty array
	for router in pl: # reading all elements in the wifi scan result file
		digits = [] # because Mac Wifi scanner export 01:23:05:07:89:0b as 1:23:5:7:89:b, i had to add 0 in the front to make it two characters/digits
		for digit in router['BSSID'].split(':'): # this part you may need to skip or eliminate if your wifi scanner export all in 2 digits as 01:23:05:07:89:0b 
			if len(digit) == 1:
				digit = "0" + digit
			digits.append(digit)
		router['BSSID']=":".join(digits) # now you have complete all-2-digit mac address by adding zero in front where missing
		
		routers.append({
			'ssid'		: router['SSID_STR'],	# wifi router name
			'bssid'		: router['BSSID'], 		# MAC address
			'rssi'		: int(router['RSSI']),	# wifi signal strength
			'channel'	: int(router['CHANNEL']) # I kept channel just to see what's more popular, in general channel 11 is useful :) because most of case it doesnt overlap with other channel except ch 11
		})

	routers = sorted(routers, key=itemgetter('rssi'), reverse=True) # sorting to see strongest first

	for n in range(0,len(routers)):		# len(router) is length/number of routers
		if routerdict.get(routers[n]['bssid']):	# check if strongest is on your router dictionary
			if routers[n]['rssi'] < -46:		# if it's weaker than 46, you are on the floor of the strongest room!
				print routerdict.get(routers[n]['bssid'])[0:6]	# lookup the rounter dictionary, and print the floor number only which is first 5 character of the room, it will be WENTW3 in this case
			else:
				print routerdict.get(routers[n]['bssid']) # so its stronger than 46, so you are in the room!
				pp.pprint(routers[n])	# print so
			break;
	print "rescanning %d" % count		# now you are out of rounter checking for-loop, lets scan again!

