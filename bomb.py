import numpy as np
from colorama import Back, Style
from entity import Entities

class Bomb(Entities):
    def __init__(self,position,size):
        super().__init__(position,size)
        self.finished = False

    def update_screen(self,screen):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                screen.screen[i+self.position[0]][j+self.position[1]]  = Back.GREEN + " " + Style.RESET_ALL


    def wall_collision(self,screen):
        if self.position[0] >= screen.lines - 1:
            self.finished = True
            return
            
    def paddle_ball_collision(self,screen,paddle):
        if self.position[0] == paddle.position[0] - 1:
            if (self.position[1] >= paddle.position[1] and self.position[1] <= paddle.position[1] + paddle.size[1] - 1):
                self.finished = True
                paddle.life_lost += 1
                
            
            

    def update(self,screen,direction ,paddle ,bricks,time,boss):
        if self.finished:
            return
        if self.position[0] >= screen.lines - 1:
            self.finished = True
            return
        super().reset_screen(screen)
        self.position[0] += 1
        self.wall_collision(screen)
        self.paddle_ball_collision(screen,paddle)
        if self.finished:
            return
        self.update_screen(screen)
        
