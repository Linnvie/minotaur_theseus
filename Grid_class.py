import networkx as nx
import copy
import random
import sys


class Grid:
    def __init__(self,  maze_infor = None, size_grid = (10,5), seed = None):  
        if maze_infor:
            self.scale_factor=1
            self.scale_factor_player=0.6
            self.scale_factor_mino=1.26
            self.scale_factor_door=0.86
            self.maze_infor = maze_infor
            self.G = self.build_maze(self.maze_infor)
            self.calculate_screen_size()
            
        else:
            self.G, self.maze_infor = self.build_random_maze(size_board = size_grid, seed = seed)
            
        self.add_move_options()

        # tính toán các ô liền kề và có đường đi vào cửa để khi player tới đó sẽ tạo hiệu ứng mở cửa
        self.goal_neighbors = []
        self.cal_door_neighbors()

    def calculate_screen_size(self):
        # Take in board, specifically size_board. 
        # Return the dimensions of the screen that will accommodate that board size. 
        # The maximum window size that the display on my MacBook can comfortably acommodate is (1400, 800)
            # At a scale_factor of 0.5, this is a maximum board dimension of 26x14
        # So if I set each tile to be 100 px, then I should start scaling for boards larger than 7x7. 

        self.size_grid = self.G.graph['size_grid']

        # Define unscaled tile size
        self.square_size_scaled = 85 # 85 px

        # Set edge buffer to be 50 px
        self.screen_padding = 50

        # Set scaling factor
        self.scale_factor = 0.7

        # Scale the tile and board size if using a board with any dimension greater than 7. 
        
        if self.size_grid[1] > 7 or self.size_grid[0]>14:
            # scaled = True
            self.square_size_scaled = int(self.square_size_scaled * self.scale_factor)
            self.scale_factor_player=0.43
            self.scale_factor_mino=0.86
            self.scale_factor_door=0.65
        # else:
            # scaled = False
        if self.size_grid[0] < 4:
            self.screen_padding = 100
            

        self.size_window = (self.size_grid[0]*self.square_size_scaled + self.screen_padding*2, self.size_grid[1]*self.square_size_scaled + self.screen_padding*2+50)
        return self.size_window, self.square_size_scaled, self.screen_padding

    def player_location(self):
        return self.G.graph["player_location"]

    def mino_location(self):
        return self.G.graph["mino_location"]

    def goal_location(self):
        return self.G.graph["goal"]     

    def build_maze(self, maze_infor, verbose = False):
        # maze_key phải là một từ điển có các thuộc tính "size_grid", "walls", "player_start", "mino_start" và "goal"
        # Trả về một đối tượng đồ thị kiểu NetworkX
        self.size_grid = maze_infor["sizeBoard"] 
        #Tạo đồ thị
        G = nx.grid_2d_graph(*self.size_grid)

        #Thêm các thuộc tính của G.graph (là kiểu dictionary)
        G.graph['size_grid'] = self.size_grid
        G.graph['player_location']= maze_infor["playerStart"]
        G.graph['mino_location'] = maze_infor["minoStart"]
        G.graph['goal'] = maze_infor["goal"]
        # Cho tất cả các cạnh của đồ thị weight đều bằng 0, tức là được đi qua (không bị tường chặn)
        G.add_edges_from(G.edges, weight = 0)

        # Đặt weight = -1 cho những cạnh là tường (không được đi qua)
        walls = maze_infor["walls"]
        G.add_edges_from(walls, weight = -1)
        if verbose:
            print(maze_infor)
        return G

    def remove_wall_edges(self, maze):
		# Xóa bỏ tất cả các tường (các cạnh trên đồ thị G của thư viện nx) (cạnh nào là tường thì xóa cạnh đó khỏi đồ thị)
        # maze.edges trả về một đối tượng loại dữ liệu "EdgeView"
        #  hàm list() để chuyển đổi EdgeView thành danh sách các cạnh, sau đó sử dụng chỉ số [0] để truy cập cạnh đầu tiên trong danh sách
		# thông tin về cạnh đầu tiên trong maze.edges, bao gồm các nút nguồn và đích của cạnh
        if "weight" in maze.edges[list(maze.edges)[0]]:
			# Biểu đồ mê cung được thông qua có thuộc tính trọng số trên các cạnh của nó. Cần phải loại bỏ những cạnh đó.
            walls = [edge for edge in maze.edges if maze.edges[edge]["weight"] == -1]
            maze_remove_wall_edges = copy.deepcopy(maze)
            maze_remove_wall_edges.remove_edges_from(walls)

        return maze_remove_wall_edges
    
    def validate_maze(self, maze):
		# Returns true if the maze has no closed off sections. This is true if the graph is connected. 
		
		# Need to remove edges of weight -1 if the edges have weight attributes
        maze_remove_wall_edges = self.remove_wall_edges(maze)
		# kiểm tra xem đồ thị maze_remove_wall_edges có liên thông (connected) hay không.
        return nx.is_connected(maze_remove_wall_edges)

    def cal_door_neighbors(self):
        reference = self.remove_wall_edges(self.G)
        node = self.G.graph["goal"]
        connected_nodes = nx.neighbors(reference, node)  
        for neighbor in connected_nodes:
            if neighbor == (node[0] + 1, node[1]) or neighbor == (node[0] - 1, node[1]) or neighbor == (node[0], node[1] - 1) or neighbor == (node[0], node[1] + 1):
                self.goal_neighbors.append(neighbor)    
        print("ok", self.goal_neighbors)

    def add_move_options(self):
        reference = self.remove_wall_edges(self.G)
        
        # for item in self.G.edges.items():
        #     print("refer", item)
		# Ở mỗi đỉnh đều có lựa chọn skip để bỏ qua lượt 
        for node in self.G.nodes:
            self.G.nodes[node]["options"] = ["skip"]
            self.G.nodes[node]["neighbors"] = [[node,"skip"]]
			# print(type(node))

			# trả về danh sách các đỉnh liền kề (có cạnh nối) của đỉnh node đồ thị reference.
            connected_nodes = nx.neighbors(reference, node)
			
            for neighbor in connected_nodes:
                if neighbor == (node[0] + 1, node[1]):
                    self.G.nodes[node]["options"].append("right")
                    self.G.nodes[node]["neighbors"].append([neighbor, "right"])
                elif neighbor == (node[0] - 1, node[1]):
                    self.G.nodes[node]["options"].append("left")
                    self.G.nodes[node]["neighbors"].append([neighbor, "left"])
                elif neighbor == (node[0], node[1] - 1):
                    self.G.nodes[node]["options"].append("up")
                    self.G.nodes[node]["neighbors"].append([neighbor,"up"])
                elif neighbor == (node[0], node[1] + 1):
                    self.G.nodes[node]["options"].append("down")
                    self.G.nodes[node]["neighbors"].append([neighbor, "down"])

    def get_move_options(self, node = None):
        # Trả về một dictionary chứa các tùy chọn di chuyển cho vị trí hiện tại của người chơi và minotaur
        move_options = {}
        if node:
			# Return the move options of the passed node instead. 
			# Return a list instead of dict
            move_options["player"] = self.G.nodes[node]["options"]
            move_options["mino"] = self.G.nodes[node]["options"][1:]
            return move_options
		
        player_location = self.player_location()
        mino_location = self.mino_location()
        move_options["player"] = self.G.nodes[player_location]["options"]
        move_options["mino"] = self.G.nodes[mino_location]["options"][1:]

        return move_options
        
    def get_neighbors(self, node = None):
		# Return a dict containing the move options for the player location and minotaur location
        neighbor_options = {}
        if node:
			# Return the move options of the passed node instead. 
			# Return a list instead of dict
            neighbor_options["player"] = self.G.nodes[node]["neighbors"]
            neighbor_options["mino"] = self.G.nodes[node]["neighbors"]
            return neighbor_options
		
        player_location = self.player_location()
        mino_location = self.mino_location()
        neighbor_options["player"] = self.G.nodes[player_location]["neighbors"]
        neighbor_options["mino"] = self.G.nodes[mino_location]["neighbors"]
        return neighbor_options
    
    def check_win_condition(self):
		# Return game_end, game_win. 
		# Return game_end = True if the player has reached the goal or encountered the minotaur. 
		# Return game_win = True if the player successfully reached the goal. 

        if self.G.graph["mino_location"] == self.G.graph["player_location"]:
			# Player Loses
            return True, False
        elif self.G.graph["player_location"] == self.G.graph["goal"] and self.G.graph["mino_location"] != self.G.graph["player_location"]:
			# Players Wins
            return True, True
        else:
			# Game is not over yet
            return False, False

    def build_random_maze(self, size_board = (10,5), seed = None, verbose = True):
        if seed is None:
            seed = random.randrange(sys.maxsize)
		
        random.seed(seed)

        num_edges = (size_board[0] * (size_board[1] - 1)) + ((size_board[0] - 1) * size_board[1])
		# num_edges are the number of edges in a graph produced by size_board. 
        expected_number_walls = num_edges / 2
        wall_threshold = expected_number_walls / num_edges
		# If random number is < wall_threshold, then build a wall along that edge.

		# Generate board Graph. 
        G = nx.grid_2d_graph(*size_board)

		# Add size attribute
        G.graph['size_board'] = size_board

        attempts_wall = 0
        attempts_tokens = 0
		# attempts_valid = 0
		# attempts_min_moves = 0

		# Generate Walls
        is_valid_maze = False
        while is_valid_maze is False:
            attempts_wall += 1
            for edge in G.edges:
                if random.random() < wall_threshold:
					# Set edge weight to -1
                    G.edges[edge]["weight"] = -1
                else:
                    G.edges[edge]["weight"] = 0

			# Validate no loops
            is_valid_maze = self.validate_maze(G)
		
		# Add player start, mino start, and goal. 
        is_valid_maze = False
        while is_valid_maze is False:
            attempts_tokens += 1
            G.graph["player_location"] = random.choice(list(G.nodes))
            G.graph["mino_location"] = random.choice(list(G.nodes))
            G.graph["goal"] = random.choice(list(G.nodes))

            if G.graph["player_location"] == G.graph["goal"] or G.graph["player_location"] == G.graph["mino_location"]:
                is_valid_maze = False
            else:
                is_valid_maze = True

        print("Wall generation attempts: " + str(attempts_wall))
        print("Token generation attempts: " + str(attempts_tokens))

		# maze_key should be a dictionary with attributes "size_board", "walls", "player_start", "mino_start", and "goal"
        maze_infor = {}
        maze_infor["size_board"] = size_board
        maze_infor["walls"] = [edge for edge in G.edges if G.edges[edge]["weight"] == -1]
        maze_infor["player_start"] = G.graph["player_location"]
        maze_infor["mino_start"] = G.graph["mino_location"]
        maze_infor["goal"] = G.graph["goal"]
        maze_infor["seed"] = seed

        if verbose:
            print(maze_infor)
		
        return G, maze_infor