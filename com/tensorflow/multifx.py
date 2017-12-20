import tensorflow as tf

from numpy.random import RandomState

batch_size = 8

x = tf.placeholder(tf.float32,shape=(None,2),name='x-input')
y_ = tf.placeholder(tf.float32,shape=(None,1),name='y-input')

w1 = tf.variable(tf.random_normal([1,2],stddev=1,seed=1))
y = tf.matmul(x,w1)

loss_less = 10
loss_more = 1
loss = tf.reduce_sum(tf.select(tf.greater(y,y_),(y-y_)*loss_more,(y_-y)*loss_less))
train_step = tf.train.AdamOptimizer(0.001).minimize(loss)



rdm = RandomState(1);