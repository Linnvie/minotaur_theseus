from Spritesheet_class import Spritesheet
import pygame, time
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, maze,  *groups, mino):
        super().__init__(groups)
        # Mê cung người chơi đang đứng
        self.maze = maze
        self.mino = mino
        self.scale=self.maze.scale_factor_player
        self.load_sprites()
        # self.sprites = sprite_sheet_down.get_animation(self.walk_down_sprite_rects, 1/10, scale = 0.5)
        self.total_moves = 0

        self.current_sprite = 0
        self.img = self.walk_down_ainms[self.current_sprite]
        #Vị trí tọa độ người chơi đang đứng trên lưới
        self.location = maze.G.graph["player_location"]
        self.moving, self.moving_up, self.moving_down, self.moving_left, self.moving_right = False, False, False, False, False

    def load_sprites(self):
        # sprite_sheet_down = pygame.image.load('Walk_Down.png').convert_alpha()
        sprite_sheet_down = Spritesheet('images/Walk_Down.png')
        walk_down_sprite_rects = [(0, 0, 105, 128),
                        (105, 0, 105, 128), 
                        (210, 0, 105, 128),
                        (313, 0, 105, 128),
                        (415, 0, 105, 128),
                        (520, 0, 105, 128),
                        (625, 0, 105, 128),
                        (730, 0, 105, 128),
                        (835, 0, 105, 128),
                        (935, 0, 105, 128)]  # Vị trí của các sprite trên sprite sheet

        self.walk_down_ainms = sprite_sheet_down.get_animation(walk_down_sprite_rects, scale = self.scale)

        sprite_sheet_up = Spritesheet('images/Walk_Up.png')
        walk_up_sprite_rects = [(2, 20, 100, 128),
                (100, 20, 100, 128), 
                (197, 20, 100, 128),
                (297, 20, 100, 128),
                (395, 20, 100, 128),
                (492, 20, 100, 128),
                (590, 20, 100, 128),
                (690, 20, 100, 128),
                (788, 20, 100, 128),
                (883, 20, 97, 128)]  # Vị trí của các sprite trên sprite sheet

        self.walk_up_ainms = sprite_sheet_up.get_animation(walk_up_sprite_rects, scale = self.scale)
        # self.store_animation("walk_up", walk_up_ainms)

        sprite_sheet_left = Spritesheet('images/Walk_Left.png')
        walk_left_sprite_rects = [(30, 0, 134, 123),
                (250, 0, 134, 123), 
                (455, 0, 134, 123),
                (660, 0, 134, 123),
                (870, 0, 134, 123),
                (1070, 0, 134, 123),
                (1270, 0, 134, 123),
                (1470, 0, 134, 123),
                (1670, 0, 134, 123),
                (1670, 0, 134, 123)]  # Vị trí của các sprite trên sprite sheet

        self.walk_left_ainms = sprite_sheet_left.get_animation(walk_left_sprite_rects, scale = self.scale)

        sprite_sheet_right = Spritesheet('images/Walk_Right.png')
        walk_right_sprite_rects = [(38, 0, 134, 123),
                (220, 0, 134, 123), 
                (410, 0, 134, 123),
                (610, 0, 134, 123),
                (810, 0, 134, 123),
                (1010, 0, 134, 123),
                (1200, 0, 134, 123),
                (1390, 0, 134, 123),
                (1580, 0, 134, 123),
                (1770, 0, 134, 123)]  # Vị trí của các sprite trên sprite sheet

        self.walk_right_ainms = sprite_sheet_right.get_animation(walk_right_sprite_rects, scale = self.scale)

    def draw(self, win):
        self.window = win
        win.blit(self.img, (1*self.maze.scale_factor+self.maze.screen_padding + self.maze.square_size_scaled*self.location[0], self.maze.screen_padding + 10*self.maze.scale_factor + self.maze.square_size_scaled*self.location[1]))
    
    def update(self,speed):
        if self.moving:
            # Chặn các thao tác di chuyển tiếp người chơi khi chưa đi đến điểm dích
            pygame.event.set_blocked(pygame.KEYDOWN)
            pygame.event.set_blocked(pygame.KEYUP)
            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
            s = round((speed/10), 1)

            if self.moving_down == True:
                player_location = (self.location[0] + 0, round((self.location[1] + s),1))
                self.img = self.walk_down_ainms[int(self.current_sprite)]
            if self.moving_up == True:
                # print("curent", int(self.current_sprite))
                player_location = (self.location[0] + 0, round((self.location[1] - s),1))
                self.img = self.walk_up_ainms[int(self.current_sprite)]
            if self.moving_left == True:
                player_location = (round((self.location[0] - s),1), self.location[1] + 0)
                self.img = self.walk_left_ainms[int(self.current_sprite)]
            if self.moving_right == True:
                player_location = (round((self.location[0] + s),1), self.location[1] + 0)
                self.img = self.walk_right_ainms[int(self.current_sprite)]
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.walk_down_ainms):
                self.current_sprite = 0
                self.img = self.walk_down_ainms[int(self.current_sprite)]
                self.moving, self.moving_up, self.moving_down, self.moving_left, self.moving_right = False, False, False, False, False
                self.maze.G.graph["player_location"] = player_location
		        # Return player_location
                self.location = player_location
                self.mino.move()

            self.maze.G.graph["player_location"] = player_location
		    # Return player_location
            self.location = player_location

    def move(self, direction=None):
        # clock = pygame.time.Clock()
        # if direction == None:
        #     pass
        if direction not in self.maze.get_move_options()["player"]:
            print("không có")
            raise ValueError(str(direction) + " is not a valid direction.")
        else:
            self.total_moves+=1
            self.moving=True
            player_location = self.maze.G.graph["player_location"]
            if direction == "skip":
                self.moving = False
                pygame.event.set_blocked(pygame.KEYDOWN)
                pygame.event.set_blocked(pygame.KEYUP)
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                self.mino.move()
            elif direction == "right":
                player_location = (self.location[0] + 1, self.location[1] + 0)
                # change_sprite_image(self.walk_right_sprite_rects, self.frame)
                self.moving_right = True
            elif direction == "left":
                player_location = (self.location[0] - 1, self.location[1] + 0)
                self.moving_left = True
            elif direction == "up" :
                player_location = (self.location[0] + 0, self.location[1] - 1)
                self.moving_up = True
            elif direction == "down":
                player_location = (self.location[0] + 0, self.location[1] + 1)
                self.moving_down = True	  
            
        return player_location

    def move_in_solve(self, direction):
        if direction not in self.maze.get_move_options()["player"]:
            print("cjeck", self.maze.get_move_options()["player"])
            raise ValueError(str(direction) + " is not a valid direction.")
        else:
            player_location = self.maze.G.graph["player_location"]
            if direction == "skip":
				# Do not change player location
                pass
            elif direction == "right":
                player_location = (self.location[0] + 1, self.location[1] + 0)
            elif direction == "left":
                player_location = (self.location[0] - 1, self.location[1] + 0)
            elif direction == "up":
                player_location = (self.location[0] + 0, self.location[1] - 1)
            elif direction == "down":
                player_location = (self.location[0] + 0, self.location[1] + 1)
		
		# Push update player_location in maze. 
        self.maze.G.graph["player_location"] = player_location
	
		# Return player_location
        self.location = player_location
        return player_location
    