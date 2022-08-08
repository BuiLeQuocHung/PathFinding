from random import randint, choice
from typing import List, Tuple
from Decorator.Singleton import Singleton
from config import CELL_COLOR_WHITE, CELL_COLOR_BROWN, CELL_COLOR_GREEN, CELL_COLOR_BLUE, \
    CELL_START_COLOR, CELL_END_COLOR

@Singleton
class Cell_color:
    def __init__(self) -> None:
        self.color = {
            1: CELL_COLOR_WHITE,   # white
            2: CELL_COLOR_BROWN,    # brown
            3: CELL_COLOR_GREEN,     # green
            4: CELL_COLOR_BLUE    # blue
        }
        
    def get_color(self, cost):
        return self.color[cost]
    
    def get_number_of_colors(self):
        return len(self.color)
    

class Cell:
    color: Cell_color = Cell_color.instance()
    def __init__(self, can_move: bool = True, cost: int = 1) -> None:
        self._can_move = can_move
        self.cost = cost
        if not self.can_move:
            self.cost = None
    
    def can_move(self) -> bool:
        return self._can_move
    
    def get_cost(self) -> int:
        return self.cost
    
    def update_cell(self, can_move: bool, cost: int) -> None:
        self._can_move = can_move
        self.cost = cost
        if not self._can_move:
            self.cost = None
    
    def get_color(self):
        if not self._can_move:
            return (0,0,0)
        return self.color.get_color(self.cost)
            
# for start and end point
class Special_Cell(Cell):
    def __init__(self, cor: Tuple, can_move: bool = True, cost: int = 1) -> None:
        super().__init__(can_move, cost)
        self.cor = cor
        
    def update_cor(self, cor):
        self.cor = cor
    
    def get_cor(self):
        return self.cor
    
    def update_cell(self, can_move: bool, cost: int) -> None:
        pass

@Singleton
class Matrix:
    color = Cell_color.instance()
    start_color = CELL_START_COLOR # red
    end_color = CELL_END_COLOR # purple
    moves = [ (1,0), (-1,0), (0,1), (0,-1) ]
    
    def __init__(self, m, n, uniform_cost = False, walls = True) -> None:
        self. m = m
        self.n = n
        self.gen_start_and_end_points()
        self.gen_matrix(uniform_cost, walls)
            
        
    def gen_start_and_end_points(self):
        start_cor = (randint(0, self.m-1), randint(0, self.n-1))
        self.start = Special_Cell(start_cor)

        end_cor = (randint(0, self.m-1), randint(0, self.n-1))
        while start_cor == end_cor:
            end_cor = (randint(0, self.m-1), randint(0, self.n-1))
        self.end = Special_Cell(end_cor)
        
    def gen_matrix(self, uniform_cost: bool, walls: bool):
        choices = [True]*8 + [False] if walls else [True]
        self.matrix = [[None]*self.n for i in range(self.m)]
        for i in range(self.m):
            for j in range(self.n):
                cost = 1 if uniform_cost else randint(1,4)
                can_move = choice(choices)
                self.matrix[i][j] = Cell(can_move, cost)
    
    def get_neighbors(self, cor) -> List[Tuple]:
        neighbors = []
        x, y = cor
        for move in self.moves:
            i, j = move
            new_cor = (x+i, y+j)
            if 0 <= x+i < self.m and 0 <= y+j < self.n and self.get_cell(new_cor).can_move():
                    neighbors.append(new_cor)
        return neighbors

    def get_color(self, cor) -> Tuple:
        if cor == self.start.get_cor():
            return self.start_color
        
        if cor == self.end.get_cor():
            return self.end_color
        
        cell = self.get_cell(cor)
        return cell.get_color()
        
    def get_cell(self, cor) -> Cell:
        i, j = cor
        if cor == self.start.get_cor():
            return self.start
        if cor == self.end.get_cor():
            return self.end
        return self.matrix[i][j]

    def get_start_cor(self) -> Tuple:
        return self.start.get_cor()
    
    def get_end_cor(self) -> Tuple:
        return self.end.get_cor()
    
    def get_width(self):
        return self.m
    
    def get_height(self):
        return self.n
    
    def update_matrix(self, matrix):
        self.matrix = matrix
    