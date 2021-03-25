# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:03:44 2020

@author: pang
"""

import win32api as wapi
import time



def key_check():
    operations = []
    if wapi.GetAsyncKeyState(0x41):
        operations.append("A")
    if wapi.GetAsyncKeyState(0x43):
        operations.append("C")
    if wapi.GetAsyncKeyState(0x58):
        operations.append("X")
    if wapi.GetAsyncKeyState(0x5A):
        operations.append("Z")
    if wapi.GetAsyncKeyState(0x54):
        operations.append("T")

    direction = []
    if wapi.GetAsyncKeyState(0x25):
        direction.append("Left")
    if wapi.GetAsyncKeyState(0x26):
        direction.append("Up")
    if wapi.GetAsyncKeyState(0x27):
        direction.append("Right")
    if wapi.GetAsyncKeyState(0x28):
        direction.append("Down")

    return operations, direction
