import pygame
from Spritesheet_class import Spritesheet
FPS = 60
class Background():
    def __init__(self, maze):

        # Vẽ mê cung theo size màn hình
        # size_window, square_size_scaled, screen_padding = calculate_screen_size(maze)
        # self.size_window = (950, 525)
        # self.screen_padding =50
         #Kích thước mỗi ô trong mecung
        # self.square_size_scaled= 85
        self.maze = maze
        self.img = pygame.transform.scale(pygame.image.load('images/background.jpg').convert(), self.maze.size_window)
        
        # self.width = self.img.get_width()
        # self.height = self.img.get_height()

        self.current_door = 0
        self.attack_animation = False
        sprite_width = 60
        sprite_height = 100
        door_sheet_down = Spritesheet('images/door.png')
        door_sprite_rects = [ (4, 0, sprite_width, sprite_height), 
                (72, 0, sprite_width, sprite_height), 
                (140, 0, sprite_width, sprite_height),
                (208, 0, sprite_width, sprite_height),
                (276, 0, sprite_width, sprite_height),
                (344, 0, sprite_width, sprite_height),
                (412, 0, sprite_width, sprite_height),]  # Vị trí của các sprite trên sprite sheet

        self.door_ainms = door_sheet_down.get_animation(door_sprite_rects, scale = 0.9)
        self.door_img = self.door_ainms[self.current_door]
        
        
        
    def draw(self, window):
        window.blit(self.img, (0,0))
        window.blit(self.door_img, (18+self.maze.screen_padding + self.maze.square_size_scaled*self.maze.G.graph['goal'][0],self.maze.screen_padding - 3  + self.maze.square_size_scaled*self.maze.G.graph['goal'][1]))
        self.draw_grid(window)
        
    # def update(self):
    #     self.x -= self.speed
    def update(self,speed):
        if self.attack_animation == True and self.current_door < 6:
            self.current_door += speed
            # if int(self.current_door) == 6:
            #     # self.current_door = 6
            #     self.attack_animation = False
            
            self.door_img = self.door_ainms[self.current_door]
   
    def draw_grid(self, window):

	    # Animation constants
        time_to_move = 0.1
        frames = int(FPS*time_to_move)

        def draw_walls():
            #Độ dày nét vẽ
            wall_width = int(self.maze.square_size_scaled/10)

            width_buffer = wall_width / 2 -1
            # Draw grids
            # Vertical
            #Đối số width là độ dày nét vẽ, start_pos là tọa độ điểm bắt đầu, end_pos là tọa độ điểm kết thúc
            # print("bg",self.maze.size_grid)
            for i in range(1,self.maze.size_grid[0]):
                pygame.draw.line( surface = window, 
                                color = (230,230,230),
                                start_pos = (self.maze.screen_padding + self.maze.square_size_scaled*i, self.maze.screen_padding - width_buffer),
                                end_pos = (self.maze.screen_padding + self.maze.square_size_scaled*i, self.maze.size_window[1] - self.maze.screen_padding + width_buffer), 
                                width = wall_width)
		    # Horizontal
            for i in range(1, self.maze.size_grid[1]):
                pygame.draw.line(surface = window, 
                                color = (230,230,230), 
                                start_pos = (self.maze.screen_padding -width_buffer, self.maze.screen_padding + self.maze.square_size_scaled*i), 
                                end_pos = (self.maze.size_window[0] - self.maze.screen_padding + width_buffer, self.maze.screen_padding + self.maze.square_size_scaled*i), 
                                width = wall_width)
            # Vẽ đường bao toàn mê cung
            # Top
            pygame.draw.line(surface = window, 
                            color = (0,0,0), 
                            start_pos = (self.maze.screen_padding - width_buffer, self.maze.screen_padding), 
                            end_pos = (self.maze.size_window[0] - self.maze.screen_padding + width_buffer, self.maze.screen_padding), 
                            width = wall_width)
		    # Left
            pygame.draw.line(surface = window, 
                            color = (0,0,0), 
                            start_pos = (self.maze.screen_padding, self.maze.screen_padding - width_buffer), 
                            end_pos = (self.maze.screen_padding, self.maze.size_window[1] - self.maze.screen_padding+ width_buffer), 
                            width = wall_width)
		    # Right
            pygame.draw.line(surface = window, 
                            color = (0,0,0), 
                            start_pos = (self.maze.size_window[0] - self.maze.screen_padding, self.maze.screen_padding - width_buffer), 
                            end_pos = (self.maze.size_window[0] - self.maze.screen_padding, self.maze.size_window[1] - self.maze.screen_padding + width_buffer), 
                            width = wall_width)
		    # Bottom
            pygame.draw.line(surface = window, 
                            color = (0,0,0), 
                            start_pos = (self.maze.screen_padding - width_buffer, self.maze.size_window[1] - self.maze.screen_padding), 
                            end_pos = (self.maze.size_window[0] - self.maze.screen_padding + width_buffer, self.maze.size_window[1] - self.maze.screen_padding), 
                            width = wall_width)
		    # Draw walls
            walls = []

            # print("èg",self.maze.G.edges.items() )
            # edge có kiểu ((2,2),(2,3))
            # for item in self.maze.G.edges.items():
            #     print("iyem", item)
            for edge, weight in self.maze.G.edges.items():
                # print("tường", edge, weight)
                if weight["weight"] == -1:
                    edge_as_list = []
                    for node in edge:
                        edge_as_list.append(list(node))
                    # print("list", edge_as_list) sẽ có dạng [[4, 1], [4, 2]]
                    walls.append(list(edge_as_list))
                    # print("wall", walls) sẽ có dạng wall [  [[0, 1], [1, 1]],  [[0, 1], [0, 2]]  ]
            for wall in walls:
                # print(wall)
                w1, w2 = self.change_wall_coordinates(wall)
                # print("w11", w1, w2)
                # +1 vì mảng bắt đầu đếm từ 0
                w1, w2 = (self.maze.screen_padding + self.maze.square_size_scaled*int(w1[0]+1),self.maze.screen_padding + self.maze.square_size_scaled*int(w1[1]+1)), (self.maze.screen_padding + self.maze.square_size_scaled*int(w2[0]+1),self.maze.screen_padding + self.maze.square_size_scaled*int(w2[1]+1))
                wx1, wy1 = w1
                wx2, wy2 = w2
           
			# Width buffers được thêm khác nhau cho các bức tường ngang và dọc. 
			# Xác định xem đoạn tường là dọc hay ngang. 
                if (wx2 - wx1) == 0:
				# Vertical
                    pygame.draw.line(surface = window, color = (0,0,0), 
                                    start_pos = (wx1, wy1 - width_buffer), 
                                    end_pos = (wx2, wy2 + width_buffer), width = wall_width)
                elif (wy2 - wy1) == 0:
				# Horizontal
                    pygame.draw.line(surface = window, color = (0,0,0), 
                                    start_pos = (wx1 - width_buffer, wy1), 
                                    end_pos = (wx2 + width_buffer, wy2), width = wall_width)
	
        for frame in range(1, frames + 1):
            # window.fill((255,255,255))
            draw_walls()

    def change_wall_coordinates(self, wall):
        # tường có dạng ((x1, y1), (x2, y2)) = [[x1, y1], [x2, y2]]
        # Đổi tọa độ tường thành tọa độ trên màn hình 
        # Tọa độ được lưu của tường là tọa độ cuae cạnh trong đồ thị nx không phải tọa độ hiển thị
        # Đổi thành tọa độ hiển thị thì cạnh ngang bị mất sẽ hiển thị thành cạnh dọc tượng trưng cho chặn đường và ngược lại
        x1 = wall[0][0]
        y1 = wall[0][1]
        x2 = wall[1][0]
        y2 = wall[1][1]

        if (y2 - y1) == 0:
			# Cùng chiều ngang
			# Để chắc rằng node 1 luôn nằm bên trái node 2, tức là cạnh đọc tọa độ từ trái sang phải
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
			    # Đổi thành chiều dọc để hiển thị
            return ((x1 + 0.5, y1 - 0.5), (x2 - 0.5, y2 + 0.5))
        elif (x2 - x1) == 0:
			# Cùng chiều dọc
			# Để chắc rằng node 1 luôn nằm trên node 2, tức là cạnh đọc tọa độ từ trên xuống dưới
            if y1 > y2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
			# Đổi thành chiều ngang để hiển thị
            return ((x1 - 0.5, y1 + 0.5),(x2 + 0.5, y2 - 0.5))