#helpful link1: https://realpython.com/python-optional-arguments/
#helpful link2: https://realpython.com/python-kwargs-and-args/
import pygame
pygame.init()

class Surface(pygame.Surface):
    def __init__(self, coords, dimensions, **kwargs):
        super().__init__(dimensions) #returns a proxy object of the parent class (pygame.Surface) initialized with (width,height). anytime self is used to call to a method in parent class, this proxy object makes that call.
        self._coords = coords
        self._dimensions = dimensions
        self._color = (255,255,255)
        self._widgets = [] #list that holds all the widgets associated with that surface
        for arg in kwargs:
            if arg == "color":               
                if isinstance(kwargs[arg],tuple):
                    if len(kwargs[arg]) != 3:
                        raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
                    else:
                        if isinstance(kwargs[arg][0],int) and isinstance(kwargs[arg][1],int) and isinstance(kwargs[arg][2],int):
                            if kwargs[arg][0] >= 0 and kwargs[arg][0] <= 255 and kwargs[arg][1] >= 0 and kwargs[arg][1] <= 255 and kwargs[arg][2] >= 0 and kwargs[arg][2] <= 255:                   
                                self._color = kwargs[arg]
                            else:
                                raise ValueError("red, green, and blue values must all be integers in range 0-255")
                        else:
                            raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise TypeError("color must be a tuple with (red,green,blue) format")    
            else:
                raise ValueError("not an argument")
    
    #places all the widgets on the surface so then window.blit can be called on the surface object and draw everything    
    def prepare(self):
        self.fill(self._color)
        for widget in self._widgets:
            widget.place()
        
        
    @property
    def coords(self):
        return self._coords
        
    @property
    def dimensions(self):
        return self._dimensions
        
    @property
    def color(self):
        return self._color
        
    @coords.setter
    def coords(self, new_coords):
        if isinstance(new_coords,tuple):
            if len(new_coords) < 2 or len(new_coords) > 2:
                raise ValueError("coords tuple must contain exactly 2 values: x, y")
            else:
                if isinstance(new_coords[0],int) and isinstance(new_coords[1],int):
                    self._coords = new_coords
                else:
                    raise ValueError("x and y values must both be integers")
        else:
            raise TypeError("coords must be a tuple with (x,y) format")
            
    @dimensions.setter
    def dimensions(self, new_dimensions):
        if isinstance(new_dimensions,tuple):
            if len(new_dimensions) < 2 or len(new_dimensions) > 2:
                raise ValueError("dimensions tuple must contain exactly 2 values: width, height")
            else:
                if isinstance(new_dimensions[0],int) and isinstance(new_dimensions[1],int):
                    self._dimensions = new_dimensions
                else:
                    raise ValueError("width and height values must both be integers")
        else:
            raise TypeError("dimensions must be a tuple with (width,height) format")
            
    @color.setter
    def color(self, new_color):
        if isinstance(new_color,tuple):
            if len(kwargs[arg]) != 3:
                raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
            else:
                if isinstance(new_color[0],int) and isinstance(new_color[1],int) and isinstance(new_color[2],int):
                    if new_color[0] >= 0 and new_color[0] <= 255 and new_color[1] >= 0 and new_color[1] <= 255 and new_color[2] >= 0 and new_color[2] <= 255:                   
                        self._color = new_color
                    else:
                        raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise ValueError("red, green, and blue values must all be integers in range 0-255")
        else:
            raise TypeError("color must be a tuple with (red,green,blue) format")
        
class Button:
    def __init__(self, parent_surface, coords, dimensions, **kwargs):
        self._parent_surface = parent_surface
        self._coords = coords
        self._dimensions = dimensions
        self._color = (255,0,0)
        self._text = "Button"
        self._text_font = "arial"
        self._text_color = (0,0,0)
        self._text_size = 15
        self._text_align = "center"
        
        for arg in kwargs:
            if arg == "color":
                if isinstance(kwargs[arg],tuple):
                    if len(kwargs[arg]) != 3:
                        raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
                    else:
                        if isinstance(kwargs[arg][0],int) and isinstance(kwargs[arg][1],int) and isinstance(kwargs[arg][2],int):
                            if kwargs[arg][0] >= 0 and kwargs[arg][0] <= 255 and kwargs[arg][1] >= 0 and kwargs[arg][1] <= 255 and kwargs[arg][2] >= 0 and kwargs[arg][2] <= 255:                   
                                self._color = kwargs[arg]
                            else:
                                raise ValueError("red, green, and blue values must all be integers in range 0-255")
                        else:
                            raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise TypeError("color must be a tuple with (red,green,blue) format")
            elif arg == "txt":
                if isinstance(kwargs[arg],str):
                    self._text = kwargs[arg]
                else:
                    raise TypeError("text must be a string")
            elif arg == "txt_font":
                if isinstance(kwargs[arg],str):
                    available_fonts = pygame.font.get_fonts()
                    if kwargs[arg] in available_fonts:
                        self._text_font = kwargs[arg]
                    else:
                        raise ValueError("not a System Font")
                else:
                    raise TypeError("font must be a string")
            elif arg == "txt_color":
                if isinstance(kwargs[arg],tuple):
                    if len(kwargs[arg]) != 3:
                        raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
                    else:
                        if isinstance(kwargs[arg][0],int) and isinstance(kwargs[arg][1],int) and isinstance(kwargs[arg][2],int):
                            if kwargs[arg][0] >= 0 and kwargs[arg][0] <= 255 and kwargs[arg][1] >= 0 and kwargs[arg][1] <= 255 and kwargs[arg][2] >= 0 and kwargs[arg][2] <= 255:                   
                                self._text_color = kwargs[arg]
                            else:
                                raise ValueError("red, green, and blue values must all be integers in range 0-255")
                        else:
                            raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise TypeError("color must be a tuple with (red,green,blue) format")
            elif arg == "txt_size":
                if isinstance(kwargs[arg],int):
                    if kwargs[arg] > 0 and kwargs[arg] <= 50:
                        self._text_size = kwargs[arg]
                    else:
                        raise ValueError("text size must be in range 1-50")
                else:
                    raise TypeError("text size must be an integer")
            elif arg == "txt_align":
                if isinstance(kwargs[arg],str):
                    if kwargs[arg] == "left" or kwargs[arg] == "right" or kwargs[arg] == "center":
                        self._text_align = kwargs[arg]
                    else:
                        raise ValueError("left, right, or center text alignments only")
                else:
                    raise TypeError("text alignment must be a string of left, right, or center")
            else:
                raise ValueError("not an argument")
            
        self._parent_surface._widgets.append(self)
                        
    def place(self):
        #draws the button on its parent surface at the correct coords but does not update it (and therefore doesn't show itself)
        pygame.draw.rect(self._parent_surface,self._color,(self._coords[0],self._coords[1],self._dimensions[0],self._dimensions[1]))
        text_font = pygame.font.SysFont(self._text_font, self._text_size)
        text_surface = text_font.render(self._text, True, self.text_color)
        text_surface_rect = text_surface.get_rect(topleft=(self._coords[0],self._coords[1]))
        if self._text_align == "left":
            text_surface_rect.topleft = (self._coords[0],self._coords[1])
        elif self._text_align == "right":
            text_surface_rect.topright = (self._coords[0]+self._dimensions[0],self._coords[1])
        else:
            text_surface_rect.center = ((self._coords[0]+self._coords[0]+self._dimensions[0])//2,(self._coords[1]+self._coords[1]+self._dimensions[1])//2)
        self._parent_surface.blit(text_surface,text_surface_rect)
           
    def was_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_xy_pos = pygame.mouse.get_pos()
            #problem: mouse_pos is of the window, not the surface
            #200 in window is different from 200 in surface
            #scale the hitbox coords
            scaled_hitbox = pygame.Rect((self._coords[0]+self._parent_surface.coords[0],self._coords[1]+self._parent_surface.coords[1]),(self._dimensions[0],self._dimensions[1]))
            if scaled_hitbox.collidepoint(mouse_xy_pos):
                return True
            else:
                return False
        else:
            return False
         
    @property
    def coords(self):
        return self._coords
        
    @property
    def dimensions(self):
        return self._dimensions
        
    @property
    def color(self):
        return self._color
        
    @property
    def text(self):
        return self._text
       
    @property
    def text_font(self):
        return self._text_font
        
    @property
    def text_color(self):
        return self._text_color
        
    @property
    def text_size(self):
        return self._text_size
        
    @property
    def text_align(self):
        return self._text_align
        
    @coords.setter
    def coords(self, new_coords):
        if isinstance(new_coords,tuple):
            if len(new_coords) != 2:
                raise ValueError("coords tuple must contain exactly 2 values: x, y")
            else:
                if isinstance(new_coords[0],int) and isinstance(new_coords[1],int):
                    self._coords = new_coords
                else:
                    raise ValueError("x and y values must both be integers")
        else:
            raise TypeError("coords must be a tuple with (x,y) format")
            
    @dimensions.setter
    def dimensions(self, new_dimensions):
        if isinstance(new_dimensions,tuple):
            if len(new_dimensions) != 2:
                raise ValueError("dimensions tuple must contain exactly 2 values: width, height")
            else:
                if isinstance(new_dimensions[0],int) and isinstance(new_dimensions[1],int):
                    self._dimensions = new_dimensions
                else:
                    raise ValueError("width and height values must both be integers")
        else:
            raise TypeError("dimensions must be a tuple with (width,height) format")
            
    @color.setter
    def color(self, new_color):
        if isinstance(new_color,tuple):
            if len(kwargs[arg]) != 3:
                raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
            else:
                if isinstance(new_color[0],int) and isinstance(new_color[1],int) and isinstance(new_color[2],int):
                    if new_color[0] >= 0 and new_color[0] <= 255 and new_color[1] >= 0 and new_color[1] <= 255 and new_color[2] >= 0 and new_color[2] <= 255:                   
                        self._color = new_color
                    else:
                        raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise ValueError("red, green, and blue values must all be integers in range 0-255")
        else:
            raise TypeError("color must be a tuple with (red,green,blue) format")
        
    @text.setter
    def text(self, new_str):
        if isinstance(new_str,str):
            self._text = new_str
        else:
            raise TypeError("text must be a string")
            
    @text_font.setter
    def text_font(self, new_font):
        if isinstance(new_font,str):
            available_fonts = pygame.font.get_fonts()
            if new_font in available_fonts:
                self._text_font = new_font
            else:
                raise ValueError("not a System Font")
        else:
            raise TypeError("font must be a string")
            
    @text_color.setter
    def text_color(self, new_color):
        if isinstance(new_color,tuple):
            if len(kwargs[arg]) != 3:
                raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
            else:
                if isinstance(new_color[0],int) and isinstance(new_color[1],int) and isinstance(new_color[2],int):
                    if new_color[0] >= 0 and new_color[0] <= 255 and new_color[1] >= 0 and new_color[1] <= 255 and new_color[2] >= 0 and new_color[2] <= 255:                   
                        self._text_color = new_color
                    else:
                        raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise ValueError("red, green, and blue values must all be integers in range 0-255")
        else:
            raise TypeError("color must be a tuple with (red,green,blue) format")
            
    @text_size.setter
    def text_size(self, new_size):
        if isinstance(new_size,int):
            if new_size > 0 and new_size <= 50:
                self._text_size = new_size
            else:
                raise ValueError("text size must be in range 1-50")
        else:
            raise TypeError("text size must be an integer")
                       
    @text_align.setter
    def text_align(self, new_alignment):
        if isinstance(new_alignment,str):
            if new_alignment == "left" or new_alignment == "right" or new_alignment == "center":
                self._text_align = new_alignment
            else:
                raise ValueError("left, right, or center text alignments only")
        else:
            raise TypeError("text alignment must be a string of left, right, or center")
                       
class Label:
    def __init__(self, parent_surface, coords, dimensions, **kwargs):
        self._parent_surface = parent_surface
        self._coords = coords
        self._dimensions = dimensions
        self._color = self._parent_surface.color
        self._text = "Label"
        self._text_font = "arial"
        self._text_color = (0,0,0)
        self._text_size = 15
        self._text_align = "center"
        
        for arg in kwargs:
            if arg == "color":
                if isinstance(kwargs[arg],tuple):
                    if len(kwargs[arg]) != 3:
                        raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
                    else:
                        if isinstance(kwargs[arg][0],int) and isinstance(kwargs[arg][1],int) and isinstance(kwargs[arg][2],int):
                            if kwargs[arg][0] >= 0 and kwargs[arg][0] <= 255 and kwargs[arg][1] >= 0 and kwargs[arg][1] <= 255 and kwargs[arg][2] >= 0 and kwargs[arg][2] <= 255:                   
                                self._color = kwargs[arg]
                            else:
                                raise ValueError("red, green, and blue values must all be integers in range 0-255")
                        else:
                            raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise TypeError("color must be a tuple with (red,green,blue) format")
            elif arg == "txt":
                if isinstance(kwargs[arg],str):
                    self._text = kwargs[arg]
                else:
                    raise TypeError("text must be a string")
            elif arg == "txt_font":
                if isinstance(kwargs[arg],str):
                    available_fonts = pygame.font.get_fonts()
                    if kwargs[arg] in available_fonts:
                        self._text_font = kwargs[arg]
                    else:
                        raise ValueError("not a System Font")
                else:
                    raise TypeError("font must be a string")
            elif arg == "txt_color":
                if isinstance(kwargs[arg],tuple):
                    if len(kwargs[arg]) != 3:
                        raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
                    else:
                        if isinstance(kwargs[arg][0],int) and isinstance(kwargs[arg][1],int) and isinstance(kwargs[arg][2],int):
                            if kwargs[arg][0] >= 0 and kwargs[arg][0] <= 255 and kwargs[arg][1] >= 0 and kwargs[arg][1] <= 255 and kwargs[arg][2] >= 0 and kwargs[arg][2] <= 255:                   
                                self._text_color = kwargs[arg]
                            else:
                                raise ValueError("red, green, and blue values must all be integers in range 0-255")
                        else:
                            raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise TypeError("color must be a tuple with (red,green,blue) format")
            elif arg == "txt_size":
                if isinstance(kwargs[arg],int):
                    if kwargs[arg] > 0 and kwargs[arg] <= 50:
                        self._text_size = kwargs[arg]
                    else:
                        raise ValueError("text size must be in range 1-50")
                else:
                    raise TypeError("text size must be an integer")
            elif arg == "txt_align":
                if isinstance(kwargs[arg],str):
                    if kwargs[arg] == "left" or kwargs[arg] == "right" or kwargs[arg] == "center":
                        self._text_align = kwargs[arg]
                    else:
                        raise ValueError("left, right, or center text alignments only")
                else:
                    raise TypeError("text alignment must be a string of left, right, or center")
            else:
                raise ValueError("not an argument")
        self._parent_surface._widgets.append(self)
                
    def place(self):
        #draws the label on its parent surface at the correct coords but does not update it (and therefore doesn't show itself)
        pygame.draw.rect(self._parent_surface,self._color,(self._coords[0],self._coords[1],self._dimensions[0],self._dimensions[1]))
        text_font = pygame.font.SysFont(self._text_font, self._text_size)
        text_surface = text_font.render(self._text, True, self.text_color)
        text_surface_rect = text_surface.get_rect(topleft=(self._coords[0],self._coords[1]))
        if self._text_align == "left":
            text_surface_rect.topleft = (self._coords[0],self._coords[1])
        elif self._text_align == "right":
            text_surface_rect.topright = (self._coords[0]+self._dimensions[0],self._coords[1])
        else:
            text_surface_rect.center = ((self._coords[0]+self._coords[0]+self._dimensions[0])//2,(self._coords[1]+self._coords[1]+self._dimensions[1])//2)
        self._parent_surface.blit(text_surface,text_surface_rect)
    
    @property
    def coords(self):
        return self._coords
        
    @property
    def dimensions(self):
        return self._dimensions
        
    @property
    def color(self):
        return self._color
        
    @property
    def text(self):
        return self._text
       
    @property
    def text_font(self):
        return self._text_font
        
    @property
    def text_color(self):
        return self._text_color
        
    @property
    def text_size(self):
        return self._text_size
        
    @property
    def text_align(self):
        return self._text_align
        
    @coords.setter
    def coords(self, new_coords):
        if isinstance(new_coords,tuple):
            if len(new_coords) < 2 or len(new_coords) > 2:
                raise ValueError("coords tuple must contain exactly 2 values: x, y")
            else:
                if isinstance(new_coords[0],int) and isinstance(new_coords[1],int):
                    self._coords = new_coords
                else:
                    raise ValueError("x and y values must both be integers")
        else:
            raise TypeError("coords must be a tuple with (x,y) format")
            
    @dimensions.setter
    def dimensions(self, new_dimensions):
        if isinstance(new_dimensions,tuple):
            if len(new_dimensions) < 2 or len(new_dimensions) > 2:
                raise ValueError("dimensions tuple must contain exactly 2 values: width, height")
            else:
                if isinstance(new_dimensions[0],int) and isinstance(new_dimensions[1],int):
                    self._dimensions = new_dimensions
                else:
                    raise ValueError("width and height values must both be integers")
        else:
            raise TypeError("dimensions must be a tuple with (width,height) format")
            
    @color.setter
    def color(self, new_color):
        if isinstance(new_color,tuple):
            if len(kwargs[arg]) != 3:
                raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
            else:
                if isinstance(new_color[0],int) and isinstance(new_color[1],int) and isinstance(new_color[2],int):
                    if new_color[0] >= 0 and new_color[0] <= 255 and new_color[1] >= 0 and new_color[1] <= 255 and new_color[2] >= 0 and new_color[2] <= 255:                   
                        self._color = new_color
                    else:
                        raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise ValueError("red, green, and blue values must all be integers in range 0-255")
        else:
            raise TypeError("color must be a tuple with (red,green,blue) format")
        
    @text.setter
    def text(self, new_str):
        if isinstance(new_str,str):
            self._text = new_str
        else:
            raise TypeError("text must be a string")
            
    @text_font.setter
    def text_font(self, new_font):
        if isinstance(new_font,str):
            available_fonts = pygame.font.get_fonts()
            if new_font in available_fonts:
                self._text_font = new_font
            else:
                raise ValueError("not a System Font")
        else:
            raise TypeError("font must be a string")
            
    @text_color.setter
    def text_color(self, new_color):
        if isinstance(new_color,tuple):
            if len(kwargs[arg]) != 3:
                raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
            else:
                if isinstance(new_color[0],int) and isinstance(new_color[1],int) and isinstance(new_color[2],int):
                    if new_color[0] >= 0 and new_color[0] <= 255 and new_color[1] >= 0 and new_color[1] <= 255 and new_color[2] >= 0 and new_color[2] <= 255:                   
                        self._text_color = new_color
                    else:
                        raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise ValueError("red, green, and blue values must all be integers in range 0-255")
        else:
            raise TypeError("color must be a tuple with (red,green,blue) format")
            
    @text_size.setter
    def text_size(self, new_size):
        if isinstance(new_size,int):
            if new_size > 0 and new_size <= 50:
                self._text_size = new_size
            else:
                raise ValueError("text size must be in range 1-50")
        else:
            raise TypeError("text size must be an integer")
            
    @text_align.setter
    def text_align(self, new_alignment):
        if isinstance(new_alignment,str):
            if new_alignment == "left" or new_alignment == "right" or new_alignment == "center":
                self._text_align = new_alignment
            else:
                raise ValueError("left, right, or center text alignments only")
        else:
            raise TypeError("text alignment must be a string of left, right, or center")        
      
class TextField:
    def __init__(self, parent_surface, coords, dimensions, **kwargs):
        self._parent_surface = parent_surface
        self._coords = coords
        self._dimensions = dimensions
        self._color = self._parent_surface.color
        self._text = "TextField"    
        self._text_font = "arial"
        self._text_color = (0,0,0)
        self._text_size = 15        
  
        for arg in kwargs:
            if arg == "color":
                if isinstance(kwargs[arg],tuple):
                    if len(kwargs[arg]) != 3:
                        raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
                    else:
                        if isinstance(kwargs[arg][0],int) and isinstance(kwargs[arg][1],int) and isinstance(kwargs[arg][2],int):
                            if kwargs[arg][0] >= 0 and kwargs[arg][0] <= 255 and kwargs[arg][1] >= 0 and kwargs[arg][1] <= 255 and kwargs[arg][2] >= 0 and kwargs[arg][2] <= 255:                   
                                self._color = kwargs[arg]
                            else:
                                raise ValueError("red, green, and blue values must all be integers in range 0-255")
                        else:
                            raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise TypeError("color must be a tuple with (red,green,blue) format")
            elif arg == "txt":
                if isinstance(kwargs[arg],str):
                    self._text = kwargs[arg]
                else:
                    raise TypeError("text must be a string")
            elif arg == "txt_font":
                if isinstance(kwargs[arg],str):
                    available_fonts = pygame.font.get_fonts()
                    if kwargs[arg] in available_fonts:
                        self._text_font = kwargs[arg]
                    else:
                        raise ValueError("not a System Font")
                else:
                    raise TypeError("font must be a string")
            elif arg == "txt_color":
                if isinstance(kwargs[arg],tuple):
                    if len(kwargs[arg]) != 3:
                        raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
                    else:
                        if isinstance(kwargs[arg][0],int) and isinstance(kwargs[arg][1],int) and isinstance(kwargs[arg][2],int):
                            if kwargs[arg][0] >= 0 and kwargs[arg][0] <= 255 and kwargs[arg][1] >= 0 and kwargs[arg][1] <= 255 and kwargs[arg][2] >= 0 and kwargs[arg][2] <= 255:                   
                                self._text_color = kwargs[arg]
                            else:
                                raise ValueError("red, green, and blue values must all be integers in range 0-255")
                        else:
                            raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise TypeError("color must be a tuple with (red,green,blue) format")
            elif arg == "txt_size":
                if isinstance(kwargs[arg],int):
                    if kwargs[arg] > 0 and kwargs[arg] <= 50:
                        self._text_size = kwargs[arg]
                    else:
                        raise ValueError("text size must be in range 1-50")
                else:
                    raise TypeError("text size must be an integer")           
            else:
                raise ValueError("not an argument")
        self._parent_surface._widgets.append(self)
                
    def was_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_xy_pos = pygame.mouse.get_pos()       
            #problem: mouse_pos is of the window, not the surface
            #200 in window is different from 200 in surface
            #scale the hitbox coords
            scaled_hitbox = pygame.Rect((self._coords[0]+self._parent_surface.coords[0],self._coords[1]+self._parent_surface.coords[1]),(self._dimensions[0],self._dimensions[1]))
            if scaled_hitbox.collidepoint(mouse_xy_pos):
                return True
            else:
                return False
        else:
            return False
            
    def place(self):
        #draws the textfield on its parent surface at the correct coords but does not update it (and therefore doesn't show itself)
        pygame.draw.rect(self._parent_surface,self._color,(self._coords[0],self._coords[1],self._dimensions[0],self._dimensions[1]))
        text_font = pygame.font.SysFont(self._text_font, self._text_size)
        text_surface = text_font.render(self._text, True, self._text_color)
        self._parent_surface.blit(text_surface,(self._coords[0],self._coords[1]))
        
    
    @property
    def coords(self):
        return self._coords
        
    @property
    def dimensions(self):
        return self._dimensions
        
    @property
    def color(self):
        return self._color
        
    @property
    def text(self):
        return self._text
       
    @property
    def text_font(self):
        return self._text_font
        
    @property
    def text_color(self):
        return self._text_color
        
    @property
    def text_size(self):
        return self._text_size
           
    @coords.setter
    def coords(self, new_coords):
        if isinstance(new_coords,tuple):
            if len(new_coords) < 2 or len(new_coords) > 2:
                raise ValueError("coords tuple must contain exactly 2 values: x, y")
            else:
                if isinstance(new_coords[0],int) and isinstance(new_coords[1],int):
                    self._coords = new_coords
                else:
                    raise ValueError("x and y values must both be integers")
        else:
            raise TypeError("coords must be a tuple with (x,y) format")
            
    @dimensions.setter
    def dimensions(self, new_dimensions):
        if isinstance(new_dimensions,tuple):
            if len(new_dimensions) < 2 or len(new_dimensions) > 2:
                raise ValueError("dimensions tuple must contain exactly 2 values: width, height")
            else:
                if isinstance(new_dimensions[0],int) and isinstance(new_dimensions[1],int):
                    self._dimensions = new_dimensions
                else:
                    raise ValueError("width and height values must both be integers")
        else:
            raise TypeError("dimensions must be a tuple with (width,height) format")
            
    @color.setter
    def color(self, new_color):
        if isinstance(new_color,tuple):
            if len(kwargs[arg]) != 3:
                raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
            else:
                if isinstance(new_color[0],int) and isinstance(new_color[1],int) and isinstance(new_color[2],int):
                    if new_color[0] >= 0 and new_color[0] <= 255 and new_color[1] >= 0 and new_color[1] <= 255 and new_color[2] >= 0 and new_color[2] <= 255:                   
                        self._color = new_color
                    else:
                        raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise ValueError("red, green, and blue values must all be integers in range 0-255")
        else:
            raise TypeError("color must be a tuple with (red,green,blue) format")
        
    @text.setter
    def text(self, new_str):
        if isinstance(new_str,str):
            self._text = new_str
        else:
            raise TypeError("text must be a string")
            
    @text_font.setter
    def text_font(self, new_font):
        if isinstance(new_font,str):
            available_fonts = pygame.font.get_fonts()
            if new_font in available_fonts:
                self._text_font = new_font
            else:
                raise ValueError("not a System Font")
        else:
            raise TypeError("font must be a string")
            
    @text_color.setter
    def text_color(self, new_color):
        if isinstance(new_color,tuple):
            if len(kwargs[arg]) != 3:
                raise ValueError("colors tuple must contain exactly 3 values: red value, green value, blue value")
            else:
                if isinstance(new_color[0],int) and isinstance(new_color[1],int) and isinstance(new_color[2],int):
                    if new_color[0] >= 0 and new_color[0] <= 255 and new_color[1] >= 0 and new_color[1] <= 255 and new_color[2] >= 0 and new_color[2] <= 255:                   
                        self._text_color = new_color
                    else:
                        raise ValueError("red, green, and blue values must all be integers in range 0-255")
                else:
                    raise ValueError("red, green, and blue values must all be integers in range 0-255")
        else:
            raise TypeError("color must be a tuple with (red,green,blue) format")
            
    @text_size.setter
    def text_size(self, new_size):
        if isinstance(new_size,int):
            if new_size > 0 and new_size <= 50:
                self._text_size = new_size
            else:
                raise ValueError("text size must be in range 1-50")
        else:
            raise TypeError("text size must be an integer")
            