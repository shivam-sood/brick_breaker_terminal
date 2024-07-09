from colorama import Back, Style
from entity import Entities
from ball import Ball
import numpy as np
class powerup(Entities):

    def __init__(self,position,size,time,power_type,velocity):
        super().__init__(position,size)
        self.__power_type = power_type
        self.__isObtained = False
        self.__active = False
        self.__start_time = 0
        self.velocity = velocity
        self.res = 0
    def is_active(self):
        return self.__active
    def get_type(self):
        return self.__power_type
    def get_time(self):
        return self.__start_time
    def update_screen(self,screen):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                screen.screen[i+self.position[0]][j+self.position[1]]  = Back.LIGHTBLACK_EX + str(self.__power_type) + Style.RESET_ALL
    
    def power(self,paddle,balls,screen):
        if self.__power_type == 1:
            paddle.reset_screen(screen)
            paddle.size[1] += 3
            paddle.update_screen(screen)
        elif self.__power_type == 2:
            paddle.reset_screen(screen)
            paddle.size[1] -= 3
            if paddle.size[1] <= 0:
                paddle.size[1] += 3
            paddle.update_screen(screen)
        elif self.__power_type == 3:
            tmp = []
            for ball in balls:
                new_ball = Ball(ball.position,ball.size,ball.velocity*-1,False)
                tmp.append(new_ball)
            balls.extend(tmp)
        elif self.__power_type == 4:
            for ball in balls:
                if ball.velocity[1] > 0:
                    ball.velocity[1] = ball.velocity[1] + 1
                else:
                    ball.velocity[1] = ball.velocity[1] - 1
                if ball.velocity[0] > 0:
                    ball.velocity[0] = ball.velocity[0] + 1
                else:
                    ball.velocity[0] = ball.velocity[0] - 1
        elif self.__power_type == 5:
            for ball in balls:
                ball.set_thruball()
        elif self.__power_type == 6:
            paddle.stick()
        elif self.__power_type == 7:
            paddle.can_shoot = True
            
    def wall_collision(self,screen):
        if self.position[0] + self.size[0] >= screen.lines:
            return
        if self.position[1] + self.size[1]>= screen.columns:
            self.position[1] = screen.columns - 1
            self.collided = True
            self.velocity[1] = -abs(self.velocity[1])
        if self.position[1] <= -1:
            self.position[1] = 0
            self.collided = True
            self.velocity[1] = abs(self.velocity[1])
        if self.position[0] <= 0:
            self.position[0] = 1
            self.collided = True
            self.velocity[0] = abs(self.velocity[0])
    def paddle_ball_collision(self,screen,paddle,time,balls):
        if self.position[0] + self.size[0] == paddle.position[0]:
            if self.position[1]+self.size[1]-1 >= paddle.position[1] and self.position[1] <= paddle.position[1] + paddle.size[1]:
                self.__isObtained = True
                self.__start_time = time
                self.__active = True
                self.collided = True
                self.power(paddle,balls,screen)
                return
    def depower(self,paddle,balls,screen):
        if self.__power_type == 1:
            paddle.reset_screen(screen)
            paddle.size[1] -= 3
            paddle.update_screen(screen)
        elif self.__power_type == 2:
            paddle.reset_screen(screen)
            paddle.size[1] += 3
            paddle.update_screen(screen)
        elif self.__power_type == 3:
            pass
        elif self.__power_type == 4:
            for ball in balls:
                if ball.velocity[0] > 0:
                    ball.velocity[0] = ball.velocity[0] - 1
                else:
                    ball.velocity[0] = ball.velocity[0] + 1
                if ball.velocity[1] > 0:
                    ball.velocity[1] = ball.velocity[1] - 1
                else:
                    ball.velocity[1] = ball.velocity[1] + 1
        elif self.__power_type == 5:
            for ball in balls:
                ball.unset_thruball()
        elif self.__power_type == 6:
            paddle.unstick()
        elif self.__power_type == 7:
            paddle.can_shoot = False
            
    def update(self,screen,paddle,time,balls):
        if self.__isObtained == False:
            if self.position[0] + self.size[0]>= screen.lines:
                return
            super().reset_screen(screen)
            
            
            # self.position[0] += self.velocity[0]
            # if self.position[0] + self.size[0] == paddle.position[0]:
            #     if self.position[1]+self.size[1]-1 >= paddle.position[1] and self.position[1] <= paddle.position[1] + paddle.size[1]:
            #         self.__isObtained = True
            #         self.__start_time = time
            #         self.__active = True
            #         self.power(paddle,balls,screen)
            #         return
            direction_array = self.velocity // np.absolute(self.velocity)
            lower_val = min(abs(self.velocity[0]),abs(self.velocity[1]))
            self.collided = False
            for _ in range(lower_val):
                direction_array = self.velocity // np.absolute(self.velocity)
                self.position = self.position + direction_array
                self.wall_collision(screen)
                self.paddle_ball_collision(screen,paddle,time,balls)
            direction_array = self.velocity // np.absolute(self.velocity)
            if abs(self.velocity[0]) < abs(self.velocity[1]):
                for _ in range(abs(self.velocity[0] - self.velocity[1])):
                    if self.collided == False:
                        self.position[1] = self.position[1] + direction_array[1]
                        self.wall_collision(screen)
                        self.paddle_ball_collision(screen,paddle,time,balls)
            elif abs(self.velocity[0]) > abs(self.velocity[1]):
                for _ in range(abs(self.velocity[0] - self.velocity[1])):
                    if self.collided == False:
                        self.position[0] = self.position[0] + direction_array[0]
                        self.wall_collision(screen)
                        self.paddle_ball_collision(screen,paddle,time,balls)
            self.collided = False
            if self.__isObtained == True:
                super().reset_screen(screen)
                return
            self.res += 1
            if self.res == 10:
                self.velocity[0] += 1
                self.res = 0
            if self.position[0] + self.size[0] > paddle.position[0]:
                return
            self.update_screen(screen)
        else:
            if time >= self.__start_time + 100 and self.__active:
                self.__active = False
                self.depower(paddle,balls,screen)