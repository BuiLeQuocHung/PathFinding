from typing import Tuple

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
        
    def is_cor_exist(self, cor) -> bool:
        return cor in self.history
    
    def get_parent(self, cur_cor: Tuple) -> Tuple:
        return self.history[cur_cor]
    
class Cost:
    def __init__(self) -> None:
        self.cost = {}
    
    def compare_cost(self, cor, new_cost) -> bool:
        """
            Return True if new_cost < cur_cost, else False
        """
        return new_cost < self.cost[cor]
    
    def update(self, cor, new_cost) -> None:
        self.cost[cor] = new_cost
        
    def get_path_cost(self, cor):
        if cor not in self.cost:
            print(list(self.cost.keys()))
        return self.cost[cor]

