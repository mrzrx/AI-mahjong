# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 08:16:51 2018

@author: kk
"""

import tensorflow as tf

KERNEL_SIZE = 3
FILTERS = 256
CHANNEL = 3

NUM_POLICY = 19



def inference(input_tensor, regularizer, train_batchnorm):
    ''' 输入模块'''
    with tf.variable_scope('layer-input'):
      #  tf.summary.histogram('layer-input/input_tensor', input_tensor)
        input_tensor_batch = batch_norm(input_tensor, CHANNEL, train_batchnorm)
        weights_input = tf.get_variable("weight_input",  [KERNEL_SIZE, KERNEL_SIZE, CHANNEL, FILTERS],
                                        initializer=tf.truncated_normal_initializer(stddev=0.1))
       # variable_summaries(weights_input, 'layer-input/w_input')
       # biases_input = tf.get_variable("bias_input", [FILTERS], initializer=tf.constant_initializer(0.0))
        
        conv_input = tf.nn.conv2d(input_tensor_batch, weights_input, strides=[1,1,1,1], padding='SAME')
        #tf.summary.histogram('layer-input/conv_input', conv_input)
        conv_input_batch_norm = batch_norm(conv_input, FILTERS, train_batchnorm)
        #variable_summaries(conv_input_batch_norm, 'layer-input/batch_input')
        relu_input = tf.nn.relu(conv_input_batch_norm)
        #tf.summary.histogram('layer-input/relu_input', relu_input)
        
    '''残差网络'''
    with tf.variable_scope('layer-res1'):
        layer_res1 = res_block(relu_input, train_batchnorm)
        
    with tf.variable_scope('layer-res2'):
        layer_res2 = res_block(layer_res1, train_batchnorm)
        
    with tf.variable_scope('layer-res3'):
        layer_res3 = res_block(layer_res2, train_batchnorm)
        
    with tf.variable_scope('layer-res4'):
        layer_res4 = res_block(layer_res3, train_batchnorm)
        
    with tf.variable_scope('layer-res5'):
        layer_res5 = res_block(layer_res4, train_batchnorm)
        
    with tf.variable_scope('layer-res6'):
        layer_res6 = res_block(layer_res5, train_batchnorm)
        
    with tf.variable_scope('layer-res7'):
        layer_res7 = res_block(layer_res6, train_batchnorm)
        
    with tf.variable_scope('layer-res8'):
        layer_res8 = res_block(layer_res7, train_batchnorm)
        
    with tf.variable_scope('layer-res9'):
        layer_res9 = res_block(layer_res8, train_batchnorm)
        
    with tf.variable_scope('layer-res10'):
        layer_res10 = res_block(layer_res9, train_batchnorm)
        
    with tf.variable_scope('layer-res11'):
        layer_res11 = res_block(layer_res10, train_batchnorm)
        
    with tf.variable_scope('layer-res12'):
        layer_res12 = res_block(layer_res11, train_batchnorm)
        
    with tf.variable_scope('layer-res13'):
        layer_res13 = res_block(layer_res12, train_batchnorm)
        
    with tf.variable_scope('layer-res14'):
        layer_res14 = res_block(layer_res13, train_batchnorm)
        
    with tf.variable_scope('layer-res15'):
        layer_res15 = res_block(layer_res14, train_batchnorm)
        
    with tf.variable_scope('layer-res16'):
        layer_res16 = res_block(layer_res15, train_batchnorm)
        
    with tf.variable_scope('layer-res17'):
        layer_res17 = res_block(layer_res16, train_batchnorm)
        
    with tf.variable_scope('layer-res18'):
        layer_res18 = res_block(layer_res17, train_batchnorm)
        
    with tf.variable_scope('layer-res19'):
        layer_res19 = res_block(layer_res18, train_batchnorm)
        
    ''' policy head '''
    with tf.variable_scope('layer-policy'):
        weights_policy = tf.get_variable("weight_p",  [1, 1, 256, 2],
                                        initializer=tf.truncated_normal_initializer(stddev=0.1))
        #biases_policy = tf.get_variable("bias_p", [2], initializer=tf.constant_initializer(0.0))
        
        conv_policy = tf.nn.conv2d(layer_res19, weights_policy, strides=[1,1,1,1], padding='SAME')
        conv_policy_batch_norm = batch_norm(conv_policy, 2, train_batchnorm)
        relu_policy = tf.nn.relu(conv_policy_batch_norm)

    shape_policy = relu_policy.get_shape().as_list()
    nodes_policy = shape_policy[1] * shape_policy[2] * shape_policy[3]
    reshaped_policy = tf.reshape(relu_policy, [shape_policy[0], nodes_policy])
    
    with tf.variable_scope('layer-policy-fc'):
        weights_policy_fc = tf.get_variable("weight_p_fc", [nodes_policy, NUM_POLICY], 
                                            initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(weights_policy_fc))
        biases_policy_fc = tf.get_variable("bias_p_fc", [NUM_POLICY], 
                                           initializer=tf.constant_initializer(0.1))
        policy_fc = tf.matmul(reshaped_policy, weights_policy_fc) + biases_policy_fc
       # output_policy = tf.nn.softmax(policy_fc)
        

    '''value head'''
    with tf.variable_scope('layer_value'):
        weights_value = tf.get_variable("weight_v", [1, 1, 256, 1],
                                       initializer=tf.truncated_normal_initializer(stddev=0.1))
        #biases_value = tf.get_variable("bias_v", [1], initializer=tf.constant_initializer(0.0))
        conv_value = tf.nn.conv2d(layer_res19, weights_value, strides=[1,1,1,1],padding='SAME')      
        conv_value_batch_norm = batch_norm(conv_value, 1, train_batchnorm)        
        relu_value = tf.nn.relu(conv_value_batch_norm)
        
    shape_value = relu_value.get_shape().as_list()
    nodes_value = shape_value[1] * shape_value[2] * shape_value[3]
    reshaped_value = tf.reshape(relu_value, [shape_value[0], nodes_value])
    
    with tf.variable_scope('layer-value-fc1'):
        weights_value_fc1 = tf.get_variable("weight_v_fc1", [nodes_value, 256], initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(weights_value_fc1))
        biases_value_fc1 = tf.get_variable("bias_v_fc1", [256], initializer=tf.constant_initializer(0.1))
        value_fc1 = tf.nn.relu(tf.matmul(reshaped_value, weights_value_fc1) + biases_value_fc1)
    #    if train: value_fc1 = tf.nn.dropout(value_fc1, 0.5)
        
    with tf.variable_scope('layer-value-fc2'):
        weights_value_fc2 = tf.get_variable("weight_v_fc2", [256, 1], initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(weights_value_fc2))
        biases_value_fc2 = tf.get_variable("bias_v_fc2", [1], initializer=tf.constant_initializer(0.1))
        value_fc2 = tf.matmul(value_fc1, weights_value_fc2) + biases_value_fc2
        output_value = tf.nn.tanh(value_fc2)
    
    return [policy_fc, output_value]
        





        
'''残差模块'''
def res_block(input, train):
    conv1_weights = tf.get_variable("weight1",  [KERNEL_SIZE, KERNEL_SIZE, FILTERS, FILTERS],
                                        initializer=tf.truncated_normal_initializer(stddev=0.1))
    #conv1_biases = tf.get_variable("bias1", [256], initializer=tf.constant_initializer(0.0))
        
    conv1 = tf.nn.conv2d(input, conv1_weights, strides=[1,1,1,1], padding='SAME')
    conv1_batch_norm = batch_norm(conv1, FILTERS, train)
    relu1 = tf.nn.relu(conv1_batch_norm)
        
        
    conv2_weights = tf.get_variable("weight2",  [KERNEL_SIZE, KERNEL_SIZE, FILTERS, FILTERS],
                                        initializer=tf.truncated_normal_initializer(stddev=0.1))
    #conv2_biases = tf.get_variable("bias2", [256], initializer=tf.constant_initializer(0.0))
        
    conv2 = tf.nn.conv2d(relu1, conv2_weights, strides=[1,1,1,1], padding='SAME')
    conv2_batch_norm = batch_norm(conv2, FILTERS, train)
    conv2_res = input + conv2_batch_norm
    
    
    return tf.nn.relu(conv2_res)
        
        
        
'''batch-norm'''
def batch_norm(input, filters, is_training):
  #  mean, variance = tf.nn.moments(input, [0,1,2])
   # scale = tf.Variable(tf.ones([filters]))
    #offset = tf.Variable(tf.zeros([filters]))
    gamma = tf.Variable(tf.ones([filters]))
    beta = tf.Variable(tf.zeros([filters]))

    pop_mean = tf.Variable(tf.zeros([filters]), trainable=False)
    pop_variance = tf.Variable(tf.ones([filters]), trainable=False)
    
    epsilon = 0.001
 #   return tf.nn.batch_normalization(input, mean, variance, beta, gamma, variance_epsilon)
    
    def batch_norm_training():
        batch_mean, batch_variance = tf.nn.moments(input, [0,1,2], keep_dims=False)
        
        decay = 0.99
        train_mean = tf.assign(pop_mean, pop_mean * decay + batch_mean * (1 - decay))
        train_variance = tf.assign(pop_variance, pop_variance * decay + batch_variance * (1 - decay))

        with tf.control_dependencies([train_mean, train_variance]):
            return tf.nn.batch_normalization(input, batch_mean, batch_variance, beta, gamma, epsilon)
 
    def batch_norm_inference():
        return tf.nn.batch_normalization(input, pop_mean, pop_variance, beta, gamma, epsilon)

    batch_normalized_output = tf.cond(is_training, batch_norm_training, batch_norm_inference)
    return batch_normalized_output
    
def variable_summaries(var, name):
    with tf.name_scope('summaries'):
        tf.summary.histogram(name, var)
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean/' + name, mean)
        stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
        tf.summary.scalar('stddev/' + name, stddev)
    
def merged():
    return tf.summary.merge_all()