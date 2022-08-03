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
        self.can_move = can_move
        self.cost = cost
        if not self.can_move:
            self.cost = None
    
    def can_move(self) -> bool:
        return self.can_move
    
    def get_cost(self) -> int:
        return self.cost

class Matrix:
    color = Cell_color()
    def __init__(self, m, n) -> None:
        self.start = (randint(0, m-1), randint(0, n-1))
        
        self.end = (randint(0, m-1), randint(0, n-1))
        while self.start == self.end:
            self.end = (randint(0, m-1), randint(0, n-1))
        
        self.m = m
        self.n = n
        self.matrix = [[Cell(can_move=True, cost=1) for j in range(self.n)] for i in range(self.m)]
        
        self.moves = [ (1,0), (-1,0), (0,1), (0,-1) ]
    
    def get_neighbors(self, cor) -> List[Tuple]:
        neightbors = []
        
        x, y = cor
        for move in self.moves:
            i, j = move
            
            new_cor = (x+i, y+j)
            if 0 <= x+i < self.m and 0 <= y+j < self.n \
                and self.get_cell(cor).can_move():
                    neightbors.append(new_cor)
        
        return neightbors

    def get_color(self, cor):
        cell = self.get_cell(cor)
        return self.color.get_color(cell.get_cost())
        
    def get_cell(self, cor) -> Cell:
        i, j = cor
        return self.matrix[i][j]

    def get_start(self) -> Tuple:
        return self.start
    
    def get_end(self) -> Tuple:
        return self.end