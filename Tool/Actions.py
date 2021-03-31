# Define the actions we may need during training
# You can define your actions here

from Tool.SendKey import PressKey, ReleaseKey
from Tool.WindowsAPI import grab_screen
import time
import cv2
import threading

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
    time.sleep(0.01)
    pass

# Move
# 0
def Move_Left():
    ReleaseKey(RIGHT_ARROW)
    PressKey(LEFT_ARROW)
    time.sleep(0.01)
# 1
def Move_Right():
    ReleaseKey(LEFT_ARROW)
    PressKey(RIGHT_ARROW)
    time.sleep(0.01)

# 2
def Turn_Left():
    ReleaseKey(RIGHT_ARROW)
    PressKey(LEFT_ARROW)
    time.sleep(0.01)
    ReleaseKey(LEFT_ARROW)

# 3
def Turn_Right():
    ReleaseKey(LEFT_ARROW)
    PressKey(RIGHT_ARROW)
    time.sleep(0.01)
    ReleaseKey(RIGHT_ARROW)

# ----------------------------------------------------------------------

# other actions
# Attack
# 0
def Attack():
    PressKey(X)
    time.sleep(0.05)
    ReleaseKey(X)
    time.sleep(0.01)
# 1
def Attack_Down():
    PressKey(DOWN_ARROW)
    PressKey(X)
    time.sleep(0.05)
    ReleaseKey(X)
    ReleaseKey(DOWN_ARROW)
    time.sleep(0.01)
# 2
def Attack_Up():
    # print("Attack up--->")
    PressKey(UP_ARROW)
    PressKey(X)
    time.sleep(0.05)
    ReleaseKey(X)
    ReleaseKey(UP_ARROW)
    time.sleep(0.01)

#JUMP
# 3
def Short_Jump():
    PressKey(C)
    PressKey(DOWN_ARROW)
    PressKey(X)
    time.sleep(0.2)
    ReleaseKey(X)
    ReleaseKey(DOWN_ARROW)
    ReleaseKey(C)

# 4
def Mid_Jump():
    PressKey(C)
    time.sleep(0.2)
    PressKey(X)
    time.sleep(0.2)
    ReleaseKey(X)
    ReleaseKey(C)


# Skill
# 5
def Skill():
    PressKey(Z)
    PressKey(X)
    time.sleep(0.1)
    ReleaseKey(Z)
    ReleaseKey(X)
    time.sleep(0.01)
# 6
def Skill_Up():
    PressKey(UP_ARROW)
    PressKey(Z)
    PressKey(X)
    time.sleep(0.15)
    ReleaseKey(UP_ARROW)
    ReleaseKey(Z)
    ReleaseKey(X)

    time.sleep(0.1)
    PressKey(X)
    time.sleep(0.01)
    ReleaseKey(X)
    time.sleep(0.01)
# 7
def Skill_Down():
    PressKey(DOWN_ARROW)
    PressKey(Z)
    PressKey(X)
    time.sleep(0.2)
    ReleaseKey(X)
    ReleaseKey(DOWN_ARROW)
    ReleaseKey(Z)
    
    for i in range(2):
        time.sleep(0.1)
        PressKey(X)
        time.sleep(0.15)
        ReleaseKey(X)
    time.sleep(0.01)


# Rush
# 8
def Rush():
    PressKey(L_SHIFT)
    time.sleep(0.25)
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
    time.sleep(1.5)
    Look_up()
    time.sleep(1)
    while True:
        station = cv2.resize(cv2.cvtColor(grab_screen(station_size), cv2.COLOR_RGBA2RGB),(1000,500))
        if station[187][612][0] > 200: 
            PressKey(C)
            time.sleep(0.1)
            ReleaseKey(C)
            break
        else:
            Look_up()
            time.sleep(0.2)


# List for action functions
Actions = [Attack, Attack_Down, Attack_Up,
           Short_Jump, Mid_Jump, Skill, Skill_Up, 
           Skill_Down, Rush, Cure]
Directions = [Move_Left, Move_Right, Turn_Left, Turn_Right]
# Run the action
def take_action(action):
    Actions[action]()

def take_direction(direc):
    Directions[direc]()



class TackAction(threading.Thread):
    def __init__(self, threadID, name, direction, action):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.direction = direction
        self.action = action
        
    def run(self):
        take_direction(self.direction)
        take_action(self.action)