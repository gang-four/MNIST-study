import tensorflow as tf

v1 =  tf.Variable(tf.constant(1.0,shape=[1]),name="v1")

v2 = tf.Variable(tf.constant(2.0,shape=[1]),name="v2")

init_op = tf.initialize_all_variables()

saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(init_op)
    #存储当前图数据到文件
    saver.save(sess,"/Users/baochuan/private_obj_git/mnist/TensorFlow-MNIST-master/mnist/test_save_net.ckpt")