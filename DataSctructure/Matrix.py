from random import randint
from typing import List, Tuple
import enum

class Cell_color:
    def __init__(self) -> None:
        self.color = {
            1: (245,245,220),   # white
            2: (210,105,30),    # brown
            3: (102,205,0),     # green
            4: (122,197,205)    # blue
        }
        
    def get_color(self, cost):
        if cost not in self.color:
            return (0,0,0) # black
        return self.color[cost]
    

class Cell:
    def __init__(self, can_move: bool = True, cost: int = 1) -> None:
        self._can_move = can_move
        self.cost = cost
        if not self.can_move:
            self.cost = None
    
    def can_move(self) -> bool:
        return self._can_move
    
    def get_cost(self) -> int:
        return self.cost

# for start and end point
class Special_Cell(Cell):
    def __init__(self, cor: Tuple, can_move: bool = True, cost: int = 1) -> None:
        super().__init__(can_move, cost)
        self.cor = cor
        
    def update_cor(self, cor):
        self.cor = cor
    
    def get_cor(self):
        return self.cor

class Matrix:
    color = Cell_color()
    start_color = (238,44,44) # red
    end_color = (139,28,98) # purple
    
    def __init__(self, m, n) -> None:
        start_cor = (randint(0, m-1), randint(0, n-1))
        self.start = Special_Cell(start_cor)

        end_cor = (randint(0, m-1), randint(0, n-1))
        while start_cor == end_cor:
            end_cor = (randint(0, m-1), randint(0, n-1))
        self.end = Special_Cell(end_cor)
        
        self.m = m
        self.n = n
        self.matrix = [[Cell(can_move=True, cost=randint(1,4)) for j in range(self.n)] for i in range(self.m)]
        
        self.moves = [ (1,0), (-1,0), (0,1), (0,-1) ]
    
    def get_neighbors(self, cor) -> List[Tuple]:
        neightbors = []
        x, y = cor
        for move in self.moves:
            i, j = move
            new_cor = (x+i, y+j)
            if 0 <= x+i < self.m and 0 <= y+j < self.n and self.get_cell(new_cor).can_move():
                    neightbors.append(new_cor)
        
        return neightbors

    def get_color(self, cor) -> Tuple:
        if cor == self.start.get_cor():
            return self.start_color
        
        if cor == self.end.get_cor():
            return self.end_color
        
        cell = self.get_cell(cor)
        return self.color.get_color(cell.get_cost())
        
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
    