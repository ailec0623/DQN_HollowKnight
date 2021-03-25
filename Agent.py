# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf

class Agent:
    def __init__(self,act_dim,act_seq,algorithm,e_greed=0.1,e_greed_decrement=0):
        self.act_dim = act_dim
        self.act_seq = act_seq
        self.algorithm = algorithm
        self.e_greed = e_greed
        self.e_greed_decrement = e_greed_decrement


    def sample(self, station):
        # print("self.e_greed: ", self.e_greed)
        acts = self.predict(station)
        for i in range(self.act_seq):
            sample = np.random.rand()  # 产生0~1之间的小数
            if sample < self.e_greed:
                acts[i] = np.random.randint(self.act_dim)  # 探索：每个动作都有概率被选择

        self.e_greed = max(
            0.05, self.e_greed - self.e_greed_decrement)  # 随着训练逐步收敛，探索的程度慢慢降低
        return acts
    
    def predict(self,station):
        station = tf.expand_dims(station,axis=0)
        actions = self.algorithm.model.predict(station)
        # print(actions.shape)
        actions = actions.reshape((self.act_seq, self.act_dim))
        acts = []
        for i in range(self.act_seq):
            acts.append(np.argmax(actions[i]))
        # print(action)
        return acts
