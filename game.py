import random
import os
from screen import Screen
from ball import Ball
from powerup import powerup
from paddle import Paddle
from brick import Brick
from pellet import Pellet
from colorama import Back, Style
from input import Get, input_to
from boss import Boss
from bomb import Bomb
class game():
    def __init__(self):
        self.input = Get()
        self.bomb_timer = 0
        self.__lives = 3
        self.__level = 1
        self.lazer_cool = 0
        self.stage1 = False
        self.stage2 = False
        self.__score = 0
        self.__time = 0
        self.__clock = 0
        self.__next_level = 0
        self.time_since_level = 0
        self.__frames = 10000
        self.__paused = False
        self.screen = Screen()
        self.powerup_prob = 0.3
        self.indes_prob = 0.1
        self.paddle = Paddle([self.screen.lines-2,(self.screen.columns-17)//2 ],[1,17])
        self.boss = Boss([1,(self.screen.columns-17)//2 ],[1,17])
        self.bricks_left = 0
        ball = Ball([self.screen.lines-3,random.randrange(self.paddle.position[1],self.paddle.position[1]+self.paddle.size[1])],[1,1],[-1,2],True)
        self.balls = [ball]
        self.objects = [ball,self.paddle]
        self.movable_objects = [ball, self.paddle]
        self.bricks = []
        self.powerups = []
        self.pellets = []
        self.bombs = []
        self.cnt_unbreakable = 0
        self.create_bricks(self.__level)
        for obj in self.objects:
            obj.update_screen(self.screen)
        
        self.gameloop()
    def defense(self):
        if self.boss.health >= 50 and self.stage1 == False and self.balls[0].position[0] > 11:
            
            for i in range(1,self.screen.columns-7,11):
                brick = Brick([5,i],[3,10],random.randrange(1,5),False)
                self.bricks.append(brick)
            self.stage1 = True
        var = 15
        if self.boss.health <= 50 and self.stage2 == False and len(self.bricks) == self.cnt_unbreakable and self.balls[0].position[0] > 18:
            if len(self.bricks) > 0:
                if self.bricks[0].position[0] >= 9 and self.bricks[0].position[0] <= 15:
                    var = 17
            for i in range(1,self.screen.columns-7,11):
                brick = Brick([var,i],[3,10],random.randrange(1,5),False)
                self.bricks.append(brick)
            self.stage2 = True
    def create_bricks(self, level):
        
        if level == 1:
            start = 6
            
            for j in range(4,self.screen.lines//2,6):
                for i in range(start,self.screen.columns-14,24):
                    if random.random() <= self.indes_prob:
                        brick = Brick([j,i],[3,10],random.randrange(1,5),True)
                    else:
                        brick = Brick([j,i],[3,10],random.randrange(1,5),False)
                    self.bricks.append(brick)
                    
            
            
        elif level == 2:
            start = 5
            for j in range(3,self.screen.lines//2,5):
                if j % 2 == 0:
                    start = 5
                else:
                    start = 15
                for i in range(start,self.screen.columns-14,20):
                    if random.random() <= self.indes_prob:
                        brick = Brick([j,i],[3,10],random.randrange(1,5),True)
                    else:
                        brick = Brick([j,i],[3,10],random.randrange(1,5),False)
                    self.bricks.append(brick)
                    
        else:
            start = 5
            
            for i in range(start,self.screen.columns-14,25):
                brick = Brick([self.screen.lines//2,i],[3,10],random.randrange(1,5),True)
                self.cnt_unbreakable += 1
                self.bricks.append(brick)
            self.boss.active = True
            self.movable_objects.append(self.boss)    
            self.bomb_timer = self.__time
        self.objects.extend(self.bricks)
        
    def update_time(self):
        self.__time += 1
        self.time_since_level += 1
    def update_clock(self):    
        self.__clock = (self.__clock + 1) % self.__frames

    def check_balls(self):
        isAnyBallLeft = False
        for balls in self.balls:
            if balls.finished == False:
                isAnyBallLeft = True
        if isAnyBallLeft == False:
            self.__lives -= 1
            ball = Ball([self.screen.lines-3,self.screen.columns//2 - 1],[1,1],[-1,2],True)
            self.paddle.reset_paddle([self.screen.lines-2,(self.screen.columns-17)//2 ],[1,17],self.screen)
            self.balls.append(ball)
            self.objects.append(ball)
            self.movable_objects.append(ball)
            for obj in self.powerups:
                obj.reset_screen(self.screen)
            self.powerups.clear()
            self.bombs.clear()
            self.pellets.clear()
    def update_game(self,direction):
        self.update_time()
        # self.paddle.update(self.screen,direction,self.paddle,self.bricks)
        # for obj in self.balls:
        #     obj.update(self.screen,direction,self.paddle,self.bricks)
        for obj in self.movable_objects:
            obj.update(self.screen,direction,self.paddle,self.bricks,self.time_since_level,self.boss)
        for obj in self.bricks:
            obj.update_screen(self.screen)
        for obj in self.powerups:
            obj.update(self.screen,self.paddle,self.__time,self.balls)
            if obj.is_active() == True and (obj.get_type() == 5):
                obj.power(self.paddle,self.balls,self.screen)
        self.movable_objects =  [self.paddle] + self.balls + self.pellets + self.bombs
        if self.__level == 3:
            self.movable_objects.append(self.boss)
    def update_bricks(self):
        temp_bricks = []
        self.bricks_left = 0
        for brick in self.bricks:
            if brick.indestructible == False:
                self.bricks_left += 1
            if brick.get_strength() > 0:
                temp_bricks.append(brick)
            else:
                # if random.random() < 1:
                if random.random() < self.powerup_prob and self.boss.active == False:
                    new_power = powerup(brick.position,[2,2],self.__time,random.randrange(1,8), brick.last_ball_velocity)
                    # new_power = powerup(brick.position,[2,2],self.__time,6, brick.last_ball_velocity)
                    self.powerups.append(new_power)
        self.__score += len(self.bricks)-len(temp_bricks)
        self.bricks = temp_bricks
    def gameloop(self):
        while 1:
            if self.__clock == 0:
                c = input_to(self.input)
                direction = 0
                if c == 'A' or c == 'a':
                    direction = -1
                elif c == 'D' or c == 'd':
                    direction = 1
                elif c == 'q' or c == 'Q':
                    return
                elif c == " ":
                    for ball in self.balls:
                        ball.unfix()
                elif c == "p" or c =="P":
                    self.__paused = not self.__paused
                elif c == "n" or c == "N":
                    self.__next_level = 1
                elif c == "u" or c == "U":
                    if self.paddle.can_shoot == True and self.__time >= self.lazer_cool + 10:
                        pellet = Pellet([self.screen.lines-3,self.paddle.position[1]],[1,1])
                        self.movable_objects.append(pellet)
                        self.pellets.append(pellet)
                        pellet = Pellet([self.screen.lines-3,self.paddle.position[1] + self.paddle.size[1] - 1],[1,1])
                        self.movable_objects.append(pellet)
                        self.pellets.append(pellet)
                        self.lazer_cool = self.__time
                if self.__paused:
                    continue
                
                self.update_game(direction)
                self.check_balls()
                self.update_bricks()
                if self.boss.health <= 70:
                    self.defense()
                if self.boss.health <= 30:
                    self.defense()
                
                if self.__level == 3 and self.boss.health <= 0:
                    os.system('clear')
                    self.__score += 1000
                    print("GAME OVER YOU WON!!!")
                    return 
                
                if (self.bricks_left == 0 and self.__level <= 2) or self.__next_level == 1:
                    self.__next_level = 0
                    self.time_since_level = 0
                    for obj in self.objects:
                        obj.reset_screen(self.screen)
                    self.bricks.clear()
                    self.balls.clear()
                    self.movable_objects.clear()
                    self.__level += 1
                    if self.__level == 4:
                        os.system('clear')
                        print("GAME OVER!!!")
                        return 
                    ball = Ball([self.screen.lines-3,self.screen.columns//2 - 1],[1,1],[-1,2],True)
                    self.paddle.reset_paddle([self.screen.lines-2,(self.screen.columns-17)//2 ],[1,17],self.screen)
                    self.balls.append(ball)
                    self.objects.append(ball)
                    self.objects.append(self.paddle)
                    self.movable_objects.append(ball)
                    self.movable_objects.append(self.paddle)
                    self.powerups.clear()
                    self.bombs.clear()
                    self.pellets.clear()
                    self.create_bricks(self.__level)
                self.__lives -= self.paddle.life_lost
                self.paddle.life_lost = 0
                for brick in self.bricks:
                    # brick.update_screen(self.screen)
                    if brick.position[0] + brick.size[0] >= self.screen.lines-1:
                        os.system('clear')
                        print("GAME OVER YOU LOST!!!!")
                        return
                time_left = 0
                for obj in self.powerups:
                    if obj.get_type() == 7:
                        time_left = max(time_left, obj.get_time())
                if self.paddle.can_shoot == True:
                    self.screen.screen[self.screen.lines-3][self.paddle.position[1]] = Back.YELLOW + " " + Style.RESET_ALL
                    self.screen.screen[self.screen.lines-3][self.paddle.position[1] + self.paddle.size[1] - 1] = Back.YELLOW + " " + Style.RESET_ALL        
                if time_left == 0 or time_left < self.__time - 100:
                    self.screen.draw_screen(self.__lives, self.__time, self.__score,self.__level, 0,self.boss.health)
                else:
                    self.screen.draw_screen(self.__lives, self.__time, self.__score,self.__level, 100 - (self.__time - time_left),self.boss.health)
                if self.paddle.can_shoot == True:
                    self.screen.screen[self.screen.lines-3][self.paddle.position[1]] = " " 
                    self.screen.screen[self.screen.lines-3][self.paddle.position[1] + self.paddle.size[1] - 1] = " " 
                if self.__lives == 0:
                    os.system('clear')
                    print("GAME OVER YOU LOST!!!!")
                    return
                if self.__level == 3:
                    if self.__time >= self.bomb_timer + 50:
                        bomb = Bomb([2,random.randrange(self.boss.position[1],self.boss.position[1]+self.boss.size[1])],[1,1])
                        self.bombs.append(bomb)
                        self.bomb_timer = self.__time
            self.update_clock()
