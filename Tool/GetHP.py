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
    # print(gray[hp_y][100],gray[hp_y][200],gray[hp_y][300])
    if(gray[hp_y][96] < 44 or gray[hp_y][96] > 46):
        # print("case 1")
        return MAX_BOSS_HP
    for i in range(97, 666):
        if gray[hp_y][i] > 25 and gray[hp_y][i] < 31:
            boss_blood += 1
        else:
            break
        #print("Count hp: ", boss_blood)

    if boss_blood - last_hp < -300:
        # print("case 2")
        return last_hp

    elif abs(boss_blood - last_hp) < 3:
        #print(boss_blood, "  ", last_hp)
        return last_hp
    return boss_blood



