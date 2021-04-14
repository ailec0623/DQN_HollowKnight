import win32gui
import win32api
import win32process
import ctypes

Psapi = ctypes.WinDLL('Psapi.dll')
Kernel32 = ctypes.WinDLL('kernel32.dll')
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010

def EnumProcessModulesEx(hProcess):
    buf_count = 256
    while True:
        LIST_MODULES_ALL = 0x03
        buf = (ctypes.wintypes.HMODULE * buf_count)()
        buf_size = ctypes.sizeof(buf)
        needed = ctypes.wintypes.DWORD()
        if not Psapi.EnumProcessModulesEx(hProcess, ctypes.byref(buf), buf_size, ctypes.byref(needed), LIST_MODULES_ALL):
            raise OSError('EnumProcessModulesEx failed')
        if buf_size < needed.value:
            buf_count = needed.value // (buf_size // buf_count)
            continue
        count = needed.value // (buf_size // buf_count)
        return map(ctypes.wintypes.HMODULE, buf[:count])

class Hp_getter():
    def __init__(self):
        hd = win32gui.FindWindow(None, "Hollow Knight")
        pid = win32process.GetWindowThreadProcessId(hd)[1]
        self.process_handle = win32api.OpenProcess(0x1F0FFF, False, pid)
        self.kernal32 = ctypes.windll.LoadLibrary(r"C:\\Windows\\System32\\kernel32.dll")

        self.hx = 0
        # get dll address
        hProcess = Kernel32.OpenProcess(
        PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
        False, pid)
        hModule  = EnumProcessModulesEx(hProcess)
        for i in hModule:
          temp = win32process.GetModuleFileNameEx(self.process_handle,i.value)
          if temp[-15:] == "UnityPlayer.dll":
            self.UnityPlayer = i.value
          if temp[-8:] == "mono.dll":
            self.mono = i.value
    
    def get_souls(self):
        base_address = self.UnityPlayer + 0x00FA0998
        offset_address = ctypes.c_long()
        offset_list = [0x10, 0x64, 0x3C, 0xC, 0x60, 0x120]
        self.kernal32.ReadProcessMemory(int(self.process_handle), base_address, ctypes.byref(offset_address), 4, None)
        for offset in offset_list:
          self.kernal32.ReadProcessMemory(int(self.process_handle), offset_address.value + offset, ctypes.byref(offset_address), 4, None)
        return offset_address.value

    def get_self_hp(self):
        base_address = self.mono + 0x1F50AC
        offset_address = ctypes.c_long()
        offset_list = [0x3B4, 0x24, 0x34, 0x48, 0x50, 0xE4]
        self.kernal32.ReadProcessMemory(int(self.process_handle), base_address, ctypes.byref(offset_address), 4, None)
        for offset in offset_list:
          self.kernal32.ReadProcessMemory(int(self.process_handle), offset_address.value + offset, ctypes.byref(offset_address), 4, None)
        return offset_address.value


    # This function can only get hp of hornet yet
    def get_boss_hp(self):
        base_address = self.UnityPlayer + 0x00FEF994 
        offset_address = ctypes.c_long()
        offset_list = [0x54, 0x8, 0x1C, 0x1C, 0x7C, 0x18, 0xAC]
        self.kernal32.ReadProcessMemory(int(self.process_handle), base_address, ctypes.byref(offset_address), 4, None)
        for offset in offset_list:
          self.kernal32.ReadProcessMemory(int(self.process_handle), offset_address.value + offset, ctypes.byref(offset_address), 4, None)
        if offset_address.value > 900:
          return 901
        elif offset_address.value < 0:
          return -1
        return offset_address.value

    # the methods below can not work yet
    def get_play_location(self):
        x = ctypes.c_long()
        x.value += self.UnityPlayer + 0x00FEF994
        offset_list = [0x4C, 0x4, 0x4, 0x10, 0x0]
        self.kernal32.ReadProcessMemory(int(self.process_handle), x, ctypes.byref(x), 4, None)
        for offset in offset_list:
          self.kernal32.ReadProcessMemory(int(self.process_handle), x.value + offset, ctypes.byref(x), 4, None)
        xx = ctypes.c_float()
        self.kernal32.ReadProcessMemory(int(self.process_handle), x.value + 0x44, ctypes.byref(xx), 4, None)

        y = ctypes.c_long()
        y.value += self.UnityPlayer + 0x00FEF994
        offset_list = [0x24, 0x104, 0x6C, 0x10, 0xAC]
        self.kernal32.ReadProcessMemory(int(self.process_handle), y, ctypes.byref(y), 4, None)
        for offset in offset_list:
          self.kernal32.ReadProcessMemory(int(self.process_handle), y.value + offset, ctypes.byref(y), 4, None)

        yy = ctypes.c_float()
        self.kernal32.ReadProcessMemory(int(self.process_handle), y.value + 0xC, ctypes.byref(yy), 4, None)

        return xx.value, yy.value

    def get_hornet_location(self):
        base_address = self.UnityPlayer + 0x00FEF994
        x = ctypes.c_long()
        offset_list = [0x20, 0x54, 0x24, 0x20, 0x5C]
        self.kernal32.ReadProcessMemory(int(self.process_handle), base_address, ctypes.byref(x), 4, None)
        for offset in offset_list:
          self.kernal32.ReadProcessMemory(int(self.process_handle), x.value + offset, ctypes.byref(x), 4, None)
          
        xx = ctypes.c_float()
        self.kernal32.ReadProcessMemory(int(self.process_handle), x.value + 0xC, ctypes.byref(xx), 4, None)

        base_address = self.UnityPlayer + 0x00FEF994
        y = ctypes.c_long()
        offset_list = [0x54, 0x8, 0x1C, 0x1C, 0x14]
        self.kernal32.ReadProcessMemory(int(self.process_handle), base_address, ctypes.byref(y), 4, None)
        for offset in offset_list:
          self.kernal32.ReadProcessMemory(int(self.process_handle), y.value + offset, ctypes.byref(y), 4, None)
     
        yy = ctypes.c_float()
        self.kernal32.ReadProcessMemory(int(self.process_handle), y.value + 0xAC, ctypes.byref(yy), 4, None)

        if xx.value > 14 and xx.value < 40:
          self.hx = xx.value
        return self.hx, yy.value