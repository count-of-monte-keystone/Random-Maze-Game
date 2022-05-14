#This is a helper program to visualize the creation of cells in order to form a grid, which is what the mazes will be generated from.
    
import pygame

width, height = 501, 501
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Grid Creation")
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
        self._cells = dict(zip(cell_locs, cell_objects)) #this assigns the row,column location of a cell as the key to that specific cell object in memory
                
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
        
def game_loop():
    clock = pygame.time.Clock()
    running = True
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