from Tool.WindowsAPI import key_check
import random



#map user input into action space
#no need anymore


class User:
    def __init__(self):
        self.D = 1
        self.DOWN = False
        self.UP = False

    def get_user_action(self):
        operation, direction = key_check()
        for d in direction:
            if d == 'Left':
                self.D = 0
            elif d =='Right':
                self.D = 1
            elif d == 'Up':
               self.UP = True
            elif d == 'Down':
               self.DOWN = True

        for op in operation:
            if op == 'C':
                return random.randint(6, 8)
            elif op == 'X':
                if self.UP:
                   self.UP = False
                   return 5
                else:
                   if self.D == 0: #left
                        return 3
                   elif self.D == 1:
                        return 4
            elif op == 'Z':
                if self.UP:
                    self.UP = False
                    return 11
                elif self.DOWN:
                    self.DOWN = False
                    return 12
                else:
                    if self.D == 0: #left
                        return 9
                    elif self.D == 1:
                        return 10
            elif op == 'Shift':
                if self.D == 0:
                    return 13
                elif self.D == 1:
                    return 14

        if 'Left' in direction:
            return 1
        elif 'Right' in direction:
            return 2

        return 0