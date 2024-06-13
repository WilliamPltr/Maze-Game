import random
import turtle
from Coordinates import Coordinates as Coor
#from tqdm import tqdm

class Graph:
    
    direction : dict = {
                (0, -1) : "S",
                (0, 1) : "N",
                (-1, 0) : "W",
                (1, 0) : "E"
            }
    
    def __init__(self, grid : list, map = None) -> None:
        if map == None:
            self.map : dict = self.get_map(grid)
        else:
            self.map = map
            
        self.origin : list = grid.copy()
        
    def __add__(self, point):
        
        map_two = self.map.copy()
        
        #If the node to add is already in the graph or does not corresponds to an existing cell of the maze grid, returns the actual graph without modifications
        if (point in self.get_keys()) or not(point[0]%2 and point[1]%2) or \
            not(0 <= point[0] < len(self.origin[0]) and 0 <= point[1] < len(self.origin)):
                return self
        
        #Else we check in which direction we can go from this point
        map_two[point] = {
            "S" : bool(not(self.origin[point[1]-1][point[0]])),
            "E" : bool(not(self.origin[point[1]][point[0]+1])),
            "W" : bool(not(self.origin[point[1]][point[0]-1])),
            "N" : bool(not(self.origin[point[1]+1][point[0]])),
            "origin" : set()
        }
        
        #We link this node to the other nodes of the graph (depending on which direction you can go from it)
        for (i, j) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            (x, y) = point
            dir = self.direction[(i, j)]
            
            #While no graph point is found we continue to go in that direction
            while map_two[point][dir]:
                
                #if we find a graph point, we add it to the possible ways from this point
                if (x+i, y+j) in map_two.keys():
                    dist =  Coor.manhatanDistance(Coor(point[0], point[1]), Coor(x+i, y+j))
                    map_two[(x+i, y+j)]["origin"].add((point, dist))
                    map_two[point]["origin"].add(((x+i, y+j), dist))
                    map_two[point][dir] = False
                else:
                    (x, y) = (x+i, y+j)
                    
        return Graph(self.origin, map_two)
    
    def __str__(self) -> str:
        ans : str = ""
        for i in range(len(self.origin)):
            for j in range(len(self.origin[i])):
                if (j, i) in self.get_keys():
                    ans += 'o'
                elif self.origin[i][j] == 1:
                    ans += '#'
                elif self.origin[i][j] == 0:
                    ans += ' '
            ans += "\n"
        return ans
    
    def show(self)->None:
        pass
    
    def is_in(self, point)-> bool:
        pass
    
    def get_map(self, grid)->dict:
        def nb_neighbors(grid, x, y)->int:
            """returns the number of cells you can go to from a given cell

            Args:
                grid (list): the maze 2D grid
                x (int): x coordinate of the point to studdy
                y (int): y coordinate of the point to study

            Returns:
                int: number of cells you can go to
            """
            return [grid[y+j][x+i] for (i, j) in [(-1, 0), (1, 0), (0, -1), (0, 1)]].count(0)
    
        def is_corridor(grid, x, y):
            """returns if a given point of the grid is situated in a corridor or not

            Args:
                grid (list): the maze 2D grid
                x (int): x coordinate of the point to studdy
                y (int): y coordinate of the point to study

            Returns:
                bool: is the point in a corridor
            """
            return grid[y+1][x] == grid[y-1][x]
            
        def get_nodes(grid)->dict:
            """Create a list of non linked nodes.

            Args:
                grid (list): the maze 2D grid

            Returns:
                nodes(dict): the map of nodes  
            """
            nodes = {}
            for y in range(1, len(grid)-1, 2):
                for x in range(1, len(grid[0])-1, 2):                    
                    if (nb_neighbors(grid, x, y) >= 3 or nb_neighbors(grid, x, y) <= 1) or not(is_corridor(grid, x, y)):
                        nodes[(x, y)]={
                            "S" : bool(grid[y-1][x] == 0),
                            "E" : bool(grid[y][x+1] == 0),
                            "W" : bool(grid[y][x-1] == 0),
                            "N" : bool(grid[y+1][x] == 0),
                            "origin" : set()
                            }
                        
            return nodes

        def link_nodes(nodes : dict)->dict:
            """Link all the nodes of a given graph map
            
            A link is the connection between two nodes. 
            A linked graph is a graph with the nodes interconected, such that from a given node, you have a list of all his 
            neighbors and the distance separating them.

            Args:
                nodes (dict): the map graph

            Returns:
                dict: the linked ap graph
            """
            
            #goes through all the nodes of the graph
            for k in list(nodes.keys()):
                (x, y) = k
                
                #for every direction
                for (i, j) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    (x, y) = (k[0]+i, k[1]+j)
                    
                    #If the node is linkable in that direction, while we haven't found another node of the graph
                    dir = self.direction[(i, j)]
                    while nodes[k][dir]:
                        
                        #If we find a graph point, we add it to the possible ways from this point
                        #Else we go one step further in that direction
                        if (x, y) in nodes.keys():
                            dist =  Coor.manhatanDistance(Coor(k[0], k[1]), Coor(x, y))
                            nodes[(x, y)]["origin"].add((k, dist))
                            nodes[k]["origin"].add(((x, y), dist))
                            nodes[k][dir] = False
                        else:
                            (x, y) = (x+i, y+j)
                            
            return nodes
        
        return link_nodes(get_nodes(grid))
    
    def get_keys(self)->tuple:
        return tuple(self.map.keys())
    
    def copy(self):
        return Graph(self.origin.copy(), self.map.copy())
