import pygame
from pygame import mixer
import requests
import ast
from Button_class import Button
from Grid_class import Grid

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

class LevelMenu(Menu):
    def __init__(self, game, w = 800, h = 600):
        Menu.__init__(self, game)
        self.state = 1

        self.page_visited = []
        self.button_state = [0]

        self.current_page = 1
        self.game.list_level_infor = []
        

        self.w = w
        self.h = h
        self.button_location = [(0,0)]
        
        self.cursor_rect.midtop = (self.w/3 -15 + self.offset, self.h/4 +120)      
        self.img = pygame.transform.scale(pygame.image.load('images/bg_menu.jpg').convert_alpha(), (self.w, self.h))

    def call_first_api(self):
        s = self.h/4 +120
        w = self.w/2
        data = self.call_api()
        # self.per_page = data["perPage"]
        if data:
            self.per_page = data["perPage"]
            self.total_pages = data["totalPages"]
            self.number_of_elements = data["numberOfElements"]
            self.handle_response(data)
            
            self.total_elements = data["totalElements"]
            for i in range(1,self.per_page+1):        
                if(i%2 == 0):
                    self.button_location.append((self.w/3*2, s))
                    s=s+80
                else:
                    self.button_location.append((self.w/3, s))    

    def cal_num_of_element(self):
        if self.current_page == self.total_pages:
            self.number_of_elements = self.total_elements%self.per_page
        else:
            self.number_of_elements = self.per_page

    def call_api(self):
        print("call api")
        url = 'http://localhost:8080/api/v1/level/'+str(self.game.account_id)+'?perPage=6&currentPage='+ str(self.current_page)
        data = []
        try:
            response = requests.get(url)
            response.raise_for_status()  # Kiểm tra lỗi HTTP

            # Kiểm tra xem có dữ liệu không
            if response.status_code == 200:
        #     # Truy cập dữ liệu trong response
                data = response.json()
                self.page_visited.append(data["currentPage"])
                print(data)
            else:
                self.game.curr_menu = self.game.error_menu
                self.run_display = False
                print("Không có dữ liệu được trả về từ API")

        except requests.exceptions.RequestException as e:
            # Xử lý lỗi nếu có
            self.game.curr_menu = self.game.error_menu
            self.run_display = False
            print(f"Đã xảy ra lỗi khi gọi API: {e}")

        except Exception as e:
            self.game.curr_menu = self.game.error_menu
            self.run_display = False
            # Xử lý các lỗi khác
            print(f"Đã xảy ra lỗi không xác định: {e}")

        print("Tiếp tục thực hiện chương trình...")
        return data
        
    def handle_response(self, data):
        for item in data["listLevel"]:
            item['sizeBoard'] = ast.literal_eval(item['sizeBoard'])
            item['minoStart'] = ast.literal_eval(item['minoStart'])
            item['playerStart'] = ast.literal_eval(item['playerStart'])
            item['goal'] = ast.literal_eval(item['goal'])
            walls_list = ast.literal_eval(item['walls'])
            item['walls'] = walls_list
            self.button_state.append(int(item['levelName']))
        
        # self.number_of_elements = data["numberOfElements"]
        self.game.list_level_infor.extend(data["listLevel"])

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

            self.button_back = Button(self.game.display,"<--", 75, 80, 40, 29, True)
            self.button_back.draw(25)
            self.button_pre = Button(self.game.display,"<", 75, self.h/4 +200, 40, 25, False)
            self.button_next = Button(self.game.display,">", 730, self.h/4 +200, 40, 25, False)

            if self.current_page != 1:
                self.button_pre.enabled = True
                self.button_pre.draw(25)
            if self.current_page != self.total_pages:
                
                self.button_next.enabled = True
                self.button_next.draw(25)
            
            for i in range(1, self.number_of_elements+1): 
                index = (self.current_page-1) * self.per_page+ i   
                # print("index1", index)   
                # moves = "0" 
                # Vòng chơi không bị khóa
                if self.game.list_level_infor[index-1]['moves'] != None:
                    moves = str(self.game.list_level_infor[index-1]['moves'])
                    if(i%2 != 0):
                        button = Button(self.game.display,"Level "+str(self.game.list_level_infor[index-1]['levelName']) + " ("+ moves+ "/"+ str(self.game.list_level_infor[index-1]['minMoves'])+")", self.w/3, s, 220, 50, True, self.game.list_level_infor[index-1]['levelName'])
                        # button.draw(28)
                    else:
                        # print("list_level_infor", index, self.list_level_infor)
                        button = Button(self.game.display, "Level "+str(self.game.list_level_infor[index-1]['levelName'])+ " ("+ moves+ "/"+ str(self.game.list_level_infor[index-1]['minMoves'])+")", self.w/3*2, s, 220, 50, True, self.game.list_level_infor[index-1]['levelName'])
                        # button.draw(28)
                        s=s+80    
                else:
                    if(i%2 != 0):
                        button = Button(self.game.display, "", self.w/3, s, 200, 50, False)
                        # button.draw(28)
                    else:
                        button = Button(self.game.display, "", self.w/3*2, s, 200, 50, False)
                
                button.draw(26)  

                
                if self.game.MOUSE_CLICK: 
                    self.state = button.state
                    
                    if button.check_click():  
                        if self.state in self.button_state:      
                            if self.game.list_level_infor[self.state-1]['moves'] == None:
                                return 
                        
                            self.game.current_level = self.state
                            self.game.maze = Grid(maze_infor=self.game.list_level_infor[self.state-1])
                            self.game.player_moves=[self.game.maze.G.graph["player_location"]]
                            self.game.load_assets()
                            
                            self.game.playing = True
                        # call api
                        self.run_display = False
                        
                               
            self.draw_cursor()
            self.blit_screen(0,0)

    def move_cursor(self):
        # print("gnhlkadmnjbhsw", self.state)
        a = (self.current_page-1)*self.per_page

        if self.game.DOWN_KEY:
             
            if self.per_page ==1 :
                return
            # print("state", self.state)       
            if self.state % self.per_page == 0 or self.state % self.per_page == self.number_of_elements or self.game.list_level_infor[self.state]['moves'] == None:
                self.cursor_rect.midtop = (self.button_location[1][0]-15 + self.offset, self.button_location[1][1])
                # print("vào trên",self.state)
                # self.state = self.button_state[self.state - (self.number_of_elements-1)]
                # self.state = self.state - (self.number_of_elements-1)
                self.state = a+1
                
            else:
                if self.state in self.button_state:
                    # print("vào dưới",self.state)
                    self.state = self.button_state[self.state+1]
                    location = self.state - a
                    self.cursor_rect.midtop = (self.button_location[location][0] -15+ self.offset, self.button_location[location][1])
                    # self.state = self.button_state[self.state + 1]
                    
            # print("current state1", self.state, self.button_location, self.button_state)

        elif self.game.UP_KEY:

            if self.per_page ==1 or self.state % self.per_page==1:
                return

            # Phần tử đầu trang sẽ là 1 tức nếu chia hết  cho 6 sẽ là phần tử cuối cùng 1 trang full
            # if self.state % self.per_page==1  :
            #     # if self.game.list_level_infor[self.state]['moves'] == None:
            #     #     self.state = (self.current_page-1)*self.per_page+1
               
            #     # else:
            #     self.state = self.button_state[self.state + (self.number_of_elements-1)]
            #     self.cursor_rect.midtop = (self.button_location[self.number_of_elements][0] -5 + self.offset, self.button_location[self.number_of_elements][1])
                
            # else:
            if self.state in self.button_state:
                self.state = self.button_state[self.state-1]
                location = self.state - a
                self.cursor_rect.midtop = (self.button_location[location][0] -15+ self.offset, self.button_location[location][1])
                   

        elif self.game.RIGHT_KEY:
            # if self.game.list_level_infor[self.state]['moves'] == None:
            #     print("dô đây nè")
            #     self.cursor_visible = False
            # else:
            #     self.cursor_visible = True
            
            if self.current_page < self.total_pages :
                             
                self.state =  self.current_page*self.per_page+1
                self.current_page +=1
                self.cal_num_of_element()
                # call api
                if (self.current_page not in self.page_visited):
                    self.handle_response(self.call_api())
                # if(self.current_page*self.per_page>self.total_pages):
                #     self.list_level_infor.extend(newList)
            # else:
            #     pass
                # self.current_page = 1
                # self.cal_num_of_element()
                # self.state = 1
                if self.game.list_level_infor[self.state]['moves'] == None:
                    self.cursor_visible = False
                else:
                    self.cursor_visible = True
            self.cursor_rect.midtop = (self.button_location[1][0] -15+ self.offset, self.button_location[1][1])

        elif self.game.LEFT_KEY:
            
            if self.current_page > 1 :
                self.current_page -=1
                self.cal_num_of_element()
                self.state =  (self.current_page-1)*self.per_page+1    
                # self.state-=1
                if (self.current_page not in self.page_visited):
                    self.handle_response(self.call_api())
            # else:
            #     pass
                # self.current_page = self.total_pages
                # self.cal_num_of_element()
                # self.state = self.total_elements
                if self.game.list_level_infor[self.state]['moves'] == None:
                    self.cursor_visible = False
                else:
                    self.cursor_visible = True
            self.cursor_rect.midtop = (self.button_location[1][0] -15+ self.offset, self.button_location[1][1])
    
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state in self.button_state:      
                if self.game.list_level_infor[self.state-1]['moves'] == None:
                    return 
               
                self.game.current_level = self.state
                self.game.maze = Grid(maze_infor=self.game.list_level_infor[self.state-1])
                self.game.player_moves=[self.game.maze.G.graph["player_location"]]
                self.game.load_assets()
                
                self.game.playing = True
            # call api
            self.run_display = False
                
        elif self.game.BACK_KEY :
            
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

        elif self.game.MOUSE_CLICK:
            if self.button_back.check_click():
                    self.game.curr_menu = self.game.main_menu
                    self.run_display = False

            if self.button_pre.check_click():
                if self.current_page > 1 :
                    self.current_page -=1
                    self.cal_num_of_element()
                    self.state =  (self.current_page-1)*self.per_page+1    
                    
                    if (self.current_page not in self.page_visited):
                        self.handle_response(self.call_api())
                
                    if self.game.list_level_infor[self.state]['moves'] == None:
                        self.cursor_visible = False
                    else:
                        self.cursor_visible = True
                        
                self.cursor_rect.midtop = (self.button_location[1][0] -15+ self.offset, self.button_location[1][1])

            if self.button_next.check_click():
                if self.current_page < self.total_pages :
                    self.state =  self.current_page*self.per_page+1
                    self.current_page +=1
                    self.cal_num_of_element()
                    # call api
                    if (self.current_page not in self.page_visited):
                        self.handle_response(self.call_api())
                    
                    if self.game.list_level_infor[self.state]['moves'] == None:
                        self.cursor_visible = False
                    else:
                        self.cursor_visible = True
                self.cursor_rect.midtop = (self.button_location[1][0] -15+ self.offset, self.button_location[1][1])

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

            self.button1 = Button(self.game.display,'Start Game', self.w/2, self.h/4 +120, 190, 50, True)
            self.button1.draw(30)

            self.button2 = Button(self.game.display,'Tutorial ', self.w/3, self.h/3 + 160, 190, 50, True)
            self.button2.draw(30)

            self.button3 = Button(self.game.display,'Mythology', self.w/3*2, self.h/3 +160 , 190, 50, True)
            self.button3.draw(30)

            self.button4 = Button(self.game.display,'Option', self.w/3, self.h/3*2 +60, 190, 50, True)
            self.button4.draw(30)

            self.button5 = Button(self.game.display,'Exit', self.w/3*2, self.h/3*2 +60, 190, 50, True)
            self.button5.draw(30)

            if(self.button1.check_hover() or self.button2.check_hover() or self.button3.check_hover() or self.button4.check_hover() or self.button5.check_hover()):
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
                self.state = 'Options'
            elif self.state == 'Options':
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
                self.state = 'Options'
            elif self.state == 'Options':
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
            # self.game.enter_sound.play()
            if self.state == 'Start':
                # self.game.playing = True
                self.game.curr_menu = self.game.level_menu
                if self.game.level_menu.page_visited==[]:
                    self.game.level_menu.call_first_api()            
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Tutorial':
                self.game.curr_menu = self.game.tutorial
            elif self.state == 'Mythology':
                self.game.curr_menu = self.game.mythology
                self.cursor_rect.midtop = (self.mythologyx + self.offset, self.mythologyy)
            elif self.state == 'Exit':
                self.game.playing = False
                self.game.running = False
                self.game.curr_menu.run_display = False
            self.run_display = False

        if self.game.MOUSE_CLICK:   
            if self.button1.check_click():
                
                self.state == 'Start'
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.game.curr_menu = self.game.level_menu
                if self.game.level_menu.page_visited==[]:
                    self.game.level_menu.call_first_api()
            if self.button2.check_click():

                self.state = "Tutorial"
                self.game.curr_menu = self.game.tutorial
                self.cursor_rect.midtop = (self.tutorialx + self.offset, self.tutorialy)
           
            if self.button3.check_click():

                self.state = "Mythology"
                self.cursor_rect.midtop = (self.mythologyx + self.offset, self.mythologyy)
                self.game.curr_menu = self.game.mythology
            if self.button4.check_click():

                self.state = "Options"
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.game.curr_menu = self.game.options
            if self.button5.check_click():
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
        scale_x= round(current_w/self.w, 2)
        scale_y1= round(current_h/self.h, 2)
        scale_y2= round(current_h/(self.h+25), 2)
        scale_y3= round(current_h/(self.h+50), 2)
        # print(scale_y)

        self.firstx, self.firsty = self.w/2 + 15, self.h / 2
        self.restartx, self.restarty = self.w/2 + 15, self.h/2+ 45
        self.mainx, self.mainy = self.w/2 + 15, self.h/2 + 95
        self.cursor_rect.midtop = (self.firstx + self.offset, self.firsty)

        while self.run_display:
                
            self.game.get_events_in_menu()
            self.check_input()
            self.game.display.blit(self.img, (0,0))

            self.game.draw_text(self.text1, 30, self.w/2, self.h/6 - 20)
            self.game.draw_text(self.text2, 22, self.w/2 , self.h/3 +5 )
            self.game.draw_text(self.text3, 22, self.w/2, self.h/3 + 35 )


            self.button1 = Button(self.game.display,self.first_choose, self.w/2, self.h/2, 160, 30, True)
            self.button1.draw(20)
            

            self.button2 = Button(self.game.display,'Restart Level', self.w/2, self.h/2 + 50, 160, 30, True)
            self.button2.draw(20)

            self.button3 = Button(self.game.display,'Back to menu', self.w/2, self.h/2 + 100, 160, 30, True)
            self.button3.draw(20)

            if(self.button1.check_hover(scale_x, scale_y1) or self.button2.check_hover(scale_x, scale_y2) or self.button3.check_hover(scale_x, scale_y3)):
                self.cursor_visible = False
            else:
                self.cursor_visible = True
     
            if self.game.MOUSE_CLICK: 
                self.game.win_sound.stop()
                self.game.lose_sound.stop()
                if self.button1.check_click(scale_x, scale_y1):
                    if self.game.game_win:
                        if self.game.current_level <= self.game.level_menu.total_elements:
                            self.game.maze = Grid(maze_infor=self.game.list_level_infor[self.game.current_level-1])
                            self.game.player_moves=[self.game.maze.G.graph["player_location"]]
                            self.game.load_assets()
                            self.game.playing = True
                        else:
                            self.game.current_level = self.game.current_level-1
                            self.game.curr_menu = self.game.level_menu
                    else:
                        self.game.undo()
                        self.game.playing = True
                if self.button2.check_click(scale_x, scale_y2):
                    self.game.restart()
                    self.game.playing = True
                if self.button3.check_click(scale_x, scale_y3):
                    self.game.curr_menu = self.game.level_menu
                self.run_display = False
        
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
            self.game.win_sound.stop()
            self.game.lose_sound.stop()
            
            if self.state == 'Main':
                self.game.curr_menu = self.game.level_menu

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
                # if self.game.list_level_infor[self.game.current_level]['moves'] == None:
                #     self.game.list_level_infor[self.game.current_level]['moves']=0
                #     # call api thêm accountlevel
                #     if self.game.list_level_infor[self.game.current_level-1]['moves'] == 0 or self.game.list_level_infor[self.game.current_level-1]['moves'] > self.game.player.total_moves:
                #         self.game.list_level_infor[self.game.current_level-1]['moves']=self.game.player.total_moves
                        # call api update accountlevel
                # self.game.current_level = self.game.current_level+1
                if self.game.current_level <= self.game.level_menu.total_elements:
                    self.game.maze = Grid(maze_infor=self.game.list_level_infor[self.game.current_level-1])
                    self.game.player_moves=[self.game.maze.G.graph["player_location"]]
                    self.game.load_assets()
                    self.game.playing = True
                else:
                    self.game.current_level = self.game.current_level-1
                    self.game.curr_menu = self.game.level_menu

            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game, w = 800, h = 600):
        Menu.__init__(self, game)
        self.state = "Music"
        self.w = w
        self.h = h
        self.musicx, self.musicy = self.w/2 - 50, self.h/4 +120
        self.volumex, self.volumey = self.w/2 -50, self.h/3 + 180
        # self.mythologyx, self.mythologyy = self.w/3*2, self.h/3 +160
        # self.optionsx, self.optionsy = self.w/3, self.h/3*2 +60   
        self.exitx, self.exity = self.w/3*2, self.h/3*2 +60
        self.cursor_rect.midtop = (self.musicx + self.offset, self.musicy)
        self.text_button1 = 'Music       On'
        self.text_button2 = 'Volume      '+str(round(self.game.current_volume*100))
        
        self.img = pygame.transform.scale(pygame.image.load('images/bg_menu.jpg').convert_alpha(), (self.w, self.h))

    def display_menu(self):
        self.run_display = True
        self.game.window = pygame.display.set_mode(size = (self.w, self.h))
        self.game.display = pygame.Surface((self.w, self.h))
        while self.run_display:
            self.game.get_events_in_menu()
            self.check_input()
            # blur_surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            # blur_surface.fill((255, 255, 255, 30))
            self.game.display.blit(self.img, (0,0))
            # self.game.display.blit(blur_surface, (0, 0))
            self.game.draw_text("Options", 40, self.w/2, self.h/5 +40 )

            self.button1 = Button(self.game.display,self.text_button1, self.w/2, self.h/4 +120, 280, 60, True)
            self.button2 = Button(self.game.display,self.text_button2, self.w/2, self.h/3 + 180, 280, 60, True)

            self.button3 = Button(self.game.display,"-", self.w/2+37, self.h/3 + 180, 20, 20, True)
            self.button4 = Button(self.game.display,"+", self.w/2+120, self.h/3 + 180, 20, 20, True)

            self.button5 = Button(self.game.display,"<--", 75, 80, 40, 29, True)
            
            self.button1.draw(30)
            self.button2.draw(30)

            self.button3.draw(20)
            self.button4.draw(19)
            self.button5.draw(25)

            if(self.button1.check_hover() or self.button2.check_hover()):
                self.cursor_visible = False
            else:
                self.cursor_visible = True  
            self.draw_cursor()
            self.blit_screen(0,0)
    
    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            if self.state == 'Music':
                self.cursor_rect.midtop = (self.volumex + self.offset, self.volumey)
                self.state = 'Volume'
            elif self.state == 'Volume':
                self.cursor_rect.midtop = (self.musicx + self.offset, self.musicy)
                self.state = 'Music'
        # elif self.game.UP_KEY:
        #     self.game.move_sound.play()
        #     if self.state == 'Start':
        #         self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
        #         self.state = 'Exit'
        #     elif self.state == 'Exit':
        #         self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
        #         self.state = 'Options'
            
    def check_input(self):
        # print(self.game.current_volume)
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Music':
                self.text_button1 = "Music       Off" if self.text_button1.find("On")!= -1 else "Music       On"
                self.game.music_on = not self.game.music_on
                # pass          
        
        elif self.game.LEFT_KEY and self.game.current_volume>=0.05 and self.state == 'Volume':
            self.game.current_volume = round(self.game.current_volume - 0.05, 2)
            self.game.set_volume()
            self.text_button2 = 'Volume      '+str(round(self.game.current_volume*100))

        elif self.game.RIGHT_KEY and self.state == 'Volume' and self.game.current_volume<=0.95:
            self.game.current_volume = round(self.game.current_volume + 0.05, 2)
            self.game.set_volume()
            self.text_button2 = 'Volume      '+str(round(self.game.current_volume*100))
            self.run_display = False

        elif self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        
        if self.game.MOUSE_CLICK:   
            if self.button1.check_click() :
                self.state == 'Music'
                self.text_button1 = "Music       Off" if self.text_button1.find("On")!= -1 else "Music       On"
                self.game.music_on = not self.game.music_on
                
            if self.button3.check_click() and self.game.current_volume>=0.05 :
                self.state = "Volume"
                self.cursor_rect.midtop = (self.volumex + self.offset, self.volumey)
                self.game.current_volume = round(self.game.current_volume - 0.05, 2)
                self.game.set_volume()
                self.text_button2 = 'Volume      '+str(round(self.game.current_volume*100))

            if self.button4.check_click() and self.game.current_volume<=0.95:
                self.state = "Volume"
                self.cursor_rect.midtop = (self.volumex + self.offset, self.volumey)
                self.game.current_volume = round(self.game.current_volume + 0.05, 2)
                self.game.set_volume()
                self.text_button2 = 'Volume      '+str(round(self.game.current_volume*100))

            if self.button5.check_click() :
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

# text_lines = ["Theseus and the Minotaur is a type of logic maze",
#              "designed by Robert Abbott. In this maze, the player acts as",
#               "King Theseus of Athens trying to escape from the labyrinth.",
#               "The main difference between this labyrinth and the standard",
#               "type of labyrinth, beyond the fact that it is set on a grid,",
#               "is the fact that the maze is not empty, there is a minotaur ",
#               "hunting the player down , and it takes two steps per maze.",
#               "The Minotaur is faster than the player, but his movements ",
#               "are predictable and often inefficient. The Minotaur is determined",
#               "by moving horizontally to see if it can get closer to the player,", 
#               "and if it can get even closer by moving vertically. ",
#               "If neither move is close to the player, the Minotaur skips the turn.",
#               "This type of maze was first published in Robert Abbott's book",
#               "Mad Mazes in 1990.The idea was later published",
#               "in the British magazine Games & Puzzles."]

class TextMenu(Menu):
    def __init__(self, game, line_high =25, size =18, x_pos=400, y_post=None, text_lines=[]):
        Menu.__init__(self, game)
        self.img = pygame.transform.scale(pygame.image.load('images/bg_menu.jpg').convert_alpha(), (800,600))
        self.line_high = line_high
        self.size = size
        self.x_pos = x_pos
        self.y_post = self.game.DISPLAY_H / 12 if y_post == None else y_post
        self.text_lines = text_lines

    def update(self, line_high =25, size =18, x_pos=400, y_post=None, text_lines=[]):
        self.line_high = line_high
        self.size = size
        self.x_pos = x_pos
        self.y_post = self.game.DISPLAY_H / 12 if y_post == None else y_post
        self.text_lines = text_lines
       

    def display_menu(self):
        self.game.window = pygame.display.set_mode(size = (800,600))
        self.run_display = True

        while self.run_display:
            self.game.get_events_in_menu()
            button1 = Button(self.game.display,"<--", 75, 80, 40, 29, True)
            
            if  self.game.BACK_KEY or (self.game.MOUSE_CLICK and button1.check_click()):
                self.run_display = False
                if self.game.curr_menu != self.game.help_menu:
                    self.game.curr_menu = self.game.main_menu
                else:
                    self.game.playing = True

            
            blur_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
            blur_surface.fill((255, 255, 255, 30))
            self.game.display.blit(self.img, (0,0))
            self.game.display.blit(blur_surface, (0, 0))    
            button1.draw(25) 
            y = 45
            for rendered_text in self.text_lines:
                y += self.line_high  # Cộng thêm độ cao của mỗi dòng
                self.game.draw_text(rendered_text , self.size, self.x_pos, self.y_post + y)
            self.blit_screen(0,0)


