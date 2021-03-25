

import cv2
import time
from Tool.GrabScreen import grab_screen
from Tool.GetHP import boss_hp, player_hp
from Tool.UserInput import User
from Tool.WindowsAPI import Contraler
import os


c = Contraler()

while True:
    c.PressKey(0x43)

# window_size = (0,0,1920,1017)
# station_size = (230, 230, 1670, 930)
# WIDTH = 768
# HEIGHT = 407

# # hp_station = cv2.cvtColor(cv2.resize(grab_screen(window_size),(WIDTH,HEIGHT)),cv2.COLOR_BGR2GRAY)
# # boss_blood = boss_hp(hp_station, 570)
# # last_hp = boss_blood
# while True:
#     # hp_station = cv2.cvtColor(cv2.resize(grab_screen(window_size),(WIDTH,HEIGHT)),cv2.COLOR_BGR2GRAY)
#     # next_boss_blood = boss_hp(hp_station, last_hp)
#     # print(boss_blood)
#     # last_hp = boss_blood
#     # boss_blood = next_boss_blood
#     screen = grab_screen(station_size)

#     cv2.imshow( "ss", screen)



#     if cv2.waitKey(5) & 0xFF == ord('q'):
#         break
# cv2.waitKey()# 视频结束后，按任意键退出
# cv2.destroyAllWindows()