#helpful link1: https://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm

import pygame, random

width, height = 501, 501
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hunt and Kill Maze Generator")
fps = 60
white = 255,255,255
black = 0,0,0

class Cell:
    def __init__(self, row, column):
        x = column*25 #multiplied by 25 because each cell is a 25x25 square
        y = row*25
        self._cell_row = row #row and col provide the location of the cell on the grid
        self._cell_col = column  
        
        self._top_left_vertex = x,y
        self._top_right_vertex = x+25,y
        self._bottom_left_vertex = x,y+25
        self._bottom_right_vertex = x+25,y+25
        
        self._visited = False
        self._has_wall = [True, True, True, True] #TOP, BOTTOM, LEFT, RIGHT
        
    def find_cell_neighbors(self, all_cells_dict):
        current_cell_location = self._cell_row,self._cell_col
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
    def cell_row(self):
        return self._cell_row
    @property
    def cell_col(self):
        return self._cell_col
        
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
        
    @property
    def cells(self):
        return self._cells
      
     
def generate_maze_from_grid(grid):
    cell_keys = list(grid.cells)
    rand_cell_key_index = random.randrange(0,len(cell_keys))
    rand_key = cell_keys[rand_cell_key_index]
    current_cell = grid.cells[rand_key]
    visited_cells = [current_cell]
    while len(visited_cells) != len(grid.cells):
        neighbors = current_cell.find_cell_neighbors(grid.cells)
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
            for key in grid.cells:
                hunted_cell = grid.cells[key]
                if hunted_cell not in visited_cells:
                    possible_killable_neighbors = hunted_cell.find_cell_neighbors(grid.cells)
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
