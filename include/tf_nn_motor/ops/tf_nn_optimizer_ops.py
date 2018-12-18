#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import numpy as np
import tensorflow as tf

def optimizer_minimize(optimizer, tensor_loss,
                        global_step=None,
                        var_list=None,
                        gate_gradients=1,#GATE_NONE = 0, GATE_OP = 1, GATE_GRAPH = 2
                        aggregation_method=None,
                        colocate_gradients_with_ops=False,
                        name=None,
                        grad_loss=None):
    step = optimizer.minimize(
                                loss=tensor_loss,
                                global_step=global_step,
                                var_list=var_list,
                                gate_gradients=gate_gradients,
                                aggregation_method=aggregation_method,
                                colocate_gradients_with_ops=colocate_gradients_with_ops,
                                name=name,
                                grad_loss=grad_loss
                            )
    return step
 
def optimizer_sgd(learning_rate=0.001, use_locking=False, name='GradientDescent'):
    return tf.train.GradientDescentOptimizer(learning_rate, use_locking, name)
     
def optimizer_adam(learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-08, use_locking=False,name='Adam'):
    return tf.train.AdamOptimizer(learning_rate, beta1, beta2, epsilon, use_locking, name)
     
def optimizer_adagrad(learning_rate=0.001, initial_accumulator_value=0.1, use_locking=False, name='Adagrad'):
    return tf.train.AdagradOptimizer(learning_rate, initial_accumulator_value, use_locking, name)
    
def optimizer_adagradda(
                        learning_rate,#0.001
                        global_step,
                        initial_gradient_squared_accumulator_value=0.1,
                        l1_regularization_strength=0.0,
                        l2_regularization_strength=0.0,
                        use_locking=False,
                        name='AdagradDA'
                        ):
    return tf.train.AdagradDAOptimizer(learning_rate, global_step,
                        initial_gradient_squared_accumulator_value,
                        l1_regularization_strength,
                        l2_regularization_strength,
                        use_locking,
                        name)








