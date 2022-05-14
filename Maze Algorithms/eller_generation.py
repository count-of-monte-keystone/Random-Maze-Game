#helpful link2: http://weblog.jamisbuck.org/2010/12/29/maze-generation-eller-s-algorithm

import pygame, random

width, height = 501, 501
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Eller's Algorithm Maze Generator")
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
          
#This algorithm works by going row by row
#First, it decides whether or not to merge (remove the right wall) between 2 cells, but only if they aren't part of the same set/path (meaning that there isn't a path one could follow from one cell to the other)
#Next, it goes back through all the merged cells and decides to remove the bottom wall of at least one of the merged cells
#Then, it goes to the next row and repeats the above steps until it reaches the final row
#In the final row, all cells that aren't in the same set/path get merged every time, no randomness like before
#pros: fast, generates mazes with one possible path
#cons: harder to code          
def generate_maze_from_grid(grid):
    for row in range (20):
        cells_in_row = grid.get_cells_in_row(row)
        paths_dict = {}
        for cell in cells_in_row:
            if paths_dict.get(cell.path_id) == None: #if a key-value pair between a specific path id and a cell doesn't exist
                cells_in_path = [cell]
                paths_dict[cell.path_id] = cells_in_path
            else: #if there is already an existing key-value pair for a specific path id and a cell
                paths_dict[cell.path_id].append(cell)
        if row != 19:
            for cell_index in range(len(cells_in_row)-1): #skip the last cell in the row because it won't have an adjacent cell to even try to merge with
                current_cell = cells_in_row[cell_index]
                adjacent_cell = grid.cells[current_cell.row,current_cell.col+1]
                if current_cell.path_id != adjacent_cell.path_id:
                    action = random.randrange(0,2)
                    if action == 1: #merge cells
                        paths_dict[current_cell.path_id] = paths_dict[current_cell.path_id] + paths_dict[adjacent_cell.path_id] #merges the path lists of the cells (these lists contain the cell objects the cell is merged with)
                        paths_dict.pop(adjacent_cell.path_id) #remove the cell-to-be-merged's key-value pair from dictionary because it is going to be merged with an existing key-value pair (there can't be the same key twice in a dictionary)
                        for cell in paths_dict[current_cell.path_id]: #updates the path_ids of all the cell objects in the newly merged list to match current_cell's path_id (might be a bit redundant but can fix later)
                            cell.path_id = current_cell.path_id
                        cell_neighbors_dict = current_cell.find_cell_neighbors(grid.cells)
                        current_cell.remove_wall("RIGHT", cell_neighbors_dict)
            for key in paths_dict:
                path_list = paths_dict[key]
                if len(path_list) > 1:
                    numb_downward_connections = random.randrange(1, len(path_list))
                    for i in range (numb_downward_connections):
                        random_cell_index = random.randrange(0, len(path_list))
                        chosen_cell = path_list[random_cell_index]
                        cell_neighbors_dict = chosen_cell.find_cell_neighbors(grid.cells)
                        chosen_cell.remove_wall("BOTTOM", cell_neighbors_dict)
                        cell_below = grid.cells[chosen_cell.row+1,chosen_cell.col]
                        cell_below.path_id = chosen_cell.path_id
                        path_list.remove(chosen_cell) #this is to avoid the same cell getting chosen twice and not establishing a different downward connection
                else:
                    numb_downward_connections = 1
                    chosen_cell = path_list[0]
                    cell_neighbors_dict = chosen_cell.find_cell_neighbors(grid.cells)
                    chosen_cell.remove_wall("BOTTOM", cell_neighbors_dict)
                    cell_below = grid.cells[chosen_cell.row+1,chosen_cell.col]
                    cell_below.path_id = chosen_cell.path_id
        else:
            for cell_index in range(len(cells_in_row)-1):
                current_cell = cells_in_row[cell_index]
                adjacent_cell = grid.cells[current_cell.row,current_cell.col+1]
                if current_cell.path_id != adjacent_cell.path_id:
                    paths_dict[current_cell.path_id] = paths_dict[current_cell.path_id] + paths_dict[adjacent_cell.path_id]
                    paths_dict.pop(adjacent_cell.path_id)
                    for cell in paths_dict[current_cell.path_id]: #updates the path_ids of all the cell objects in the newly merged list to match current_cell's path_id (might be a bit redundant but can fix later)
                        cell.path_id = current_cell.path_id
                    cell_neighbors_dict = current_cell.find_cell_neighbors(grid.cells)
                    current_cell.remove_wall("RIGHT", cell_neighbors_dict)
                    adjacent_cell.path_id = current_cell.path_id
                    
                    
    
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
