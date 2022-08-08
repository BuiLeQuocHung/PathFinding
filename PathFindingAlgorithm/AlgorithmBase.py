from typing import List, Tuple
from DataStructure.Matrix import Matrix
from PathFindingAlgorithm.Helper.AlgorithmHelper import History

class AlgorithmBase:
    def __init__(self, matrix: Matrix) -> None:
        self.matrix = matrix
    
    def path_finding():
        """
            find path from start_point to end_point
        """
        raise NotImplementedError('Implement path finding please!!')
    
    def gen_path(self, history_map: History, start_cor, end_cor):
        """
            Gen path from start to end using history_map.
            Not include start and end point.
        """
        
        path = []
        cor = history_map.get_parent(end_cor)
        while cor and cor != start_cor:
            path = [cor] + path
            cor = history_map.get_parent(cor)
        return path
    
    def update_path(self, path: List[Tuple]):
        self.path = path
        
    def get_path(self) -> List[Tuple]:
        return self.path

    def update_processing_order(self, processing_order: List[Tuple]):
        self.processing_order = processing_order
    
    def get_processing_order(self):
        return self.processing_order
    
    def update_cost(self, cost):
        self.cost = cost
        
    def get_cost(self):
        return self.cost