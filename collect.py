import subprocess
import plistlib
import sqlite3
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

location_name = raw_input('Enter location name: ').split(' ')
location_table = "_".join(location_name)

conn = sqlite3.connect('wgdl.db')
c = conn.cursor()
location_table = 'BU_Starbucks'

c.execute("DROP TABLE {}".format(location_table))
c.execute("CREATE TABLE {} (timestamp char(26))".format(location_table,))
# c.execute("CREATE TABLE routers (bssid char(17) primary key, ssid char(32), channel SMALLINT)")
# c.execute("CREATE INDEX index ON {}".format(loc))


airport_cmd = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s -x > airport.plist"

for count in range(1, 101):
    timenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print "%s Scan %i" % (timenow, count)

    subprocess.check_output(airport_cmd, shell=True)
    pl = plistlib.readPlist('airport.plist')

    c.execute("""INSERT INTO '{}' (timestamp) VALUES (?);""".format(location_table), (timenow,))

    for router in pl:
        bssid = normalize_bssid(router['BSSID'])
        rssi = int(router['RSSI'])
        ssid = router['SSID_STR']
        channel = router['CHANNEL']

        c.execute('SELECT bssid FROM routers WHERE bssid = ?', (bssid,))
        exist = c.fetchone()
        if exist is None:
            c.execute('INSERT INTO routers VALUES (?, ?, ?)', (bssid, ssid, channel))

        columns = [i[1] for i in c.execute('PRAGMA table_info({})'.format(location_table))]
        if bssid not in columns:
            c.execute("ALTER TABLE {} ADD COLUMN '{}' SMALLINT DEFAULT(-100);".format(location_table, bssid))

        c.execute("""UPDATE {} SET '{}' = '{}'
            WHERE timestamp = '{}'""".format(location_table, bssid, rssi, timenow))

        conn.commit()

    print 'Number of routers: %s' % len(columns)
conn.close()
