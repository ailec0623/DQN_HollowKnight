

import cv2
import time
from Tool.GetHP import Hp_getter
from Tool.UserInput import User
from Tool.WindowsAPI import grab_screen
from Tool.Actions import take_action, restart, take_direction
from Tool.Helper import pause_game, direction_reward, distance_reward
import os
import Tool.WindowsAPI
import Tool.SendKey


print("WinAPI:")
start_time = time.time()
Tool.WindowsAPI.PressKey(0x26)
print("send key time: ", time.time() - start_time)

start_time = time.time()
Tool.WindowsAPI.ReleaseKey(0x26)
print("release key time: ", time.time() - start_time)


print("User32:")
start_time = time.time()
Tool.SendKey.PressKey(0x26)
print("send key time: ", time.time() - start_time)

start_time = time.time()
Tool.SendKey.ReleaseKey(0x26)
print("release key time: ", time.time() - start_time)






# from Model import Model




# ACTION_DIM = 9
# INPUT_SHAPE = (200, 400, 3)

# model = Model(INPUT_SHAPE, ACTION_DIM)

# print(model.act_model.get_layer(index=0).summary())
# print(len(model.act_model.get_layer(index=4).get_layer(index=0).get_layer(index=1).get_weights()))
# print(len(model.act_model.get_layer(index=4).get_layer(index=1).get_layer(index=0).get_weights()))
# print(len(model.act_model.get_layer(index=4).get_layer(index=1).get_layer(index=1).get_weights()))

# print(len(model.act_model.get_layer(index=5).get_layer(index=0).get_layer(index=0).get_weights()))
# print(len(model.act_model.get_layer(index=5).get_layer(index=0).get_layer(index=1).get_weights()))
# print(len(model.act_model.get_layer(index=5).get_layer(index=1).get_layer(index=0).get_weights()))
# print(len(model.act_model.get_layer(index=5).get_layer(index=1).get_layer(index=1).get_weights()))

# print(len(model.act_model.get_layer(index=6).get_layer(index=0).get_layer(index=0).get_weights()))
# print(len(model.act_model.get_layer(index=6).get_layer(index=0).get_layer(index=1).get_weights()))
# print(len(model.act_model.get_layer(index=6).get_layer(index=1).get_layer(index=0).get_weights()))
# print(len(model.act_model.get_layer(index=6).get_layer(index=1).get_layer(index=1).get_weights()))

# print(len(model.act_model.get_layer(index=7).get_layer(index=0).get_layer(index=0).get_weights()))
# print(len(model.act_model.get_layer(index=7).get_layer(index=0).get_layer(index=1).get_weights()))
# print(len(model.act_model.get_layer(index=7).get_layer(index=1).get_layer(index=0).get_weights()))
# print(len(model.act_model.get_layer(index=7).get_layer(index=1).get_layer(index=1).get_weights()))

# print(len(model.act_model.get_layer(index=8).get_layer(index=0).get_layer(index=0).get_weights()))
# print(len(model.act_model.get_layer(index=8).get_layer(index=0).get_layer(index=1).get_weights()))
# print(len(model.act_model.get_layer(index=8).get_layer(index=1).get_layer(index=0).get_weights()))
# print(len(model.act_model.get_layer(index=8).get_layer(index=1).get_layer(index=1).get_weights()))



# action = 11
# directions = [0,1,0,1,3]
# actions = [4,4,4,4,4]
# # actions = [action, action, action, action, action]
# while True:
#     paused = True
#     paused = pause_game(paused)
#     for i in range(5):
#         print(1)
#         take_direction(directions[i])
#         take_action(actions[i])
        

# for x in os.listdir("./act_memory"):
#     print(1)




# window_size = (0,0,1920,1017)
# station_size = (230, 230, 1670, 930)
# WIDTH = 400
# HEIGHT = 200

# hp_station = cv2.cvtColor(cv2.resize(grab_screen(station_size),(WIDTH,HEIGHT)),cv2.COLOR_BGR2GRAY)
# # boss_blood = boss_hp(hp_station, 570)
# # last_hp = boss_blood
# # next_self_blood  = player_hp(hp_station)

# min_hp = 9

# check_point = (612, 187)
# # start_time = time.time()

# h = Hp_getter()
# last_hy = 0
# while True:
#     # take_action(6)
#     px, py = h.get_play_location()
#     hx, hy = h.get_hornet_location()
#     if last_hy > 32 and last_hy < 32.5 and hy > 32 and last_hy < 32.5:
#         print("skill")
#     last_hy = hy
#     time.sleep(0.25)
    # print(direction_reward(0, px, hx), "   ",distance_reward(0, px, hx), " ", px - hx)
    # print(h.get_play_location(), "   ",h.get_hornet_location())
    # hp_station = cv2.cvtColor(cv2.resize(grab_screen(station_size),(WIDTH,HEIGHT)),cv2.COLOR_RGBA2RGB)
    # fn = "./test_img/" + str(i) + ".png"
    # cv2.imwrite(fn, hp_station)
    # time.sleep(0.02)
    # print(time.time() - start_time)
    # print(hp_station[401][97], " ", hp_station[401][98]," ", hp_station[401][99])
    # station = cv2.resize(cv2.cvtColor(grab_screen(station_size), cv2.COLOR_RGBA2RGB),(WIDTH,HEIGHT))
    # print(hp_station[187][300])
    # next_boss_blood = boss_hp(hp_station, last_hp)
    # print(next_boss_blood)
    # print(boss_blood)
    # last_hp = boss_blood
    # boss_blood = next_boss_blood
    # print(hp_station[95][40])
    # if(hp_station[40][95] != 56 and hp_station[300][30] > 20 and hp_station[200][30] > 20):
    #     # print("Not in game yet")
    #     continue
    # next_self_blood = player_hp(hp_station)
    # if next_self_blood - min_hp < 0 and next_self_blood - min_hp > -3:
    #     print(next_self_blood)
    #     min_hp = next_self_blood
    # if next_self_blood ==9 and min_hp != 9:
    #     print("----------------------------------------")
    #     min_hp = 9
#     cv2.circle(hp_station, (300, 187), 5, (255, 0, 0), 4, 1)
#     # cv2.line(hp_station,(96, 400), (666, 400), (255, 255, 255), 4, 1)
#     # print(station[187][612])
#     cv2.imshow( "ss", hp_station)



#     if cv2.waitKey(5) & 0xFF == ord('q'):
#         break
# cv2.waitKey()# 视频结束后，按任意键退出
# cv2.destroyAllWindows()




'''
170
195
217
242
4
21
37
49
62

'''