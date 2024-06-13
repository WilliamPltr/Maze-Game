import random
import turtle
import time

from Maze import Maze

class Menue():
    temporary_obj = []
    Runing = False
    
    def __init__(self, menue_duration = 15, w = 600, h = 600) -> None:
        self.w, self.h = max(w, 0) , max(h, 0)
        self.mw, self.mh = max(w-100, 0), max(h, 0)
        self.screen = self.turt_init()
        self.cell_width = None
        self.m = Maze(42)
        
        #Show usefull informations to the user, such as the commands to use 
        turtle.hideturtle()
        turtle.speed(0)
        turtle.penup()
        turtle.goto(-250, 0)
        
        for i in range(menue_duration):
            turtle.write(f"The program will start in {menue_duration-i}s:\nSPACE : for solving a random start to end path\nC: Normal maze solution (bottum to top)\nRIGHTARROW : for changing the maze\nQ : for quit", font=("Arial", 24, "normal"))
            time.sleep(1)
            turtle.clear()

        self.maze_walls, self.cell_width = self.turt_maze()
            
    def done(self):
        turtle.done()
    
    def listen(self):
        self.screen.listen()
        

    def turt_init(self):
        """Initialise the trutle window

        Returns:
            _type_: _description_
        """
        # Set up the turtle screen
        screen = turtle.Screen()
        screen.title("Maze")
        screen.setup(width=self.mw, height=self.mh)
        return screen
        
    def turt_maze(self): #maze_walls, cell_width = turt_maze(screen, m.get_grid())
        """Show the maze on the window screen

        Returns:
            _type_: _description_
        """
        maze = self.m.get_grid()
        self.screen.tracer(0)  # Turn off screen updates to speed up rendering
        
        # Calculate cell size based on maze dimensions
        rows = len(maze)
        cols = len(maze[0])
        
        cell_width = self.h / cols
        cell_height = cell_width

        def draw_wall(x, y):
            wall = turtle.Turtle()
            wall.hideturtle()
            wall.speed(0)
            wall.penup()
            wall.color("black")
            wall.shape("square")
            wall.shapesize(cell_height / 20, cell_width / 20)
            wall.goto(x, y)
            wall.stamp()
            return wall

        def draw_maze(maze):
            walls = []
            
            for (x, y) in ((x, y) for x in range(cols) for y in range(rows)):
                    if maze[y][x] == 1:
                        x_coord = x * cell_width - (self.w//2)
                        y_coord = (self.h//2) - (y + 1) * cell_height
                        walls.append(draw_wall(x_coord, y_coord))
            return walls

        # Draw the maze walls
        maze_walls = draw_maze(maze)

        # Update and display the screen
        self.screen.update()
        self.screen.tracer(1)  # Re-enable screen updates
        
        self.cell_width = cell_width
        
        return maze_walls, cell_width
    
    # Function to show a path on the maze window
    def turt_draw_path(self, path):
        """Draw best path

        Args:
            path (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        
        def draw_points(x, y, color):
            wall = turtle.Turtle()
            wall.hideturtle()
            wall.speed(0)
            wall.penup()
            wall.color(color)
            wall.shape("square")
            wall.shapesize((self.cell_width / 20)*0.80, (self.cell_width / 20)*0.8)
            wall.goto(x+(self.cell_width / 20)*0.10, y+(self.cell_width / 20)*0.10)
            wall.stamp()
            
            return wall
        
        # Create a turtle to draw the path
        path_turtle = turtle.Turtle()
        
        path_turtle.hideturtle()
        path_turtle.pensize(1)
        path_turtle.speed(0)
        path_turtle.penup()
        
        points= [draw_points((path[0][0] * self.cell_width - (self.w//2)), ((self.h//2) - (path[0][1] + 1) * self.cell_width), "yellow"), \
            draw_points((path[-1][0] * self.cell_width - (self.w//2)), ((self.h//2) - (path[-1][1] + 1) * self.cell_width), "blue")]
        
        path_turtle.pensize(3)
        #path_turtle.speed(min(((self.w//self.cell_width)//100)*3, 10))
        path_turtle.speed(0)
        path_turtle.penup()
        path_turtle.color("red")
        
        # Set the same properties as the maze turtle
        path_turtle.setx(path[0][0] * self.cell_width - (self.w//2))
        path_turtle.sety((self.h//2) - (path[0][1] + 1) * self.cell_width)
        
        # Draw the path using turtle graphics
        path_turtle.pendown()
        
        #if the path is long, we speed up the showing process  so it doesn't take ages for big mazes
        if len(path) > 20:
            
            self.screen.tracer(0)  # Turn off screen updates to speed up rendering
            for x, y in path[:-15]:
                path_turtle.goto(x * self.cell_width - (self.w//2), (self.h//2) - (y + 1) * self.cell_width)
                
            # Update and display the screen
            self.screen.update()
            self.screen.tracer(1)  # Re-enable screen updates
            
            for x, y in path[-15:]:
                path_turtle.goto(x * self.cell_width - (self.w//2), (self.h//2) - (y + 1) * self.cell_width)
                
        else:
            for x, y in path:
                path_turtle.goto(x * self.cell_width - (self.w//2), (self.h//2) - (y + 1) * self.cell_width)
                
                
        self.temporary_obj.extend(points)
        self.temporary_obj.append(path_turtle)
    
    @classmethod
    def clear_tempObj(cls):
        
        for obj in cls.temporary_obj:
            obj.clear()
        cls.temporary_obj.clear()
        
    def listen(self):
        self.screen.listen()
    
    def onkeypress(self, fun, key=None):
        self.screen.onkeypress(fun, key)
        
    def onscreenclick(self, fun, btn=1, add=None):
        self.screen.onscreenclick(fun, btn, add)
        
    def get_mouse_click_coor(self, x,y)->tuple:
        "Start button implementation"
        turtle.onscreenclick(self.get_mouse_click_coor)
        #print(x, y)
    
    def bye(self):
        self.screen.bye()
    
    def update(self):
        self.screen.update()
    
    def tracer(self, n):
        self.screen.tracer(n)
    
    def create_maze(self):
        if not self.Runing:
            self.Runing = True
            
            self.screen.tracer(0)  # Turn off screen updates to speed up rendering
            self.clear_tempObj()
            for w in self.maze_walls:
                w.clear()
            
            self.m = Maze(int(self.screen.numinput("Please enter a maze size", "", 42, minval=7, maxval=500)/2)) #Max : 250 due to screen size and screen resolution
            self.maze_walls, self.cell_width = self.turt_maze()
            
            self.screen.update()
            self.screen.tracer(1)  # Re-enable screen updates
            self.screen.listen()
            
            self.Runing = False
    
    def follow_path(self):
        if not self.Runing:
            self.Runing = True
            self.clear_tempObj()
            start = random.choice(tuple((x, y) for x in range(1, self.m.length, 2) for y in range(1, self.m.width, 2)))
            end = random.choice(tuple((x, y) for x in range(1, self.m.length, 2) for y in range(1, self.m.width, 2)))
            self.turt_draw_path(self.m.find_sol(start, end))
            self.screen.listen()
            self.Runing = False
    
    def classic(self):
        if not self.Runing:
            start = (1, self.m.width-1)
            end = (self.m.length-1, 1)
            
            maze = self.m.get_grid()
            self.screen.tracer(0)  # Turn off screen updates to speed up rendering
            
            # Calculate cell size based on maze dimensions
            rows = len(maze)
            cols = len(maze[0])
            
            cell_width = self.h / cols
            cell_height = cell_width
            
            def draw_wall(x, y):
                wall = turtle.Turtle()
                wall.hideturtle()
                wall.speed(0)
                wall.penup()
                wall.color("white")
                wall.shape("square")
                wall.shapesize(cell_height / 20, cell_width / 20)
                wall.goto(x, y)
                wall.stamp()
                return wall
            
            self.Runing = True
            self.clear_tempObj()
            
            self.temporary_obj.append(draw_wall(0* cell_width - (self.w//2), (self.h//2) - (start[1] + 1) * cell_height))
            self.temporary_obj.append(draw_wall((end[0]+1)* cell_width - (self.w//2), (self.h//2) - (end[1] + 1) * cell_height))
            
            # Update and display the screen
            self.screen.update()
            self.screen.tracer(1)  # Re-enable screen updates
            
            self.cell_width = cell_width
            self.turt_draw_path(self.m.find_sol(start, end))
            self.screen.listen()
            self.Runing = False
    
    def exit(self):
        if not self.Runing:
            
            self.screen.listen()
            self.screen.bye()
    
    
    
    # screen.listen()
    # screen.onkeypress(follow_path, 'space')
    # screen.onkeypress(create_maze, 'Right')
    # screen.onkeypress(exit, 'q')
    
    # # Keep the window open
    # turtle.done()
