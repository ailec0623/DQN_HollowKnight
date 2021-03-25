# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf

class Agent:
    def __init__(self,act_dim,algorithm,e_greed=0.1,e_greed_decrement=0):
        self.act_dim = act_dim
        self.algorithm = algorithm
        self.e_greed = e_greed
        self.e_greed_decrement = e_greed_decrement


    def sample(self, station):
        # print("self.e_greed: ", self.e_greed)
        sample = np.random.rand()  # 产生0~1之间的小数
        if sample < self.e_greed:
            act = np.random.randint(self.act_dim)  # 探索：每个动作都有概率被选择
        else:
            act = self.predict(station)  # 选择最优动作
            # print(act)
        self.e_greed = max(
            0.01, self.e_greed - self.e_greed_decrement)  # 随着训练逐步收敛，探索的程度慢慢降低
        return act
    
    def predict(self,station):
        station = tf.expand_dims(station,axis=0)
        action = self.algorithm.model.predict(station)
        # print(action)
        return np.argmax(action)
