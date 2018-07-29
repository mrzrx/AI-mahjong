# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 15:08:44 2018

@author: kk

"""
import numpy as np
import tensorflow as tf
import majiang_inference
import time
import os



BATCH_SIZE = 8
IMAGE_SIZE = 34
IMAGE_CHANNELS = 3

REGULARAZTION_RATE = 0.0001
MOVING_AVERAGE_DECAY = 0.99

LEARNING_RATE_BASE = 0.01
LEARNING_DECAY_STEPS = 1000
LEARNING_RATE_DECAY = 0.99

TRAINING_STEPS=100000
TRAINDATANUM=99972

Traindatapath=os.getcwd() + "/traindata/"
MODEL_SAVE_PATH=os.getcwd() + "/parameterdata/"
MODEL_NAME="model.ckpt"


def train():
    
    
    x = tf.placeholder(tf.float32, [BATCH_SIZE,
                                    IMAGE_SIZE,
                                    IMAGE_SIZE,
                                    IMAGE_CHANNELS], name='x-input')
    y_policy_ = tf.placeholder(tf.float32, [None,19], name='y-policy')
    y_value_ = tf.placeholder(tf.float32, [None,1], name='y-value')
    is_training = tf.placeholder(tf.bool, shape=[])

    regularizer = tf.contrib.layers.l2_regularizer(REGULARAZTION_RATE)
    
    y_policy, y_value = majiang_inference.inference(x, regularizer, is_training) 
    
    global_step = tf.Variable(0, trainable=False)
    
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variables_averages_op = variable_averages.apply(tf.trainable_variables())

    cross_entropy_mean_v = tf.reduce_mean(tf.square(y_value_ - y_value))  
    
    y_policy_softmax = tf.nn.softmax(y_policy_)
    cross_entropy_p = tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_policy_softmax, logits=y_policy)
    cross_entropy_mean_p = tf.reduce_mean(cross_entropy_p)
    
    cross_entropy_mean = cross_entropy_mean_v + cross_entropy_mean_p
    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
                                         
    learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step, LEARNING_DECAY_STEPS, LEARNING_RATE_DECAY, staircase=True)
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    
    with tf.control_dependencies([train_step, variables_averages_op]):
        train_op = tf.no_op(name='train')
        
  #  merged = majiang_inference.merged()
    saver_save = tf.train.Saver()
    
    #variable_averages_ = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY)
    variables_to_restore = variable_averages.variables_to_restore()
    saver_restore=tf.train.Saver(variables_to_restore)
   
    
    with tf.Session() as sess:
       # summary_writer = tf.summary.FileWriter('D:/0others/data/TensorFlow/majiang_data/tensorboard', sess.graph)
        
        tf.global_variables_initializer().run()      
        
        ckpt=tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
        if ckpt and ckpt.model_checkpoint_path:
            saver_restore.restore(sess,ckpt.model_checkpoint_path)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        for i in range(TRAINING_STEPS):
            time_start = time.clock()
            
            x_batch, y_police_batch, y_value_batch = next_batch(i)
            
            _, loss_value, step = sess.run([train_op, loss, global_step], 
                                  feed_dict={x:x_batch, y_policy_:y_police_batch, y_value_:y_value_batch, is_training:True})
            
          #  summary_writer.add_summary(summary, i)
            
          #  if i % 100 == 0:
            print("After %d training step(s), loss on training batch is %g." % (step, loss_value))
            print("time used=", (time.clock() - time_start))
            f = open("printlog.txt", 'a')
            print("After %d training step(s), loss on training batch is %g." % (step, loss_value), file=f)
            print("time used=", (time.clock() - time_start), file=f)
            f.close()
            
            saver_save.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)
   # summary_writer.close()
            
            
def next_batch(batch_num):
    start = (batch_num * BATCH_SIZE) % TRAINDATANUM
    end = min(start+BATCH_SIZE, TRAINDATANUM)
    
    #batch_datax=np.array([[[[0 for x in range(3)] for y in range(34)]for z in range(34)]for b in range(BATCH_SIZE)])
    batch_datax=np.array([[[[0 for x in range(3)] for y in range(34)]for z in range(34)]for b in range(BATCH_SIZE)])
    batch_datay_policy=np.array([[0 for z in range(19)]for b in range(BATCH_SIZE)])
    batch_datay_value=np.array([[0 for z in range(1)] for b in range(BATCH_SIZE)])
    b=0
    for t in range(start, end):
        datapath=Traindatapath+'data'+str(t)+'.txt'
        data=np.loadtxt(datapath)
        #b = t - start
        for i in range(34):
            for j in range(34):
                batch_datax[b][i][j][0]=data[i][j]
                batch_datax[b][i][j][1]=data[i][j]
                batch_datax[b][i][j][2]=data[i][j]

        for i in range(19):
            batch_datay_policy[b][i]=data[i][34]
        
        batch_datay_value[b][0]=data[19][34]
        b+=1
    return [batch_datax,batch_datay_policy,batch_datay_value]






def main(argv = None):
    tf.reset_default_graph()
    train()
    
if __name__ == '__main__':
    tf.app.run()
    
    