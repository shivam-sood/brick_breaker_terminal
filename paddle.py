import numpy as np
from colorama import Back, Style
from entity import Entities



class Paddle(Entities):

    def __init__(self,position,size):
        super().__init__(position,size)
        self.velocity = [0,4]
        self.sticky = False
        self.life_lost = 0
        self.can_shoot = False
    def reset_paddle(self,position,size,screen):
        super().reset_screen(screen)
        self.position = np.array(position)
        self.size = np.array(size)
        self.update_screen(screen)

    def unstick(self):
        self.sticky = False
    def stick(self):
        self.sticky = True
        
    def update_screen(self,screen):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                screen.screen[i+self.position[0]][j+self.position[1]]  = Back.YELLOW + " " + Style.RESET_ALL
    
    def update(self,screen,direction,paddle,bricks,time ,boss ):
        super().reset_screen(screen)
        self.position[1] = self.position[1] + direction*self.velocity[1]
        if self.position[1] <= 0:
            self.position[1] = 0
        if self.position[1] + self.size[1]-1 >= screen.columns:
            self.position[1] = screen.columns - self.size[1]
        self.update_screen(screen)