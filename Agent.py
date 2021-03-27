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


    def act_sample(self, station):
        # print("self.e_greed: ", self.e_greed)
        acts = self.act_predict(station)
        for i in range(self.act_seq):
            sample = np.random.rand()  # 产生0~1之间的小数
            if sample < self.e_greed:
                acts[i] = np.random.randint(self.act_dim)  # 探索：每个动作都有概率被选择

        self.e_greed = max(
            0.05, self.e_greed - self.e_greed_decrement)  # 随着训练逐步收敛，探索的程度慢慢降低
        return acts
    
    def act_predict(self,station):
        station = tf.expand_dims(station,axis=0)
        actions = self.algorithm.act_model.predict(station)
        # print(actions.shape)
        actions = actions.reshape((self.act_seq, self.act_dim))
        acts = []
        for i in range(self.act_seq):
            acts.append(np.argmax(actions[i]))
        # print(action)
        return acts


    def move_sample(self, obs):
        sample = np.random.rand()  # 产生0~1之间的小数
        if sample < self.e_greed:
            act = np.random.randint(3)  # 探索：每个动作都有概率被选择
        else:
            act = self.move_predict(obs)  # 选择最优动作
        self.e_greed = max(
            0.01, self.e_greed - self.e_greed_decrement)  # 随着训练逐步收敛，探索的程度慢慢降低
        return act
    
    def move_predict(self,obs):
        obs = tf.expand_dims(obs,axis=0)
        action = self.algorithm.move_model.predict(obs)
        return np.argmax(action)
