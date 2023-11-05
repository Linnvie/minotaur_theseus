import pygame
from Button_class import Button

class Menu():
    def __init__(self, game):
        self.game = game
        self.cursor_visible = True
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        if self.cursor_visible:
            self.game.draw_text('>', 30, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self, x, y):
        self.game.window.blit(self.game.display, (x, y))
        pygame.display.update()
        self.game.reset_keys()


menu_items = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", "Level 8", "Level 9", "Level 10"]
page = 0
items_per_page = 6
total_pages = -(-len(menu_items) // items_per_page)
class LevelMenu(Menu):
    def __init__(self, game, w = 800, h = 600):
        Menu.__init__(self, game)
        self.state = 1
        self.w = w
        self.h = h
        self.button_location = [(0,0)]
        self.button_state = [0]
        self.cursor_rect.midtop = (self.w/3 + self.offset, self.h/4 +120)      
        self.img = pygame.transform.scale(pygame.image.load('images/bg_menu.jpg').convert_alpha(), (self.w, self.h))
        s = self.h/4 +120
        w = self.w/2
        for i in range(1,items_per_page+1):        
            index = page * items_per_page + i
            if index < len(menu_items):
                if(i%2 == 0):
                    self.button_location.append((self.w/3*2, s))
                    s=s+80
                else:
                    self.button_location.append((self.w/3, s))    
                self.button_state.append(i)
    def display_menu(self):  
        self.run_display = True
        self.game.window = pygame.display.set_mode(size = (self.w, self.h))
        self.game.display = pygame.Surface((self.w, self.h))
        while self.run_display:
            self.game.get_events_in_menu()
            self.check_input()
            blur_surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            blur_surface.fill((255, 255, 255, 30))
            self.game.display.blit(self.img, (0,0))
            self.game.display.blit(blur_surface, (0, 0))

            self.game.draw_text("Robert Abbott's", 40, self.w/2, self.h/6 +25 )
            self.game.draw_text("Theseus and the Minotaur", 40, self.w/2, self.h/6 +75 )
            s = self.h/4 +120
            w = self.w/2
            for i in range(items_per_page):        
                index = page * items_per_page + i
                if index < len(menu_items):
                    if(i%2 == 0):
                        button = Button(self.game.display, menu_items[i], self.w/3, s, 190, 50, True)
                        button.draw(30,10)
                    else:
                        button = Button(self.game.display, menu_items[i], self.w/3*2, s, 190, 50, True)
                        button.draw(30,10)
                        s=s+80           
            self.draw_cursor()
            self.blit_screen(0,0)

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == self.button_state[6]:
                self.cursor_rect.midtop = (self.button_location[1][0] + self.offset, self.button_location[1][1])
                self.state = self.button_state[1]
            else:
                if self.state in self.button_state:
                    self.cursor_rect.midtop = (self.button_location[self.state +1][0] + self.offset, self.button_location[self.state+1][1])
                    self.state = self.button_state[self.state+1]
            print("current state1", self.state, self.button_location, self.button_state)
        elif self.game.UP_KEY:
            if self.state == self.button_state[1]:
                self.cursor_rect.midtop = (self.button_location[6][0] + self.offset, self.button_location[6][1])
                self.state = self.button_state[6]
            else:
                if self.state in self.button_state:
                    self.cursor_rect.midtop = (self.button_location[self.state -1][0] + self.offset, self.button_location[self.state-1][1])
                    self.state = self.button_state[self.state-1]
            print("current state1", self.state)
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state in self.button_state:
                self.game.playing = True
            self.run_display = False

class MainMenu(Menu):
    def __init__(self, game, w = 800, h = 600):
        Menu.__init__(self, game)
        self.state = "Start"
        self.w = w
        self.h = h
        self.startx, self.starty = self.w/2, self.h/4 +120
        self.tutorialx, self.tutorialy = self.w/3, self.h/3 + 160
        self.mythologyx, self.mythologyy = self.w/3*2, self.h/3 +160
        self.optionsx, self.optionsy = self.w/3, self.h/3*2 +60   
        self.exitx, self.exity = self.w/3*2, self.h/3*2 +60
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        
        self.img = pygame.transform.scale(pygame.image.load('images/bg_menu.jpg').convert_alpha(), (self.w, self.h))

    def display_menu(self):
        self.run_display = True
        self.game.window = pygame.display.set_mode(size = (self.w, self.h))
        self.game.display = pygame.Surface((self.w, self.h))
        while self.run_display:
            self.game.get_events_in_menu()
            self.check_input()
            blur_surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            blur_surface.fill((255, 255, 255, 30))
            self.game.display.blit(self.img, (0,0))
            self.game.display.blit(blur_surface, (0, 0))

            self.game.draw_text("Robert Abbott's", 40, self.w/2, self.h/6 +25 )
            self.game.draw_text("Theseus and the Minotaur", 40, self.w/2, self.h/6 +75 )

            button1 = Button(self.game.display,'Start Game', self.w/2, self.h/4 +120, 190, 50, True)
            button1.draw(30,10)

            button2 = Button(self.game.display,'Tutorial ', self.w/3, self.h/3 + 160, 190, 50, True)
            button2.draw(30,10)

            button3 = Button(self.game.display,'Mythology', self.w/3*2, self.h/3 +160 , 190, 50, True)
            button3.draw(30,10)

            button4 = Button(self.game.display,'Option', self.w/3, self.h/3*2 +60, 190, 50, True)
            button4.draw(30,10)

            button5 = Button(self.game.display,'Exit', self.w/3*2, self.h/3*2 +60, 190, 50, True)
            button5.draw(30,10)

            if(button1.check_hover() or button2.check_hover() or button3.check_hover()):
                self.cursor_visible = False
            else:
                self.cursor_visible = True  
            self.draw_cursor()
            self.blit_screen(0,0)

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.tutorialx + self.offset, self.tutorialy)
                self.state = 'Tutorial'
            elif self.state == 'Tutorial':
                self.cursor_rect.midtop = (self.mythologyx + self.offset, self.mythologyy)
                self.state = 'Mythology'
            elif self.state == 'Mythology':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Option'
            elif self.state == 'Option':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Option'
            elif self.state == 'Option':
                self.cursor_rect.midtop = (self.mythologyx + self.offset, self.mythologyy)
                self.state = 'Mythology'
            elif self.state == 'Mythology':
                self.cursor_rect.midtop = (self.tutorialx + self.offset, self.tutorialy)
                self.state = 'Tutorial'
            elif self.state == 'Tutorial':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                # self.game.playing = True
                self.game.curr_menu = self.game.level_menu
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Tutorial':
                self.game.curr_menu = self.game.tutorial
            elif self.state == 'Mythology':
                self.game.curr_menu = self.game.mythology
            elif self.state == 'Exit':
                self.game.playing = False
                self.game.running = False
                self.game.curr_menu.run_display = False
            self.run_display = False

class EndMenu(Menu):
    def __init__(self, game, text1, text2, text3, first_choose, w = 338, h = 434):
        Menu.__init__(self, game)
        
        self.state = first_choose
        self.text1=text1
        self.text2=text2
        self.text3=text3
        self.first_choose = first_choose
        self.w = w
        self.h = h
        self.img = pygame.transform.scale(pygame.image.load('images/bg_end.jpg').convert_alpha(), (self.w, self.h))

    def display_menu(self):
        
        self.game.display = pygame.Surface((self.w,self.h))
        self.run_display = True
        infoObject = pygame.display.Info()  
        current_w, current_h = infoObject.current_w, infoObject.current_h
        self.firstx, self.firsty = self.w/2 + 15, self.h / 2
        self.restartx, self.restarty = self.w/2 + 15, self.h/2+ 45
        self.mainx, self.mainy = self.w/2 + 15, self.h/2 + 95
        self.cursor_rect.midtop = (self.firstx + self.offset, self.firsty)

        while self.run_display:
            
            # print(self.game.START_KEY)
            self.game.get_events_in_menu()
            self.check_input()
            # self.game.display.fill(self.game.BLACK)
            blur_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
            blur_surface.fill((255, 255, 255, 30))
            # print(self.game.playing)
            self.game.display.blit(self.img, (0,0))
            # self.game.display.blit(blur_surface, (0, 0))

            self.game.draw_text(self.text1, 30, self.w/2, self.h/6 - 20)
            self.game.draw_text(self.text2, 22, self.w/2 , self.h/3 +5 )
            self.game.draw_text(self.text3, 22, self.w/2, self.h/3 + 35 )


            button1 = Button(self.game.display,self.first_choose, self.w/2, self.h/2, 160, 30, True)
            button1.draw(20,10)

            button2 = Button(self.game.display,'Restart Level', self.w/2, self.h/2 + 50, 160, 30, True)
            button2.draw(20,10)

            button3 = Button(self.game.display,'Back to menu', self.w/2, self.h/2 + 100, 160, 30, True)
            button3.draw(20,10)

            if(button1.check_hover() or button2.check_hover() or button3.check_hover()):
                self.cursor_visible = False
            else:
                self.cursor_visible = True
        
            self.draw_cursor()
            self.blit_screen((current_w - self.w)/2, (current_h - self.h)/2)
        
    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == self.first_choose:
                self.cursor_rect.midtop = (self.restartx + self.offset, self.restarty)
                self.state = 'Restart'
            elif self.state == 'Restart':
                self.cursor_rect.midtop = (self.mainx + self.offset, self.mainy)
                self.state = 'Main'
            elif self.state == 'Main':
                self.cursor_rect.midtop = (self.firstx + self.offset, self.firsty)
                self.state = self.first_choose
        elif self.game.UP_KEY:
            if self.state == self.first_choose:
                self.cursor_rect.midtop = (self.mainx + self.offset, self.mainy)
                self.state = 'Main'
            elif self.state == 'Main':
                self.cursor_rect.midtop = (self.firstx + self.offset, self.firsty)
                self.state = 'Restart'
            elif self.state == 'Restart':
                self.cursor_rect.midtop = (self.restartx + self.offset, self.restarty)
                self.state = self.first_choose

    def check_input(self):
        # print("checkinputD",self.state)
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Main':
                self.game.curr_menu = self.game.main_menu
            elif self.state == 'Restart':    
                # code restart lại vòng
                self.game.restart()
                self.game.playing = True
            elif self.state == 'Undo':
                #code undo lại bước cuối cùng
                self.game.undo()
                self.game.playing = True
            elif self.state == 'Next':
                print("next")
                # self.game.reset_keys()
                #code undo lại bước cuối cùng
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        # self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.volx, self.voly = 200, 200 + 20
        # self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.controlsx, self.controlsy = 200, 240
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        self.img = pygame.transform.scale(pygame.image.load('images/bg_menu.jpg').convert_alpha(), (700,525))
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass

text_lines = ["Theseus and the Minotaur is a type of logic maze",
             "designed by Robert Abbott. In this maze, the player acts as",
              "King Theseus of Athens trying to escape from the labyrinth.",
              "The main difference between this labyrinth and the standard",
              "type of labyrinth, beyond the fact that it is set on a grid,",
              "is the fact that the maze is not empty, there is a minotaur ",
              "hunting the player down , and it takes two steps per maze.",
              "The Minotaur is faster than the player, but his movements ",
              "are predictable and often inefficient. The Minotaur is determined",
              "by moving horizontally to see if it can get closer to the player,", 
              "and if it can get even closer by moving vertically. ",
              "If neither move is close to the player, the Minotaur skips the turn.",
              "This type of maze was first published in Robert Abbott's book",
              "Mad Mazes in 1990.The idea was later published",
              "in the British magazine Games & Puzzles."]

class TextMenu(Menu):
    def __init__(self, game, line_high =25, size =18):
        Menu.__init__(self, game)
        self.img = pygame.transform.scale(pygame.image.load('images/bg_menu.jpg').convert_alpha(), (800,600))
        self.line_high = line_high
        self.size = size

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.get_events_in_menu()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            blur_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
            blur_surface.fill((255, 255, 255, 30))
            self.game.display.blit(self.img, (0,0))
            self.game.display.blit(blur_surface, (0, 0))     
            y = 45
            for rendered_text in text_lines:
                y += self.line_high  # Cộng thêm độ cao của mỗi dòng
                self.game.draw_text(rendered_text , self.size, 400, self.game.DISPLAY_H / 12 + y)
            self.blit_screen(0,0)


