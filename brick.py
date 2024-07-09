from colorama import Back, Style
from entity import Entities

class Brick(Entities):

    def __init__(self,position,size,strength,indestructible):
        super().__init__(position,size)
        self.__strength = strength
        self.indestructible = indestructible
        self.cnt = 0
        self.last_ball_velocity = [-1,-1]
    def get_strength(self):
        return self.__strength
    def lower_brick(self,screen):
        super().reset_screen(screen)
        self.position[0] += 1
        self.update_screen(screen)
    def update_screen(self,screen):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.indestructible:
                    screen.screen[i+self.position[0]][j+self.position[1]]  = Back.MAGENTA + " " + Style.RESET_ALL
                elif self.__strength == 4:
                    if self.cnt == 0:
                        screen.screen[i+self.position[0]][j+self.position[1]]  = Back.LIGHTGREEN_EX + " " + Style.RESET_ALL
                    elif self.cnt == 1:
                        screen.screen[i+self.position[0]][j+self.position[1]]  = Back.BLUE + " " + Style.RESET_ALL
                    elif self.cnt == 2:
                        screen.screen[i+self.position[0]][j+self.position[1]]  = Back.RED + " " + Style.RESET_ALL
                    
                elif self.__strength == 3:
                    screen.screen[i+self.position[0]][j+self.position[1]]  = Back.RED + " " + Style.RESET_ALL
                elif self.__strength == 2:
                    screen.screen[i+self.position[0]][j+self.position[1]]  = Back.BLUE + " " + Style.RESET_ALL
                elif self.__strength == 1:
                    screen.screen[i+self.position[0]][j+self.position[1]]  = Back.LIGHTGREEN_EX + " " + Style.RESET_ALL
                else:
                    screen.screen[i+self.position[0]][j+self.position[1]]  = " "

        self.cnt = (self.cnt + 1)%3
                
    def update(self,screen,thru_ball):
        super().reset_screen(screen)
        if self.indestructible == False:
            if self.__strength == 4:
                self.__strength = self.cnt % 3 + 1
            else:
                self.__strength -= 1
        if thru_ball:
            self.__strength = 0
            self.indestructible = False
        self.update_screen(screen)
