#This is a helper program for moving the gamepiece (red square) through the maze without going through any walls.

import pygame, random

width, height = 501, 501
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Through the Maze")
fps = 10 #FPS has to be low to make more precise movements of game piece possible (higher FPS = more sensitivity)
white = 255,255,255
black = 0,0,0
red = 255,0,0

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
        
    def remove_wall(self, wall_to_remove, cell_neighbors): #find a way to not have to pass an entire dictionary in. should just be able to specificy wall to remove.
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
        #get each cell object
            #go through its walls list
            #if it has a wall, get the vertices for that wall and draw a white line connecting them on the grid
            #otherwise, if the wall is missing, don't draw anything
        for key in self._cells:
            cell = self._cells[key]
            if cell.has_wall[0] == True:
                pygame.draw.line(window,white,cell.top_left_vertex,cell.top_right_vertex)
            if cell.has_wall[1] == True:
                pygame.draw.line(window,white,cell.bottom_left_vertex,cell.bottom_right_vertex)
            if cell.has_wall[2] == True:
                pygame.draw.line(window,white,cell.bottom_left_vertex,cell.top_left_vertex)
            if cell.has_wall[3] == True:
                pygame.draw.line(window,white,cell.top_right_vertex,cell.bottom_right_vertex)
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
    current_cell = grid.cells[0,0]
    current_cell.visited = True
    visited_cells = 1
    
    while visited_cells != 400:
        cell_neighbors_dict = current_cell.find_cell_neighbors(grid.cells)
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
        
def game_loop():
    x = 0
    y = 0
    width = 24
    height = 24
    row = 0
    col = 0
    current_cell = row,col
    
    #start in cell at (0,0)
    #draw the game piece
    #if up arrow pressed...draw game piece in cell at (row-1,col)
    #if down arrow pressed...draw game piece in cell at (row+1,col)
    #if left arrow pressed...draw game piece in cell at (row,col-1)
    #if right arrow pressed...draw game piece in cell at (row,col+1)
    #but only if the game piece won't be moving through the wall of the cell
    #can determine if the desired path of the game piece will hit a wall by...
        #if trying to go up, check if current cell has a top wall and move up if it not
        #if trying to go down, check if current cell has a bottom wall and move move down if not
        #if trying to go left, check if current cell has a left wall and move left if not
        #if trying to go right, check if current cell has a right wall and move right if not
        #moving = redrawing game piece in the cell above/below/left/right of current cell
    clock = pygame.time.Clock()
    running = True
    generate_maze_from_grid(maze_grid)
    pygame.draw.rect(window, red, (x,y,width,height))
    pygame.display.update()
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False     
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if maze_grid.cells[current_cell].has_wall[2] == False:
                current_cell = maze_grid.cells[current_cell].row,maze_grid.cells[current_cell].col-1
                x-=25
        elif keys[pygame.K_RIGHT]:
            if maze_grid.cells[current_cell].has_wall[3] == False:
                current_cell = maze_grid.cells[current_cell].row,maze_grid.cells[current_cell].col+1
                x+=25
        elif keys[pygame.K_UP]:
            if maze_grid.cells[current_cell].has_wall[0] == False:
                current_cell = maze_grid.cells[current_cell].row-1,maze_grid.cells[current_cell].col
                y-=25
        elif keys[pygame.K_DOWN]:
            if maze_grid.cells[current_cell].has_wall[1] == False:
                current_cell = maze_grid.cells[current_cell].row+1,maze_grid.cells[current_cell].col
                y+=25           
        window.fill(black)
        pygame.draw.rect(window, red, (x,y,width,height))
        maze_grid.display_grid()
        pygame.display.update()
    pygame.quit()
    
if __name__ == "__main__":
    maze_grid = Grid()
    game_loop()