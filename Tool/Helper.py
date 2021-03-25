from Tool.WindowsAPI import key_check
import time

def mean(d):
    t = 0
    for i in d:
        t += i
    return t / len(d)

def count_self_reward(next_self_blood, min_hp):
    if next_self_blood - min_hp < 0 and next_self_blood != 0:
        self_blood_reward = 35 * (next_self_blood - min_hp)
        min_hp = next_self_blood
        return self_blood_reward, min_hp
    return 0, min_hp

def count_boss_reward(next_boss_blood, boss_blood):
    if abs(next_boss_blood - boss_blood) > 3:
        # boss_blood_reward = 30
        return boss_blood - next_boss_blood
    return 0

def action_judge(boss_blood, next_boss_blood, self_blood, next_self_blood, min_hp):
    # get action reward
    # Player dead
    if next_self_blood - self_blood > 5:     
        reward = -35
        done = 1
        min_hp = 9
        print("Player dead.")
        return reward, done, min_hp
    #boss dead
    elif next_boss_blood - boss_blood > 200:   
        reward = 30
        done = 2
        min_hp = 9
        print("Boss dead. Case 1", " ", next_boss_blood, " ", boss_blood)
        return reward, done, min_hp

    # playing
    else:
        self_blood_reward, min_hp = count_self_reward(next_self_blood, min_hp)
        boss_blood_reward = count_boss_reward(next_boss_blood, boss_blood)
        
        # # Do nothing
        # if(action == 0):
        #     pass
        #     # self_blood_reward += 1
        # # Move reward
        # elif(action == 1):
        #     pass
        #     # self_blood_reward += 1

        # elif(action == 2):
        #     pass
        #     # self_blood_reward += 1

        # # Attack reward
        # # Only get reward after attact
        # elif(action == 3):
        #     # It is good for model to try more movement
        #     boss_blood_reward -= 0

        # elif(action == 4):
        #     # It is good for model to try more movement
        #     boss_blood_reward -= 0

        # elif(action == 5):
        #     # It is good for model to try more movement
        #     boss_blood_reward -= 2

        # #Jump reward
        # elif(action == 6):
        #     pass
        #     # self_blood_reward += 1  
        # elif(action == 7):
        #     pass
        #     # self_blood_reward += 1  
        # elif(action == 8):
        #     pass
        #     # self_blood_reward += 1  


        # # Skill reward
        # elif(action == 9):
        #     if boss_blood_reward != 0:
        #         boss_blood_reward += 20
        #     # else:
        #     #     boss_blood_reward -= 10

        # elif(action == 10):
        #     if boss_blood_reward != 0:
        #         boss_blood_reward += 20
        #     # else:
        #     #     boss_blood_reward -= 10

        # elif(action == 11):
        #     if boss_blood_reward != 0:
        #         boss_blood_reward += 20

        # elif(action == 12):
        #     if boss_blood_reward != 0:
        #         boss_blood_reward += 20
        #     # else:
        #     #     boss_blood_reward -= 5

        # # rush reward
        # elif(action == 13):
        #     pass
        #     # self_blood_reward += 1
        # elif(action == 14):
        #     pass
        #     # self_blood_reward += 1

        reward = self_blood_reward + boss_blood_reward

        done = 0
        emergence_break = 0
        return reward, done, min_hp

# Paused training
def pause_game(paused):
    op, d = key_check()
    if 'T' in op:
        if paused:
            paused = False
            print('start game')
            time.sleep(1)
        else:
            paused = True
            print('pause game')
            time.sleep(1)
    if paused:
        print('paused')
        while True:
            op, d = key_check()
            # pauses game and can get annoying.
            if 'T' in op:
                if paused:
                    paused = False
                    print('start game')
                    time.sleep(1)
                    break
                else:
                    paused = True
                    time.sleep(1)
    return paused