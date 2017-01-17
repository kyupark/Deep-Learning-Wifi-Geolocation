import subprocess
import plistlib
import sqlite3
from operator import itemgetter
from datetime import datetime

conn = sqlite3.connect('wgc-test.db')
c = conn.cursor()
loc = 'BULaw_MF_Room1'

c.execute("DROP TABLE {}".format(loc))
c.execute("CREATE TABLE {} (no INTEGER, bssid CHAR(17), rssi SMALLINT, ssid CHAR(32), channel SMALLINT, time TEXT)".format(loc))


airport_cmd = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s -x > airport.plist"

for count in range(1, 101):
    print "trial no %i" % count
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%f')

    subprocess.check_output(airport_cmd, shell=True)
    pl = plistlib.readPlist('airport.plist')

    routers = []
    for router in pl:
        digits = []
        for digit in router['BSSID'].split(':'):
            if len(digit) == 1:
                digit = "0" + digit
            digits.append(digit)
        router['BSSID']=":".join(digits)

        bssid = router['BSSID']
        rssi = int(router['RSSI'])
        ssid = router['SSID_STR']
        channel = router['CHANNEL']

        print bssid, rssi, ssid, channel

        c.execute("INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?)".format(loc), (count, bssid, rssi, ssid, channel, time))

        conn.commit()
conn.close()
