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
from Tool.WindowsAPI import grab_screen
import os

x = 130
y = 50
step = 22
points = []
for i in range(9):
    points.append((x + i * step, y))

MAX_BOSS_HP = 570
hp_y = 400



def player_hp(gray):
    hp = 0
    # print("---------------------------")
    
    if(gray[40][95] != 56 and gray[300][30] > 20 and gray[200][30] > 20):
        # print(gray[40][95], ", ", gray[300][30], ", ", gray[200][30])
        return 9
    for idx, point in enumerate(points):
        x_, y_ = point[0], point[1]
        pixel = gray[y_][x_] +  gray[y_+1][x_] +gray[y_-1][x_] +gray[y_][x_+1] +gray[y_][x_-1]

        if idx == 0:
            if pixel == 150:
                # print(idx, "case 1", pixel)
                pass
            elif((pixel > 58 and pixel < 100 )  or (pixel >= 196 and pixel <= 241) or (pixel >= 145 and pixel <= 180)):
                # print(idx, "case 2", pixel)
                hp = idx + 1
            else: 
                pass
                # print(idx, "case 3", pixel)
        else:
            # print(pixel )
            if pixel == 150:
                # print(idx, "case 1", pixel)
                pass
            elif((pixel > 60 and pixel < 100 ) or (pixel >= 196 and pixel <= 241) or (pixel >= 144 and pixel <= 180)):
                # print(idx, "case 2", pixel)
                hp = idx + 1
            else: 
                # print(idx, "case 3", pixel)
                pass
                # print(pixel, i)

    # print(hp)
    if hp == 0:
        return 1
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



