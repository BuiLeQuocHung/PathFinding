from typing import List, Tuple
from Algorithm.AlgorithmBase import AlgorithmBase
from DataSctructure.PathFinding_helper import History

class DFS(AlgorithmBase):
    def __init__(self, matrix) -> None:
        super().__init__(matrix)
        
    def path_finding(self):        
        start = self.matrix.get_start()
        end = self.matrix.get_end()
        
        stack = [start]
        
        history_map = History()
        history_map.update(None, start)
        
        processing_order = []
        
        while stack:
            cur_cor = stack.pop()
            
            if cur_cor not in [start, end]:
                processing_order.append(cur_cor)

            if cur_cor == end:
                break
            
            for next_cor in self.matrix.get_neighbors(cur_cor):
                if not history_map.is_cor_exist(next_cor):
                    history_map.update(cur_cor, next_cor)
                    stack.append(next_cor)
        
        if history_map.is_cor_exist(end):
            path = self.gen_path(history_map)
        else:
            path = []
            
        self.update_path(path)
        self.update_processing_order(processing_order)
    
    def update_path(self, path: List[Tuple]):
        self.path = path
        
    def get_path(self) -> List[Tuple]:
        return self.path

    def update_processing_order(self, processing_order: List[Tuple]):
        self.processing_order = processing_order
    
    def get_processing_order(self):
        return self.processing_order