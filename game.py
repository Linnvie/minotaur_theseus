import pygame
from pygame import mixer
from Grid_class import Grid
from Player_class import Player
from Minotaur_class import Minotaur
from Background_class import Background
from Menu_class import *
from solve import *
import sys, math

FPS = 60
class Game():
    def __init__(self):
        pygame.init()
        mixer.init()
        
        self.window = pygame.display.set_mode(size = (700, 525))
        pygame.display.set_caption('Theseus and the Minotaur')
        self.playing, self.running =False, True
        self.game_end = False
        self.clock = pygame.time.Clock()
        
        self.current_volume = 0.5
        
        self.music_on = True
        mixer.music.load('musics/bg_music.mp3')
        self.win_sound = mixer.Sound('musics/win.mp3')
        self.move_sound = mixer.Sound('musics/move.mp3')
        self.enter_sound = mixer.Sound('musics/enter.mp3')
        self.open_sound = mixer.Sound('musics/open_door.mp3')
        self.set_volume()
        
             
        # self.maze = Grid()
        # self.player_moves=[self.maze.G.graph["player_location"]]
        # self.load_assets()

        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY = False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 700, 525
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.font_name = 'freesansbold.ttf'
        
        self.main_menu = MainMenu(self)
        
        self.options = OptionsMenu(self)
        self.tutorial = TextMenu(self)
        self.mythology = TextMenu(self)
        self.error_menu = TextMenu(self,line_high =60, size =40, x_pos=400, y_post=120, text_lines=["Server error!", " Please check ","your network connection!"])
        self.win_menu = EndMenu(self,"Well done!", "You escaped", "the Minotaur!","Next")
        self.lose_menu = EndMenu(self, "Oh no...", "The Minotaur", "got you!", "Undo")
        self.curr_menu = self.main_menu
        self.level_menu = LevelMenu(self)

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
                    self.playing = False
                    # self.reset_keys()
                    # pygame.event.set_allowed(pygame.KEYDOWN)
                    # pygame.event.set_allowed(pygame.KEYUP)
                    # self.START_KEY = True
                    self.curr_menu = self.main_menu
                    # self.window = pygame.display.set_mode(size = (700, 525))

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    # Up
                    try: 
                        self.player_moves.append(self.player.move("up"))
                        # self.mino.move()
                    except ValueError: 
                        print("LỖI", ValueError)
                        pass

                if event.key == pygame.K_w or event.key == pygame.K_DOWN:
                    # Up
                    try: 
                        self.player_moves.append(self.player.move("down"))
                    except ValueError: 
                        print("LỖI", ValueError)
                        pass
                
                if event.key == pygame.K_w or event.key == pygame.K_LEFT:
                    # Up
                    try: 
                        self.player_moves.append(self.player.move("left"))
                        # self.mino.move()
                    except ValueError: 
                        print("LỖI", ValueError)
                        pass
                
                if event.key == pygame.K_w or event.key == pygame.K_RIGHT:
                    # Up
                    try: 
                        self.player_moves.append(self.player.move("right"))
                        # self.mino.move()
                    except ValueError: 
                        print("LỖI", ValueError)
                        pass
        
                if event.key == pygame.K_SPACE:
                    # Skip
                    try: 
                        self.player_moves.append(self.player.move("skip"))  
                        pass
                    except ValueError: 
                        pass

                if event.key == pygame.K_BACKSPACE:
                    # Reset board
                    self.restart()

                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.undo()

                if event.key == pygame.K_o:
				
                    self.maze.G.graph["player_location"] = self.player_moves[0]
                    self.maze.G.graph["mino_location"] = self.mino.mino_moves[0]
			
                    print("sol",solve(self.maze))
				
                if event.key == pygame.K_p:	
                    self.maze.G.graph["player_location"] = self.player_moves[0]
                    self.maze.G.graph["mino_location"] = self.mino.mino_moves[0]
				
                    print("sol2",solve2(self.maze))

                if event.key == pygame.K_m:
                    self.maze.G.graph["player_location"] = self.player_moves[0]
                    self.maze.G.graph["mino_location"] = self.mino.mino_moves[0]
					
                    print("sol3",solve3(self.maze))
    
          
        # print("move",self.player_moves, self.mino.mino_moves, self.maze.G.graph["player_location"], self.maze.G.graph["mino_location"])

    def restart(self):
        # print("restart")
        self.player.total_moves = 0
        self.mino.movings = []
        self.maze.G.graph["player_location"] = self.player_moves[0]
        self.maze.G.graph["mino_location"] = self.mino.mino_moves[0]
        self.player.location = self.player_moves[0]
        self.mino.location = self.mino.mino_moves[0]
        self.player_moves = [self.player.location]
        self.mino.mino_moves = [self.mino.location]

    def undo(self):
        if len(self.player_moves)>1:
            self.maze.G.graph["player_location"] = self.player_moves[-2]
            self.maze.G.graph["mino_location"] = self.mino.mino_moves[-3]
            self.player.location = self.maze.G.graph["player_location"]
            self.mino.location = self.maze.G.graph["mino_location"]
            # self.mino.movings = []
            self.player_moves.pop()
            self.mino.mino_moves.pop()
            self.mino.mino_moves.pop()

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
                    if self.music_on:
                        self.move_sound.play()
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
    
    def update(self):
        if self.maze.G.graph["player_location"] in self.maze.goal_neighbors:
            self.bg.attack_animation = True
            if self.bg.current_door ==1:
                self.open_sound.play()

        game_end, game_win = self.check_game_end()
        if game_end and game_win:
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
            if self.current_level==self.level_menu.total_elements:
                self.current_level = self.current_level+1

            if self.current_level<self.level_menu.total_elements:

                if self.list_level_infor[self.current_level]['moves'] == None:
                    self.list_level_infor[self.current_level]['moves']=0
                # call api thêm accountlevel


                self.current_level = self.current_level+1
                self.level_menu.state = self.current_level
                a = (self.level_menu.current_page-1)*self.level_menu.per_page
                # di chuyển cursor trong level menu
                self.level_menu.cursor_rect.midtop = (self.level_menu.button_location[self.current_level-a][0] -5+ self.level_menu.offset, self.level_menu.button_location[self.current_level-a][1])


            self.playing = False
            # self.reset_keys()
            pygame.event.set_allowed(pygame.KEYDOWN)
            pygame.event.set_allowed(pygame.KEYUP)
            self.curr_menu = self.win_menu
        
        elif game_end and not game_win:
            print("Lose")
            self.playing = False
            # self.reset_keys()
            pygame.event.set_allowed(pygame.KEYDOWN)
            pygame.event.set_allowed(pygame.KEYUP)
            self.curr_menu = self.lose_menu
                     
    def load_assets(self):

        self.mino = Minotaur(self.maze)
        self.bg = Background(self.maze)
        self.font = pygame.font.Font(
            # '8-BIT WONDER.TTF'
            'freesansbold.ttf'
            , 20)
        self.player = Player(self.maze, mino=self.mino)

    def render(self):
        self.bg.draw(self.window)
        self.player.draw(self.window, 50, 85)
        self.mino.draw(self.window, 50,85)
        self.bg.update(1)
        self.mino.update(0.5)
        self.player.update(1)
        text = self.font.render("Level: "+ str(self.current_level), True, (0,0,0))
        self.window.blit(text, (100, 15))
        move = self.font.render("Moves: "+ str(self.player.total_moves), True, (0,0,0))
        self.window.blit(move, (250, 15))

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
        if self.maze.G.graph["mino_location"] == self.maze.G.graph["player_location"]:
            return True, False
        elif self.maze.G.graph["player_location"] == self.maze.G.graph["goal"] and self.maze.G.graph["mino_location"] != self.maze.G.graph["player_location"]:
            return True, True
        else:
            return False, False

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY = False, False, False, False, False, False

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
        























# def transfer_to_screen_coordinates(coordinates, screen_padding, square_size_scaled):
# 		# Tọa độ các node này sẽ nằm chính giữa các ô vuông đã vẽ của mê cung square_size_scaled/2
#     screen_coordinates = (screen_padding + square_size_scaled*coordinates[0] , screen_padding + square_size_scaled*coordinates[1])
#     return screen_coordinates
# def calculate_screen_size(grid):
# 	# Đưa vào thông tin ma trận mê cung.
#     # Trả về kích thước của màn hình phù hợp với kích thước mê cung đó. 
# 	size_grid = grid.G.graph["size_grid"]

# 	# Xác định kích thước ô chưa chia tỷ lệ
# 	square_size = 100 # 100 px

# 	# Set padding cho mê cung so với màn hình game = 50px
# 	screen_padding = 50

# 	# Set scaling factor
# 	scale_factor = 0.5

# 	# Nếu số ô ngang hoặc dọc lớn hơn 7 thì scale kích thước mỗi ô lại vì 1 ô chưa scale là 100px nếu x7 là hơn 700px 
# 	max_square_num = max(size_grid[0], size_grid[1])

# 	if max_square_num > 7:
# 		scaled = True
# 		square_size_scaled = int(square_size * scale_factor)
# 	else:
# 		scaled = False
# 		square_size_scaled = square_size

#     # Tính toán kích thước màn hình chơi
#     # Chiều ngang = số ô ngang*tỉ lệ scale đã tính toán+paddingx x2 cho 2 đầu, chiều dọc tương tự
# 	size_window = (size_grid[0]*square_size_scaled + screen_padding*2, size_grid[1]*square_size_scaled + screen_padding*2)
	
#     # Trả về kích thước màn hình, kích thước mỗi ô, padding để bắt đầu vẽ màn hình chơi
# 	return size_window, square_size_scaled, screen_padding

# def draw_grid():
# 	# Vẽ mê cung theo size màn hình
# 	# size_window, square_size_scaled, screen_padding = calculate_screen_size(maze)
#     size_window = (820,460)
#     screen_padding =50

#     #Kích thước mỗi ô trong mecung
#     square_size_scaled= 72
# 	# Animation constants
#     fps = 60
#     time_to_move = 0.1
#     frames = int(fps*time_to_move)

    

    # Hàm chuyển tọa độ các node trong networkx (G.graph) thành tọa độ trên màn hình chơi
    # input là tọa độ node của đỉnh đồ thị vd (0,1)
    

    # def calculate_edges_coordinates(edge):
	# 	# Mỗi cạnh của đồ thị được cấu thành từ 2 đỉnh với tọa độ ((x1, y1), (x2, y2))
	# 	# Hàm để tính toán các đỉnh vad cạnh đồ thị networkx(G.graph) thành tọa độ trên màn hình chơi

    #     x1 = edge[0][0]
    #     y1 = edge[0][1]
    #     x2 = edge[1][0]
    #     y2 = edge[1][1]
    #     # nếu 2 đỉnh có cùng y (nằm trên cùng 1 hàng)
    #     if (y2 - y1) == 0:
	# 		# Set coordinates such that pos 1 is left of pos 2
    #         if x1 > x2:
    #             x1, x2 = x2, x1
    #         y1, y2 = y2, y1
    #         return (transfer_to_screen_coordinates((x1 + 0.5, y1 - 0.5)), transfer_to_screen_coordinates((x2 - 0.5, y2 + 0.5)))
    #     # nếu 2 đỉnh có cùng x (nằm trên cùng 1 cột)
    #     elif (x2 - x1) == 0:
	# 		# Set coordinates such that pos 1 is above of pos 2
    #         if y1 > y2:
    #             x1, x2 = x2, x1
    #             y1, y2 = y2, y1
    #         return (transfer_to_screen_coordinates((x1 - 0.5, y1 + 0.5)), transfer_to_screen_coordinates((x2 + 0.5, y2 - 0.5)))

    
    # def draw_walls():
    #     #Độ dày nét vẽ
    #     wall_width = int(square_size_scaled/10)

    #     width_buffer = wall_width / 2 -1
	# 	# Draw grids
	# 	# Vertical
    #     #Đối số width là độ dày nét vẽ, start_pos là tọa độ điểm bắt đầu, end_pos là tọa độ điểm kết thúc
    #     for i in range(1,10):
    #         pygame.draw.line(surface = window, color = (230,230,230), start_pos = (screen_padding + square_size_scaled*i, screen_padding - width_buffer), end_pos = (screen_padding + square_size_scaled*i, size_window[1] - screen_padding + width_buffer), width = wall_width)
	# 	# Horizontal
    #     for i in range(1, 5):
    #         pygame.draw.line(surface = window, color = (230,230,230), start_pos = (screen_padding - width_buffer, screen_padding + square_size_scaled*i), end_pos = (size_window[0] - screen_padding + width_buffer, screen_padding + square_size_scaled*i), width = wall_width)
	# 	# Vẽ đường bao toàn mê cung
	# 	# Top
    #     pygame.draw.line(surface = window, color = (0,0,0), start_pos = (screen_padding - width_buffer, screen_padding), end_pos = (size_window[0] - screen_padding + width_buffer, screen_padding), width = wall_width)
	# 	# Left
    #     pygame.draw.line(surface = window, color = (0,0,0), start_pos = (screen_padding, screen_padding - width_buffer), end_pos = (screen_padding, size_window[1] - screen_padding+ width_buffer), width = wall_width)
	# 	# Right
    #     pygame.draw.line(surface = window, color = (0,0,0), start_pos = (size_window[0] - screen_padding, screen_padding - width_buffer), end_pos = (size_window[0] - screen_padding, size_window[1] - screen_padding + width_buffer), width = wall_width)
	# 	# Bottom
    #     pygame.draw.line(surface = window, color = (0,0,0), start_pos = (screen_padding - width_buffer, size_window[1] - screen_padding), end_pos = (size_window[0] - screen_padding + width_buffer, size_window[1] - screen_padding), width = wall_width)
		# Draw walls
		# Get list of wall coordinate pairs
		# walls = []
		# for edge, weight in board.G.edges.items():
		# 	if weight["weight"] == -1:
		# 		edge_as_list = []
		# 		for node in edge:
		# 			edge_as_list.append(list(node))
		# 		walls.append(list(edge_as_list))
		# for wall in walls:
		# 	w1, w2 = adj_wall_coordinates(wall)
		# 	wx1, wy1 = w1
		# 	wx2, wy2 = w2

		# 	# Width buffers are added differently for horizontal and vertical walls. 
		# 	# Determine if wall segment is vertical or horizontal. 
		# 	if (wx2 - wx1) == 0:
		# 		# Vertical
		# 		pygame.draw.line(surface = window, color = (0,0,0), start_pos = (wx1, wy1 - width_buffer), end_pos = (wx2, wy2 + width_buffer), width = wall_width)
		# 	elif (wy2 - wy1) == 0:
		# 		# Horizontal
		# 		pygame.draw.line(surface = window, color = (0,0,0), start_pos = (wx1 - width_buffer, wy1), end_pos = (wx2 + width_buffer, wy2), width = wall_width)
    # for frame in range(1, frames + 1):
    #     # window.fill((255,255,255))
    #     draw_walls()
# if __name__ == "__main__":
	# Khởi tạo các biến và đối tượng
	# Tạo mới mê cung theo thông tin mê cung đã thiết lập của vòng chơi mới
    # maze = Grid()

	# # mino = Minotaur(maze)

	# # Run main
	# # Set window size
    # window = pygame.display.set_mode(size = (820, 460))
    # pygame.display.set_caption('Theseus and the Minotaur')

    # BG = pygame.image.load('background.jpg')
    # BG = pygame.transform.scale(BG, (820, 460))

    # font = pygame.font.Font('freesansbold.ttf', 20)
    # big_font = pygame.font.Font('freesansbold.ttf', 50)
    # timer = pygame.time.Clock()
    
    # fps = 60
    # run = True
    # draw = True
    # game_end = False

    # bg = Background()
    # # bg.draw()
    # player_moves=[]    
    # player_img = pygame.image.load('player.jpg').convert_alpha()
    # player_img = pygame.transform.scale(player_img, (72, 72))
    # player_window_location = transfer_to_screen_coordinates(maze.G.graph["player_location"], 50, 72)
    # player = Player(maze, player_img)
    # while run:
    #     # timer.tick(fps)
    #     # window.blit(BG, rect)
    #     bg.draw()
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             run = False
    #         if event.type == pygame.KEYDOWN and not game_end:
    #             if event.key == pygame.K_w or event.key == pygame.K_UP:
	# 				# Up
    #                 try: 
    #                     player_moves.append(player.move("up"))
    #                 except ValueError: 
    #                     print("LỖI", ValueError)
    #                     pass
    #     draw_grid() 
    #     # window.blit(img, img_rect)
    #     player.draw(window, 50, 72)
    #     pygame.display.update()   
    #     # if draw:
    #     #     player.draw(window)
    #     #     draw = False
    # fps.tick(60)
    # pygame.quit()
    # sys.exit()

