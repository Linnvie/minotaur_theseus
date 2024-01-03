import pygame
from pygame import mixer
from Grid_class import Grid
from Player_class import Player
from Minotaur_class import Minotaur
from Background_class import Background
from Menu_class import *
from solve import *
import sys, math
import atexit

FPS = 60

text_lines1 = ["The Minotaur, a half-man, half-bull monster, spread terror",
             "throughout Crete, so King Minos ordered Daedalus to make ",
              "a maze to trap it.Then King Minos of Crete won the war with",
              "the Athenians and required Athens to sacrifice seven young",
              "men and seven young women every nine years to the Minotaur.",
              "Understanding this dissatisfaction, Prince Theseus immediately ",
              "volunteered to be one of those who paid tribute. In the game,",
              "players will play the role of Theseus, trapped in the mythical",
              "Labyrinth, forced to fight the ferocious Minotaur by finding",
              "a way out of the maze before being eaten by the Minotaur. ", 
              "Theseus will defeat the Minotaur when he escapes all the",
              "mazes because he exhausts the Minotaur while chasing.",
              "This type of maze was first published in Robert Abbott's book",
              "Mad Mazes in 1990.The idea was later published",
              "in the British magazine Games & Puzzles."]

text_lines2 = [
             "Player must move Theseus to the exit before being captured",
              "by the Minotaur (player moves Theseus 1 step, Minotaur will",
              "move 2 following the law of the Minotaur always trying to get",
              "closer to Theseus. If the Minotaur could move a square horizontally",
              " and come closer to Theseus, the Minotaur will do it.",
              "If the Minotaur can't move horizontally, he'll move vertically.",
              "If there are no moves near the player, the Minotaur will skip the turn).",
              "",
              "Play with mouse: Right-click the corresponding Button on screen",
              "to move Theseus and use the same functions as pressing the key.",
              "",
              "Play with the keyboard: Use 4 up, down, left and right keys or",
              "WASD to move Theseus to any square, press spacebar to ",
              "skip turn, press Backspace key to return to the beginning of",
              "the game screen, press Shift key to undo repeat the previous",
              "step, press o to get help, press end to return to the menu.",
              
              ]

class Game():
    def __init__(self):
        pygame.init()
        mixer.init()

        self.account_id = 1
        
        self.window = pygame.display.set_mode(size = (700, 525))
        pygame.display.set_caption('Theseus and the Minotaur')
        self.playing, self.running =False, True
        self.game_end = False
        self.clock = pygame.time.Clock()
        
        self.current_volume = 0.5
        
        self.music_on = True
        mixer.music.load('musics/bg_music.mp3')
        self.win_sound = mixer.Sound('musics/win_sound.mp3')
        self.lose_sound = mixer.Sound('musics/lose_sound.mp3')
        self.move_sound = mixer.Sound('musics/move_sound.mp3')
        self.enter_sound = mixer.Sound('musics/enter_sound.mp3')
        self.open_sound = mixer.Sound('musics/open_door_sound.mp3')
        self.set_volume()
        
             
        # self.maze = Grid()
        # self.player_moves=[self.maze.G.graph["player_location"]]
        # self.load_assets()

        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY,self.MOUSE_CLICK = False, False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 700, 525
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.font_name = 'freesansbold.ttf'
        
        self.main_menu = MainMenu(self)
        
        self.options = OptionsMenu(self)
        self.tutorial = TextMenu(self, text_lines= text_lines2)
        self.mythology = TextMenu(self, text_lines= text_lines1)
        self.help_menu = TextMenu(self, size =25, line_high =30)
        self.error_menu = TextMenu(self,line_high =60, size =40, x_pos=400, y_post=120, text_lines=["Server error!", " Please check ","your network connection!"])
        self.win_menu = EndMenu(self,"Well done!", "You escaped", "the Minotaur!","Next")
        self.lose_menu = EndMenu(self, "Oh no...", "The Minotaur", "got you!", "Undo")
        self.curr_menu = self.main_menu
        self.level_menu = LevelMenu(self)

        self.new_data = []
        # Đăng ký hàm save_data để chạy khi chương trình kết thúc
        atexit.register(self.save_and_update_data)

    def save_and_update_data(self):
        # gọi API để lưu dữ liệu
        print("Saving data...")
        if len(self.new_data)>0:
            print("Saving data olala")
            url = 'http://localhost:8080/api/v1/save-update-level'

            print("dataaaa", self.new_data)

            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=self.new_data, headers=headers)

            if response.status_code == 200:
                print("Request successful")
                # print(response.json())
            else:
                print("Request failed with status code:", response.status_code)
                print(response.text)  

    def set_volume(self):
        pygame.mixer.music.set_volume(self.current_volume)
        self.win_sound.set_volume(self.current_volume)
        self.move_sound.set_volume(self.current_volume)
        self.enter_sound.set_volume(self.current_volume)
        self.open_sound.set_volume(self.current_volume)

    def get_events_in_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                self.curr_menu.run_display = False
            
            # print("kiểm tra")
            if event.type == pygame.KEYDOWN and not self.game_end:
                if event.key == pygame.K_END:
                    self.back_level_page()

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.player_move("up")

                if event.key == pygame.K_w or event.key == pygame.K_DOWN:
                    self.player_move("down")
                
                if event.key == pygame.K_w or event.key == pygame.K_LEFT:
                    self.player_move("left")
                
                if event.key == pygame.K_w or event.key == pygame.K_RIGHT:
                    self.player_move("right")
        
                if event.key == pygame.K_SPACE:
                    self.player_move("skip")

                if event.key == pygame.K_BACKSPACE:
                    # Reset board
                    self.restart()

                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.undo()

                if event.key == pygame.K_o:
				
                    self.maze.G.graph["player_location"] = self.player_moves[0]
                    self.maze.G.graph["mino_location"] = self.mino.mino_moves[0]
			
                    solve(self.maze)
				
                if event.key == pygame.K_p:	
                    self.maze.G.graph["player_location"] = self.player_moves[0]
                    self.maze.G.graph["mino_location"] = self.mino.mino_moves[0]
				
                    print("sol2",solve2(self.maze))

                if event.key == pygame.K_m:
                    self.show_hint()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.music_on:
                    self.enter_sound.play() 

                if self.button_up.check_click():
                    self.player_move("up")

                if self.button_down.check_click():
                    self.player_move("down")

                if self.button_left.check_click():
                    self.player_move("left")

                if self.button_right.check_click():
                    self.player_move("right")

                if self.button_skip.check_click():
                    self.player_move("skip")

                if self.button_undo.check_click():
                    self.undo()

                if self.button_restart.check_click():
                    self.restart()

                if self.button_help.check_click():
                    self.show_hint()

                if self.button_back.check_click():
                    self.back_level_page()

                    
        # print("move",self.player_moves, self.mino.mino_moves, self.maze.G.graph["player_location"], self.maze.G.graph["mino_location"])
    
    def show_hint(self):
        self.maze.G.graph["player_location"] = self.player_moves[0]
        self.maze.G.graph["mino_location"] = self.mino.mino_moves[0]
        
        is_solve, solves =  solve3(self.maze)
        solves_half = solves[:(len(solves)//2)]
        solves =  [" -> ".join(str(x) for x in solves_half[i:i+5]) for i in range(0, len(solves_half), 5)]
        
        self.help_menu.text_lines = solves
        self.curr_menu = self.help_menu
        self.playing=False

    def restart(self):
        # print("restart")
        if self.game_win:
            self.current_level = self.current_level-1
        self.player.total_moves = 0
        self.mino.movings = []
        self.maze.G.graph["player_location"] = self.player_moves[0]
        self.maze.G.graph["mino_location"] = self.mino.mino_moves[0]
        self.player.location = self.player_moves[0]
        self.mino.location = self.mino.mino_moves[0]
        self.player_moves = [self.player.location]
        self.mino.mino_moves = [self.mino.location]

    def undo(self):
        # self.current_level = self.current_level-1
        if len(self.player_moves)>1:
            self.maze.G.graph["player_location"] = self.player_moves[-2]
            self.maze.G.graph["mino_location"] = self.mino.mino_moves[-3]
            self.player.location = self.maze.G.graph["player_location"]
            self.mino.location = self.maze.G.graph["mino_location"]
            # self.mino.movings = []
            self.player.total_moves+=1
            self.player_moves.pop()
            self.mino.mino_moves.pop()
            self.mino.mino_moves.pop()

    def player_move(self, direction):
        try: 
            self.player_moves.append(self.player.move(direction))
        except ValueError: 
            print("LỖI", ValueError)
            pass

    def back_level_page(self):
        self.playing = False
        self.level_menu.state = self.current_level
        a = (self.level_menu.current_page-1)*self.level_menu.per_page
        # di chuyển cursor trong level menu
        self.level_menu.cursor_rect.midtop = (self.level_menu.button_location[self.current_level-a][0] -15+ self.level_menu.offset, self.level_menu.button_location[self.current_level-a][1])
        self.curr_menu = self.level_menu

    def get_events_in_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.music_on:
                        self.enter_sound.play() 
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                   
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    if self.music_on:
                        self.move_sound.play()
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    if self.music_on:
                        self.move_sound.play()
                    self.UP_KEY = True
                if event.key == pygame.K_RIGHT:
                    if self.music_on:
                        self.move_sound.play()
                    self.RIGHT_KEY = True
                if event.key == pygame.K_LEFT:
                    if self.music_on:
                        self.move_sound.play()
                    self.LEFT_KEY = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.music_on:
                    self.enter_sound.play()
                self.MOUSE_CLICK = True  
   
    def update(self):
        if self.maze.G.graph["player_location"] in self.maze.goal_neighbors:
            self.bg.attack_animation = True
            if self.music_on:
                if self.bg.current_door ==1:
                    self.open_sound.play()

        game_end, self.game_win = self.check_game_end()
        if game_end and self.game_win:
            if self.music_on:
                self.win_sound.play()
            print("WIN")
            
            # kiểm tra nếu chưa có api của vòng đó thì gọi
            if self.current_level%6==0 and self.level_menu.current_page<self.level_menu.total_pages:
                self.level_menu.current_page +=1
                self.level_menu.cal_num_of_element()
                if (self.level_menu.current_page not in self.level_menu.page_visited):
                    self.level_menu.handle_response(self.level_menu.call_api())
            if self.list_level_infor[self.current_level-1]['moves'] == 0 or self.list_level_infor[self.current_level-1]['moves'] > self.player.total_moves:
                self.list_level_infor[self.current_level-1]['moves']=self.player.total_moves

                # call api sửa accountlevel
                item = {"accountId":self.account_id,
                        "levelId":self.list_level_infor[self.current_level-1]["id"],
                        "moves":self.player.total_moves}
                for i in self.new_data:
                    if i["levelId"] == item["levelId"]:
                        # Nếu tìm thấy, chỉnh sửa giá trị moves
                        i["moves"] = item["moves"]
                        break
                else:
                # Nếu không tìm thấy, thêm new_item vào self.new_data
                    self.new_data.append(item)



            if self.current_level==self.level_menu.total_elements:
                self.current_level = self.current_level+1

            if self.current_level<self.level_menu.total_elements :
                if self.list_level_infor[self.current_level]['moves'] == None:
                    self.list_level_infor[self.current_level]['moves']=0
                    # call api thêm accountlevel
                    self.new_data.append({"accountId":self.account_id,
                                        "levelId":self.list_level_infor[self.current_level]["id"],
                                        "moves":0})


                self.current_level = self.current_level+1
                self.level_menu.state = self.current_level
                a = (self.level_menu.current_page-1)*self.level_menu.per_page
                # di chuyển cursor trong level menu
                self.level_menu.cursor_rect.midtop = (self.level_menu.button_location[self.current_level-a][0] -15+ self.level_menu.offset, self.level_menu.button_location[self.current_level-a][1])
                

            self.playing = False
            # self.reset_keys()
            pygame.event.set_allowed(pygame.KEYDOWN)
            pygame.event.set_allowed(pygame.KEYUP)
            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
            self.curr_menu = self.win_menu
        
        elif game_end and not self.game_win:
            print("Lose")
            if self.music_on:
                self.lose_sound.play()
            self.playing = False
            # self.reset_keys()
            pygame.event.set_allowed(pygame.KEYDOWN)
            pygame.event.set_allowed(pygame.KEYUP)
            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
            self.curr_menu = self.lose_menu
                     
    def load_assets(self):
        w, h = game.maze.size_window
        
        self.mino = Minotaur(self.maze)
        self.bg = Background(self.maze)

        self.button_back = Button(self.window,"<--", 60, 25, 30, 20, True)
        self.button_undo = Button(self.window,"Undo", w/2+180, h-30, 65, 25, True)
        self.button_restart = Button(self.window,"Restart", w/2+180, h-70, 65, 25, True)
        self.button_up = Button(self.window,"Up", w/2-105, h-72, 60, 30, True)
        self.button_down = Button(self.window,"Down", w/2-105, h-25, 60, 30, True)
        self.button_left = Button(self.window,"Left", w/2-80-105, h-54, 60, 30, True)
        self.button_right = Button(self.window,"Right", w/2+80-105, h-54, 60, 30, True)
        self.button_skip = Button(self.window,"Skip", w/2+60, h-54, 60, 30, True)
        self.button_help = Button(self.window,"Help", w-75, 25, 60, 25, True)
        
        self.font = pygame.font.Font(
            # '8-BIT WONDER.TTF'
            'freesansbold.ttf'
            , 20)
        self.player = Player(self.maze, mino=self.mino)

    def render(self):
        self.bg.draw(self.window)
        self.player.draw(self.window)
        self.mino.draw(self.window)
        self.button_back.draw(15)
        self.button_down.draw(15)
        self.button_up.draw(15)
        self.button_left.draw(15)
        self.button_right.draw(15)
        self.button_restart.draw(15)
        self.button_skip.draw(15)
        self.button_undo.draw(15)
        self.button_help.draw(15)
        self.bg.update(1)
        self.mino.update(0.5)
        self.player.update(1)
        text = self.font.render("Level: "+ str(self.current_level), True, (0,0,0))
        self.window.blit(text, (100, 15))
        move = self.font.render("Moves: "+ str(self.player.total_moves), True, (0,0,0))
        self.window.blit(move, (230, 15))

    def draw_text(self, text, size, x, y, color = (0,0,0) ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True,color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
  
    def run(self):
        while self.playing:    
            self.get_events_in_game()
            self.render()
            self.update()
            pygame.time.delay(50)
            self.clock.tick(60)
            pygame.display.update()

    def check_game_end(self):
        if len(self.mino.movings)==0:
            if self.maze.G.graph["mino_location"] == self.maze.G.graph["player_location"]:
                return True, False
            elif self.maze.G.graph["player_location"] == self.maze.G.graph["goal"] and self.maze.G.graph["mino_location"] != self.maze.G.graph["player_location"]:
                return True, True
        
        return False, False

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY, self.MOUSE_CLICK = False, False, False, False, False, False, False
    
if __name__ == "__main__":
    game = Game()
    while game.running:
        if game.playing:
            if game.music_on:
                mixer.music.play(-1)
            game.get_events_in_game()
            game.window = pygame.display.set_mode(size = game.maze.size_window)
            game.run()
        else:
            mixer.music.stop()
            # game.get_events_in_menu()
            game.curr_menu.display_menu()
        # game.reset_keys()
