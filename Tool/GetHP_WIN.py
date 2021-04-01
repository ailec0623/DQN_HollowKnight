import win32gui
import win32api
import win32process
import ctypes

class Hp_getter():
    def __init__(self):
        hd = win32gui.FindWindow(None, "Hollow Knight")
        pid = win32process.GetWindowThreadId(self.hd)[1]
        self.process_handle = win32api.OpenProcess(0x1F0FFF, False, pid)

        self.kernal32 = ctypes.windll.LoadLibrary(r"C:\Windows\System32\kernel32.dll")


    def get_self_hp(self):
        hp = ctypes.c_int()
        self.kernal32.ReadProcessMemory(int(self.process_handle), 0x0000000, ctypes.byref(hp), 4, None)
        return hp.value