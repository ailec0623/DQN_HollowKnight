# Define the actions we may need during training
# You can define your actions here

from Tool.SendKey import PressKey, ReleaseKey
import time

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
    pass

# Move
# 1
def Move_Left():
    PressKey(LEFT_ARROW)
    time.sleep(0.1)
    ReleaseKey(LEFT_ARROW)
# 2
def Move_Right():
    PressKey(RIGHT_ARROW)
    time.sleep(0.1)
    ReleaseKey(RIGHT_ARROW)

# Attack
# 3
def Attack_Left():
    PressKey(LEFT_ARROW)
    PressKey(X)
    time.sleep(0.05)
    ReleaseKey(LEFT_ARROW)
    ReleaseKey(X)
# 4
def Attack_Right():
    PressKey(RIGHT_ARROW)
    PressKey(X)
    time.sleep(0.05)
    ReleaseKey(RIGHT_ARROW)
    ReleaseKey(X)
# 5
def Attack_Up():
    PressKey(UP_ARROW)
    PressKey(X)
    time.sleep(0.05)
    ReleaseKey(UP_ARROW)
    ReleaseKey(X)

#JUMP, actions below can ignore in a simple model for a easy BOSS
# 6
def Short_Jump():
    PressKey(C)
    time.sleep(0.1)
    ReleaseKey(C)
# 7
def Mid_Jump():
    PressKey(C)
    time.sleep(0.5)
    ReleaseKey(C)
# 8
def Long_Jump():
    PressKey(C)
    time.sleep(0.5)
    ReleaseKey(C)
    PressKey(C)
    time.sleep(0.5)
    ReleaseKey(C)

# Rush
# 9
def Rush_Left():
    PressKey(LEFT_ARROW)
    PressKey(L_SHIFT)
    time.sleep(0.05)
    ReleaseKey(LEFT_ARROW)
    ReleaseKey(L_SHIFT)
# 10
def Rush_Right():
    PressKey(RIGHT_ARROW)
    PressKey(L_SHIFT)
    time.sleep(0.05)
    ReleaseKey(RIGHT_ARROW)
    ReleaseKey(L_SHIFT)

# Skill
# 11
def Skill_Left():
    PressKey(LEFT_ARROW)
    PressKey(Z)
    time.sleep(0.05)
    ReleaseKey(LEFT_ARROW)
    ReleaseKey(Z)
# 12
def Skill_Right():
    PressKey(RIGHT_ARROW)
    PressKey(Z)
    time.sleep(0.05)
    ReleaseKey(RIGHT_ARROW)
    ReleaseKey(Z)
# 13
def Skill_Up():
    PressKey(UP_ARROW)
    PressKey(Z)
    time.sleep(0.05)
    ReleaseKey(UP_ARROW)
    ReleaseKey(Z)
# 14
def Skill_Down():
    PressKey(DOWN_ARROW)
    PressKey(Z)
    time.sleep(0.05)
    ReleaseKey(DOWN_ARROW)
    ReleaseKey(Z)

# Cure
#15
def Cure():
    PressKey(A)
    time.sleep(1)
    ReleaseKey(A)





# Restart function
# it restart a new game
# it is not in actions space
def Look_up():
    PressKey(UP_ARROW)
    time.sleep(0.05)
    ReleaseKey(UP_ARROW)

def restart():
    time.sleep(5)
    Look_up()
    time.sleep(5)
    Look_up()
    time.sleep(1)
    Short_Jump()


# List for action functions
Actions = [Nothing, Move_Left, Move_Right, Attack_Left, Attack_Right, Attack_Up,
           Short_Jump, Mid_Jump, Long_Jump, Rush_Left, Rush_Right,
           Skill_Down, Skill_Left, Skill_Right, Skill_Up, Cure]

# Run the action
def take_action(action):
    Actions[action]()