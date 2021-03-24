# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 21:10:06 2021

@author: pang
"""

import Tool.Helper
from Tool.Actions import take_action, restart
from Tool.GrabScreen import grab_screen
from Tool.GetHP import boss_hp, player_hp
from Model import DQN


import numpy as np
import cv2
import time
import random
import os
import pandas as pd
import random
import tensorflow.compat.v1 as tf

DQN_model_path = "model_gpu"
DQN_log_path = "logs_gpu/"

action_name = ["Nothing", "Move_Left", "Move_Right", "Attack_Left", "Attack_Right", "Attack_Up",
           "Short_Jump", "Mid_Jump", "Long_Jump", "Skill_Down", "Skill_Left", 
           "Skill_Right", "Skill_Up", "Rush_Left", "Rush_Right", "Cure"]

HP_WIDTH = 768
HP_HEIGHT = 407
WIDTH = 152
HEIGHT = 80

window_size = (0,0,1920,1017)

action_size = 13
# action[n_choose,j,k,m,r]
# j-attack, k-jump, m-defense, r-dodge, n_choose-do nothing

EPISODES = 3000
big_BATCH_SIZE = 24
UPDATE_STEP = 50
# times that evaluate the network
num_step = 0
# used to save log graph
target_step = 0
# used to update target Q network
paused = True
# used to stop training

if __name__ == '__main__':
    PASS_COUNT = 0
    agent = DQN(WIDTH, HEIGHT, action_size, DQN_model_path, DQN_log_path)
    print("Model init successfully")
    # DQN init
    paused = Tool.Helper.pause_game(paused)
    # paused at the begin
    emergence_break = 0     
    # emergence_break is used to break down training
    # 用于防止出现意外紧急停止训练防止错误训练数据扰乱神经网络
    for episode in range(EPISODES):
        restart()
        screen_gray = cv2.cvtColor(grab_screen(window_size),cv2.COLOR_BGR2GRAY)
        # collect station gray graph
        station = cv2.resize(screen_gray,(WIDTH,HEIGHT))
        hp_station = cv2.resize(screen_gray,(HP_WIDTH,HP_HEIGHT))
        # change graph to WIDTH * HEIGHT for station input
        boss_blood = boss_hp(hp_station, 570)
        last_hp = boss_blood
        self_blood = player_hp(hp_station)
        # count init blood
        target_step = 0
        # used to update target Q network
        done = 0
        total_reward = 0
        min_hp = 9

        last_time = time.time()
        while True:
            station = np.array(station).reshape(-1,HEIGHT,WIDTH,1)[0]
            # reshape station for tf input placeholder
            #print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
            target_step += 1
            # get the action by state
            action = agent.Choose_Action(station)
            take_action(action)
            # take station then the station change
            screen_gray = cv2.cvtColor(grab_screen(window_size),cv2.COLOR_BGR2GRAY)
            # collect blood gray graph for count self and boss blood

            next_station = cv2.resize(screen_gray,(WIDTH,HEIGHT))
            next_hp_station = cv2.resize(screen_gray,(HP_WIDTH,HP_HEIGHT))

            next_boss_blood = boss_hp(next_hp_station, last_hp)
            last_hp = boss_blood
            next_self_blood = player_hp(next_hp_station)

            next_station = np.array(next_station).reshape(-1,HEIGHT,WIDTH,1)[0]
            reward, done, min_hp, emergence_break = Tool.Helper.action_judge(action, boss_blood, next_boss_blood,
                                                               self_blood, next_self_blood, min_hp, emergence_break)
            if reward != 0 and reward != -1 and reward != 1:
                print(action_name[action], ": ", reward)
            # get action reward
            if emergence_break == 100:
                # emergence break , save model and paused
                # 遇到紧急情况，保存数据，并且暂停
                print("emergence_break")
                agent.save_model()
                paused = True
            agent.Store_Data(station, action, reward, next_station, done)
            if len(agent.replay_buffer) > big_BATCH_SIZE:
                num_step += 1
                # save loss graph
                # print('train')
                agent.Train_Network(big_BATCH_SIZE, num_step)
            if target_step % UPDATE_STEP == 0:
                agent.Update_Target_Network()
                # update target Q network
            station = next_station
            self_blood = next_self_blood
            boss_blood = next_boss_blood
            total_reward += reward
            paused = Tool.Helper.pause_game(paused)
            if done == 1:
                break
            elif done == 2:
                PASS_COUNT += 1
                time.sleep(6)
                break
        if episode % 10 == 0:
            agent.save_model()
            # save model
        print('episode: ', episode, '\nEvaluation Average Reward:', total_reward/target_step, "\nPass count: ", PASS_COUNT)
        
        
            
            
            
            
            
        
        
    
    