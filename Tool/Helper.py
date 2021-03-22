from Tool.GetKeys import key_check
import time

def action_judge(boss_blood, next_boss_blood, self_blood, next_self_blood, emergence_break):
    # get action reward
    # emergence_break is used to break down training
    if next_self_blood < 3:     # Player dead
        if emergence_break < 2:
            reward = -1000
            done = 1
            emergence_break += 1
            return reward, done, emergence_break
        else:
            reward = -1000
            done = 1
            emergence_break = 100
            return reward, done, emergence_break
    
    elif next_boss_blood - boss_blood > 100:   #boss dead
        if emergence_break < 2:
            reward = 0
            done = 1
            emergence_break += 1
            return reward, done, emergence_break
        else:
            reward = 0
            done = 1
            emergence_break = 100
            return reward, done, emergence_break

    else:
        self_blood_reward = 0
        boss_blood_reward = 0
        # Self hp reward judge
        if next_self_blood - self_blood < 0:
            self_blood_reward = -50

        # Boss hp reward judge
        if next_boss_blood - boss_blood <= -5:
            boss_blood_reward = boss_blood - next_boss_blood

        reward = self_blood_reward + boss_blood_reward - 1
        done = 0
        emergence_break = 0
        return reward, done, emergence_break

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