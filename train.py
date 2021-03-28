# -*- coding: utf-8 -*-
import numpy as np
from tensorflow.keras.models import load_model
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
from Tool.Actions import take_action, restart
from Tool.WindowsAPI import grab_screen
from Tool.GetHP import boss_hp, player_hp
from Tool.UserInput import User

window_size = (0,0,1920,1017)
station_size = (230, 230, 1670, 930)

HP_WIDTH = 768
HP_HEIGHT = 407
WIDTH = 1000
HEIGHT = 500
ACTION_DIM = 9
INPUT_SHAPE = (HEIGHT, WIDTH, 3)


LEARN_FREQ = 30  # 训练频率，不需要每一个step都learn，攒一些新增经验后再learn，提高效率
MEMORY_SIZE = 200  # replay memory的大小，越大越占用内存
MEMORY_WARMUP_SIZE = 32  # replay_memory 里需要预存一些经验数据，再从里面sample一个batch的经验让agent去learn
BATCH_SIZE = 32  # 每次给agent learn的数据数量，从replay memory随机里sample一批数据出来
LEARNING_RATE = 0.001  # 学习率
GAMMA = 0.99  # reward 的衰减因子，一般取 0.9 到 0.999 不等

action_name = ["Attack", "Attack_Down", "Attack_Up",
           "Short_Jump", "Mid_Jump", "Skill", "Skill_Up", 
           "Skill_Down", "Rush", "Cure"]

move_name = ["Nothing", "Move_Left", "Move_Right"]

USER = False
DELEY_REWARD = 2
ACTION_SEQ = 3



def run_episode(algorithm,agent,act_rmp,move_rmp,PASS_COUNT,paused):
    restart()
    
    act_station = cv2.resize(cv2.cvtColor(grab_screen(station_size), cv2.COLOR_RGBA2RGB),(WIDTH,HEIGHT))
    act_hp_station = cv2.cvtColor(cv2.resize(grab_screen(window_size),(HP_WIDTH,HP_HEIGHT)),cv2.COLOR_BGR2GRAY)

    act_boss_hp = boss_hp(act_hp_station, 570)
    act_boss_last_hp = act_boss_hp
    act_self_hp = player_hp(act_hp_station)
    min_hp = 9


    move_station = cv2.resize(cv2.cvtColor(grab_screen(station_size), cv2.COLOR_RGBA2RGB),(WIDTH,HEIGHT))
    move_hp_station = cv2.cvtColor(cv2.resize(grab_screen(window_size),(HP_WIDTH,HP_HEIGHT)),cv2.COLOR_BGR2GRAY)

    move_boss_hp = boss_hp(move_hp_station, 570)
    move_boss_last_hp = move_boss_hp
    move_self_hp = player_hp(move_hp_station)



    step = 0
    done = 0
    total_reward = 0



    start_time = time.time()
    # Deley Reward
    DeleyReward = collections.deque(maxlen=DELEY_REWARD)
    DeleyStation = collections.deque(maxlen=DELEY_REWARD)
    DeleyActions = collections.deque(maxlen=DELEY_REWARD)

    # move direction of player 0 for stay, 1 for left, 2 for right
    direction = 0
    while True:
        
        # player hp bar is not in normal state and the left pixels are not black
        if(act_hp_station[40][95] != 56 and act_hp_station[300][30] > 20 and act_hp_station[200][30] > 20):
            print("Not in game yet 1")
            continue
        
        # there is not boss hp bar
        if act_hp_station[401][98] != 0 and act_hp_station[401][98] == 0:
            print("Not in game yet 2")
            continue

        last_time = time.time()
        # no more than 10 mins
        # if time.time() - start_time > 600:
        #     break

        step += 1

        
        actions = agent.act_sample(act_station)

        # execute action in action seq
        for action in actions:
            d = agent.move_sample(move_station)
            # print("Move:", move_name[d] )

            if d == direction:
                pass
            elif d == 0:
                Tool.Actions.Nothing()
            elif d == 1:
                Tool.Actions.Move_Left()
            elif d == 2:
                Tool.Actions.Move_Right()

            take_action(action)

            # print("Action: ", action_name[action])

            next_move_station = cv2.resize(cv2.cvtColor(grab_screen(station_size), cv2.COLOR_RGBA2RGB),(WIDTH,HEIGHT))
            next_move_hp_station = cv2.cvtColor(cv2.resize(grab_screen(window_size),(HP_WIDTH,HP_HEIGHT)),cv2.COLOR_BGR2GRAY)

            next_move_boss_hp = boss_hp(next_move_hp_station, move_boss_last_hp)
            move_boss_last_hp = move_boss_hp
            next_move_self_hp = player_hp(next_move_hp_station)

            if min_hp == 9 and next_move_self_hp == 1:
                next_move_self_hp = 9

            reward, done, min_hp = Tool.Helper.action_judge(move_boss_hp, next_move_boss_hp,move_self_hp, next_move_self_hp, min_hp)
            # print(reward)

            move_rmp.append((move_station, d, reward, next_move_station,done))



            if done == 1:
                Tool.Actions.Nothing()
                break
            elif done == 2:
                Tool.Actions.Nothing()
                break

            move_station = next_move_station
            move_self_hp = next_move_self_hp
            move_boss_hp = next_move_boss_hp
            direction = d

        if done == 1:
            Tool.Actions.Nothing()
            break
        elif done == 2:
            PASS_COUNT += 1
            Tool.Actions.Nothing()
            break


        next_act_station = cv2.resize(cv2.cvtColor(grab_screen(station_size), cv2.COLOR_RGBA2RGB),(WIDTH,HEIGHT))
        next_act_hp_station = cv2.cvtColor(cv2.resize(grab_screen(window_size),(HP_WIDTH,HP_HEIGHT)),cv2.COLOR_BGR2GRAY)

        next_act_boss_hp = boss_hp(next_act_hp_station, act_boss_last_hp)

        act_boss_last_hp = act_boss_hp

        next_act_self_hp = player_hp(next_act_hp_station)

        if min_hp == 9 and next_move_self_hp == 1:
            next_move_self_hp = 9


        reward, done, min_hp = Tool.Helper.action_judge(act_boss_hp, next_act_boss_hp,act_self_hp, next_act_self_hp, min_hp)
        DeleyReward.append(reward)
        DeleyStation.append(act_station)
        DeleyActions.append(actions)
        reward = mean(DeleyReward)
        # print("reward: ",reward,"self_hp: ",next_act_self_hp,"boss_hp: ",next_act_boss_hp)

        if len(DeleyReward) >= DELEY_REWARD:
            act_rmp.append((DeleyStation[0],DeleyActions[0],reward,DeleyStation[1],done))
        
        total_reward += reward
        paused = Tool.Helper.pause_game(paused)

        if done == 1:
            Tool.Actions.Nothing()
            break
        elif done == 2:
            PASS_COUNT += 1
            Tool.Actions.Nothing()
            break

        act_station = next_act_station
        act_self_hp = next_act_self_hp
        act_boss_hp = next_act_boss_hp

    if (len(move_rmp) > MEMORY_WARMUP_SIZE):
        print("move learning")
        batch_station,batch_moveions,batch_reward,batch_next_station,batch_done = move_rmp.sample(BATCH_SIZE)
        algorithm.move_learn(batch_station,batch_moveions,batch_reward,batch_next_station,batch_done)   

    if (len(act_rmp) > MEMORY_WARMUP_SIZE):
        print("act learning")
        batch_station,batch_actions,batch_reward,batch_next_station,batch_done = act_rmp.sample(BATCH_SIZE)
        algorithm.act_learn(batch_station,batch_actions,batch_reward,batch_next_station,batch_done)

    return total_reward, step, PASS_COUNT


if __name__ == '__main__':

    os.environ['CUDA_VISIBLE_DEVICES'] = '/gpu:0'
    PASS_COUNT = 0                                       # pass count

    act_rpm = ReplayMemory(MEMORY_SIZE, file_name='./act_memory', user = USER)         # experience pool
    move_rpm = ReplayMemory(MEMORY_SIZE,file_name='./move_memory', user = USER)         # experience pool
    
    # new model, if exit save file, load it
    model = Model(INPUT_SHAPE, ACTION_DIM, ACTION_SEQ)  
    if os.path.exists('dqn_act_model.h5'):
        print("model exists , load model\n")
        model.load_model()
    algorithm = DQN(model, gamma=GAMMA, learnging_rate=LEARNING_RATE)
    agent = Agent(ACTION_DIM,ACTION_SEQ,algorithm,e_greed=0.5,e_greed_decrement=1e-5)
    
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
            total_reward, total_step = user_run(algorithm,user,act_rpm, PASS_COUNT, paused)            
            model.save_mode()
        else:
            total_reward, total_step, PASS_COUNT = run_episode(algorithm,agent,act_rpm,move_rpm, PASS_COUNT, paused)
            if episode % 10 == 1:
                model.save_mode()
        print("Episode: ", episode, ", mean(reward):", total_reward/total_step,", pass_count: " , PASS_COUNT)

