import tensorflow as tf
import numpy as np
import argparse
import os
import sys
import math
import pickle
from sklearn.svm import SVC
from scipy import misc
from six.moves import xrange
import cv2
from sklearn.preprocessing import normalize

class FaceNet():

    def __init__(self, model_path):
        self.model_path = model_path

    def predict(self, input_batch):
        input_batch=tf.transpose(input_batch, [0, 2, 3, 1])
        input_batch=tf.image.resize(input_batch,(160,160))
        input_batch=(tf.cast(input_batch, tf.float32) - 127.5) / 128.0
        input_map = {'image_batch': input_batch, 'phase_train': False}
        with tf.gfile.GFile(self.model_path, "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def, input_map=input_map, name='')
            # Get output tensor
            embeddings = graph.get_tensor_by_name("embeddings:0")
            print('embeddings.shape:')
            print(embeddings.shape)
            return tf.math.l2_normalize(embeddings)

    # config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)
    # config.gpu_options.allow_growth = True
    # self.session = tf.Session(config=config, graph=self.graph)

    # img = cv2.imread(img_path)
    # embed = self.session.run(self.output, feed_dict={self.input: self.preprocess_img(img), self.phase_train_placeholder: False})
    # embed = normalize(embed)
    # embed = embed.reshape((512,))
    # config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)
    # config.gpu_options.allow_growth = True
    # self.session = tf.Session(config=config, graph=self.graph)
    # batch_size_placeholder = tf.placeholder(tf.int32, name='batch_size')
    # minibatch0, channel1, height2, width3
    #
    #
    # # Get TensorFlow expression(s) for the output(s) of this network, given the inputs.
    # def get_output_for(self, *in_expr, return_as_list=False, **dynamic_kwargs):
    #     assert len(in_expr) == self.num_inputs
    #     all_kwargs = dict(self.static_kwargs)
    #     all_kwargs.update(dynamic_kwargs)
    #     with tf.variable_scope(self.scope, reuse=True):
    #         assert tf.get_variable_scope().name == self.scope
    #         named_inputs = [tf.identity(expr, name=name) for expr, name in zip(in_expr, self.input_names)]
    #
    #         out_expr = self._build_func(*named_inputs, **all_kwargs)
    #     assert is_tf_expression(out_expr) or isinstance(out_expr, tuple)
    #     if return_as_list:
    #         out_expr = [out_expr] if is_tf_expression(out_expr) else list(out_expr)
    #     return out_expr
    #
    # def preprocess_img(self, x):
    #     x = cv2.resize(x, (160, 160))
    #     y = (np.float32(x) - 127.5) / 128.0
    #     return np.expand_dims(y, 0)