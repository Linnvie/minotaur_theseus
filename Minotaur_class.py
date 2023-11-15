from Spritesheet_class import Spritesheet
from AnimationSprite_class import AnimationSprite
import pygame


# ban đầu 820,460,  50,72,  mino 1.05,   player 0.5

class Minotaur(AnimationSprite):
    def __init__(self, maze):
        self.maze = maze
        #Vị trí tọa độ mino đang đứng trên lưới
        self.location = maze.G.graph["mino_location"]
        self.load_sprites()

        self.current_sprite = 0
        self.img = self.walk_down_ainms[1]
    
        self.movings = []
        self.mino_moves = [self.maze.G.graph["mino_location"]]
        self.current_moving = None
        
    def draw(self, win, screen_padding, square_size_scaled):
        # print(screen_padding, square_size_scaled)
        win.blit(self.img, (14+screen_padding + square_size_scaled*self.location[0], 4+ screen_padding + square_size_scaled*self.location[1]))

    def load_sprites(self):
        sprite_width = 48
        sprite_height = 64
        sprite_sheet = Spritesheet('images/minotaur.png')
        walk_down_sprite_rects = [(0, 132, sprite_width, sprite_height),
                (48, 130, sprite_width, sprite_height),
                (96, 132, sprite_width, sprite_height),
                (48, 130, sprite_width, sprite_height),
                (0, 132, sprite_width, sprite_height),
                        ] 

        self.walk_down_ainms = sprite_sheet.get_animation(walk_down_sprite_rects, scale = 1.28)

        walk_up_sprite_rects = [(0, 2, sprite_width, sprite_height),
                 (48, 0, sprite_width, sprite_height),
                (96, 2, sprite_width, sprite_height),
                (48, 0, sprite_width, sprite_height),
                (0, 2, sprite_width, sprite_height),
               ]  

        self.walk_up_ainms = sprite_sheet.get_animation(walk_up_sprite_rects, scale = 1.28)

        walk_left_sprite_rects = [(0, 192, sprite_width, sprite_height),
                (48, 190, sprite_width, sprite_height),
                (96, 192, sprite_width, sprite_height),
                (48, 190, sprite_width, sprite_height),
                 (0, 192, sprite_width, sprite_height)
             ]  # Vị trí của các sprite trên sprite sheet

        self.walk_left_ainms = sprite_sheet.get_animation(walk_left_sprite_rects, scale = 1.28)

        walk_right_sprite_rects = [(0, 67, sprite_width, sprite_height),
                (48, 65, sprite_width, sprite_height),
                (96, 67, sprite_width, sprite_height),
                (48, 65, sprite_width, sprite_height),
                (0, 67, sprite_width, sprite_height)
            ]  # Vị trí của các sprite trên sprite sheet

        self.walk_right_ainms = sprite_sheet.get_animation(walk_right_sprite_rects, scale = 1.28)
    
    def update(self,speed):
        if len(self.movings)>0:
            # print("đếm", self.movings)
            self.current_moving = self.movings[0]
            # 5 là mỗi hoạt ảnh có 5 tấm hình
            s = round((speed/5), 1)

            if self.current_moving == "down":
                mino_location = (self.location[0] + 0, round((self.location[1] + s),1))
                self.img = self.walk_down_ainms[int(self.current_sprite)]
            if self.current_moving == "up":
                # print("curent", int(self.current_sprite))
                mino_location = (self.location[0] + 0, round((self.location[1] - s),1))
                self.img = self.walk_up_ainms[int(self.current_sprite)]
            if self.current_moving == "left":
                mino_location = (round((self.location[0] - s),1), self.location[1] + 0)
                self.img = self.walk_left_ainms[int(self.current_sprite)]
            if self.current_moving == "right":
                mino_location = (round((self.location[0] + s),1), self.location[1] + 0)
                self.img = self.walk_right_ainms[int(self.current_sprite)]
            self.current_sprite += speed

            if int(self.current_sprite) >= len(self.walk_down_ainms):
                self.current_sprite = 0
                self.img = self.walk_down_ainms[1]
            #   loại bước đi ra khỏi mảng bước đi khi đã lặp đủ 1 lần chuyển động
                self.movings.pop(0)
                self.maze.G.graph["mino_location"] = mino_location
		# Return player_location
                self.location = mino_location
                # self.mino.move()

            self.maze.G.graph["mino_location"] = mino_location
		# Return player_location
            self.location = mino_location
        else:
            pygame.event.set_allowed(pygame.KEYDOWN)
            pygame.event.set_allowed(pygame.KEYUP)

    def move(self):
        
        # print("vào move")
        stay_location = self.maze.G.graph["mino_location"] 
        x = 0
        while x<2:

            mino_location = self.maze.G.graph["mino_location"]
            player_location = self.maze.G.graph["player_location"]

            move_options = self.maze.get_move_options()["mino"]

            if ("right" in move_options) and (mino_location[0] < player_location[0]):
                mino_location = (mino_location[0]+1, mino_location[1])
                self.movings.append("right")

            elif ("left" in move_options) and (mino_location[0] > player_location[0]):
                mino_location = (mino_location[0]-1, mino_location[1])
                self.movings.append("left")

            elif ("up" in move_options) and (mino_location[1] > player_location[1]):
                mino_location = (mino_location[0], mino_location[1]-1)
                self.movings.append("up")

            elif ("down" in move_options) and (mino_location[1] < player_location[1]):
                mino_location = (mino_location[0], mino_location[1]+1)
                self.movings.append("down")

            self.mino_moves.append(mino_location)
            self.maze.G.graph["mino_location"] = mino_location
            x+=1
        # if len(self.count>0):
        #     self.moving = True
        self.maze.G.graph["mino_location"] = stay_location
        # self.location = mino_location
        return mino_location

    def move_in_solve(self):
		# Return new coordinates that the Minotaur will move to
        mino_location = self.maze.G.graph["mino_location"]
        player_location = self.maze.G.graph["player_location"]

        remaining_moves = 2

        while remaining_moves > 0:
            move_options = self.maze.get_move_options()["mino"]
			# Check right
            if "right" in move_options and player_location[0] > mino_location[0]:
                mino_location = (mino_location[0] + 1, mino_location[1] + 0)
			#Check left
            elif "left" in move_options and player_location[0] < mino_location[0]:
                mino_location = (mino_location[0] - 1, mino_location[1] + 0)
			# Check up
            elif "up" in move_options and player_location[1] < mino_location[1]:
                mino_location = (mino_location[0] + 0, mino_location[1] - 1)
			# Check down
            elif "down" in move_options and player_location[1] > mino_location[1]:
                mino_location = (mino_location[0] + 0, mino_location[1] + 1)
			
			# If the Minotaur is not able to horizontally or vertically, then it can't move. 
            remaining_moves -= 1

			# Push update mino_location in maze. 
            self.maze.G.graph["mino_location"] = mino_location

        self.location = mino_location
        return mino_location

        