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
from Tool.Actions import take_action, restart,take_direction
from Tool.WindowsAPI import grab_screen
from Tool.GetHP import boss_hp, player_hp
from Tool.UserInput import User

window_size = (0,0,1920,1017)
station_size = (230, 230, 1670, 930)

HP_WIDTH = 768
HP_HEIGHT = 407
WIDTH = 400
HEIGHT = 200
ACTION_DIM = 9
INPUT_SHAPE = (HEIGHT, WIDTH, 3)

LEARN_FREQ = 30  # 训练频率，不需要每一个step都learn，攒一些新增经验后再learn，提高效率
MEMORY_SIZE = 200  # replay memory的大小，越大越占用内存
MEMORY_WARMUP_SIZE = 20  # replay_memory 里需要预存一些经验数据，再从里面sample一个batch的经验让agent去learn
BATCH_SIZE = 8  # 每次给agent learn的数据数量，从replay memory随机里sample一批数据出来
LEARNING_RATE = 0.001  # 学习率
GAMMA = 0.99  # reward 的衰减因子，一般取 0.9 到 0.999 不等

action_name = ["Attack", "Attack_Down", "Attack_Up",
           "Short_Jump", "Mid_Jump", "Skill", "Skill_Up", 
           "Skill_Down", "Rush", "Cure"]

move_name = ["Move_Left", "Move_Right", "Turn_Left", "Turn_Right"]

USER = False
DELEY_REWARD = 3




def run_episode(algorithm,agent,act_rmp,move_rmp,PASS_COUNT,paused):
    restart()
    
    for i in range(1):
        if (len(move_rmp) > MEMORY_WARMUP_SIZE):
            print("move learning")
            batch_station,batch_actions,batch_reward,batch_next_station,batch_done = move_rmp.sample(BATCH_SIZE)
            algorithm.move_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)   

        if (len(act_rmp) > MEMORY_WARMUP_SIZE):
            print("action learning")
            batch_station,batch_actions,batch_reward,batch_next_station,batch_done = act_rmp.sample(BATCH_SIZE)
            algorithm.act_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)




    station = cv2.resize(cv2.cvtColor(grab_screen(station_size), cv2.COLOR_RGBA2RGB),(WIDTH,HEIGHT))
    hp_station = cv2.cvtColor(cv2.resize(grab_screen(window_size),(HP_WIDTH,HP_HEIGHT)),cv2.COLOR_BGR2GRAY)

    boss_hp_value = boss_hp(hp_station, 570)
    boss_last_hp = boss_hp_value
    self_hp = player_hp(hp_station)
    min_hp = 9


    step = 0
    done = 0
    total_reward = 0


    # start_time = time.time()
    # Deley Reward
    DeleyReward = collections.deque(maxlen=DELEY_REWARD)
    DeleyStation = collections.deque(maxlen=DELEY_REWARD)
    DeleyActions = collections.deque(maxlen=DELEY_REWARD)
    DeleyDirection = collections.deque(maxlen=DELEY_REWARD)

    # move direction of player 0 for stay, 1 for left, 2 for right
    while True:
        
        # player hp bar is not in normal state and the left pixels are not black
        if(hp_station[40][95] != 56 and hp_station[300][30] > 20 and hp_station[200][30] > 20):
            # print("Not in game yet 1")
            hp_station = cv2.cvtColor(cv2.resize(grab_screen(window_size),(HP_WIDTH,HP_HEIGHT)),cv2.COLOR_BGR2GRAY)
            continue
        
        # there is not boss hp bar
        if hp_station[401][98] != 0 and hp_station[401][98] == 0:
            # print("Not in game yet 2")
            hp_station = cv2.cvtColor(cv2.resize(grab_screen(window_size),(HP_WIDTH,HP_HEIGHT)),cv2.COLOR_BGR2GRAY)
            continue

        # last_time = time.time()
        # no more than 10 mins
        # if time.time() - start_time > 600:
        #     break

        

        d = agent.move_sample(station)
        action = agent.act_sample(station)
        step += 1

        # print("Move:", move_name[d] )
        take_direction(d)
        take_action(action)


        next_station = cv2.resize(cv2.cvtColor(grab_screen(station_size), cv2.COLOR_RGBA2RGB),(WIDTH,HEIGHT))
        next_hp_station = cv2.cvtColor(cv2.resize(grab_screen(window_size),(HP_WIDTH,HP_HEIGHT)),cv2.COLOR_BGR2GRAY)

        next_boss_hp_value = boss_hp(next_hp_station, boss_last_hp)
        boss_last_hp = boss_hp_value
        next_self_hp = player_hp(next_hp_station)

        if min_hp == 9 and next_self_hp == 1:
            next_self_hp = 9

        reward, done, min_hp = Tool.Helper.action_judge(boss_hp_value, next_boss_hp_value,self_hp, next_self_hp, min_hp)
            # print(reward)
        print( action_name[action], ", ", move_name[d], ", ", reward)

        DeleyReward.append(reward)
        DeleyStation.append(station)
        DeleyActions.append(action)
        DeleyDirection.append(d)

        print(mean(DeleyReward))


        if len(DeleyReward) >= DELEY_REWARD:
            move_rmp.append((DeleyStation[0],DeleyDirection[0],mean(DeleyReward),DeleyStation[1],done))
            act_rmp.append((DeleyStation[0],DeleyActions[0],mean(DeleyReward),DeleyStation[1],done))

        station = next_station
        self_hp = next_self_hp
        boss_hp_value = next_boss_hp_value
            

        # if (len(act_rmp) > MEMORY_WARMUP_SIZE and int(step/ACTION_SEQ) % LEARN_FREQ == 0):
        #     print("action learning")
        #     batch_station,batch_actions,batch_reward,batch_next_station,batch_done = act_rmp.sample(BATCH_SIZE)
        #     algorithm.act_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)

        total_reward += reward
        paused = Tool.Helper.pause_game(paused)

        if done == 1:
            Tool.Actions.Nothing()
            break
        elif done == 2:
            PASS_COUNT += 1
            Tool.Actions.Nothing()
            break



    for i in range(2):
        if (len(move_rmp) > MEMORY_WARMUP_SIZE):
            print("move learning")
            batch_station,batch_moveions,batch_reward,batch_next_station,batch_done = move_rmp.sample(BATCH_SIZE)
            algorithm.move_learn(batch_station,batch_moveions,batch_reward,batch_next_station,batch_done)   

        if (len(act_rmp) > MEMORY_WARMUP_SIZE):
            print("action learning")
            batch_station,batch_actions,batch_reward,batch_next_station,batch_done = act_rmp.sample(BATCH_SIZE)
            algorithm.act_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)

    return total_reward, step, PASS_COUNT


if __name__ == '__main__':

    # In case of out of memory
    config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
    config.gpu_options.allow_growth = True
    config.gpu_options.allow_growth = True      #程序按需申请内存
    sess = tf.compat.v1.Session(config = config)

    PASS_COUNT = 0                                       # pass count

    act_rmp = ReplayMemory(MEMORY_SIZE, file_name='./act_memory', user = USER)         # experience pool
    move_rmp = ReplayMemory(MEMORY_SIZE,file_name='./move_memory', user = USER)         # experience pool
    
    # new model, if exit save file, load it
    model = Model(INPUT_SHAPE, ACTION_DIM)  
    if os.path.exists('./model/act_model.h5'):
        print("model exists , load model\n")
        model.load_model()
    algorithm = DQN(model, gamma=GAMMA, learnging_rate=LEARNING_RATE)
    agent = Agent(ACTION_DIM,algorithm,e_greed=0.5,e_greed_decrement=1e-5)
    
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
        if USER: # train by human, no need anymore
            total_reward, total_step = user_run(algorithm,user,act_rmp, PASS_COUNT, paused)            
            model.save_mode()
        else:
            if episode % 10 == 1:
                algorithm.replace_target()

            total_reward, total_step, PASS_COUNT = run_episode(algorithm,agent,act_rmp, move_rmp, PASS_COUNT, paused)

            if episode % 10 == 1:
                model.save_mode()
                
        print("Episode: ", episode, ", mean(reward):", total_reward/total_step,", pass_count: " , PASS_COUNT)

