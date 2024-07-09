import numpy as np
from colorama import Back, Style
from entity import Entities



class Boss(Entities):

    def __init__(self,position,size):
        super().__init__(position,size)
        self.velocity = [0,4]
        self.health = 100
        self.active = False

        
    def update_screen(self,screen):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                screen.screen[i+self.position[0]][j+self.position[1]]  = Back.YELLOW + " " + Style.RESET_ALL
        # screen.screen[self.position[0]][self.position[1]]  = Back.YELLOW + "^" + Style.RESET_ALL
        # screen.screen[self.position[0] ][self.position[1]+ self.size[1]-1]  = Back.YELLOW + "^" + Style.RESET_ALL
        ufo = ".-=-."
        for i in range(len(ufo)):
            screen.screen[self.position[0]][i+self.position[1] + self.size[1]//2 - 2]  = Back.YELLOW + ufo[i] + Style.RESET_ALL
    def update(self,screen,direction ,paddle ,bricks,time ,boss):
        super().reset_screen(screen)
        self.position[1] = self.position[1] + direction*self.velocity[1]
        if self.position[1] <= 0:
            self.position[1] = 0
        if self.position[1] + self.size[1]-1 >= screen.columns:
            self.position[1] = screen.columns - self.size[1]
        self.update_screen(screen)