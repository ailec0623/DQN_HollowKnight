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

action_name = ["Attack", "Attack_Down", "Attack_Up",
           "Short_Jump", "Mid_Jump", "Skill", "Skill_Up", 
           "Skill_Down", "Rush", "Cure"]

move_name = ["Move_Left", "Move_Right", "Turn_Left", "Turn_Right"]

DELAY_REWARD = 1




def run_episode(hp, algorithm,agent,act_rmp_correct,act_rmp_wrong, move_rmp_correct, move_rmp_wrong,PASS_COUNT,paused):
    restart()
    # learn while load game
    for i in range(1):
        if (len(move_rmp_correct) > MEMORY_WARMUP_SIZE):
            # print("move learning")
            batch_station,batch_actions,batch_reward,batch_next_station,batch_done = move_rmp_correct.sample(BATCH_SIZE)
            algorithm.move_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)   

        if (len(act_rmp_correct) > MEMORY_WARMUP_SIZE):
            # print("action learning")
            batch_station,batch_actions,batch_reward,batch_next_station,batch_done = act_rmp_correct.sample(BATCH_SIZE)
            algorithm.act_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)
        if (len(move_rmp_wrong) > MEMORY_WARMUP_SIZE):
            # print("move learning")
            batch_station,batch_actions,batch_reward,batch_next_station,batch_done = move_rmp_wrong.sample(BATCH_SIZE)
            algorithm.move_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)   

        if (len(act_rmp_wrong) > MEMORY_WARMUP_SIZE):
            # print("action learning")
            batch_station,batch_actions,batch_reward,batch_next_station,batch_done = act_rmp_wrong.sample(BATCH_SIZE)
            algorithm.act_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)
    
    step = 0
    done = 0
    total_reward = 0

    start_time = time.time()
    # Delay Reward
    DelayMoveReward = collections.deque(maxlen=DELAY_REWARD)
    DelayActReward = collections.deque(maxlen=DELAY_REWARD)
    DelayStation = collections.deque(maxlen=DELAY_REWARD + 1) # 1 more for next_station
    DelayActions = collections.deque(maxlen=DELAY_REWARD)
    DelayDirection = collections.deque(maxlen=DELAY_REWARD)
    
    while True:
        boss_hp_value = hp.get_boss_hp()
        self_hp = hp.get_self_hp()
        if boss_hp_value > 800 and  boss_hp_value <= 900 and self_hp >= 1 and self_hp <= 9:
            break
        

    thread1 = FrameBuffer(1, "FrameBuffer", WIDTH, HEIGHT, maxlen=FRAMEBUFFERSIZE)
    thread1.start()

    last_hornet_y = 0
    while True:
        step += 1
        # last_time = time.time()
        # no more than 10 mins
        # if time.time() - start_time > 600:
        #     break

        # in case of do not collect enough frames
        while(len(thread1.buffer) < FRAMEBUFFERSIZE):
            time.sleep(0.1)
        
        stations = thread1.get_buffer()
        boss_hp_value = hp.get_boss_hp()
        self_hp = hp.get_self_hp()
        player_x, player_y = hp.get_play_location()
        hornet_x, hornet_y = hp.get_hornet_location()
        soul = hp.get_souls()

        move, action = agent.sample(stations, soul)

        take_direction(move)
        take_action(action)
        
        
        next_station = thread1.get_buffer()
        next_boss_hp_value = hp.get_boss_hp()
        next_self_hp = hp.get_self_hp()
        next_player_x, next_player_y = hp.get_play_location()
        next_hornet_x, next_hornet_y = hp.get_hornet_location()
        hornet_skill1 = False
        if last_hornet_y > 32 and last_hornet_y < 32.5 and hornet_y > 32 and hornet_y < 32.5:
            hornet_skill1 = True
        last_hornet_y = hornet_y
        # get reward
        move_reward = Tool.Helper.move_judge(self_hp, next_self_hp, player_x, next_player_x, hornet_x, next_hornet_x, move, hornet_skill1)

        act_reward, done = Tool.Helper.action_judge(boss_hp_value, next_boss_hp_value,self_hp, next_self_hp, next_player_x, next_hornet_x, action)
            # print(reward)
        # print( action_name[action], ", ", move_name[d], ", ", reward)
        
        DelayMoveReward.append(move_reward)
        DelayActReward.append(act_reward)
        DelayStation.append(stations)
        DelayActions.append(action)
        DelayDirection.append(move)

        if len(DelayStation) >= DELAY_REWARD + 1:
            if DelayMoveReward[0] > 0:
                move_rmp_correct.append(DelayStation[0],DelayDirection[0],DelayMoveReward[0],DelayStation[1],done)
            if DelayMoveReward[0] < 0:
                move_rmp_wrong.append(DelayStation[0],DelayDirection[0],DelayMoveReward[0],DelayStation[1],done)

        if len(DelayStation) >= DELAY_REWARD + 1:
            if mean(DelayActReward) > 0:
                act_rmp_correct.append(DelayStation[0],DelayActions[0],mean(DelayActReward),DelayStation[1],done)
            if mean(DelayActReward) < 0:
                act_rmp_wrong.append(DelayStation[0],DelayActions[0],mean(DelayActReward),DelayStation[1],done)

        station = next_station
        self_hp = next_self_hp
        boss_hp_value = next_boss_hp_value
            

        # if (len(act_rmp) > MEMORY_WARMUP_SIZE and int(step/ACTION_SEQ) % LEARN_FREQ == 0):
        #     print("action learning")
        #     batch_station,batch_actions,batch_reward,batch_next_station,batch_done = act_rmp.sample(BATCH_SIZE)
        #     algorithm.act_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)

        total_reward += act_reward
        paused = Tool.Helper.pause_game(paused)

        if done == 1:
            Tool.Actions.Nothing()
            break
        elif done == 2:
            PASS_COUNT += 1
            Tool.Actions.Nothing()
            break


    thread1.stop()

    for i in range(1):
        if (len(move_rmp_correct) > MEMORY_WARMUP_SIZE):
            # print("move learning")
            batch_station,batch_actions,batch_reward,batch_next_station,batch_done = move_rmp_correct.sample(BATCH_SIZE)
            algorithm.move_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)   

        if (len(act_rmp_correct) > MEMORY_WARMUP_SIZE):
            # print("action learning")
            batch_station,batch_actions,batch_reward,batch_next_station,batch_done = act_rmp_correct.sample(BATCH_SIZE)
            algorithm.act_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)
        if (len(move_rmp_wrong) > MEMORY_WARMUP_SIZE):
            # print("move learning")
            batch_station,batch_actions,batch_reward,batch_next_station,batch_done = move_rmp_wrong.sample(BATCH_SIZE)
            algorithm.move_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)   

        if (len(act_rmp_wrong) > MEMORY_WARMUP_SIZE):
            # print("action learning")
            batch_station,batch_actions,batch_reward,batch_next_station,batch_done = act_rmp_wrong.sample(BATCH_SIZE)
            algorithm.act_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)

    return total_reward, step, PASS_COUNT


if __name__ == '__main__':

    # In case of out of memory
    config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
    config.gpu_options.allow_growth = True      #程序按需申请内存
    sess = tf.compat.v1.Session(config = config)

    PASS_COUNT = 0                                       # pass count
    total_remind_hp = 0

    act_rmp_correct = ReplayMemory(MEMORY_SIZE, file_name='./act_correct_memory')         # experience pool
    act_rmp_wrong = ReplayMemory(MEMORY_SIZE, file_name='./act_wrong_memory')         # experience pool
    move_rmp_correct = ReplayMemory(MEMORY_SIZE,file_name='./move_correct_memory')         # experience pool
    move_rmp_wrong = ReplayMemory(MEMORY_SIZE,file_name='./move_wrong_memory')         # experience pool
    
    # new model, if exit save file, load it
    model = Model(INPUT_SHAPE, ACTION_DIM)  

    # Hp counter
    hp = Hp_getter()


    model.load_model()
    algorithm = DQN(model, gamma=GAMMA, learnging_rate=LEARNING_RATE)
    agent = Agent(ACTION_DIM,algorithm,e_greed=0,e_greed_decrement=1e-6)
    
    # get user input, no need anymore
    # user = User()

    # paused at the begining
    paused = True
    paused = Tool.Helper.pause_game(paused)

    max_episode = 30000
    # 开始训练
    episode = 0
    while episode < max_episode:    # 训练max_episode个回合，test部分不计算入episode数量
        # 训练
        episode += 1     
        # if episode % 20 == 1:
        #     algorithm.replace_target()

        total_reward, total_step, PASS_COUNT = run_episode(hp, algorithm,agent,act_rmp_correct,act_rmp_wrong, move_rmp_correct, move_rmp_wrong, PASS_COUNT, paused)
                
        print("Episode: ", episode, ", pass_count: " , PASS_COUNT, ", average remind hp:", total_remind_hp / episode)

