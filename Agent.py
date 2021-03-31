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
        
        pred_move, pred_act = self.algorithm.model.predict(station)
        print(pred_move)

        sample = np.random.rand()  
        if sample < self.e_greed:
            move = np.random.randint(4)  # 探索：每个动作都有概率被选择
        else:
            move = np.argmax(pred_move)
        self.e_greed = max(
            0.05, self.e_greed - self.e_greed_decrement)  

        sample = np.random.rand() 
        if sample < self.e_greed:
            act = np.random.randint(self.act_dim)  
        else:
            act = np.argmax(pred_act)
        self.e_greed = max(
            0.05, self.e_greed - self.e_greed_decrement)  
        return move, act
    

    def act_sample(self, station):
        # print("self.e_greed: ", self.e_greed)
        sample = np.random.rand() 
        if sample < self.e_greed:
            act = np.random.randint(self.act_dim)  # 探索：每个动作都有概率被选择
        else:
            act = self.act_predict(station)  
        self.e_greed = max(
            0.05, self.e_greed - self.e_greed_decrement)  
        return act
    
    def act_predict(self,station):
        station = tf.expand_dims(station,axis=0)
        action = self.algorithm.act_model.predict(station)
        return np.argmax(action)


    def move_sample(self, obs):
        sample = np.random.rand()  
        if sample < self.e_greed:
            move = np.random.randint(4)  # 探索：每个动作都有概率被选择
        else:
            move = self.move_predict(obs)  
        self.e_greed = max(
            0.05, self.e_greed - self.e_greed_decrement)  
        return move
    
    def move_predict(self,obs):
        obs = tf.expand_dims(obs,axis=0)
        direction = self.algorithm.move_model.predict(obs)
        # print(direction)
        return np.argmax(direction)
