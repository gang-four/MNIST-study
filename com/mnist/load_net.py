import tensorflow as tf

v1 = tf.Variable(tf.constant(1.0,shape=[1]),name="v1")
v2 = tf.Variable(tf.constant(2.0,shape=[1]),name="v2")
result = v1 + v2

saver = tf.train.Saver()

with tf.Session() as sess:
    #加载文件中的图数据
    saver.restore(sess,"/Users/baochuan/private_obj_git/mnist/TensorFlow-MNIST-master/mnist/test_save_net.ckpt")
    print(sess.run(result))