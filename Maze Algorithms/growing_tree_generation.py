#helpful link1: https://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm

import pygame, random

width, height = 501, 501
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Growing Tree Algorithm Maze Generator")
fps = 60
white = 255,255,255
black = 0,0,0

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
        self._path_id = Cell.cell_number
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
                
                new_top_left_vertex = self._top_left_vertex[0]+1, self._top_left_vertex[1] #for preventing an extra pixel from getting deleted on the left/right walls
                new_top_right_vertex = self._top_right_vertex[0]-1, self._top_right_vertex[1]
                pygame.draw.line(window,black,new_top_left_vertex,new_top_right_vertex)
                pygame.display.update()
                
        elif wall_to_remove == "BOTTOM":
            if self._has_wall[1]:
                self._has_wall[1] = False
                neighbor_below = cell_neighbors["BELOW"]
                neighbor_below.has_wall[0] = False
                
                new_bottom_left_vertex = self._bottom_left_vertex[0]+1, self._bottom_left_vertex[1] #for preventing an extra pixel from getting deleted on the left/right walls
                new_bottom_right_vertex = self._bottom_right_vertex[0]-1, self._bottom_right_vertex[1]
                pygame.draw.line(window,black,new_bottom_left_vertex,new_bottom_right_vertex)
                pygame.display.update()
                
        elif wall_to_remove == "LEFT":
            if self._has_wall[2]:
                self._has_wall[2] = False
                neighbor_left = cell_neighbors["LEFT"]
                neighbor_left.has_wall[3] = False
                
                new_top_left_vertex = self._top_left_vertex[0], self._top_left_vertex[1]+1 #for preventing an extra pixel from getting deleted on the top/bottom walls
                new_bottom_left_vertex = self._bottom_left_vertex[0], self._bottom_left_vertex[1]-1
                pygame.draw.line(window,black,new_top_left_vertex,new_bottom_left_vertex)
                pygame.display.update()
                
        else:
            if self._has_wall[3]:
                self._has_wall[3] = False 
                neighbor_right = cell_neighbors["RIGHT"]
                neighbor_right.has_wall[2] = False
                
                new_top_right_vertex = self._top_right_vertex[0], self._top_right_vertex[1]+1 #for preventing an extra pixel from getting deleted on the top/bottom walls
                new_bottom_right_vertex = self._bottom_right_vertex[0], self._bottom_right_vertex[1]-1
                pygame.draw.line(window,black,new_top_right_vertex,new_bottom_right_vertex)
                pygame.display.update()
            
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
    def __init__(self):
        cell_locs = []
        cell_objects = []
        for r in range (20):
            for c in range(20):
                cell_locs.append((r,c))
                cell_objects.append(Cell(r,c))
        self._cells = dict(zip(cell_locs, cell_objects)) #this maps the row,column location of a cell to that specific cell object's location in memory
                
    def display_grid(self):
        for key in self._cells:
            cell = self._cells[key]
            pygame.draw.line(window,white,cell.top_left_vertex,cell.top_right_vertex)
            pygame.draw.line(window,white,cell.top_right_vertex,cell.bottom_right_vertex)
            pygame.draw.line(window,white,cell.bottom_right_vertex,cell.bottom_left_vertex)
            pygame.draw.line(window,white,cell.bottom_left_vertex,cell.top_left_vertex)
        pygame.display.update()
        
    def get_cells_in_row(self, row_number):
        cell_locs = []
        for col in range (20):
            location = (row_number, col)
            cell_locs.append(location)

        cells = []
        for cell_location in cell_locs:
            cells.append(self._cells[cell_location])
        return cells

    @property
    def cells(self):
        return self._cells
          
         
def generate_maze_from_grid(grid):
    #random.seed(maze_seed)
    cell_keys = list(grid.cells)
    rand_cell_key_index = random.randrange(0,len(cell_keys))
    rand_key = cell_keys[rand_cell_key_index]
    exploratory_cells = [grid.cells[rand_key]]
    exploratory_cells[0].visited = True
    #playing with how exploratory cells are chosen
    #1% chance for oldest, 45% chance for newest, 45% chance for random, 9% chance for hybrid
    selection_method = random.randrange(0,101)
    while exploratory_cells:
        random_cell_index = None
        if selection_method == 0: #oldest cell
            random_cell_index = 0
        elif selection_method >=1 and selection_method <=45: #newest cell
            random_cell_index = len(exploratory_cells)-1
        elif selection_method >=46 and selection_method <=91: #random cell
            random_cell_index = random.randrange(0, len(exploratory_cells))
        else: #hybrid
            rand_selection_method = random.randrange(0,3)
            if rand_selection_method == 0: #oldest cell
                random_cell_index = 0
            elif rand_selection_method == 1: #newest cell
                random_cell_index = len(exploratory_cells)-1
            else: #completely random cell
                random_cell_index = random.randrange(0, len(exploratory_cells))
        rand_cell = exploratory_cells[random_cell_index]
        neighbors = rand_cell.find_cell_neighbors(grid._cells)
        unvisited_neighbors = []
        for key in neighbors:
            if neighbors[key].visited == False:
                unvisited_neighbors.append(neighbors[key])
        if len(unvisited_neighbors) == 0:
            exploratory_cells.remove(rand_cell)
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
            exploratory_cells.append(rand_neighbor)
            rand_neighbor.visited = True
    
def game_loop():
    clock = pygame.time.Clock()
    running = True
    generate_maze_from_grid(maze_grid)
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False           
    pygame.quit()
    
if __name__ == "__main__":
    maze_grid = Grid()
    maze_grid.display_grid()
    game_loop()
