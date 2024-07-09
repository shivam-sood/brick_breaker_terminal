import numpy as np
from colorama import Back, Style
from entity import Entities

class Pellet(Entities):
    def __init__(self,position,size):
        super().__init__(position,size)
        self.finished = False

    def update_screen(self,screen):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                screen.screen[i+self.position[0]][j+self.position[1]]  = Back.CYAN + " " + Style.RESET_ALL


    def wall_collision(self):
        if self.position[0] <= 0:
            self.finished = True
            return
            
    def brick_collision(self,screen,bricks):
        for brick in bricks:
            if (self.position[0] == brick.position[0]+brick.size[0]) and self.position[1] >= brick.position[1] and self.position[1] <= brick.position[1] + brick.size[1]-1:
                brick.update(screen,False)
                self.finished = True
    def boss_collision(self,boss):
        if boss.active == False:
            return
        if self.position[0] == 2 and self.position[1] >= boss.position[1] and self.position[1] <= boss.position[1] + boss.size[1] -1:
            boss.health -= 10
            self.finished = True       
    def update(self,screen,direction ,paddle ,bricks,time,boss):
        if self.finished:
            return
        if self.position[0] < 0:
            self.finished = True
            return
        super().reset_screen(screen)
        self.position[0] -= 1
        self.wall_collision()
        self.brick_collision(screen,bricks)
        self.boss_collision(boss)
        if self.finished:
            return
        self.update_screen(screen)
        
