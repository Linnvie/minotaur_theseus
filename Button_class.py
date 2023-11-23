import pygame
class Button:
    def __init__(self, window, text, x, y, width, height, enabled, state=None):
        self.window = window
        self.text = text
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.enabled = enabled
        self.state = state
        self.block  = pygame.transform.scale(pygame.image.load('images/block.png').convert_alpha(), (self.height , self.height-10))
    
    def change_text(self, new_text):
        self.text = new_text
        
    def draw(self, font_size):
        font = pygame.font.Font('freesansbold.ttf', font_size)
        button_text = font.render(self.text, True, 'black')
        button_rect = pygame.rect.Rect((self.x_pos-self.width//2, self.y_pos-self.height//2), (self.width, self.height))

        if self.enabled:
            # if self.check_hover():
            #     pygame.draw.rect(self.window, 'blue', button_rect, 0, 5)
            # else:
            #     pygame.draw.rect(self.window, 'light gray', button_rect, 0, 5)
         
            if self.check_click():
                pygame.draw.rect(self.window, 'gray', button_rect, 0, 5)
            else:
                pygame.draw.rect(self.window, 'light gray', button_rect, 0, 5)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.window.blit(button_text, text_rect)

        else:
            pygame.draw.rect(self.window, 'gray', button_rect, 0, 5)
            self.window.blit(self.block, (self.x_pos - 22, self.y_pos -21))

        pygame.draw.rect(self.window, 'black', button_rect, 2, 5)
        # self.window.blit(button_text, (self.x_pos-self.width//2+padding, self.y_pos-self.height//2+padding))

        # text_rect = button_text.get_rect(center=button_rect.center)  # Đặt văn bản vào giữa hình chữ nhật

        # Hiển thị văn bản
        
    def check_click(self, scale_x=1, scale_y=1):
        mouse_pos = pygame.mouse.get_pos()
        # print(mouse_pos)
        left_click = pygame.mouse.get_pressed()[0]
        
        button_rect = pygame.rect.Rect((self.x_pos* scale_x-self.width//2, self.y_pos*scale_y-self.height//2), (self.width, self.height))
        if left_click and button_rect.collidepoint(mouse_pos) and self.enabled:
            
            return True
        else:
            return False

    # scale lấy màn hình lớn hơn chia màn hình bé hơn
    def check_hover(self, scale_x=1, scale_y=1):
        mouse_pos = pygame.mouse.get_pos()
        # print(mouse_pos)
        button_rect = pygame.rect.Rect((self.x_pos* scale_x-self.width//2, self.y_pos*scale_y-self.height//2), (self.width, self.height))
        if button_rect.collidepoint(mouse_pos) and self.enabled:
            return True
        else:
            return False







# FPS = 60
# class Game():
#     def __init__(self):
#         pygame.init()
#         self.maze = Grid()
#         self.window = pygame.display.set_mode(size = (950, 525))
#         pygame.display.set_caption('Theseus and the Minotaur')
#         self.player_moves=[self.maze.G.graph["player_location"]]
      
#         self.playing, self.running =True, True
#         self.game_end = False
#         self.clock = pygame.time.Clock()

#         self.load_assets()
 
#         self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
#         self.DISPLAY_W, self.DISPLAY_H = 700, 525
#         self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
#         self.font_name = 'freesansbold.ttf'
#         #self.font_name = pygame.font.get_default_font()
#         self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
#         self.main_menu = MainMenu(self)
#         self.options = OptionsMenu(self)
#         self.credits = CreditsMenu(self)
#         self.curr_menu = self.main_menu


#     def get_events_in_game(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running, self.playing = False, False
#                 self.curr_menu.run_display = False

#             # if self.playing:
#             if event.type == pygame.KEYDOWN and not self.game_end:
#                 if event.key == pygame.K_a:
#                     self.playing = False
#                     self.START_KEY = True
#                     self.curr_menu = self.main_menu
                    
#                 if event.key == pygame.K_w or event.key == pygame.K_UP:
#                     # Up
#                     try: 
#                         self.player_moves.append(self.player.move("up"))
#                         # self.mino.move()
#                     except ValueError: 
#                         print("LỖI", ValueError)
#                         pass

#                 if event.key == pygame.K_w or event.key == pygame.K_DOWN:
#                     # Up
#                     try: 
#                         self.player_moves.append(self.player.move("down"))
#                     except ValueError: 
#                         print("LỖI", ValueError)
#                         pass
                
#                 if event.key == pygame.K_w or event.key == pygame.K_LEFT:
#                     # Up
#                     try: 
#                         self.player_moves.append(self.player.move("left"))
#                         # self.mino.move()
#                     except ValueError: 
#                         print("LỖI", ValueError)
#                         pass
                
#                 if event.key == pygame.K_w or event.key == pygame.K_RIGHT:
#                     # Up
#                     try: 
#                         self.player_moves.append(self.player.move("right"))
#                         # self.mino.move()
#                     except ValueError: 
#                         print("LỖI", ValueError)
#                         pass
        
#                 if event.key == pygame.K_SPACE:
#                     # Skip
#                     try: 
#                         self.player_moves.append(self.player.move("skip"))  
#                         pass
#                     except ValueError: 
#                         pass

#                 if event.key == pygame.K_BACKSPACE:
#                     # Reset board
#                     self.maze.G.graph["player_location"] = self.player_moves[0]
#                     self.maze.G.graph["mino_location"] = self.mino.mino_moves[0]
#                     self.player.location = self.player_moves[0]
#                     self.mino.location = self.mino.mino_moves[0]
#                     self.player_moves = [self.player.location]
#                     self.mino.mino_moves = [self.mino.location]

#                 if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
#                     if len(self.player_moves)>1:
#                         self.maze.G.graph["player_location"] = self.player_moves[-2]
#                         self.maze.G.graph["mino_location"] = self.mino.mino_moves[-3]
#                         self.player.location = self.maze.G.graph["player_location"]
#                         self.mino.location = self.maze.G.graph["mino_location"]
#                         self.player_moves.pop()
#                         self.mino.mino_moves.pop()
#                         self.mino.mino_moves.pop()
    
#             # print("move",self.player_moves, self.mino.mino_moves, self.maze.G.graph["player_location"], self.maze.G.graph["mino_location"])
#             if self.maze.G.graph["player_location"] in self.maze.goal_neighbors:
#                 self.bg.attack_animation = True

#             game_end, game_win = self.check_game_end()
#             if game_end and game_win:
#                 win_message = "YOU WIN!"
#                 print("WIN")
#             elif game_end and not game_win:
#                 print("Lose")
#                 win_message = "YOU LOSE!"
#             else:
#                 win_message = " "  
#             # else:        
#             #     if event.type == pygame.KEYDOWN:
#             #         if event.key == pygame.K_RETURN:
#             #             self.START_KEY = True
#             #         if event.key == pygame.K_BACKSPACE:
#             #             self.BACK_KEY = True
#             #         if event.key == pygame.K_DOWN:
#             #             self.DOWN_KEY = True
#             #         if event.key == pygame.K_UP:
#             #             self.UP_KEY = True         
#     def load_assets(self):

#         self.mino = Minotaur(self.maze)
#         self.bg = Background(self.maze)
#         self.font = pygame.font.Font(
#             # '8-BIT WONDER.TTF'
#             'freesansbold.ttf'
#             , 20)
#         self.player = Player(self.maze, mino=self.mino)


#     def render(self):
#         self.bg.draw(self.window)
#         self.player.draw(self.window, 50, 85)
#         self.mino.draw(self.window, 50,85)
#         self.player.update(1)
#         self.bg.update(1)
#         self.mino.update(0.5)

#     def draw_text(self, text, size, x, y, color = (0,0,0) ):
#         font = pygame.font.Font(self.font_name,size)
#         text_surface = font.render(text, True,color)
#         text_rect = text_surface.get_rect()
#         text_rect.center = (x,y)
#         self.display.blit(text_surface,text_rect)

#     def run(self):

#         while self.playing:  
#             # if clock() > self.next_frame:
#             #     self.frame = (frame+1)%10
#             #     self.next_frame += 80

#             # self.check_events()
#             # if self.START_KEY:
#             #     self.playing= False
         
#             self.get_events_in_game()
#             self.render()
#             pygame.time.delay(50)
#             self.clock.tick(60)
#             pygame.display.update()

#     def check_game_end(self):
#         if self.maze.G.graph["mino_location"] == self.maze.G.graph["player_location"]:
#             return True, False
#         elif self.maze.G.graph["player_location"] == self.maze.G.graph["goal"] and self.maze.G.graph["mino_location"] != self.maze.G.graph["player_location"]:
#             return True, True
#         else:
#             return False, False

    
#     def reset_keys(self):
#         self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

# if __name__ == "__main__":
#     game = Game()
#     while game.running:
#         # game.curr_menu.display_menu()
#         # game.get_events_in_game()
#         # if game.playing:
#         #     game.window = pygame.display.set_mode(size = (950, 525))
#         #     game.run()
#         # else:
#         #     game.window = pygame.display.set_mode(size = (700, 525))
        
#         # game.reset_keys()
#         game.run()