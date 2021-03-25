import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api



class Contraler:
  def __init__(self):
    self.hwnd = win32gui.FindWindow(None,'Hollow Knight')

  def grab_screen(self, region=None):
  
    # print(hwin)
    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(self.hwnd)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return img
  

  def PressKey(self, hexKeyCode):
    win32gui.PostMessage(self.hwnd, win32con.WM_KEYDOWN, hexKeyCode, 0)


  def ReleaseKey(self, hexKeyCode):
    win32gui.PostMessage(self.hwnd, win32con.WM_KEYUP, hexKeyCode, 0)