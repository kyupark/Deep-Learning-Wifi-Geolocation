import subprocess
import plistlib
import sqlite3
import time
from operator import itemgetter
from datetime import datetime

def normalize_bssid(bssid):
    digits = []
    for digit in bssid.split(':'):
        if len(digit) == 1:
            digit = "0" + digit
        digits.append(digit)
    bssid=":".join(digits)
    return bssid

location_table = 'BU-L-MF-S' # raw_input('Enter location name: ')

conn = sqlite3.connect('wgdl.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS '{}'".format(location_table))
c.execute("CREATE TABLE '{}' (bssid char(17) primary key, ssid char(32), channel SMALLINT)".format(location_table,))

airport_cmd = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s -x > airport.plist"

count = 1
while count <= 10:
    timenow = datetime.now().strftime('%H:%M:%S') # '%Y-%m-%d %H:%M:%S.%f'

    try:
        p = subprocess.call(airport_cmd, shell=True)
        print "%s Scan %i" % (timenow, count)
        pl = plistlib.readPlist('airport.plist')
    except:
        print "Failed, trying again"
        time.sleep(1)
        continue

    c.execute("ALTER TABLE '{}' ADD COLUMN '{}' SMALLINT DEFAULT(-100);".format(location_table, timenow))

    for router in pl:
        bssid = normalize_bssid(router['BSSID'])
        rssi = int(router['RSSI'])
        ssid = router['SSID_STR']
        channel = router['CHANNEL']

        c.execute("SELECT bssid FROM '{}' WHERE bssid = ?".format(location_table), (bssid,))
        exist = c.fetchone()
        if exist is None:
            c.execute("INSERT INTO '{}' (bssid, ssid, channel) VALUES (?, ?, ?)".format(location_table), (bssid, ssid, channel))

        c.execute("""UPDATE '{}' SET '{}' = '{}' WHERE bssid = '{}'""".format(location_table, timenow, rssi, bssid))

        conn.commit()

    cursor = c.execute("select * from '{}';".format(location_table))
    print 'Number of routers: %i' % len(cursor.fetchall())
    count += 1
conn.close()
