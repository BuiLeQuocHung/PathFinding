from typing import Tuple
from random import randint

class Point:
    def __init__(self, cor: Tuple, cost: int) -> None:
        self.cost = cost
        self.cor = cor
    
    def get_cost(self) -> int:
        return self.cost
    
    def get_cor(self) -> Tuple:
        return self.cor
    
class History:
    def __init__(self) -> None:
        self.history = {}
        
    def update(self, parent_cor: Tuple, cur_cor: Tuple) -> None:
        self.history[cur_cor] = parent_cor
    
    def get_parent(self, cur_cor: Tuple) -> Tuple:
        return self.history[cur_cor]
    
class Cost:
    def __init__(self) -> None:
        self.cost = {}
    
    def is_cor_exist(self, cor):
        return cor in self.cost
    
    def compare_cost(self, cor, new_cost):
        return new_cost < self.cost[cor]
    
    def update(self, cor, new_cost):
        self.cost[cor] = new_cost

class Cell:
    def __init__(self, can_move: bool = True, cost: int = 1) -> None:
        self.can_move = can_move
        self.cost = cost
        if not self.can_move:
            self.cost = None
    
    def can_move(self):
        return self.can_move
    
    def get_cost(self):
        return self.cost

class Matrix:
    def __init__(self, m, n) -> None:
        self.start = (randint(0, m-1), randint(0, n-1))
        
        self.end = (randint(0, m-1), randint(0, n-1))
        while self.start == self.end:
            self.end = (randint(0, m-1), randint(0, n-1))
        
        self.m = m
        self.n = n
        self.matrix = [[Cell(can_move=True, cost=1) for j in range(self.n)] for i in range(self.m)]
        
        self.moves = [ (1,0), (-1,0), (0,1), (0,-1) ]
    
    def get_neighbors(self, cor):
        neightbors = []
        
        x, y = cor
        for move in self.moves:
            i, j = move
            
            new_cor = (x+i, y+j)
            if 0 <= x+i < self.m and 0 <= y+j < self.n \
                and self.get_cell(cor).can_move():
                    neightbors.append(new_cor)
        
        return neightbors
        
    def get_cell(self, cor) -> Cell:
        i, j = cor
        return self.matrix[i][j]

    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end