import win32gui
import win32api
import win32process
import ctypes


class Hp_getter():
    def __init__(self):
        hd = win32gui.FindWindow(None, "Hollow Knight")
        pid = win32process.GetWindowThreadProcessId(hd)[1]
        self.process_handle = win32api.OpenProcess(0x1F0FFF, False, pid)
        self.kernal32 = ctypes.windll.LoadLibrary(r"C:\\Windows\\System32\\kernel32.dll")


    def get_self_hp(self):
        base_address = 0x10000000 + 0x1F50AC
        offset_address = ctypes.c_long()
        offset_list = [0x3B4, 0x24, 0x34, 0x48, 0x50, 0xE4]
        self.kernal32.ReadProcessMemory(int(self.process_handle), base_address, ctypes.byref(offset_address), 4, None)
        for offset in offset_list:
          self.kernal32.ReadProcessMemory(int(self.process_handle), offset_address.value + offset, ctypes.byref(offset_address), 4, None)
        return offset_address.value


    # This function can only get hp of hornet yet
    def get_boss_hp(self):
        base_address = 0x7B560000 + 0xFEF994
        offset_address = ctypes.c_long()
        offset_list = [0x54, 0x8, 0x1C, 0xFC, 0x18, 0xAC]
        self.kernal32.ReadProcessMemory(int(self.process_handle), base_address, ctypes.byref(offset_address), 4, None)
        for offset in offset_list:
          self.kernal32.ReadProcessMemory(int(self.process_handle), offset_address.value + offset, ctypes.byref(offset_address), 4, None)
        if offset_address.value > 900:
          return 901
        elif offset_address.value < 0:
          return -1
        return offset_address.value


    def get_play_location(self):
        base_address = 0x7B560000 + 0xF9D918
        x = ctypes.c_long()
        offset_list = [0x40, 0x248, 0x168, 0xC, 0x8, 0x1B4]
        self.kernal32.ReadProcessMemory(int(self.process_handle), base_address, ctypes.byref(x), 4, None)
        for offset in offset_list:
          self.kernal32.ReadProcessMemory(int(self.process_handle), x.value + offset, ctypes.byref(x), 4, None)
        
        base_address = 0x7B560000 + 0xF9D918
        y = ctypes.c_long()
        offset_list = [0x40, 0x328, 0x32C, 0x68, 0x40, 0x308]
        self.kernal32.ReadProcessMemory(int(self.process_handle), base_address, ctypes.byref(y), 4, None)
        for offset in offset_list:
          self.kernal32.ReadProcessMemory(int(self.process_handle), y.value + offset, ctypes.byref(y), 4, None)

        
        return x.value, y.value

    def get_hornet_location(self):
        base_address = 0x7B560000 + 0x00FEF994
        x = ctypes.c_long()
        offset_list = [0x20, 0x54, 0x24, 0x20, 0x5C, 0x2C]
        self.kernal32.ReadProcessMemory(int(self.process_handle), base_address, ctypes.byref(x), 4, None)
        for offset in offset_list:
          self.kernal32.ReadProcessMemory(int(self.process_handle), x.value + offset, ctypes.byref(x), 4, None)
        
        base_address = 0x7B560000 + 0x00FEF994
        y = ctypes.c_long()
        offset_list = [0x24, 0x1B0, 0x1C, 0x14, 0x18, 0x2C, 0xC]
        self.kernal32.ReadProcessMemory(int(self.process_handle), base_address, ctypes.byref(y), 4, None)
        for offset in offset_list:
          self.kernal32.ReadProcessMemory(int(self.process_handle), y.value + offset, ctypes.byref(y), 4, None)

        
        return x.value, y.value