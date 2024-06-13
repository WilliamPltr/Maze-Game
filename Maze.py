# Module for creating a maze and finding the shortest path between two points in it

import random
import turtle
from Coordinates import Coordinates as Coor
from Graph import Graph
#from tqdm import tqdm

class Maze:
    def __init__(self, length, width = None) -> None:
        
        pass
    
        if width == None:
            width = length
        
        self.length = length*2
        self.width = width*2
        self.grid : list      = self.make_grid(length, width)
        self.graph : Graph    = Graph(self.grid)
        
        self.solutions : dict = {}
        
        pass
    
    def __str__(self) -> str:
        ans : str = ""
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    ans += '#'
                elif self.grid[i][j] == 0:
                    ans += ' '
            ans += "\n"
        return ans
    
    def show(self, cell_length)->None:
        pass
    
    def get_grid(self)->list:
        return self.grid
    
    def get_graph(self)->Graph:
        return self.graph
    
    def find_sol(self, start: tuple, end: tuple) -> list:
        "Solves a maze using the A* algorithm, returns a list of nodes to explore"
        
        def clean_path(path : list)->list:
            """Return a clean version of the path, preventing it from having alligned values which makes them useless

            Args:
                path (list): The shortest path

            Raises:
                TypeError: is the path given is not a list

            Returns:
                list: the speed_optimized shortedt_path
            """
            if type(path) != list:
                raise TypeError(f"Expected type : list, got : {type(path)}")
            
            if len(path) <= 2 :
                return path
            
            to_remove = ()
            for idx in range(2, len(path)):
                for i in (0, 1):
                    if path[idx-2][i] == path[idx-1][i] == path[idx][i]:
                        to_remove += (path[idx-1], )
            
            for supp in to_remove:
                path.remove(supp)
                
            return path
            

        def next_node(open_list: list)->tuple:
            """Get the next node to explore from the open list

            Args:
                open_list (list): the open list of nodes.

            Returns:
                open_list: the list of nodes with a node score for each
                curr_node: current_node (x, y) position
            """
            #Retrieve the node with the lowest score from the open list
            curr_score, curr_node = tuple(open_list[0])

            for n in open_list:
                if n[0] < curr_score:
                    curr_score = n[0]
                    curr_node = n[1]
                    
            # Remove the chosen node from the open list and return it along with the updated open list
            open_list.remove((curr_score, curr_node))
            return open_list, curr_node

        #Create a copy of the graph, add start and end nodes to it
        nest_graph: Graph = self.graph.copy()
 
        nest_graph = nest_graph + start

        nest_graph = nest_graph + end
    
        #Check if a solution for the given start and end nodes have already been calculated, if so returns that solution
        if (start, end) in self.solutions.keys():
            return self.solutions[(start, end)]

        open_list: list = list()  # List to store nodes to be explored
        storage: dict = dict()  # Dictionary to store node information

        curr_node = start
        
        keys = nest_graph.get_keys()
        
        #Initialize storage for each node in the graph
        for node in keys:
            storage[node] = {
                "F": None,
                "G": None,
                "H": None,
                "Last": None
            }

        #Set initial values for start node in the storage dictionary
        storage[start]["F"] = 0
        storage[start]["G"] = 0
        storage[start]["H"] = 0

        # Add the start node to the open list with score 0
        open_list.append((0, start))

        #A* algorithm - continue until the current node is the end node
        while curr_node != end:

            #Explore neighbors of the current node
            for n in nest_graph.map[curr_node]["origin"]:
                
                # try:
                #     storage[n[0]]["G"]
                # except:
                #     raise Exception(f"key error : {n[0]}\nFor : {storage.keys()}")
                
                if n[0] in storage.keys() and (storage[n[0]]["G"] is None or storage[n[0]]["G"] > storage[curr_node]["G"] + n[1]):
                    #Update the G, H, F scores and the last node for the neighbor
                    storage[n[0]]["G"] = storage[curr_node]["G"] + n[1]
                    storage[n[0]]["H"] = Coor.manhatanDistance(Coor(n[0][0], n[0][1]), Coor(end[0], end[1]))
                    storage[n[0]]["F"] = storage[n[0]]["G"] + storage[n[0]]["H"]
                    storage[n[0]]["Last"] = curr_node

                    open_list.append((storage[n[0]]["F"], n[0]))  # Add neighbor to the open list

            open_list, curr_node = next_node(open_list)  # Get the next node to explore

        #Reconstruct the path from end to start using the stored information (backtracking, going from the origin point of the end)
        ans = [end]
        curr_node = end
        while curr_node != start:
            curr_node = storage[curr_node]["Last"]
            ans.append(curr_node)
            
        #Reverse the path to get it from start to end
        ans.reverse()
        
        # Store the solution so if doesn't have to be re-computed if teh user ask for this path again
        self.solutions[(start, end)] = tuple(clean_path(ans))
        
        return self.solutions[(start, end)]

    
    @staticmethod
    def make_grid(l : int,
                 w : int) -> list:
        """Use the Hunt and kill algorithm to create a maze grid (much faster than the backtracking algorithm for large mazes)

        Args:
            l (int): the length of the grid
            w (int): the heigth of the grid
            
        Returns:
            grid (list): a 2D grid representing the maze
        """
        def visited_neigh(x : int,
                              y: int)->list:
            """return the list of all the nearby cells which are in the visited list

            Args:
                x (int): x coordinate
                y (int): y coordinate

            Returns:
                listing(list): all the nearby cells which are in the visited list
            """
            listing = []
            for (i, j) in [(-2, 0), (0, -2), (2, 0), (0, 2)]:
                if (0 < x+i < len(grid[0]) and 0 < y+j < len(grid)) and (x+i, y+j) in visited:
                    listing.append((x+i, y+j))
            return listing
            
        def non_visited_neigh(x : int,
                              y: int)->list:
            """return the list of all the nearby cells which are not in the visited list

            Args:
                x (int): x coordinate
                y (int): y coordinate

            Returns:
                listing(list): all the nearby cells which are not in the visited list
            """
            listing = []
            for (i, j) in [(-2, 0), (0, -2), (2, 0), (0, 2)]:
                if (0 < x+i < len(grid[0]) and 0 < y+j < len(grid)) and (x+i, y+j) not in visited:
                    listing.append((x+i, y+j))
            return listing
    
        #Initiate the grid
        grid = [[1 for _ in range((l*2)+1)]]
        for _ in range((w)):
                grid += [[1]+[i%2 for i in range((l*2)-1)]+[1], [1 for _ in range((l*2)+1)]]
            
        # Initialize tqdm with the total number of iterations
        #description = "Creating the maze..."
        #total_iterations = (l*w)  # Total number of iterations you expect
        #progress_bar = tqdm(total=total_iterations, desc=description)
        
        #Set the hunter at a random starting point and add it to the visited list
        cursor              = (random.choice([i for i in range(1, l-1, 2)]), random.choice([i for i in range(1, w-1, 2)]))
        visited : set       = set([cursor])
        #progress_bar.update(1)  # Manually update the progress bar
        
        #Do a first random walk
        possible_path   = non_visited_neigh(cursor[0], cursor[1])
        if len(possible_path):
            visited.add(cursor)
            
            #Start the random walk by actualising the cursor position to a random nearby non visited cell
            while len(possible_path):
                actual_pos = random.choice(non_visited_neigh(cursor[0], cursor[1]))
                visited.add(actual_pos)
                
                #progress_bar.update(1)  # Manually update the progress bar
                
                #We brak the wall between our current cell and the cell randomly chosen
                x_midd, y_midd = (actual_pos[0]-cursor[0])//2, (actual_pos[1]-cursor[1])//2
                grid[cursor[1]+y_midd][cursor[0]+x_midd] = 0
                
                #We actualyse the cursor position and non visited neighbors
                cursor = actual_pos
                possible_path   = non_visited_neigh(cursor[0], cursor[1])

        #the cursor index is used for backtracking
        while len(visited) < l * w:
            
            for (x, y) in ((i, j) for i in range(1, l*2, 2) for j in range(1, w*2, 2)):
                if (x, y) not in visited:
                    
                    neighb = visited_neigh(x, y)
                    if len(neighb):
                        neighb = random.choice(neighb)
                        cursor = (x, y)
                        
                        #Break the wall between the current cell and the visited neighbor
                        x_midd, y_midd = (neighb[0]-cursor[0])//2, (neighb[1]-cursor[1])//2
                        grid[cursor[1]+y_midd][cursor[0]+x_midd] = 0
                        #progress_bar.update(1)  # Manually update the progress bar
                        
                        possible_path   = non_visited_neigh(cursor[0], cursor[1])
                        visited.add((x, y))
                        
                        #Start the random walk by actualising the cursor position to a random nearby non visited cell
                        while len(possible_path):
                            actual_pos = random.choice(non_visited_neigh(cursor[0], cursor[1]))
                            visited.add(actual_pos)
                            
                            #progress_bar.update(1)  # Manually update the progress bar
                            
                            #We brak the wall between our current cell and the cell randomly chosen
                            x_midd, y_midd = (actual_pos[0]-cursor[0])//2, (actual_pos[1]-cursor[1])//2
                            grid[cursor[1]+y_midd][cursor[0]+x_midd] = 0
                            
                            #We actualyse the cursor position and non visited neighbors
                            cursor = actual_pos
                            possible_path   = non_visited_neigh(cursor[0], cursor[1])

        #progress_bar.close()  # Close the progress bar when done
        
        return grid
    
    def pr_bestPath(self, start, end)->None:
        """Print a board with the points of the graph you have to follow for going from the "start" point to the "end" point

        Args:
            start (tuple): starting point
            end (tuple): ending point
        """
        path = self.find_sol(start, end)
        
        ans : str = ""
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    ans += '#'
                elif (j, i) in path:
                    ans += '.'
                elif self.grid[i][j] == 0:
                    ans += ' '
            ans += "\n"
        print(ans)
