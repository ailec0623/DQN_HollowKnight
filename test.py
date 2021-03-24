

import cv2
import time
from Tool.GrabScreen import grab_screen


window_size = (0,0,1920,1017)
station_size = (230, 230, 1670, 930)
WIDTH = 768
HEIGHT = 407
while True:
    screen = grab_screen(station_size)
    screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2BGR)
    #screen = cv2.resize(screen,(WIDTH,HEIGHT))
    #cv2.rectangle(screen, (230, 230), (1670, 930), (255, 0, 0), 4, 4)
    cv2.imshow('window1',screen)

    
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
cv2.waitKey()# 视频结束后，按任意键退出
cv2.destroyAllWindows()