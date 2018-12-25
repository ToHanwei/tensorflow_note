# -*- coding: utf-8 -*-
#第14课：可视化神经网络


import tensorflow as tf
import numpy as np

def add_layer(inputs,input_size,output_size,activation_function=None):
    with tf.name_scope('Weight'):
        Weight=tf.Variable(tf.random_normal((input_size,output_size)))
    with tf.name_scope('Biase'):
        Biase=tf.Variable(tf.zeros((1,output_size))+0.01)
    with tf.name_scope('Weight_Biase_block'):
        wpb=tf.matmul(inputs,Weight)+Biase

    if activation_function is None:
        ret=wpb
    else:
        ret=activation_function(wpb)
    return ret

x_data=np.linspace(-1,1,30)[:,np.newaxis]
noise=np.random.normal(0,0.05,x_data.shape)
y_data=np.square(x_data)-0.5+noise

with tf.name_scope('input_block'):
    x_ph=tf.placeholder(tf.float32,[None,1])
    y_ph=tf.placeholder(tf.float32,[None,1])
with tf.name_scope('layer_1'):
    l1=add_layer(x_ph,1,10,activation_function=tf.nn.relu)
with tf.name_scope('layer_output'):
    output=add_layer(l1,10,1,activation_function=None)

with tf.name_scope('loss_block'):
    loss=tf.reduce_mean(tf.reduce_sum(tf.square(output-y_ph),reduction_indices=[1]))
gdo=tf.train.GradientDescentOptimizer(0.1)
with tf.name_scope('train_block'):
    train=gdo.minimize(loss)

init = tf.initialize_all_variables()
with tf.Session() as sess:
    writer = tf.train.SummaryWriter('tensorlogs/', sess.graph)
    # writer = tf.summary.FileWriter("tensorlogs/", sess.graph)
    sess.run(init)
    for i in range(0,1000):
        sess.run(train,feed_dict={x_ph:x_data,y_ph:y_data})
        if i%50==0:
            print sess.run(loss,feed_dict={x_ph:x_data,y_ph:y_data})




