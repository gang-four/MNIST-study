# _*_ coding:utf-8 _*_
import os

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

import numpy as np
import mnist_inference



#一次循环数据数量
BATCH_SIZE = 100

#基础学习率 用于梯度下降算发 (这个公式包含学习率 损失函数  当前节点参数 )得出下一个节点参数
LEARNING_RATE_BASE = 0.8

#学习率的衰减率  在每次学习后学习率根据这个参数下降 防止参数在局部或者全局最优解左右回荡而不能到达最优解问题
LEANING_RATE_DECAY = 0.99

#模型复杂度的正则化项在损失函数中的系数，这是放在过拟合问题公式中的参数 损失函数 + 这个系数 * R(w)描述模型复杂度的函数目前tensflow提供了2种  L1 和 L2
REGULARIZATION_RATE= 0.0001

#训练轮数
TRAINING_STEPS= 30000

#滑动平均衰减率用于滑动平均模型(shadow_veriable = decay * shadow_variable + (1-decay) * variable) 滑动平均模型在随机梯度下降算法(就是在使用梯度下降算法的时候训练数据是乱序和重复随机出现使其减少出现局部最优解问题)的基础上使模型更加健壮
#公式说明
# shadow_veriable 表示影子变量  variable 表示待更新的变量 decay为衰减率 控制模型更新的速度 tensflow 提供了滑动平滑模型算法tf.train.ExponentialMovingAverage
MOVING_AVERAGE_DECAY= 0.99

MODEL_SAVE_PATH = "/Users/baochuan/private_obj_git/mnist/TensorFlow-MNIST-master/mnist"

MODEL_NAME = "model.ckpt"


def train(mnist):

    #训练数据矩阵
    # x = tf.placeholder(tf.float32,[BATCH_SIZE,mnist_inference.INPUT_NODE],name="x-input")

    x = tf.placeholder(tf.float32,[BATCH_SIZE,mnist_inference.IMAGE_SIZE,mnist_inference.IMAGE_SIZE,mnist_inference.NUM_CHANNELS],name='x-input')

    #正确答案矩阵
    y_ = tf.placeholder(tf.float32,[None,mnist_inference.OUTPUT_NODE],name="y-input")

    # 获取l2正则化损失函数根据设置的损失系数 正则化系数 * 正则化函数(L2:对权重矩阵取平方和然后除以2)
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)

    #调用inference方法获取没有平滑处理的输出参数 是一个长度为10的一维数组
    y = mnist_inference.inference(x,1,regularizer)

    #定义计算滑动平均计算的步数 用以控制衰减率的变化 这里设置层0 表示每次一10分之一(0.1)和设置的默认衰减率进行对比    每次计算的衰减率 = min(默认衰减率,0.1)
    global_step = tf.Variable(0,trainable=False)

    #声明滑动平均对象 用于后面对参数进行滑动平均处理计算
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY,global_step)

    #定义一个更新变量滑动平均的操作 每次执行这个操作就会修改tf.trainable_variables()所表示的集合中的值
    #tf.trainable_variables() 表示当前计算图中的所有非trainable=False的数据集合 同 Graphkeys.TRAINABLE_VARIABLES
    variable_averages_op = variable_averages.apply(tf.trainable_variables())
    #tf.argmax(y_,1) 返回每行中最大的值
    #获取交叉熵 这里获取是一个集合
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y,labels=tf.argmax(y_,1))

    # 求交叉熵的平均值
    cross_entropy_mean = tf.reduce_mean(cross_entropy)

    # 总损失值 = 交叉熵平均值 + 正则化损失的和
    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))

    # 计算学习率
    # 这个函数代代表的公示  学习率 = 初始学习率（LEARNING_RATE_BASE） * 衰减系数（LEANING_RATE_DECAY） ^ （当前迭代的轮数(global_step)/ 总的训练样本数量(mnist.train.num_examples))
    learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step, mnist.train.num_examples,
                                               LEANING_RATE_DECAY)
    # 通过下面函数可以 自动修改global_step的值 从而使learning_rate也可以自动更新  这里只是用于优化
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

    # 为了一次完成通过反向传播更新网络中的参数 和 更新滑动平均值 所以使用如下函数达到一次完成多个操作
    with tf.control_dependencies([train_step, variable_averages_op]):
        train_op = tf.no_op(name="train")

    saver = tf.train.Saver()
    with tf.Session() as sess: #创建一个session
        #初始化所有Variable定义的数据
        tf.initialize_all_variables().run()
        for i in range(TRAINING_STEPS):
            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            reshaped_xs= np.reshape(xs,(BATCH_SIZE,mnist_inference.IMAGE_SIZE,mnist_inference.IMAGE_SIZE,mnist_inference.NUM_CHANNELS))
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: reshaped_xs, y_: ys})
            #每训练1000次验证并打印一下当前正确率
            if i % 1000 == 0:
                print("After %d training step(s), loss on traing batch is %g." % (step,loss_value))
                saver.save(sess,os.path.join(MODEL_SAVE_PATH,MODEL_NAME),global_step = global_step)


def main(argv=None):
    # 因为长城防火墙问题mnist的数据可能会下载不成功，这里给出一个地址可以先行下载 然后把数据放在你定义的路径下即可  https://github.com/golbin/TensorFlow-MNIST   这个地址下面有mnist的数据
    mnist = input_data.read_data_sets("/Users/baochuan/private_obj_git/mnist/TensorFlow-MNIST-master/mnist/data/",
                                      one_hot=True)
    # print("训练数据",mnist.train.num_examples)
    #
    #
    # print("验证数据",mnist.validation.num_examples)
    #
    # print("测试数据",mnist.test.num_examples)
    #
    # print("训练数据结构",mnist.train.images[0])
    #
    # print("训练数据标记结果",mnist.train.labels[0]).#一个batch循环数据的数量
    # batch_size = 100
    #返回训练数据矩阵和答案数据矩阵
    # xs,ys = mnist.train.next_batch(batch_size)
    # print("X shap:",xs.shape) #[100:784] 表示训练数据有100个 每个是个784长度的数据 也就组成了100*784的矩阵
    # print("Y shape:",ys.shape) #[100:10] 表示对应的答案有100个 每个答案的长度是10个 组成了100*10的矩阵
    train(mnist)

if __name__ == '__main__':
    tf.app.run()


