# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 09:45:04 2020

@author: pang
API for get Hp state about BOSS and player
For different game and resolution, you need to modify this file to make sure it works correctly
"""

import numpy as np
from PIL import ImageGrab
import cv2
import time
from Tool.GrabScreen import grab_screen
# from GrabScreen import grab_screen
import os

x = 129
y = 50
step = 22
points = []
for i in range(9):
    points.append((x + i * step, y))

MAX_BOSS_HP = 570
hp_y = 400



def player_hp(gray):
    hp = 0
    #print("---------------------------")
    for point in points:
        x_, y_ = point[0], point[1]
        #print(gray[y][x])
        if(gray[y_][x_] > 190):
            hp+=1
    return hp

def boss_hp(gray, last_hp):
    boss_blood = 0

    #print(gray[hp_y][97],gray[hp_y][200],gray[hp_y][400])
    #print(gray[hp_y][600],gray[hp_y][668],gray[hp_y][671])
    if(gray[hp_y][96] < 44 or gray[hp_y][96] > 46):
        return MAX_BOSS_HP
    for boss_bd_num in gray[hp_y]:
        if boss_bd_num > 25 and boss_bd_num < 31:
            boss_blood += 1
        #print("Count hp: ", boss_blood)

    if boss_blood - last_hp < -300:
        return MAX_BOSS_HP

    elif abs(boss_blood - last_hp) < 3:
        #print(boss_blood, "  ", last_hp)
        return last_hp
    return boss_blood



# window_size = (0,0,1920,1017)
# last_time = time.time()

# # screen_gray = cv2.cvtColor(grab_screen(window_size),cv2.COLOR_BGR2GRAY)#灰度图像收集
# # screen_gray = cv2.resize(screen_gray,(768,407))
# # cv2.line(screen_gray, (97, 405), (671, 405), (255, 0, 0), 1, 4)

# # #self_blood = player_hp(screen_gray)
# # #boss_blood = boss_hp(screen_gray)
# # #print(self_blood)
# # # for point in points:
# # #     cv2.circle(screen_gray, point, 1, (255, 0, 0), 1)

# # cv2.imshow('test.jpg', screen_gray)
# hp = 355
# while(True):
#     screen_gray = cv2.cvtColor(grab_screen(window_size),cv2.COLOR_BGR2GRAY)#灰度图像收集
#     screen_gray = cv2.resize(screen_gray,(768,407))

#     #hp = player_hp(screen_gray)
#     hp = boss_hp(screen_gray, hp)
#     print(hp)
#     # for point in points:
#     #     cv2.circle(screen_gray, point, 1, (255, 0, 0), 1)
#     cv2.line(screen_gray, (97, hp_y), (671, hp_y), (255, 0, 0), 1, 4)

#     cv2.imshow('window1',screen_gray)

#     #测试时间用
#     #print('loop took {} seconds'.format(time.time()-last_time))
#     last_time = time.time()
    
    
#     if cv2.waitKey(5) & 0xFF == ord('q'):
#         break
# cv2.waitKey()# 视频结束后，按任意键退出
# cv2.destroyAllWindows()



