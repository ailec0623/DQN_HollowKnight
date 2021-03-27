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

# move actions
# 0
def Nothing():
    ReleaseKey(LEFT_ARROW)
    ReleaseKey(RIGHT_ARROW)
    time.sleep(0.1)
    pass

# Move
# 1
def Move_Left():
    ReleaseKey(RIGHT_ARROW)
    time.sleep(0.03)
    PressKey(LEFT_ARROW)
    time.sleep(0.05)
# 2
def Move_Right():
    ReleaseKey(LEFT_ARROW)
    time.sleep(0.03)
    PressKey(RIGHT_ARROW)
    time.sleep(0.05)

# ----------------------------------------------------------------------

# other actions
# Attack
# 0
def Attack():
    PressKey(X)
    time.sleep(0.08)
    ReleaseKey(X)
    time.sleep(0.2)
# 1
def Attack_Down():
    PressKey(DOWN_ARROW)
    PressKey(X)
    time.sleep(0.07)
    ReleaseKey(X)
    ReleaseKey(DOWN_ARROW)
    time.sleep(0.2)
# 2
def Attack_Up():
    # print("Attack up--->")
    PressKey(UP_ARROW)
    PressKey(X)
    time.sleep(0.07)
    ReleaseKey(X)
    ReleaseKey(UP_ARROW)
    time.sleep(0.2)

#JUMP
# 3
def Short_Jump():
    PressKey(C)
    time.sleep(0.1)
    ReleaseKey(C)
    time.sleep(0.05)
# 4
def Mid_Jump():
    PressKey(C)
    time.sleep(0.5)
    ReleaseKey(C)
    time.sleep(0.05)

# Skill
# 5
def Skill():
    PressKey(Z)
    PressKey(X)
    time.sleep(0.2)
    ReleaseKey(Z)
    ReleaseKey(X)
    time.sleep(0.1)
# 6
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
# 7
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
# 8
def Rush():
    PressKey(L_SHIFT)
    time.sleep(0.45)
    ReleaseKey(L_SHIFT)
    time.sleep(0.05)



# Cure
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
    while True:
        station = cv2.resize(cv2.cvtColor(grab_screen(station_size), cv2.COLOR_RGBA2RGB),(1000,500))
        if station[187][300][0] != 0: 
            time.sleep(1)
        else:
            break
    time.sleep(1)
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
Actions = [Attack, Attack_Down, Attack_Up,
           Short_Jump, Mid_Jump, Skill, Skill_Up, 
           Skill_Down, Rush, Cure]

# Run the action
def take_action(action):
    Actions[action]()