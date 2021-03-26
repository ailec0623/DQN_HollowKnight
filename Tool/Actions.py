# Define the actions we may need during training
# You can define your actions here

from Tool.SendKey import PressKey, ReleaseKey
from Tool.WindowsAPI import grab_screen
import time
import cv2
# Hash code for key we may use: https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes?redirectedfrom=MSDN
UP_ARROW = 0x26
DOWN_ARROW = 0x28
LEFT_ARROW = 0x25
RIGHT_ARROW = 0x27

L_SHIFT = 0xA0
A = 0x41
C = 0x43
X = 0x58
Z = 0x5A

# 0
def Nothing():
    # print("Do nothing--->")
    time.sleep(0.1)
    pass

# Move
# 1
def Move_Left():
    # print("Move left--->")
    PressKey(LEFT_ARROW)
    time.sleep(0.2)
    ReleaseKey(LEFT_ARROW)
    time.sleep(0.05)
# 2
def Move_Right():
    # print("Move right--->")
    PressKey(RIGHT_ARROW)
    time.sleep(0.2)
    ReleaseKey(RIGHT_ARROW)
    time.sleep(0.05)

# Attack
# 3
def Attack_Left():
    # print("Attack left--->")
    PressKey(LEFT_ARROW)
    time.sleep(0.08)
    ReleaseKey(LEFT_ARROW)

    PressKey(X)
    ReleaseKey(X)
    time.sleep(0.2)
# 4
def Attack_Right():
    # print("Attack right--->")
    PressKey(RIGHT_ARROW)
    time.sleep(0.08)
    ReleaseKey(RIGHT_ARROW)

    PressKey(X)
    ReleaseKey(X)
    time.sleep(0.2)
# 5
def Attack_Up():
    # print("Attack up--->")
    PressKey(UP_ARROW)
    PressKey(X)
    time.sleep(0.07)
    ReleaseKey(X)
    ReleaseKey(UP_ARROW)
    time.sleep(0.2)

#JUMP, actions below can ignore in a simple model for a easy BOSS
# 6
def Short_Jump():
    PressKey(C)
    time.sleep(0.1)
    ReleaseKey(C)
    time.sleep(0.05)
# 7
def Mid_Jump():
    PressKey(C)
    time.sleep(0.5)
    ReleaseKey(C)
    time.sleep(0.05)

# Skill
# 8
def Skill_Left():
    PressKey(LEFT_ARROW)
    time.sleep(0.08)
    PressKey(Z)
    PressKey(X)
    time.sleep(0.2)
    ReleaseKey(LEFT_ARROW)
    ReleaseKey(Z)
    ReleaseKey(X)
    time.sleep(0.1)
# 9
def Skill_Right():
    PressKey(RIGHT_ARROW)
    time.sleep(0.08)
    PressKey(Z)
    PressKey(X)
    time.sleep(0.2)
    ReleaseKey(RIGHT_ARROW)
    ReleaseKey(Z)
    ReleaseKey(X)
    time.sleep(0.1)
# 10
def Skill_Up():
    PressKey(UP_ARROW)
    PressKey(Z)
    PressKey(X)
    time.sleep(0.3)
    ReleaseKey(UP_ARROW)
    ReleaseKey(Z)
    ReleaseKey(X)

    time.sleep(0.1)
    PressKey(X)
    time.sleep(0.1)
    ReleaseKey(X)
    time.sleep(0.1)
# 11
def Skill_Down():
    PressKey(DOWN_ARROW)
    PressKey(Z)
    PressKey(X)
    time.sleep(0.2)
    ReleaseKey(X)
    ReleaseKey(DOWN_ARROW)
    ReleaseKey(Z)
    
    for i in range(3):
        time.sleep(0.1)
        PressKey(X)
        time.sleep(0.15)
        ReleaseKey(X)
    time.sleep(0.1)


# Rush
# 12
def Rush_Left():
    PressKey(LEFT_ARROW)
    PressKey(L_SHIFT)
    time.sleep(0.45)
    ReleaseKey(LEFT_ARROW)
    ReleaseKey(L_SHIFT)
    time.sleep(0.05)
# 13
def Rush_Right():
    PressKey(RIGHT_ARROW)
    PressKey(L_SHIFT)
    time.sleep(0.45)
    ReleaseKey(RIGHT_ARROW)
    ReleaseKey(L_SHIFT)
    time.sleep(0.01)



# Cure
#14
def Cure():
    PressKey(A)
    time.sleep(1.4)
    ReleaseKey(A)
    time.sleep(0.1)


# Restart function
# it restart a new game
# it is not in actions space
def Look_up():
    PressKey(UP_ARROW)
    time.sleep(0.1)
    ReleaseKey(UP_ARROW)

def restart():
    station_size = (230, 230, 1670, 930)
    time.sleep(5)
    Look_up()
    time.sleep(2.5)
    Look_up()
    time.sleep(1)
    while True:
        station = cv2.resize(cv2.cvtColor(grab_screen(station_size), cv2.COLOR_RGBA2RGB),(1000,500))
        if station[187][612][0] > 200: 
            Short_Jump()
            break
        else:
            Look_up()
            time.sleep(0.5)


# List for action functions
Actions = [Nothing, Move_Left, Move_Right, Attack_Left, Attack_Right, Attack_Up,
           Short_Jump, Mid_Jump, Skill_Left, Skill_Right, Skill_Up, 
           Skill_Down, Rush_Left, Rush_Right, Cure]

# Run the action
def take_action(action):
    Actions[action]()