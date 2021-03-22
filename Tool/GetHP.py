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
import os

# def self_blood_count(self_gray):
#     self_blood = 0
#     for self_bd_num in self_gray[469]:
#         if self_bd_num > 90 and self_bd_num < 98:
#             self_blood += 1
#     return self_blood
def player_hp(gray):
    return 10

def boss_hp(gray):
    boss_blood = 0
    #print(boss_gray[405][96], boss_gray[405][200],boss_gray[405][400])
    if(gray[405][96] != 43):
        return 574
    for boss_bd_num in gray[405]:
        if boss_bd_num > 27 and boss_bd_num < 30:
            boss_blood += 1
    return boss_blood



# window_size = (0,0,3840,2035)  
# last_time = time.time()
# while(True):
#     screen_gray = cv2.cvtColor(grab_screen(window_size),cv2.COLOR_BGR2GRAY)#灰度图像收集
#     screen_gray = cv2.resize(screen_gray,(768,407))
#     #cv2.line(screen_gray, (97, 405), (671, 405), (255, 0, 0), 1, 4)

#     #self_blood = self_blood_count(screen_gray)
#     boss_blood = boss_hp(screen_gray)
    
#     cv2.imshow('window1',screen_gray)

#     #测试时间用
#     print('loop took {} seconds'.format(time.time()-last_time))
#     last_time = time.time()
    
    
#     if cv2.waitKey(5) & 0xFF == ord('q'):
#         break
# cv2.waitKey()# 视频结束后，按任意键退出
# cv2.destroyAllWindows()
