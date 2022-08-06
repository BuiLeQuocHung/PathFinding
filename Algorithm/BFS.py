from typing import List, Tuple
from Algorithm.AlgorithmBase import AlgorithmBase
from DataSctructure.PathFinding_helper import History

class BFS(AlgorithmBase):
    def __init__(self, matrix) -> None:
        super().__init__(matrix)
        
    def path_finding(self):        
        start_cor = self.matrix.get_start_cor()
        end_cor = self.matrix.get_end_cor()
        
        queue = [start_cor]
        
        history_map = History()
        history_map.update(None, start_cor)
        
        processing_order = []
        
        while queue:
            cur_cor = queue.pop(0)
            
            if cur_cor not in [start_cor, end_cor]:
                processing_order.append(cur_cor)

            if cur_cor == end_cor:
                break
            
            for next_cor in self.matrix.get_neighbors(cur_cor):
                if not history_map.is_cor_exist(next_cor):
                    history_map.update(cur_cor, next_cor)
                    queue.append(next_cor)
        
        if history_map.is_cor_exist(end_cor):
            path = self.gen_path(history_map)
        else:
            path = []
            
        self.update_path(path)
        self.update_processing_order(processing_order)