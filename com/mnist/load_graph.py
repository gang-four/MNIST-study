import tensorflow as tf

saver = tf.train.import_meta_graph("/Users/baochuan/private_obj_git/mnist/TensorFlow-MNIST-master/mnist/test_save_net.ckpt.meta")
with tf.Session() as sess:
    saver.restore(sess,"/Users/baochuan/private_obj_git/mnist/TensorFlow-MNIST-master/mnist/test_save_net.ckpt")

    print(sess.run(tf.get_default_graph().get_tensor_by_name("v2:0")))