import os
import sys

class Screen():
    def __init__(self):
        term_size = os.get_terminal_size()
        self.lines = term_size.lines
        self.columns = term_size.columns
        self.screen = []
        for _ in range(self.lines):
            temp_array = []
            for _ in range(self.columns):
                temp_array.append(" ")
            self.screen.append(temp_array)
        
    def draw_screen(self,lives,time,score,level,t,health):
        os.system('clear')
        sys.stdout.flush()
        line_number = 0
        # text = ""
        for line in self.screen:
            if line_number == 0:
                print("Time:{} Lives:{} Score:{} level:{} laser powerup time left:{} Boss Health:{}".format(time,lives,score,level,t,health))
                # text += "Time:{}   Lives:{}   Score:{}\n".format(time,lives,score)
                
                line_number += 1
                continue
            for char in line:
                print(char,end='')
                
                # text += char
            if line_number != len(self.screen) - 1:
                # text += "\n"
                print("")
                
            line_number += 1
        # print("")
        # sys.stdout.flush()
        # print(text,end='')
