# -*- coding: utf-8 -*-
import tensorflow as tf
import majiang_inference
import majiang_train
#import os
import numpy as np

BATCH_SIZE = 1
TRAINDATANUM = 1000   #测试用

Traindatapath="D:/0others/data/TensorFlow/majiang_data/traindata/"
MODEL_SAVE_PATH="D:/0others/data/TensorFlow/majiang_data/parameterdata/"


def NNAIeval():
    #xx=np.array(xx)
    with tf.Graph().as_default() as g:

        #xx=np.array(xx)
        
        x=tf.placeholder(tf.float32,[BATCH_SIZE,34,34,3],name='x-input')
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
              
            # batch_dx = DATA1TO3(xx)
             batch_dx = next_batch(1)         #测试用
            
             p,v = sess.run([y_p,y_v], feed_dict={x: batch_dx, is_training:False}) 
         
           
#             np.savetxt("a1.txt",aaa[:,:,:,0]) 
          #   print(aaa[:,:,:,0])
 #            print(bbb)
#             np.savetxt("b1.txt",bbb[0,:,:,0]) 
#             np.savetxt("c1.txt",ccc[0,:,:,0]) 
#             np.savetxt("d1.txt",ddd[0,:,:,0]) 
#             np.savetxt("e1.txt",fff[0,:,:,0]) 

             print("神经网络输出结果")
             print(p)
             print("胜率：" )
             print(v)
            # return [p,v]

  


    
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
    

def next_batch(batch_num):               #测试用
    start = (batch_num * BATCH_SIZE) % TRAINDATANUM
    end = min(start+BATCH_SIZE, TRAINDATANUM)
    
    #batch_datax=np.array([[[[0 for x in range(3)] for y in range(34)]for z in range(34)]for b in range(BATCH_SIZE)])
    batch_datax=np.array([[[[0 for x in range(3)] for y in range(34)]for z in range(34)]for b in range(BATCH_SIZE)])
    b=0
    for t in range(start, end):
        datapath=Traindatapath+str(t)+'.txt'
        data=np.loadtxt(datapath)
        #b = t - start
        for i in range(34):
            for j in range(34):
                batch_datax[b][i][j][0]=data[i][j]
                batch_datax[b][i][j][1]=data[i][j]
                batch_datax[b][i][j][2]=data[i][j]
        b+=1
    return batch_datax


def main(argv=None):
    NNAIeval()

if __name__ == '__main__':
    tf.app.run() 
