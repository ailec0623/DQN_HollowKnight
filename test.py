

import cv2
import time
from Tool.GrabScreen import grab_screen
from Tool.GetHP import boss_hp, player_hp
from Tool.UserInput import User
import os




count = 0
for x in os.listdir('./user_data/'):
    count += 1
print(count)
# # User input test
# action_name = ["Nothing", "Move_Left", "Move_Right", "Attack_Left", "Attack_Right", "Attack_Up",
#            "Short_Jump", "Mid_Jump", "Long_Jump", "Skill_Left", "Skill_Right", 
#            "Skill_Up", "Skill_Down", "Rush_Left", "Rush_Right", "Cure"]
# while True:
#     user = User()
#     print(action_name[user.get_user_action()])




# Windows and Hp test

# window_size = (0,0,1920,1017)
# station_size = (230, 230, 1670, 930)
# WIDTH = 768
# HEIGHT = 407

# hp_station = cv2.cvtColor(cv2.resize(grab_screen(window_size),(WIDTH,HEIGHT)),cv2.COLOR_BGR2GRAY)
# boss_blood = boss_hp(hp_station, 570)
# last_hp = boss_blood
# while True:
#     hp_station = cv2.cvtColor(cv2.resize(grab_screen(window_size),(WIDTH,HEIGHT)),cv2.COLOR_BGR2GRAY)
#     next_boss_blood = boss_hp(hp_station, last_hp)
#     print(boss_blood)
#     last_hp = boss_blood
#     boss_blood = next_boss_blood
#     #screen = cv2.resize(screen,(WIDTH,HEIGHT))
#     #cv2.rectangle(screen, (230, 230), (1670, 930), (255, 0, 0), 4, 4)


    
#     if cv2.waitKey(5) & 0xFF == ord('q'):
#         break
# cv2.waitKey()# 视频结束后，按任意键退出
# cv2.destroyAllWindows()