#################
##    Class    ##
## @ArthurrMrv ##
#################

class Coordinates:
    
    def __init__(self, x : int, y : int) -> None:
        
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        
        return f"{(self.x, self.y)}"
    
    def __sub__(self, SecondCoordinate):
        
        if type(SecondCoordinate) != Coordinates:
            
            raise Exception(f"{type(self)} and {type(SecondCoordinate)} can't be substract.")
        
        else:
            
            return Coordinates(self.x - SecondCoordinate.x, self.y - SecondCoordinate.y)
    
    def addToX(self, number):
        
        if (type(number) != float) and (type(number) != int):
            
            raise Exception(f"You can't add {type(number)} to an x coordinate.")
        
        else:
            
            return Coordinates(self.x + number, self.y)
        
    def addToY(self, number):
        
        if (type(number) != float) and (type(number) != int):
            
            raise Exception(f"You can't add {type(number)} to an y coordinate.")
        
        else:
            
            return Coordinates(self.x, self.y + number)
    
    def __isub__(self, SecondCoordinate):
        
        if type(SecondCoordinate) != Coordinates:
            
            raise Exception(f"{type(self)} and {type(SecondCoordinate)} can't be substract.")
        
        else:
            
            return self - SecondCoordinate
    
    def __add__(self, SecondCoordinate):
        
        if type(SecondCoordinate) != Coordinates:
            
            raise Exception(f"{type(self)} and {type(SecondCoordinate)} can't be added.")
        
        else:
            
            return Coordinates(self.x + SecondCoordinate.x, self.y + SecondCoordinate.y)
    
    def __iadd__(self, SecondCoordinate):
        
        if type(SecondCoordinate) != Coordinates:
            
            raise Exception(f"{type(self)} and {type(SecondCoordinate)} can't be added.")
        
        else:
            
            return self + SecondCoordinate
    
    def __eq__(self, SecondCoordinate) -> bool:
        
        if type(SecondCoordinate) != Coordinates:
            
            raise Exception("{self} and {SecondCoordinates} are not both coordinates.")
        
        else:
            
            return (self.x == SecondCoordinate.x) and (self.y == SecondCoordinate.y)
    
    def __ne__(self, SecondCoordinate) -> bool:
        
        if type(SecondCoordinate) != Coordinates:
            
            raise Exception("{self} and {SecondCoordinates} are not both coordinates.")
        
        else:
            
            return (self.x != SecondCoordinate.x) or (self.y != SecondCoordinate.y)
    
    def __mul__(self, SecondCoordinate):
        
        if (type(SecondCoordinate) == int) or (type(SecondCoordinate) == float):
            
            return Coordinates(self.x*SecondCoordinate, self.y*SecondCoordinate)
        
        elif type(SecondCoordinate) == Coordinates:
            
            return Coordinates(self.x*SecondCoordinate.x, self.y*SecondCoordinate.y)
        
        else:
            
            raise Exception(f'Trying to multiply {type(self)} with {type(SecondCoordinate)}.')
    
    def __truediv__(self, SecondCoordinate):
        
        if (type(SecondCoordinate) == int) or (type(SecondCoordinate) == float):
            
            return Coordinates(self.x/SecondCoordinate, self.y/SecondCoordinate)
        
        elif type(SecondCoordinate) == Coordinates:
            
            return Coordinates(self.x/SecondCoordinate.x, self.y/SecondCoordinate.y)
        
        else:
            
            raise Exception(f'Trying to divide {type(self)} with {type(SecondCoordinate)}.')
    
    def tuple(self):
        
        return (self.x, self.y)
    
    def convert(self, function):
        
        return Coordinates(function(self.x), function(self.y))
    
    def __floordiv__(self, SecondCoordinate):
        
        ThirdCoordinate = self / SecondCoordinate
        
        return Coordinates(int(ThirdCoordinate.x), int(ThirdCoordinate.y))
    
    @staticmethod
    def manhatanDistance(CoordinateOne, CoordinateTwo) -> float:
        if (type(CoordinateOne) != Coordinates) or (type(CoordinateTwo) != Coordinates):
            
            raise Exception("{CoordinateOne} and/or {CoordinateTwo} is/are not coordinate(s).")
        
        else:
            
            try:
                
                return int(abs(CoordinateOne.x - CoordinateTwo.x) + abs(CoordinateOne.y - CoordinateTwo.y))
            
            except ValueError:
                
                return float(abs(CoordinateOne.x - CoordinateTwo.x) + abs(CoordinateOne.y - CoordinateTwo.y))

    @staticmethod
    def euclidianDistance(CoordinateOne, CoordinateTwo) -> float:
        
        if (type(CoordinateOne) != Coordinates) or (type(CoordinateTwo) != Coordinates):
            
            raise Exception("{CoordinateOne} and/or {CoordinateTwo} is/are not coordinate(s).")
        
        else:
            
            return max(abs(CoordinateOne.x - CoordinateTwo.x), abs(CoordinateOne.y - CoordinateTwo.y))
        
    @staticmethod
    def tradiDistance(CoordinateOne, CoordinateTwo) -> float:
        
        if (type(CoordinateOne) != Coordinates) or (type(CoordinateTwo) != Coordinates):
            
            raise Exception("{CoordinateOne} and/or {CoordinateTwo} is/are not coordinate(s).")
        
        else:
            
            return pow(pow(CoordinateOne.x - CoordinateTwo.x, 2) + pow(CoordinateOne.y - CoordinateTwo.y, 2), 0.5)
        
    @staticmethod
    def random_Coordinates(x_min, x_max, y_min, y_max, coordinates_excluded : list = []):
        
        if (x_min > x_max) or (y_min > y_max):
            
            raise Exception(f' A minimum is greatter than a maximum : {x_min} > {x_max} or {y_min} > {y_max}.')
        
        possible_x : set = { i for i in range(x_min, x_max)}
        possible_y : set = { i for i in range(y_min, y_max)}
        
        impossibles_x : set = { i for i in [coordinate.x for coordinate in coordinates_excluded]}
        impossibles_y : set = {i for i in [coordinate.y for coordinate in coordinates_excluded]}
        
        if len(possible_x - impossibles_x) == 0:
            
            raise Exception('All the available x are impossible')
        
        elif len(possible_y - impossibles_y) == 0:
            
            raise Exception('All the available y are impossible')

        else:
            
            import random
            
            random_coordinate = Coordinates(random.randint(x_min, x_max), random.randint(y_min, y_max))
            
            while random_coordinate in coordinates_excluded:
                
                random_coordinate = Coordinates(random.randint(x_min, x_max), random.randint(y_min, y_max))
            
            return random_coordinate
