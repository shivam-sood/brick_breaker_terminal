import numpy as np
from colorama import Back, Style
from entity import Entities

class Ball(Entities):
    def __init__(self,position,size,velocity,fixed):
        super().__init__(position,size)
        self.fixed = fixed
        self.finished = False
        self.velocity = np.array(velocity)
        self.thru_ball = False
        self.collided = False
    def unfix(self):
        self.fixed = False
    def fix(self):
        self.fixed = True
    def set_thruball(self):
        self.thru_ball = True
    def unset_thruball(self):
        self.thru_ball = False

    def update_screen(self,screen):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                screen.screen[i+self.position[0]][j+self.position[1]]  = Back.WHITE + " " + Style.RESET_ALL


    def wall_collision(self,screen):
        if self.position[0] >= screen.lines:
            self.finished = True
            return
        
        if self.position[1] >= screen.columns:
            self.position[1] = screen.columns - 1
            self.velocity[1] = -abs(self.velocity[1])
        if self.position[1] <= -1:
            self.position[1] = 0
            self.velocity[1] = abs(self.velocity[1])
        if self.position[0] <= 0:
            self.position[0] = 1
            self.velocity[0] = abs(self.velocity[0])
            
    def paddle_ball_collision(self,screen,paddle,bricks,time):
        if self.position[0] == paddle.position[0] - 1:
            if (self.position[1] >= paddle.position[1] and self.position[1] <= paddle.position[1] + paddle.size[1]//3) or (self.position[1] >= paddle.position[1] + 2*paddle.size[1]//3 and self.position[1] <= paddle.position[1] + 3*paddle.size[1]//3):
                if time >= 200:
                    for brick in bricks:
                        brick.lower_brick(screen)
                    
                lower_val = min(abs(self.velocity[0]),abs(self.velocity[1]))
                higher_val = max(abs(self.velocity[0]),abs(self.velocity[1]))
                self.velocity[0] = -abs(self.velocity[0])
                direction_array = self.velocity // np.absolute(self.velocity)
                self.velocity = direction_array
                self.velocity[0] *= lower_val
                self.velocity[1] *= higher_val
                if paddle.sticky:
                    self.fix()
                    paddle.unstick()
            elif self.position[1] >= paddle.position[1] + paddle.size[1]//3 and self.position[1] <= paddle.position[1] + 2*paddle.size[1]//3:
                if time >= 200:
                    for brick in bricks:
                        brick.lower_brick(screen)
                        
                lower_val = min(abs(self.velocity[0]),abs(self.velocity[1]))
                higher_val = max(abs(self.velocity[0]),abs(self.velocity[1]))
                self.velocity[0] = -abs(self.velocity[0])
                direction_array = self.velocity // np.absolute(self.velocity)
                self.velocity = direction_array
                self.velocity[0] *= higher_val
                self.velocity[1] *= lower_val
                if paddle.sticky:
                    self.fix()
                    paddle.unstick()
    def boss_collision(self,boss):
        if boss.active == False:
            return
        if self.position[0] == 2 and self.position[1] >= boss.position[1] and self.position[1] <= boss.position[1] + boss.size[1] -1:
            boss.health -= 10
            self.collided = True
            self.velocity[0] = abs(self.velocity[0])

    def brick_collision(self,screen,bricks):
        for brick in bricks:
            if (self.position[0] == brick.position[0]-1) and self.position[1] >= brick.position[1] and self.position[1] <= brick.position[1] + brick.size[1]-1 and self.velocity[0] > 0:
                brick.update(screen,self.thru_ball)
                self.collided = True
                if not self.thru_ball:
                    self.velocity[0] = -abs(self.velocity[0])
            elif self.position[0] == brick.position[0]+brick.size[0] and self.position[1] >= brick.position[1] and self.position[1] <= brick.position[1] + brick.size[1]-1 and self.velocity[0] < 0:
                brick.update(screen,self.thru_ball)
                self.collided = True
                if not self.thru_ball:
                    self.velocity[0] = abs(self.velocity[0])
            elif self.position[1] == brick.position[1]-1 and self.position[0] >= brick.position[0] and self.position[0] <= brick.position[0] + brick.size[0]-1 and self.velocity[1] > 0:
                brick.update(screen,self.thru_ball)
                self.collided = True
                if not self.thru_ball:
                    self.velocity[1] = -abs(self.velocity[1])
            elif self.position[1] == brick.position[1]+brick.size[1] and self.position[0] >= brick.position[0] and self.position[0] <= brick.position[0] + brick.size[0]-1 and self.velocity[1] < 0:
                brick.update(screen,self.thru_ball)
                self.collided = True
                if not self.thru_ball:
                    self.velocity[1] = abs(self.velocity[1])
            elif self.position[0] == brick.position[0]-1 and self.position[1] == brick.position[1]-1 and self.velocity[0] > 0 and self.velocity[1] > 0:
                brick.update(screen,self.thru_ball)
                self.collided = True
                if not self.thru_ball:
                    
                    self.velocity[0] = -abs(self.velocity[0])
                    self.velocity[1] = -abs(self.velocity[1])
            elif self.position[0] == brick.position[0]-1 and self.position[1] == brick.position[1]+brick.size[1] and self.velocity[0] > 0 and self.velocity[1] < 0:
                brick.update(screen,self.thru_ball)
                self.collided = True
                if not self.thru_ball:
                    self.velocity[0] = -abs(self.velocity[0])
                    self.velocity[1] = abs(self.velocity[1])
            elif self.position[0] == brick.position[0]+brick.size[0] and self.position[1] == brick.position[1]-1 and self.velocity[0] < 0 and self.velocity[1] > 0:
                brick.update(screen,self.thru_ball)
                self.collided = True
                if not self.thru_ball:
                    self.velocity[0] = abs(self.velocity[0])
                    self.velocity[1] = -abs(self.velocity[1])
            elif self.position[0] == brick.position[0]+brick.size[0] and self.position[1] == brick.position[1]+brick.size[1] and self.velocity[0] < 0 and self.velocity[1] < 0:
                brick.update(screen,self.thru_ball)
                self.collided = True
                if not self.thru_ball:
                    self.velocity[0] = abs(self.velocity[0])
                    self.velocity[1] = abs(self.velocity[1])
    def update(self,screen,direction,paddle,bricks,time,boss):
        if self.fixed == False:
            if self.position[0] >= screen.lines-1:
                self.finished = True
                return
            super().reset_screen(screen)
            direction_array = self.velocity // np.absolute(self.velocity)
            lower_val = min(abs(self.velocity[0]),abs(self.velocity[1]))
            self.collided = False
            for _ in range(lower_val):
                if self.fixed == True:
                    break
                direction_array = self.velocity // np.absolute(self.velocity)
                self.position = self.position + direction_array
                self.wall_collision(screen)
                self.paddle_ball_collision(screen,paddle,bricks,time)
                self.brick_collision(screen,bricks)
                self.boss_collision(boss)
            direction_array = self.velocity // np.absolute(self.velocity)
            if abs(self.velocity[0]) < abs(self.velocity[1]):
                if self.collided == False:
                    if self.fixed == False:
                        self.position[1] = self.position[1] + direction_array[1]
                        self.wall_collision(screen)
                        self.paddle_ball_collision(screen,paddle,bricks,time)
                        self.brick_collision(screen,bricks)
                        self.boss_collision(boss)
                else:
                    if self.fixed == False:
                        self.position[1] = self.position[1] + direction_array[1]
            elif abs(self.velocity[0]) > abs(self.velocity[1]):
                if self.collided == False:
                    if self.fixed == False:
                        self.position[0] = self.position[0] + direction_array[0]
                        self.wall_collision(screen)
                        self.paddle_ball_collision(screen,paddle,bricks,time)
                        self.brick_collision(screen,bricks)
                        self.boss_collision(boss)
                    else:
                        if self.fixed == False:
                            self.position[0] = self.position[0] + direction_array[0]
            if self.collided:
                self.last_ball_velocity = self.velocity
            if self.finished:
                return
            self.update_screen(screen)
        else:
            super().reset_screen(screen)
            self.position[1] = self.position[1] + direction*paddle.velocity[1]
            if self.position[1] <= 0:
                self.position[1] = 0
            if self.position[1] + self.size[1]-1 >= screen.columns:
                self.position[1] = screen.columns - self.size[1]
            self.update_screen(screen)
