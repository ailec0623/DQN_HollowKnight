# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf

class Agent:
    def __init__(self,act_dim,algorithm,e_greed=0.1,e_greed_decrement=0):
        self.act_dim = act_dim
        self.algorithm = algorithm
        self.e_greed = e_greed
        self.e_greed_decrement = e_greed_decrement


    def sample(self, station, soul):
        
        pred_move, pred_act = self.algorithm.model.predict(station)
        # print(pred_move)
        pred_move = pred_move.numpy()
        pred_act = pred_act.numpy()
        sample = np.random.rand()  
        if sample < self.e_greed:
            move = np.random.randint(4)  # 探索：每个动作都有概率被选择
        else:
            move = np.argmax(pred_move)
        self.e_greed = max(
            0.01, self.e_greed - self.e_greed_decrement)  

        sample = np.random.rand() 
        if sample < self.e_greed:
            act = np.random.randint(self.act_dim)  
        else:
            act = np.argmax(pred_act)
            if soul < 33:
                if act == 4 or act == 5:
                    pred_act[0][4] = -20
                    pred_act[0][5] = -20
            act = np.argmax(pred_act)

        self.e_greed = max(
            0.05, self.e_greed - self.e_greed_decrement)  
        return move, act
    