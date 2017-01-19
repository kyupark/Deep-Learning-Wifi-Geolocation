import sqlite3

def findCommon(ar1, ar2, ar3, n1, n2, n3):
    # Initialize starting indexes for ar1[], ar2[] and ar3[]
    ar = []

    i, j, k = 0, 0, 0
    # Iterate through three arrays while all arrays have elements
    while (i < n1 and j < n2 and k< n3):
        # If x = y and y = z, print any of them and move ahead
        # in all arrays
        if (ar1[i] == ar2[j] and ar2[j] == ar3[k]):
            ar.append(ar1[i])
            i += 1
            j += 1
            k += 1
        # x < y
        elif ar1[i] < ar2[j]:
            i += 1
        # y < z
        elif ar2[j] < ar3[k]:
            j += 1
        # We reach here when x > y and z < y, i.e., z is smallest
        else:
            k += 1
    return ar

conn = sqlite3.connect('wgdl.db')
# c = conn.execute("select bssid from 'routers' where bssid LIKE 'BU %'")
c = conn.execute("select * from 'BU_Law_MF_Carrel'")
room1 = [description[0] for description in c.description]

c = conn.execute("select * from 'BU_Law_MF_Elevator'")
room2 = [description[0] for description in c.description]

c = conn.execute("select * from 'BU_Law_MF_Scanner'")
room3 = [description[0] for description in c.description]

room1.sort()
room2.sort()
room3.sort()

n1 = len(room1)
n2 = len(room2)
n3 = len(room3)
print "Common elements are",
len(findCommon(room1, room2, room3, n1, n2, n3))
