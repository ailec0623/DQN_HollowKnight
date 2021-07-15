# -*- coding: utf-8 -*-
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf
import os
import cv2
import time
import collections
import matplotlib.pyplot as plt

from Model import Model
from DQN import DQN
from Agent import Agent
from ReplayMemory import ReplayMemory


import Tool.Helper
import Tool.Actions
from Tool.Helper import mean, is_end
from Tool.Actions import take_action, restart,take_direction, TackAction
from Tool.WindowsAPI import grab_screen
from Tool.GetHP import Hp_getter
from Tool.UserInput import User
from Tool.FrameBuffer import FrameBuffer

window_size = (0,0,1920,1017)
station_size = (230, 230, 1670, 930)

HP_WIDTH = 768
HP_HEIGHT = 407
WIDTH = 400
HEIGHT = 200
ACTION_DIM = 7
FRAMEBUFFERSIZE = 4
INPUT_SHAPE = (FRAMEBUFFERSIZE, HEIGHT, WIDTH, 3)

LEARN_FREQ = 30  # 训练频率，不需要每一个step都learn，攒一些新增经验后再learn，提高效率
MEMORY_SIZE = 200  # replay memory的大小，越大越占用内存
MEMORY_WARMUP_SIZE = 24  # replay_memory 里需要预存一些经验数据，再从里面sample一个batch的经验让agent去learn
BATCH_SIZE = 24  # 每次给agent learn的数据数量，从replay memory随机里sample一批数据出来
LEARNING_RATE = 0.00001  # 学习率
GAMMA = 0.99  # reward 的衰减因子，一般取 0.9 到 0.999 不等

action_name = ["Attack", "Attack_Up",
           "Short_Jump", "Mid_Jump", "Skill_Up", 
           "Skill_Down", "Rush", "Cure"]

move_name = ["Move_Left", "Move_Right", "Turn_Left", "Turn_Right"]

DELAY_REWARD = 1


if __name__ == '__main__':

    # In case of out of memory
    config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
    config.gpu_options.allow_growth = True      #程序按需申请内存
    sess = tf.compat.v1.Session(config = config)

    PASS_COUNT = 0                                       # pass count
    total_remind_hp = 0

    act_rmp_correct = ReplayMemory(MEMORY_SIZE, file_name='./act_memory')         # experience pool
    act_rmp_wrong = ReplayMemory(MEMORY_SIZE, file_name='./act_memory')         # experience pool
    move_rmp_correct = ReplayMemory(MEMORY_SIZE,file_name='./move_memory')         # experience pool
    move_rmp_wrong = ReplayMemory(MEMORY_SIZE,file_name='./move_memory')         # experience pool
    
    # new model, if exit save file, load it
    model = Model(INPUT_SHAPE, ACTION_DIM)  

    # Hp counter
    hp = Hp_getter()


    model.load_model()
    algorithm = DQN(model, gamma=GAMMA, learnging_rate=LEARNING_RATE)
    agent = Agent(ACTION_DIM,algorithm,e_greed=0.6,e_greed_decrement=1e-6)
    
    # get user input, no need anymore
    # user = User()

    # paused at the begining


    # 开始训练
    episode = 0

    for x in os.listdir(act_rmp_correct.file_name):
        file_name = act_rmp_correct.file_name + "/" + x
        act_rmp_correct.load(file_name)
        for i in range(10):
            if (len(act_rmp_correct) > MEMORY_WARMUP_SIZE):
                # print("action learning")
                batch_station,batch_actions,batch_reward,batch_next_station,batch_done = act_rmp_correct.sample(BATCH_SIZE)
                algorithm.act_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)

    for x in os.listdir(move_rmp_correct.file_name):
        file_name = move_rmp_correct.file_name + "/" + x
        move_rmp_correct.load(file_name)
        for i in range(10):
            if (len(move_rmp_correct) > MEMORY_WARMUP_SIZE):
                # print("action learning")
                batch_station,batch_actions,batch_reward,batch_next_station,batch_done = move_rmp_correct.sample(BATCH_SIZE)
                algorithm.move_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)

    model.save_mode()
    # while episode < max_episode:    # 训练max_episode个回合，test部分不计算入episode数量
    #     # 训练
           
    #     # if episode % 20 == 1:
    #     #     algorithm.replace_target()
    #     act_rmp_correct.load(act_rmp_correct.file_name+ "/memory_" + str(episode) +".txt")
    #     move_rmp_correct.load(move_rmp_correct.file_name+ "/memory_" + str(episode) +".txt")

    #     run_episode(algorithm,act_rmp_correct, move_rmp_correct)

    #     if episode % 10 == 1:
    #         model.save_mode()
    #     episode += 1  
    #     print("Episode: ", episode)

