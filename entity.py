import numpy as np


class Entities():
    def __init__(self,position,size):
        self.position = np.array(position)
        self.size = np.array(size)
        
    def reset_screen(self,screen):
        try: 
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    screen.screen[i+self.position[0]][j+self.position[1]]  = " "
        except:
            return