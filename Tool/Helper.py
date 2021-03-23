from Tool.GetKeys import key_check
import time

def action_judge(action, boss_blood, next_boss_blood, self_blood, next_self_blood, min_hp, emergence_break):
    # get action reward
    # emergence_break is used to break down training
    if next_self_blood - self_blood > 5:     # Player dead
        if emergence_break < 2:
            reward = -45
            done = 1
            min_hp = 9
            emergence_break += 1
            print("Player dead. Case 1")
            return reward, done, min_hp, emergence_break
        else:
            reward = -45
            done = 1
            min_hp = 9
            emergence_break = 100
            print("Player dead. Case 2")
            return reward, done, min_hp, emergence_break
    
    elif next_boss_blood - boss_blood > 200:   #boss dead
        if emergence_break < 2:
            reward = 0
            done = 1
            min_hp = 9
            emergence_break += 1
            print("Boss dead. Case 1", " ", next_boss_blood, " ", boss_blood)
            return reward, done, min_hp, emergence_break
        else:
            reward = 0
            done = 1
            min_hp = 9
            emergence_break = 100
            print("Boss dead. Case 2")
            return reward, done, min_hp, emergence_break

    else:
        self_blood_reward = 0
        boss_blood_reward = 0

        # Move reward
        if(action < 3):
            if next_self_blood - min_hp < 0 and next_self_blood != 0:
                self_blood_reward = -45
                min_hp = next_self_blood
            self_blood_reward += 1


        # Attack reward
        # Only get reward after attact
        elif(action > 2 and action < 6):
            if next_self_blood - min_hp < 0 and next_self_blood != 0:
                self_blood_reward = -45
                min_hp = next_self_blood
            if abs(next_boss_blood - boss_blood) > 3:
                boss_blood_reward = 30
            # It is good for model to try more movement
            # boss_blood_reward -= 1

        #Jump reward
        elif(action > 6 and action < 9):
              if next_self_blood - min_hp < 0 and next_self_blood != 0:
                self_blood_reward = -45
                min_hp = next_self_blood

        # Skill reward
        elif(action > 8 and action < 13):
            if next_self_blood - min_hp < 0 and next_self_blood != 0:
                self_blood_reward = -45
                min_hp = next_self_blood
            if abs(next_boss_blood - boss_blood) > 3:
                boss_blood_reward = 40
            else:
                boss_blood_reward -= 10


        reward = self_blood_reward + boss_blood_reward
        done = 0
        emergence_break = 0
        return reward, done, min_hp, emergence_break

# Paused training
def pause_game(paused):
    keys = key_check()
    if 'T' in keys:
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
            keys = key_check()
            # pauses game and can get annoying.
            if 'T' in keys:
                if paused:
                    paused = False
                    print('start game')
                    time.sleep(1)
                    break
                else:
                    paused = True
                    time.sleep(1)
    return paused