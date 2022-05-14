import basicgui, pygame, random, tkinter, sys
from tkinter import messagebox
pygame.init()

dummy_tk_window = tkinter.Tk() #because messagebox is part of tkinter, need to have a tkinter window for it otherwise it will create its own, which looks weird
dummy_tk_window.withdraw() #hiding the empty tkinter window

WINDOW_WIDTH, WINDOW_HEIGHT = 750,750
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Random Maze Game")
terminal_border = pygame.image.load(r'full filepath to fallout_terminal_border.jpg')

FPS = 10 #FPS has to be low to make more precise movements of game piece possible (higher FPS = more sensitivity)
WHITE = 255,255,255
BLACK = 0,0,0
RED = 255,0,0
GREEN = 0,255,0
DARKISH_BLUE = 0,45,255
GOLD = 255,215,0

class Cell:
    cell_number = 0
    def __init__(self, row, column):
        x = column*25 #multiplied by 25 because each cell is a 25x25 square
        y = row*25
        self._row = row #row and col provide the location of the cell on the grid
        self._col = column
        
        self._top_left_vertex = x,y
        self._top_right_vertex = x+25,y
        self._bottom_left_vertex = x,y+25
        self._bottom_right_vertex = x+25,y+25
        
        self._visited = False
        self._has_wall = [True, True, True, True] #TOP, BOTTOM, LEFT, RIGHT
        self._path_id = Cell.cell_number #path - formed from cells that can be moved between, this is just putting a number to that path of traversable cells
        Cell.cell_number += 1
        
    def find_cell_neighbors(self, all_cells_dict): 
        current_cell_location = self._row,self._col
        possible_neighbors = [(current_cell_location[0]-1,current_cell_location[1]), #above
                              (current_cell_location[0]+1,current_cell_location[1]), #below
                              (current_cell_location[0],current_cell_location[1]-1), #left
                              (current_cell_location[0],current_cell_location[1]+1)  #right
                              ]
        actual_neighbors = {}
        neighbor_types = ["ABOVE", "BELOW", "LEFT", "RIGHT"]
        if possible_neighbors[0] in all_cells_dict:
            actual_neighbors[neighbor_types[0]] = all_cells_dict[possible_neighbors[0]] #maps position of neighboring cell to its cell object
        if possible_neighbors[1] in all_cells_dict:
            actual_neighbors[neighbor_types[1]] = all_cells_dict[possible_neighbors[1]]
        if possible_neighbors[2] in all_cells_dict:
            actual_neighbors[neighbor_types[2]] = all_cells_dict[possible_neighbors[2]]
        if possible_neighbors[3] in all_cells_dict:
            actual_neighbors[neighbor_types[3]] = all_cells_dict[possible_neighbors[3]]
                
        return actual_neighbors     
        
    def remove_wall(self, wall_to_remove, cell_neighbors):
        if wall_to_remove == "TOP":
            if self._has_wall[0]:
                #first update this cell's wall list
                #find this cell's neighbors
                #determine if a neighbor is above, below, to left of, or to the right of this cell
                #depending on the position of the neighbor in relation to this cell, update the opposite wall in that neighbor's wall list
                    #ex: if this cell has a neighbor above it, update the wall list of that neighbor to indicate that its BOTTOM wall has been removed
                self._has_wall[0] = False
                neighbor_above = cell_neighbors["ABOVE"]
                neighbor_above.has_wall[1] = False
                
        elif wall_to_remove == "BOTTOM":
            if self._has_wall[1]:
                self._has_wall[1] = False
                neighbor_below = cell_neighbors["BELOW"]
                neighbor_below.has_wall[0] = False
 
        elif wall_to_remove == "LEFT":
            if self._has_wall[2]:
                self._has_wall[2] = False
                neighbor_left = cell_neighbors["LEFT"]
                neighbor_left.has_wall[3] = False

        else:
            if self._has_wall[3]:
                self._has_wall[3] = False 
                neighbor_right = cell_neighbors["RIGHT"]
                neighbor_right.has_wall[2] = False
                 
    @property
    def row(self):
        return self._row
    @property
    def col(self):
        return self._col
        
    @property
    def top_left_vertex(self):
        return self._top_left_vertex
        
    @property
    def top_right_vertex(self):
        return self._top_right_vertex
        
    @property
    def bottom_left_vertex(self):
        return self._bottom_left_vertex
        
    @property
    def bottom_right_vertex(self):
        return self._bottom_right_vertex
        
    @property
    def has_wall(self):
        return self._has_wall
        
    @has_wall.setter
    def has_wall(self, index, wall_bool):
        self._has_wall[index] = wall_bool
        
    @property
    def visited(self):
        return self._visited
        
    @visited.setter
    def visited(self, visited_bool):
        self._visited = visited_bool
        
    @property
    def path_id(self):
        return self._path_id
        
    @path_id.setter
    def path_id(self, new_id):
        self._path_id = new_id

class Grid:
    def __init__(self, size):
        cell_locs = []
        cell_objects = []
        self.rows = size[0]//25 #cells are 25 pixels by 25 pixels so number of rows and cols is equal to surface dimensions/25
        self.cols = size[1]//25
        for r in range (self.rows): 
            for c in range(self.cols):
                cell_locs.append((r,c))
                cell_objects.append(Cell(r,c))
        self._cells = dict(zip(cell_locs, cell_objects)) #this maps the (row,column) location of a cell to that specific cell object's location in memory
        self._adjacency_list = {} #this maps each cell object to every one of its neighbors (neighbors here being cells that have a wall missing such that one can travel between them)
        self._generation_algo_used = None #this is the name of the algorithm used to generate a maze from the grid, None if maze hasn't been generated
        
    #function for getting the cell objects of a particular row number    
    def get_cells_in_row(self, row_number):
        cell_locs = []
        for col in range (self.cols):
            location = (row_number, col)
            cell_locs.append(location)

        cells = []
        for cell_location in cell_locs:
            cells.append(self._cells[cell_location])
        return cells
        
    #internal/private function for generating the adjacency list of the cells's of the maze    
    def _generate_adjacency_list(self):       
        for key in self._cells:
            current_cell= self._cells[key]
            possible_neighbors = current_cell.find_cell_neighbors(self._cells)
            actual_neighbors = []
            if current_cell.has_wall[0] == False:
                actual_neighbors.append(possible_neighbors["ABOVE"])
            if current_cell.has_wall[1] == False:
                actual_neighbors.append(possible_neighbors["BELOW"])
            if current_cell.has_wall[2] == False:
                actual_neighbors.append(possible_neighbors["LEFT"])
            if current_cell.has_wall[3] == False:
                actual_neighbors.append(possible_neighbors["RIGHT"])
            self._adjacency_list[current_cell] = actual_neighbors
            
    #internal/private function for generating a maze using Eller's algorithm    
    def _ellers_algorithm(self, maze_seed):
        random.seed(maze_seed)
        
        #going row by row and merging cells
        for row in range (self.rows):
        
            #mapping the path ID of all the cells in the current row to all cells in that particular path
            cells_in_row = self.get_cells_in_row(row)
            paths_dict = {}
            for cell in cells_in_row:
                if paths_dict.get(cell.path_id) == None: #if a key-value pair between a specific path id and a cell doesn't exist
                    cells_in_path = [cell]
                    paths_dict[cell.path_id] = cells_in_path
                else: #if there is already an existing key-value pair for a specific path id and a cell
                    paths_dict[cell.path_id].append(cell)
            
            #if not in the final row of the maze
            if row != self.rows-1:
                #randomy deciding (for each cell) to merge that cell with the cell to the right of it
                for cell_index in range(len(cells_in_row)-1): #skip the last cell in the row because it won't have an adjacent cell to even try to merge with
                    current_cell = cells_in_row[cell_index]
                    adjacent_cell = self._cells[current_cell.row,current_cell.col+1]
                    if current_cell.path_id != adjacent_cell.path_id:
                        action = random.randrange(0,2)
                        if action == 1: #merge cells
                            paths_dict[current_cell.path_id] = paths_dict[current_cell.path_id] + paths_dict[adjacent_cell.path_id] #combines the path lists of the cells (these lists contain the cell objects the cell is merged with)
                            paths_dict.pop(adjacent_cell.path_id) #remove the cell-to-be-merged's key-value pair from dictionary because it is going to be merged with an existing key-value pair (there can't be the same key twice in a dictionary)
                            for cell in paths_dict[current_cell.path_id]: #updates the path_ids of all the cell objects in the newly merged list to match current_cell's path_id (might be a bit redundant but can fix later)
                                cell.path_id = current_cell.path_id
                            cell_neighbors_dict = current_cell.find_cell_neighbors(self._cells)
                            current_cell.remove_wall("RIGHT", cell_neighbors_dict)
                            
                #randomly deciding for randomly chosen cells in each path to remove that cell's bottom wall to establish a downward connection (aka extend the path) to a cell in the next row            
                for key in paths_dict:
                    path_list = paths_dict[key]
                    if len(path_list) > 1: #if a path has more than 1 cell in that row
                        numb_downward_connections = random.randrange(1, len(path_list))                                                                                                                                                                            
                        for i in range (numb_downward_connections):
                            random_cell_index = random.randrange(0, len(path_list))
                            chosen_cell = path_list[random_cell_index]
                            cell_neighbors_dict = chosen_cell.find_cell_neighbors(self._cells)
                            chosen_cell.remove_wall("BOTTOM", cell_neighbors_dict)
                            cell_below = self._cells[chosen_cell.row+1,chosen_cell.col]
                            cell_below.path_id = chosen_cell.path_id
                            path_list.remove(chosen_cell) #this is to avoid the same cell getting chosen twice and not establishing a different downward connection
                    else: #if there is only 1 cell in a path for that row
                        numb_downward_connections = 1
                        chosen_cell = path_list[0]
                        cell_neighbors_dict = chosen_cell.find_cell_neighbors(self._cells)
                        chosen_cell.remove_wall("BOTTOM", cell_neighbors_dict)
                        cell_below = self._cells[chosen_cell.row+1,chosen_cell.col]
                        cell_below.path_id = chosen_cell.path_id
             
            #if in the final row of the maze
            else:
                #merge any cells that aren't in the same path, no randomness
                for cell_index in range(len(cells_in_row)-1):
                    current_cell = cells_in_row[cell_index]
                    adjacent_cell = self._cells[current_cell.row,current_cell.col+1]
                    if current_cell.path_id != adjacent_cell.path_id:
                        paths_dict[current_cell.path_id] = paths_dict[current_cell.path_id] + paths_dict[adjacent_cell.path_id]
                        paths_dict.pop(adjacent_cell.path_id)
                        for cell in paths_dict[current_cell.path_id]:
                            cell.path_id = current_cell.path_id
                        cell_neighbors_dict = current_cell.find_cell_neighbors(self._cells)
                        current_cell.remove_wall("RIGHT", cell_neighbors_dict)
                        adjacent_cell.path_id = current_cell.path_id
        self._generate_adjacency_list()
        
    #internal/private function for generating a maze using the Aldous-Broder algorithm    
    def _aldous_broder_algorithm(self, maze_seed):
        random.seed(maze_seed)
        cell_keys = list(self._cells)
        rand_cell_key_index = random.randrange(0,len(cell_keys))
        rand_key = cell_keys[rand_cell_key_index]
        current_cell = self._cells[rand_key]
        current_cell.visited = True
        total_cells_in_maze = self.rows*self.cols
        visited_cells = 1
    
        while visited_cells != total_cells_in_maze:
            cell_neighbors_dict = current_cell.find_cell_neighbors(self._cells)
            possible_keys = []
            for key in cell_neighbors_dict:
                possible_keys.append(key)
            random_key_index = random.randrange(len(possible_keys))
            chosen_neighbor = cell_neighbors_dict[possible_keys[random_key_index]]
            if chosen_neighbor.visited == False:
                chosen_neighbor_pos = possible_keys[random_key_index]
                if chosen_neighbor_pos == "ABOVE":
                    current_cell.remove_wall("TOP", cell_neighbors_dict)
                elif chosen_neighbor_pos == "BELOW":
                    current_cell.remove_wall("BOTTOM", cell_neighbors_dict)
                elif chosen_neighbor_pos == "LEFT":
                    current_cell.remove_wall("LEFT", cell_neighbors_dict)
                else:
                    current_cell.remove_wall("RIGHT", cell_neighbors_dict)
                chosen_neighbor.visited = True
                visited_cells+=1
            current_cell = chosen_neighbor
        self._generate_adjacency_list()
        
    #internal/private function for generating a maze using the Growing Tree algorithm    
    def _growing_tree_algorithm(self, maze_seed):
        random.seed(maze_seed)
        cell_keys = list(self._cells)
        rand_cell_key_index = random.randrange(0,len(cell_keys))
        rand_key = cell_keys[rand_cell_key_index]
        exploratory_cells = [self._cells[rand_key]] #list of cells that might still have unvisited neighbors whose walls can be removed to further build the maze structure
        exploratory_cells[0].visited = True
        selection_method = random.randrange(0,101) #determines how a cell to explore from is chosen
        while exploratory_cells:
            #determining a cell in exploratory_cells to explore from
            random_cell_index = None
            if selection_method == 0: #choose the oldest cell
                random_cell_index = 0
            elif selection_method >=1 and selection_method <=45: #choose the newest cell
                random_cell_index = len(exploratory_cells)-1
            elif selection_method >=46 and selection_method <=91: #choose a random cell
                random_cell_index = random.randrange(0, len(exploratory_cells))
            else: #hybrid - choose the oldest, newest, or a random cell
                rand_selection_method = random.randrange(0,3)
                if rand_selection_method == 0: #choose the oldest cell
                    random_cell_index = 0
                elif rand_selection_method == 1: #choose the newest cell
                    random_cell_index = len(exploratory_cells)-1
                else: #choose a random cell
                    random_cell_index = random.randrange(0, len(exploratory_cells))
                    
            #determining if a cell can be explored
            #a cell with unvisited neighbors can be explored because those unvisited neighbors can have walls removed to expand the maze without creating loops/cycles
            #a cell without unvisited neighbors can't be explored because removing any walls from the visited neighbors would introduce loops/cycles and the maze wouldn't be perfect
            #eventually all cells will have been visited (had a wall removed) so there will be no way to remove any walls without creating loops/cycles (generation ends at this point)
            rand_cell = exploratory_cells[random_cell_index]
            neighbors = rand_cell.find_cell_neighbors(self._cells)
            unvisited_neighbors = []
            for key in neighbors:
                if neighbors[key].visited == False:
                    unvisited_neighbors.append(neighbors[key])
            
            #none of the walls can be removed between rand_cell's and any of its neighbors without creating loops/cycles
            if len(unvisited_neighbors) == 0:
                exploratory_cells.remove(rand_cell)
                
            #a wall between rand_cell and one of its neighbors can be removed without creating loops/cycles
            else:
                rand_neighbor_index = random.randrange(0,len(unvisited_neighbors))
                rand_neighbor = unvisited_neighbors[rand_neighbor_index]
                position_keys = neighbors.keys()
                neighbor_pos = None
                for key in position_keys:
                    if neighbors[key] == rand_neighbor:
                        neighbor_pos = key
                        break
                if neighbor_pos == "ABOVE":
                    rand_cell.remove_wall("TOP", neighbors)
                elif neighbor_pos == "BELOW":
                    rand_cell.remove_wall("BOTTOM", neighbors)
                elif neighbor_pos == "LEFT":
                    rand_cell.remove_wall("LEFT", neighbors)
                else:
                    rand_cell.remove_wall("RIGHT", neighbors)
                #don't remove rand_cell from exploratory_cells yet because it may still have unvisited neighbors (only one was chosen to remove a wall from, could still be more)
                exploratory_cells.append(rand_neighbor)
                rand_neighbor.visited = True
        self._generate_adjacency_list()
        
    #internal/private function for generating a maze using the Hunt and Kill algorithm    
    def _hunt_and_kill_algorithm(self, maze_seed):
        random.seed(maze_seed)
        cell_keys = list(self._cells)
        rand_cell_key_index = random.randrange(0,len(cell_keys))
        rand_key = cell_keys[rand_cell_key_index]
        current_cell = self._cells[rand_key]
        visited_cells = [current_cell]
        while len(visited_cells) != len(self._cells):
            neighbors = current_cell.find_cell_neighbors(self._cells)
            unvisited_neighbors = []
            for key in neighbors:
                if neighbors[key] not in visited_cells:
                    unvisited_neighbors.append(neighbors[key])
                
            if len(unvisited_neighbors) > 0:
                rand_unvis_neighbor_index = random.randrange(0,len(unvisited_neighbors))
                rand_neighbor = unvisited_neighbors[rand_unvis_neighbor_index]
                rand_neighbor_pos = None
                for key in neighbors:
                    if neighbors[key] == rand_neighbor:
                        rand_neighbor_pos = key
                        break
                if rand_neighbor_pos == "ABOVE":
                    current_cell.remove_wall("TOP",neighbors)
                elif rand_neighbor_pos == "BELOW":
                    current_cell.remove_wall("BOTTOM",neighbors)
                elif rand_neighbor_pos == "LEFT":
                    current_cell.remove_wall("LEFT",neighbors)
                else:
                    current_cell.remove_wall("RIGHT",neighbors)
                visited_cells.append(rand_neighbor)
                current_cell = rand_neighbor
            
            else:
                #"hunting" a random cell and finding neighbor cells to "kill" during the kill phase
                for key in self._cells:
                    hunted_cell = self._cells[key]
                    if hunted_cell not in visited_cells:
                        possible_killable_neighbors = hunted_cell.find_cell_neighbors(self._cells)
                        killable_neighbors = []
                        for key in possible_killable_neighbors:
                            if possible_killable_neighbors[key] in visited_cells:
                                killable_neighbors.append(possible_killable_neighbors[key])
                        if len(killable_neighbors) > 0: #this is to prevent an unvisited cell with no visited neighbors from being used because then things will break
                    
                            #"Killing" a random neighbor cell
                            rand_killable_neighbor_index = random.randrange(0,len(killable_neighbors))
                            rand_killable_neighbor = killable_neighbors[rand_killable_neighbor_index]
                            rand_killable_neighbor_pos = None
                            for key in possible_killable_neighbors:
                                if possible_killable_neighbors[key] == rand_killable_neighbor:
                                    rand_killable_neighbor_pos = key
                                    break
                    
                            #Creating a path between the hunted cell and the randomly killed neighbor, then resuming normal path making from hunted_cell
                            if rand_killable_neighbor_pos == "ABOVE":
                                hunted_cell.remove_wall("TOP",possible_killable_neighbors)
                            elif rand_killable_neighbor_pos == "BELOW":
                                hunted_cell.remove_wall("BOTTOM",possible_killable_neighbors)
                            elif rand_killable_neighbor_pos == "LEFT":
                                hunted_cell.remove_wall("LEFT",possible_killable_neighbors)
                            else:
                                hunted_cell.remove_wall("RIGHT",possible_killable_neighbors)
                            visited_cells.append(hunted_cell)
                            current_cell = hunted_cell
                            break
        self._generate_adjacency_list()
        
        
    #function for calling to maze generation functions that remove walls such that a maze-like structure is created from the grid    
    def generate_maze(self, maze_algo, maze_seed):
        random.seed(maze_seed) #have to do this so that, if random generation is selected, the same algorithm is chosen for initial generation and also solution displaying (solution maze is different otherwise)
        if maze_algo == "RANDOM":
            algorithm = random.randrange(0,4)
            if algorithm == 0:
                self._generation_algo_used = "ELLER'S"
                self._ellers_algorithm(maze_seed)
            elif algorithm == 1:
                self._generation_algo_used = "ALDOUS-BRODER"
                self._aldous_broder_algorithm(maze_seed)
            elif algorithm == 2:
                self._generation_algo_used = "GROWING TREE"
                self._growing_tree_algorithm(maze_seed)
            else:
                self._generation_algo_used = "HUNT & KILL"
                self._hunt_and_kill_algorithm(maze_seed)
        elif maze_algo == "ELLER'S":
            self._generation_algo_used = "ELLER'S"
            self._ellers_algorithm(maze_seed)
        elif maze_algo == "ALDOUS-BRODER":
            self._generation_algo_used = "ALDOUS-BRODER"
            self._aldous_broder_algorithm(maze_seed)
        elif maze_algo == "GROWING TREE":
            self._generation_algo_used = "GROWING TREE"
            self._growing_tree_algorithm(maze_seed)
        else:
            self._generation_algo_used = "HUNT & KILL"
            self._hunt_and_kill_algorithm(maze_seed)
         
    #function that uses a slightly modified DFS to find the path from start_cell to target_cell
    def find_path_from(self, start_cell, target_cell):
        current_cell = start_cell
        path = [current_cell]
        
        #inner function for finding all children cells (cells below start_cell on a tree) reachable from start_cell 
        def depth_first_search(start_cell):
            stack = []
            visited_cells = []
            stack.append(start_cell)
            while stack:
                current_cell = stack.pop()
                if current_cell not in visited_cells:
                    visited_cells.append(current_cell)
                    neighbors = self._adjacency_list[current_cell]
                    for neighbor in neighbors:
                        #condition below prevents searching backwards from start_cell, which would result in every cell having a path to target_cell
                        #which would also not give the optimal path from start_cell to target_cell (might include certain turns/moves that go to dead ends)
                        #dead ends cells cause infinite loops without this condition because of the if neighbor not in path: condition below (dead end cells will not have any neighbors not in path if able to search backwards)
                        if neighbor not in visited_cells and neighbor not in path: 
                            stack.append(neighbor)
            return visited_cells
            
        #for every cell, perform a downward-only DFS from each of its neighbors and see if you can reach target_cell from any of them
        #perfect mazes only have one path from one cell to another so only one neighbor will work
        #if you can, add that neighbor to the path list and repeat the first step for its neighbors
        #in the end, only the cells that can reach target_cell will be in the path
        while target_cell not in path:
            #to speed things up, maybe not even both with a DFS for a cell with only one neighbor?
            for neighbor in self._adjacency_list[current_cell]:
                if neighbor not in path:
                    reachable_cells = depth_first_search(neighbor)
                    if target_cell in reachable_cells:
                        path.append(neighbor)
                        current_cell = neighbor
                        break
        return path

    @property
    def cells(self):
        return self._cells
        
    @property
    def adjacency_list(self):
        return self._adjacency_list
        
    @property
    def generation_algo_used(self):
        return self._generation_algo_used

class MainMenuSurface(basicgui.Surface):
    def __init__(self):
        super().__init__((125,100),(515,500),color=BLACK)
        self._surface_header = basicgui.Label(self,(200,5),(100,25),txt="RANDOM MAZE GAME",txt_color=GREEN,txt_size=35,txt_font="couriernew")
        self._play_btn = basicgui.Button(self,(220,250),(55,25),color=BLACK,txt="PLAY",txt_color=GREEN,txt_size=20,txt_font="couriernew")
        self._settings_btn = basicgui.Button(self,(200,350),(100,25),color=BLACK,txt="SETTINGS",txt_color=GREEN,txt_size=20,txt_font="couriernew")
    
    @property
    def play_btn(self):
        return self._play_btn
        
    @property
    def settings_btn(self):
        return self._settings_btn
    
class SettingsSurface(basicgui.Surface):
    def __init__(self):
        super().__init__((125,100),(515,500),color=BLACK)
        self._surface_header = basicgui.Label(self,(200,5),(100,25),txt="SETTINGS",txt_color=GREEN,txt_size=35,txt_font="couriernew")
        self._maze_size_lbl = basicgui.Label(self,(50,125),(100,25),txt="MAZE SIZE:",txt_color=GREEN,txt_size=17,txt_align="left",txt_font="couriernew")
        self._small_maze_btn = basicgui.Button(self,(65,150),(55,25),color=BLACK,txt="SMALL",txt_color=GREEN,txt_font="couriernew")
        self._medium_maze_btn = basicgui.Button(self,(65,200),(55,25),color=BLACK,txt="MEDIUM",txt_color=GREEN,txt_font="couriernew")
        self._big_maze_btn = basicgui.Button(self,(65,250),(55,25),color=BLACK,txt="BIG",txt_color=GREEN,txt_font="couriernew")
        self._time_limit_lbl = basicgui.Label(self,(200,125),(100,25),txt="TIME LIMIT:",txt_color=GREEN,txt_size=17,txt_align="left",txt_font="couriernew")
        self._thirty_sec_btn = basicgui.Button(self,(220,150),(55,25),color=BLACK,txt="0:30",txt_color=GREEN,txt_size=17,txt_font="couriernew")
        self._forty_five_sec_btn = basicgui.Button(self,(220,200),(55,25),color=BLACK,txt="0:45",txt_color=GREEN,txt_size=17,txt_font="couriernew")
        self._sixty_sec_btn = basicgui.Button(self,(220,250),(55,25),color=BLACK,txt="1:00",txt_color=GREEN,txt_size=17,txt_font="couriernew")      
        self._gamepiece_color_lbl = basicgui.Label(self,(350,125),(100,25),txt="GAMEPIECE COLOR:",txt_color=GREEN,txt_size=17,txt_align="left",txt_font="couriernew")
        self._red_val_txtfld = basicgui.TextField(self,(365,150),(30,15),color=RED,txt="255",txt_font="couriernew")
        self._green_val_txtfld = basicgui.TextField(self,(415,150),(30,15),color=GREEN,txt="0",txt_font="couriernew")
        self._blue_val_txtfld = basicgui.TextField(self,(465,150),(30,15),color=DARKISH_BLUE,txt="0",txt_font="couriernew")
        self._adv_settings_btn = basicgui.Button(self,(200,400),(100,25),color=BLACK,txt="ADVANCED",txt_color=GREEN,txt_size=20,txt_font="couriernew")
        self._back_btn = basicgui.Button(self,(200,450),(100,25),color=BLACK,txt="BACK",txt_color=GREEN,txt_size=20,txt_font="couriernew")
        
    @property
    def small_maze_btn(self):
        return self._small_maze_btn
        
    @property
    def medium_maze_btn(self):
        return self._medium_maze_btn
        
    @property
    def big_maze_btn(self):
        return self._big_maze_btn
        
    @property
    def thirty_sec_btn(self):
        return self._thirty_sec_btn
        
    @property
    def forty_five_sec_btn(self):
        return self._forty_five_sec_btn
        
    @property
    def sixty_sec_btn(self):
        return self._sixty_sec_btn
        
    @property
    def red_val_txtfld(self):
        return self._red_val_txtfld
        
    @property
    def green_val_txtfld(self):
        return self._green_val_txtfld
        
    @property
    def blue_val_txtfld(self):
        return self._blue_val_txtfld
        
    @property
    def adv_settings_btn(self):
        return self._adv_settings_btn
        
    @property
    def back_btn(self):
        return self._back_btn
        
class AdvancedSettingsSurface(basicgui.Surface):
    def __init__(self):
        super().__init__((125,100),(515,500),color=BLACK)
        self._surface_header = basicgui.Label(self,(200,5),(100,25),txt="ADVANCED SETTINGS",txt_color=GREEN,txt_size=35,txt_font="couriernew")
        self._gen_algo_lbl = basicgui.Label(self,(25,100),(100,25),txt="MAZE ALGORITHM:",txt_color=GREEN,txt_size=17,txt_align="left",txt_font="couriernew")
        self._aldous_broder_btn = basicgui.Button(self,(40,125),(115,25),color=BLACK,txt="ALDOUS-BRODER",txt_color=GREEN,txt_font="couriernew")
        self._ellers_btn = basicgui.Button(self,(40,175),(100,25),color=BLACK,txt="ELLER'S",txt_color=GREEN,txt_font="couriernew")
        self._growing_tree_btn = basicgui.Button(self,(40,225),(100,25),color=BLACK,txt="GROWING TREE",txt_color=GREEN,txt_font="couriernew")
        self._hunt_and_kill_btn = basicgui.Button(self,(40,275),(100,25),color=BLACK,txt="HUNT AND KILL",txt_color=GREEN,txt_font="couriernew")
        self._rand_algo_btn = basicgui.Button(self,(40,325),(100,25),color=BLACK,txt="RANDOM",txt_color=GREEN,txt_font="couriernew")
        self._seed_lbl = basicgui.Label(self,(400,100),(100,25),txt="MAZE SEED:",txt_color=GREEN,txt_size=17,txt_align="left",txt_font="couriernew")
        self._seed_txtfld = basicgui.TextField(self,(400,125),(90,15),color=WHITE,txt="",txt_font="couriernew")
        self._back_btn = basicgui.Button(self,(200,450),(100,25),color=BLACK,txt="BACK",txt_color=GREEN,txt_size=20,txt_font="couriernew")
        
    @property
    def aldous_broder_btn(self):
        return self._aldous_broder_btn
        
    @property
    def ellers_btn(self):
        return self._ellers_btn
        
    @property
    def growing_tree_btn(self):
        return self._growing_tree_btn
        
    @property
    def hunt_and_kill_btn(self):
        return self._hunt_and_kill_btn
        
    @property
    def rand_algo_btn(self):
        return self._rand_algo_btn
        
    @property
    def seed_txtfld(self):
        return self._seed_txtfld
        
    @property
    def back_btn(self):
        return self._back_btn

class GameOverSurface(basicgui.Surface):
    def __init__(self):
        super().__init__((125,100),(515,500),color=BLACK)
        self._surface_header = basicgui.Label(self,(200,5),(100,25),txt="GAME OVER",txt_color=GREEN,txt_size=35,txt_font="couriernew")
        self._score_lbl = basicgui.Label(self,(125,150),(250,25),txt="Your Score: XXXX",txt_color=GREEN,txt_size=25,txt_font="couriernew")
        self._replay_btn = basicgui.Button(self,(200,250),(100,25),color=BLACK,txt="PLAY AGAIN",txt_color=GREEN,txt_size=20,txt_font="couriernew")
        self._solution_btn = basicgui.Button(self,(200,340),(100,25),color=BLACK,txt="SOLUTION",txt_color=GREEN,txt_size=20,txt_font="couriernew")
        self._main_menu_btn = basicgui.Button(self,(200,425),(100,25),color=BLACK,txt="MAIN MENU",txt_color=GREEN,txt_size=20,txt_font="couriernew")
        
    @property
    def score_lbl(self):
        return self._score_lbl
        
    @property
    def replay_btn(self):
        return self._replay_btn
        
    @property
    def solution_btn(self):
        return self._solution_btn
        
    @property
    def main_menu_btn(self):
        return self._main_menu_btn

class MazeSurface(basicgui.Surface):
    def __init__(self, top_left_vertex, dimensions):
        super().__init__(top_left_vertex,dimensions,color=BLACK)
        self._maze_grid = Grid((dimensions[0],dimensions[1]-50))
        self._surrender_btn = basicgui.Button(self,(2,dimensions[1]-25),(100,25),color=BLACK,txt="SURRENDER",txt_color=GREEN,txt_size=20,txt_font="couriernew")
        self._timer_lbl = basicgui.Label(self,(dimensions[1]//2-25,dimensions[1]-25),(50,25),color=BLACK,txt="0:00",txt_color=GREEN,txt_size=20,txt_font="couriernew")
        self._back_btn = basicgui.Button(self,(dimensions[0]-50,dimensions[1]-25),(55,25),color=BLACK,txt="BACK",txt_color=GREEN,txt_size=20,txt_font="couriernew")
        
    @property
    def maze_grid(self):
        return self._maze_grid
        
    @property
    def surrender_btn(self):
        return self._surrender_btn
        
    @property
    def timer_lbl(self):
        return self._timer_lbl
        
    @property
    def back_btn(self):
        return self._back_btn

class SoltuionDisplayerSurface(basicgui.Surface):
    def __init__(self, top_left_vertex, dimensions):
        super().__init__(top_left_vertex,dimensions,color=BLACK)
        self._maze_grid = Grid((dimensions[0],dimensions[1]-50))
        self._algo_lbl = basicgui.Label(self,(dimensions[0]//2-25,0),(50,25),color=BLACK,txt="ALGO NAME",txt_color=GREEN,txt_size=20,txt_font="couriernew")
        self._seed_lbl = basicgui.Label(self,(5,dimensions[1]-25),(100,25),color=BLACK,txt="SEED: XXXX",txt_color=GREEN,txt_size=20,txt_align="left",txt_font="couriernew")
        self._back_btn = basicgui.Button(self,(dimensions[0]-50,dimensions[1]-25),(55,25),color=BLACK,txt="BACK",txt_color=GREEN,txt_size=20,txt_font="couriernew")
        
    @property
    def maze_grid(self):
        return self._maze_grid
        
    @property
    def algo_lbl(self):
        return self._algo_lbl
        
    @property
    def seed_lbl(self):
        return self._seed_lbl
        
    @property
    def back_btn(self):
        return self._back_btn

def game_loop():
    #Creating surfaces
    main_menu = MainMenuSurface()
    settings = SettingsSurface()
    advanced_settings = AdvancedSettingsSurface()
    game_over = GameOverSurface()
    
    #General variables
    maze_size = (501,501)  #medium-sized maze by default
    maze_seed = None #just to make this accessible for later, value gets assigned later
    maze_algo = "RANDOM"
    time_limit = 30
    score = None
    current_surface = "MAIN MENU"
    clock = pygame.time.Clock()
    running = True
    
    while running:  
        if current_surface == "MAIN MENU":
            window.fill(BLACK) #this draws over anything previously drawn, effectively erasing it
            main_menu.prepare()
            window.blit(terminal_border,(0,0))
            window.blit(main_menu,main_menu.coords) #this works because of the proxy object created in basicgui that stores the dimensions of the surface
            pygame.display.flip()
            
            while current_surface == "MAIN MENU" and running == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
                    #play_btn event handler
                    elif main_menu.play_btn.was_clicked(event):
                        current_surface = "MAZE"
                        
                    #settings_btn event handler
                    elif main_menu.settings_btn.was_clicked(event):
                        current_surface = "SETTINGS"
                       
        elif current_surface == "MAZE":
            window.fill(BLACK)
            
            #gettings coordinates of surface's top left vertex to draw from
            surface_top_left_x = 0
            surface_top_left_y = 0
            if maze_size[0] == 401:
                surface_top_left_x = 175
                surface_top_left_y = 150
            elif maze_size[0] == 501:
                surface_top_left_x = 125
                surface_top_left_y = 100
            else:
                surface_top_left_x = 100
                surface_top_left_y = 75
            maze_surface = MazeSurface((surface_top_left_x,surface_top_left_y),(maze_size[0],maze_size[1]+50))
            
            #determining seed value for maze and using it to generate a maze
            if advanced_settings.seed_txtfld.text == "":
                maze_seed = random.randrange(sys.maxsize)
            else:
                maze_seed = int(advanced_settings.seed_txtfld.text)
            maze_surface.maze_grid.generate_maze(maze_algo, maze_seed)
            maze_surface.maze_grid.cells[((maze_size[0]//25)-1,(maze_size[1]//25)-1)].has_wall[3] = False #removing the right wall of the end cell to indicate where to go
            
            #laying out (but not displaying) everything on maze_surface
            maze_surface.prepare() #because prepare() fills the surface with its background color, it is hiding the lines and gamepiece if they are drawn before calling it so it has to be called first
            window.blit(terminal_border,(0,0))
            #get each cell object
            #go through its walls list
            #if it has a wall, get the vertices for that wall and draw a white line connecting them on the grid
            #otherwise, if the wall is missing, don't draw anything
            for key in maze_surface.maze_grid.cells:
                cell = maze_surface.maze_grid.cells[key]
                if cell.has_wall[0] == True:
                    pygame.draw.line(maze_surface,GREEN,cell.top_left_vertex,cell.top_right_vertex)
                if cell.has_wall[1] == True:
                    pygame.draw.line(maze_surface,GREEN,cell.bottom_left_vertex,cell.bottom_right_vertex)
                if cell.has_wall[2] == True:
                    pygame.draw.line(maze_surface,GREEN,cell.bottom_left_vertex,cell.top_left_vertex)
                if cell.has_wall[3] == True:
                    pygame.draw.line(maze_surface,GREEN,cell.top_right_vertex,cell.bottom_right_vertex)
                               
            #creating a timer event to limit how long user can play        
            timer_event = pygame.event.Event(pygame.USEREVENT, attr1="timer_countdown")
            pygame.event.post(timer_event)
            pygame.time.set_timer(timer_event, 1000)
                        
            #variables for position of the gamepiece as well as its RGB color
            gamepiece_x = 1
            gamepiece_y = 1
            gamepiece_color = (int(settings.red_val_txtfld.text),int(settings.green_val_txtfld.text),int(settings.blue_val_txtfld.text))
            
            #keeping track of the cell the user is currently in
            row = 0
            col = 0
            current_cell = (row,col)
            end_cell = ((maze_size[0]//25)-1,(maze_size[1]//25)-1)
            
            #variables for determining user's score at the end
            time_left = time_limit
            total_moves = 0
            score = 0
            
            #displaying maze_surface on the screen
            window.blit(maze_surface,maze_surface.coords)
            pygame.display.flip()
            
            while current_surface == "MAZE" and running == True:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
                    #timer_event event handler    
                    elif event == timer_event:
                        time_left-=1
                        maze_surface.timer_lbl.text = f'0:{time_left:02d}'
                        if time_left == 0:
                            pygame.time.set_timer(timer_event,0)
                            score = maze_size[0]-total_moves
                            current_surface = "GAME OVER"
                            
                    #back_btn event handler        
                    elif maze_surface.back_btn.was_clicked(event):
                        pygame.time.set_timer(timer_event,0)
                        current_surface = "MAIN MENU"
                        
                    #surrender_btn event handler    
                    elif maze_surface.surrender_btn.was_clicked(event):
                        pygame.time.set_timer(timer_event,0)
                        score = 0
                        current_surface = "GAME OVER"
                        
                #if time hasn't run out or the user hasn't pressed the back or surrender buttons       
                if current_surface == "MAZE":
                    if current_cell == end_cell:
                        pygame.time.set_timer(timer_event,0)
                        score = (maze_size[0]+time_left)-total_moves
                        current_surface = "GAME OVER"
                    else:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_LEFT]:
                            if maze_surface.maze_grid.cells[current_cell].has_wall[2] == False:
                                current_cell = (maze_surface.maze_grid.cells[current_cell].row,maze_surface.maze_grid.cells[current_cell].col-1)
                                gamepiece_x-=25
                                total_moves+=1
                        elif keys[pygame.K_RIGHT]:
                            if maze_surface.maze_grid.cells[current_cell].has_wall[3] == False:
                                current_cell = (maze_surface.maze_grid.cells[current_cell].row,maze_surface.maze_grid.cells[current_cell].col+1)
                                gamepiece_x+=25
                                total_moves+=1                                
                        elif keys[pygame.K_UP]:
                            if maze_surface.maze_grid.cells[current_cell].has_wall[0] == False:
                                current_cell = (maze_surface.maze_grid.cells[current_cell].row-1,maze_surface.maze_grid.cells[current_cell].col)
                                gamepiece_y-=25
                                total_moves+=1
                        elif keys[pygame.K_DOWN]:
                            if maze_surface.maze_grid.cells[current_cell].has_wall[1] == False:
                                current_cell = (maze_surface.maze_grid.cells[current_cell].row+1,maze_surface.maze_grid.cells[current_cell].col)
                                gamepiece_y+=25
                                total_moves+=1
                                
                        #updating surface to display any changes
                        maze_surface.prepare()
                        for key in maze_surface.maze_grid.cells:
                            cell = maze_surface.maze_grid.cells[key]
                            if cell.has_wall[0] == True:
                                pygame.draw.line(maze_surface,GREEN,cell.top_left_vertex,cell.top_right_vertex)
                            if cell.has_wall[1] == True:
                                pygame.draw.line(maze_surface,GREEN,cell.bottom_left_vertex,cell.bottom_right_vertex)
                            if cell.has_wall[2] == True:
                                pygame.draw.line(maze_surface,GREEN,cell.bottom_left_vertex,cell.top_left_vertex)
                            if cell.has_wall[3] == True:
                                pygame.draw.line(maze_surface,GREEN,cell.top_right_vertex,cell.bottom_right_vertex)
                        pygame.draw.rect(maze_surface, gamepiece_color,(gamepiece_x,gamepiece_y,24,24))
                        window.blit(maze_surface,maze_surface.coords)
                        pygame.display.flip()
                                    
        elif current_surface == "SETTINGS":
            window.fill(BLACK)
            settings.prepare()
            window.blit(terminal_border,(0,0))
            window.blit(settings,settings.coords)
            pygame.display.flip()
            
            active_txtfld = None #stores the TextField object that was clicked
            txtfld_active = False #indicates if a TextField is active, doesn't matter which one
            
            while current_surface == "SETTINGS" and running == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
                    #small_maze_btn event handler    
                    elif settings.small_maze_btn.was_clicked(event):
                        maze_size = (401,401)
                        messagebox.showinfo("Settings Change", "Small maze size selected.")
                        if txtfld_active:
                            if active_txtfld.text == "":
                                active_txtfld.text = "0"
                            elif int(active_txtfld.text) > 255:
                                active_txtfld.text = "255"
                            else:
                                active_txtfld.text = str(int(active_txtfld.text))
                        txtfld_active = False
                        
                    #medium_maze_btn event handler    
                    elif settings.medium_maze_btn.was_clicked(event):
                        maze_size = (501,501)
                        messagebox.showinfo("Settings Change", "Medium maze size selected.")
                        if txtfld_active:
                            if active_txtfld.text == "":
                                active_txtfld.text = "0"
                            elif int(active_txtfld.text) > 255:
                                active_txtfld.text = "255"
                            else:
                                active_txtfld.text = str(int(active_txtfld.text))
                        txtfld_active = False
                        
                    #big_maze_btn event handler    
                    elif settings.big_maze_btn.was_clicked(event):
                        maze_size = (551,551)
                        messagebox.showinfo("Settings Change", "Big maze size selected.")
                        if txtfld_active:
                            if active_txtfld.text == "":
                                active_txtfld.text = "0"
                            elif int(active_txtfld.text) > 255:
                                active_txtfld.text = "255"
                            else:
                                active_txtfld.text = str(int(active_txtfld.text))
                        txtfld_active = False
                        
                    #thirty_sec_btn event handler    
                    elif settings.thirty_sec_btn.was_clicked(event):
                        time_limit = 30
                        messagebox.showinfo("Settings Change", "30 second time limit selected.")
                        if txtfld_active:
                            if active_txtfld.text == "":
                                active_txtfld.text = "0"
                            elif int(active_txtfld.text) > 255:
                                active_txtfld.text = "255"
                            else:
                                active_txtfld.text = str(int(active_txtfld.text))
                        txtfld_active = False
                        
                    #forty_five_sec_btn event handler    
                    elif settings.forty_five_sec_btn.was_clicked(event):
                        time_limit = 45
                        messagebox.showinfo("Settings Change", "45 second time limit selected.")
                        if txtfld_active:
                            if active_txtfld.text == "":
                                active_txtfld.text = "0"
                            elif int(active_txtfld.text) > 255:
                                active_txtfld.text = "255"
                            else:
                                active_txtfld.text = str(int(active_txtfld.text))
                        txtfld_active = False
                        
                    #sixty_sec_btn event handler    
                    elif settings.sixty_sec_btn.was_clicked(event):
                        time_limit = 60
                        messagebox.showinfo("Settings Change", "1 minute time limit selected.")
                        if txtfld_active:
                            if active_txtfld.text == "":
                                active_txtfld.text = "0"
                            elif int(active_txtfld.text) > 255:
                                active_txtfld.text = "255"
                            else:
                                active_txtfld.text = str(int(active_txtfld.text))
                        txtfld_active = False
                        
                    #red_val_txtfld event handler    
                    elif settings.red_val_txtfld.was_clicked(event):
                        if txtfld_active: #this is in case the user switches from one TextField to another without hitting enter in the first TextField
                            previously_active_txtfld = active_txtfld
                            if previously_active_txtfld.text == "":
                                previously_active_txtfld.text = "0"
                            elif int(previously_active_txtfld.text) > 255:
                                previously_active_txtfld.text = "255"
                            else:
                                previously_active_txtfld.text = str(int(previously_active_txtfld.text))
                        active_txtfld = settings.red_val_txtfld
                        txtfld_active = True
                        
                    #green_val_txtfld event handler    
                    elif settings.green_val_txtfld.was_clicked(event):
                        if txtfld_active:
                            previously_active_txtfld = active_txtfld
                            if previously_active_txtfld.text == "":
                                previously_active_txtfld.text = "0"
                            elif int(previously_active_txtfld.text) > 255:
                                previously_active_txtfld.text = "255"
                            else:
                                previously_active_txtfld.text = str(int(previously_active_txtfld.text))
                        active_txtfld = settings.green_val_txtfld
                        txtfld_active = True
                        
                    #blue_val_txtfld event handler    
                    elif settings.blue_val_txtfld.was_clicked(event):
                        if txtfld_active:
                            previously_active_txtfld = active_txtfld
                            if previously_active_txtfld.text == "":
                                previously_active_txtfld.text = "0"
                            elif int(previously_active_txtfld.text) > 255:
                                previously_active_txtfld.text = "255"
                            else:
                                previously_active_txtfld.text = str(int(previously_active_txtfld.text))
                        active_txtfld = settings.blue_val_txtfld
                        txtfld_active = True
                    
                    #event handler for if a key was pressed after a TextField was clicked on    
                    elif event.type == pygame.KEYDOWN and txtfld_active == True: 
                        if event.key == pygame.K_RETURN:
                            if active_txtfld.text != "": 
                                if int(active_txtfld.text) >= 0 and int(active_txtfld.text) <= 255: #RGB values have to be between 0-255
                                    active_txtfld.text = str(int(active_txtfld.text)) #this is in case a number like 011 is entered, which is a valid number but looks weird, so int cast fixes it
                                else:
                                    active_txtfld.text = "255"
                            else:
                                active_txtfld.text = "0"
                            txtfld_active = False #because enter was pressed, user is done typing now
                        elif event.key == pygame.K_BACKSPACE:
                            active_txtfld.text = active_txtfld.text[:-1]
                        elif event.unicode.isdigit():
                            active_txtfld.text += event.unicode
                            
                    #adv_settings_btn event handler        
                    elif settings.adv_settings_btn.was_clicked(event):
                        current_surface = "ADVANCED SETTINGS"
                        if txtfld_active:
                            if active_txtfld.text == "":
                                active_txtfld.text = "0"
                            elif int(active_txtfld.text) > 255:
                                active_txtfld.text = "255"
                            else:
                                active_txtfld.text = str(int(active_txtfld.text))
                        txtfld_active = False
                        
                    #back_btn event handler    
                    elif settings.back_btn.was_clicked(event):
                        current_surface = "MAIN MENU"
                        if txtfld_active:
                            if active_txtfld.text == "":
                                active_txtfld.text = "0"
                            elif int(active_txtfld.text) > 255:
                                active_txtfld.text = "255"
                            else:
                                active_txtfld.text = str(int(active_txtfld.text))
                        txtfld_active = False    
                        
                #updating surface to display any changes        
                settings.prepare()
                window.blit(settings,settings.coords)
                pygame.display.flip()
                              
        elif current_surface == "ADVANCED SETTINGS":
            window.fill(BLACK)
            advanced_settings.prepare()
            window.blit(terminal_border,(0,0))
            window.blit(advanced_settings,advanced_settings.coords)
            pygame.display.flip()
            
            active_txtfld = None #stores the TextField object that was clicked
            txtfld_active = False #indicates if a TextField is active, doesn't matter which one
            
            while current_surface == "ADVANCED SETTINGS" and running == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
                    #aldous_broder_btn event handler
                    elif advanced_settings.aldous_broder_btn.was_clicked(event):
                        maze_algo = "ALDOUS-BRODER"
                        messagebox.showinfo("Advanced Settings Change", "Aldous-Broder generation algorithm selected.")
                        if txtfld_active:
                            if active_txtfld.text != "":
                                active_txtfld.text = str(int(active_txtfld.text[:10]))
                        txtfld_active = False
                        
                    #ellers_btn event handler    
                    elif advanced_settings.ellers_btn.was_clicked(event):
                        maze_algo = "ELLER'S"
                        messagebox.showinfo("Advanced Settings Change", "Eller's generation algorithm selected.")
                        if txtfld_active:
                            if active_txtfld.text != "":
                                active_txtfld.text = str(int(active_txtfld.text[:10]))
                        txtfld_active = False
                        
                    #growing_tree_btn event handler    
                    elif advanced_settings.growing_tree_btn.was_clicked(event):
                        maze_algo = "GROWING TREE"
                        messagebox.showinfo("Advanced Settings Change", "Growing Tree generation algorithm selected.")
                        if txtfld_active:
                            if active_txtfld.text != "":
                                active_txtfld.text = str(int(active_txtfld.text[:10]))
                        txtfld_active = False
                        
                    #hunt_and_kill_btn event handler    
                    elif advanced_settings.hunt_and_kill_btn.was_clicked(event):
                        maze_algo = "HUNT AND KILL"
                        messagebox.showinfo("Advanced Settings Change", "Hunt and Kill generation algorithm selected.")
                        if txtfld_active:
                            if active_txtfld.text != "":
                                active_txtfld.text = str(int(active_txtfld.text[:10]))
                        txtfld_active = False
                        
                    #rand_algo_btn event handler    
                    elif advanced_settings.rand_algo_btn.was_clicked(event):
                        maze_algo = "RANDOM"
                        messagebox.showinfo("Advanced Settings Change", "Random generation algorithm selected.")  
                        if txtfld_active:
                            if active_txtfld.text != "":
                                active_txtfld.text = str(int(active_txtfld.text[:10]))
                        txtfld_active = False
                        
                    #seed_txtfld event handler    
                    elif advanced_settings.seed_txtfld.was_clicked(event):
                        active_txtfld = advanced_settings.seed_txtfld
                        txtfld_active = True
                        
                    #event handler for if a key was pressed after a TextField was clicked on   
                    elif event.type == pygame.KEYDOWN and txtfld_active == True: #if a key was pressed after a TextField was clicked on                 
                        if event.key == pygame.K_RETURN:
                            if active_txtfld.text != "":
                                active_txtfld.text = str(int(active_txtfld.text[:10])) #max seed length is 10 so slice everything off after 8th integer
                            txtfld_active = False #because enter was pressed, user is done typing now
                        elif event.key == pygame.K_BACKSPACE:
                            active_txtfld.text = active_txtfld.text[:-1]
                        elif event.unicode.isdigit():
                            active_txtfld.text += event.unicode
                            
                    #back_btn event handler    
                    elif advanced_settings.back_btn.was_clicked(event):
                        current_surface = "SETTINGS"
                        if txtfld_active:
                            if active_txtfld.text != "": #have to still check if text is empty otherwise int cast will crash program
                                active_txtfld.text = str(int(active_txtfld.text[:10]))
                        txtfld_active = False

                #updating surface to display any changes            
                advanced_settings.prepare()
                window.blit(advanced_settings,advanced_settings.coords)
                pygame.display.flip()
                              
        elif current_surface == "GAME OVER":
            window.fill(BLACK)
            game_over.score_lbl.text = "YOUR SCORE: %s" % (str(score))
            game_over.prepare()
            window.blit(terminal_border,(0,0))
            window.blit(game_over,game_over.coords)
            pygame.display.flip()
            
            while current_surface == "GAME OVER" and running == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
                    #replay_btn event handler    
                    elif game_over.replay_btn.was_clicked(event):
                        current_surface = "MAZE"
                        
                    #main_menu_btn event handler    
                    elif game_over.main_menu_btn.was_clicked(event):
                        current_surface = "MAIN MENU"
                        
                    #solution_btn event handler    
                    elif game_over.solution_btn.was_clicked(event):
                        current_surface = "SOLUTION DISPLAYER"
            
        elif current_surface == "SOLUTION DISPLAYER":
            window.fill(BLACK)
            surface_top_left_x = 0
            surface_top_left_y = 0
            if maze_size[0] == 401:
                surface_top_left_x = 175
                surface_top_left_y = 150
            elif maze_size[0] == 501:
                surface_top_left_x = 125
                surface_top_left_y = 100
            else:
                surface_top_left_x = 100
                surface_top_left_y = 75
            solution_displayer_surface = SoltuionDisplayerSurface((surface_top_left_x,surface_top_left_y),(maze_size[0],maze_size[1]+50))
            solution_displayer_surface.maze_grid.generate_maze(maze_algo,maze_seed)
            solution_displayer_surface.maze_grid.cells[((maze_size[0]//25)-1,(maze_size[1]//25)-1)].has_wall[3] = False
            
            solution_displayer_surface.algo_lbl.text = solution_displayer_surface.maze_grid.generation_algo_used
            solution_displayer_surface.seed_lbl.text = "SEED: %s" % (str(maze_seed))
            solution_displayer_surface.prepare()
            window.blit(terminal_border,(0,0))
            #get each cell object
            #go through its walls list
            #if it has a wall, get the vertices for that wall and draw a white line connecting them on the grid
            #otherwise, if the wall is missing, don't draw anything
            for key in solution_displayer_surface.maze_grid.cells:
                cell = solution_displayer_surface.maze_grid.cells[key]
                if cell.has_wall[0] == True:
                    pygame.draw.line(solution_displayer_surface,GREEN,cell.top_left_vertex,cell.top_right_vertex)
                if cell.has_wall[1] == True:
                    pygame.draw.line(solution_displayer_surface,GREEN,cell.bottom_left_vertex,cell.bottom_right_vertex)
                if cell.has_wall[2] == True:
                    pygame.draw.line(solution_displayer_surface,GREEN,cell.bottom_left_vertex,cell.top_left_vertex)
                if cell.has_wall[3] == True:
                    pygame.draw.line(solution_displayer_surface,GREEN,cell.top_right_vertex,cell.bottom_right_vertex)
                    
            #figuring out path from start_cell_loc to end_cell_loc
            start_cell_loc = (0,0)
            end_cell_loc = ((maze_size[0]//25)-1,(maze_size[0]//25)-1)
            path = solution_displayer_surface.maze_grid.find_path_from(solution_displayer_surface.maze_grid.cells[start_cell_loc], solution_displayer_surface.maze_grid.cells[end_cell_loc])
            for cell in path:
                pygame.draw.rect(solution_displayer_surface,GOLD,(cell.top_left_vertex[0]+10,cell.top_left_vertex[1]+10,5,5))
                
            window.blit(solution_displayer_surface,solution_displayer_surface.coords)
            pygame.display.flip()
            
            while current_surface == "SOLUTION DISPLAYER" and running == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
                    #back_btn event handler    
                    elif solution_displayer_surface.back_btn.was_clicked(event):
                        current_surface = "GAME OVER"
                        
    pygame.quit()
  
if __name__ == "__main__":
    game_loop()
