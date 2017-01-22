import sqlite3
import pprint
import numpy as np
import tensorflow as tf

pp = pprint.PrettyPrinter(indent=4)

conn = sqlite3.connect('wgdl.db')

r1 = 'BU-L-MF-C'
r2 = 'BU-L-MF-E'
r3 = 'BU-L-MF-S'

c = conn.execute("""select r1.*
    from '{}' r1, '{}' r2, '{}' r3
    where r1.bssid = r2.bssid and r1.bssid = r3.bssid ORDER BY bssid""".format(r1, r2, r3))
room1 = c.fetchall()

c = conn.execute("""select r2.*
    from '{}' r1, '{}' r2, '{}' r3
    where r1.bssid = r2.bssid and r1.bssid = r3.bssid ORDER BY bssid""".format(r1, r2, r3))
room2 = c.fetchall()

c = conn.execute("""select r3.*
    from '{}' r1, '{}' r2, '{}' r3
    where r1.bssid = r2.bssid and r1.bssid = r3.bssid ORDER BY bssid""".format(r1, r2, r3))
room3 = c.fetchall()

A = np.transpose(room1)[3:,:]
ones = np.ones((A.shape[0], 1))
zeros = np.zeros((A.shape[0], 1))
AA = np.hstack((A, ones, zeros, zeros))

A = np.transpose(room2)[3:,:]
ones = np.ones((A.shape[0], 1))
zeros = np.zeros((A.shape[0], 1))
BB = np.hstack((A, zeros, ones, zeros))

A = np.transpose(room3)[3:,:]
ones = np.ones((A.shape[0], 1))
zeros = np.zeros((A.shape[0], 1))
CC = np.hstack((A, zeros, zeros, ones))

ABC = np.vstack((AA, BB, CC))
np.random.shuffle(ABC)

xy = ABC
x_data = np.asarray(xy)[3:,:-3]
y_data = np.asarray(xy)[3:,-3:]

x_test = np.asarray(xy)[:3,:-3]
y_test = np.asarray(xy)[:3,-3:]

xs = x_data.shape[1]
ys = y_data.shape[1]

# xs = 100
# ys = 3

X = tf.placeholder("float", [None, xs])
Y = tf.placeholder("float", [None, ys])

W = tf.Variable(tf.zeros([xs, ys]))
hypothesis = tf.nn.softmax(tf.matmul(X, W))

learning_rate = 0.0001
cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(hypothesis), reduction_indices=1))

optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    for step in xrange(10001):
        sess.run(optimizer, feed_dict={X:x_data, Y:y_data})
        if step % 500 == 0:
            print step, sess.run(cost, feed_dict={X:x_data, Y:y_data}), sess.run(W)

    a = sess.run(hypothesis, feed_dict={X:x_test})
    print a, sess.run(tf.arg_max(a, 1))
    print y_test
