# -*- coding: utf-8 -*-
import tensorflow as tf
import majiang_inference
import majiang_train
#import os
import numpy as np


MODEL_SAVE_PATH="D:/data/TensorFlow/tensorflow_codes/mahjong/parameterdata/"


def NNAIeval(xx):
    #xx=np.array(xx)
    with tf.Graph().as_default() as g:
        xx=np.array(xx)
        
        x=tf.placeholder(tf.float32,[1,34,34,3],name='x-input')
        is_training = tf.placeholder(tf.bool, shape=[])
        y_p,y_v=majiang_inference.inference(x,None,is_training)
        
        variable_averages = tf.train.ExponentialMovingAverage(majiang_train.MOVING_AVERAGE_DECAY)
        variables_to_restore = variable_averages.variables_to_restore()
        saver=tf.train.Saver(variables_to_restore)
        
        with tf.Session() as sess:
             ckpt=tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
             if ckpt and ckpt.model_checkpoint_path:
                 saver.restore(sess,ckpt.model_checkpoint_path) 
             else:
                 print("No checkpoint file found")
                 return 
              
             batch_dx = DATA1TO3(xx)

            
             p,v = sess.run([y_p,y_v], feed_dict={x: batch_dx, is_training:False}) 
         

             return [p,v]

  


    
def DATA1TO3(xx):
    for i in range(34):
        for j in range(15):
            xx[i][15+j]=xx[i][j]
    batch_datax=np.array([[[[0 for x in range(3)] for y in range(34)]for z in range(34)]for b in range(1)])
    for i in range(34):
        for j in range(34):
            batch_datax[0][i][j][0]=xx[i][j]
            batch_datax[0][i][j][1]=xx[i][j]
            batch_datax[0][i][j][2]=xx[i][j]
    return batch_datax
    





