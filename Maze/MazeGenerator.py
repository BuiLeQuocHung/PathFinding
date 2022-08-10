import random
from typing import Tuple, List
from DataStructure.Matrix import Cell
from Decorator.Singleton import Singleton

class MazeGenerator:
    def __init__(self, m, n) -> None:
        self.m = m
        self.n = n
        
    def get_cell(self, cor) -> Cell:
        i, j = cor
        return self.matrix[i][j]
        
    def get_step_neighbors(self, cor) -> List[Tuple]:
        moves = [ (2,0), (-2,0), (0,2), (0,-2) ]
        neighbors = []
        
        x, y = cor
        for move in moves:
            i, j = move
            new_cor = (x+i, y+j)
            if 1 <= x+i < self.m - 1 and 1 <= y+j < self.n - 1 and self.surrounded_by_walls(new_cor):
                neighbors.append(new_cor)
        return neighbors
    
    def surrounded_by_walls(self, cor) -> bool:
        moves = [ (1,0), (-1,0), (0,1), (0,-1) ]
        
        x, y = cor
        for move in moves:
            i, j = move
            new_cor = (x+i, y+j)
            if 1 <= x+i < self.m - 1 and 1 <= y+j < self.n - 1 and self.get_cell(new_cor).can_move():
                return False
        return True
    
    def gen_maze(self):
        self.matrix = [[None]* self.n for i in range(self.m)]
        for i in range(self.m):
            for j in range(self.n):
                self.matrix[i][j] = Cell(can_move=False)
        
        
        for i in range(1, self.m - 1, 2):
            for j in range(1, self.n - 1, 2):
                self.matrix[i][j] = Cell(can_move=True, cost=random.randint(1,4))
        
        stack = []
        current_cell = (1, 1)
        
        while True:
            neighbours = self.get_step_neighbors(current_cell)
            
            if not neighbours:
                if not stack:
                    return self.matrix
                current_cell = stack.pop()
                continue
            
            next_cell = random.choice(neighbours)
            middle_cell = self.middle_cell(current_cell, next_cell)
            self.get_cell(middle_cell).update_cell(can_move=True, cost=random.randint(1,4))
            stack.append(current_cell)
            current_cell = next_cell
            
    def middle_cell(self, cor1: Tuple, cor2: Tuple) -> Tuple:
        x1, y1 = cor1
        x2, y2 = cor2
        return ( (x1+x2)//2, (y1+y2)//2 )