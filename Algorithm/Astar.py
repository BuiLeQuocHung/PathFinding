from typing import List, Tuple
from DataSctructure.Heap import MinHeap
from DataSctructure.PathFinding_helper import Cost, History, Point
from Algorithm.AlgorithmBase import AlgorithmBase

class Astar(AlgorithmBase):
    path = []
    processing_order = []
    
    def __init__(self, matrix) -> None:
        super().__init__(matrix)
        
    def path_finding(self):
        start = self.matrix.get_start()
        end = self.matrix.get_end()
        
        min_heap = MinHeap()
        min_heap.add(Point(start, self.matrix.get_cell(start).get_cost()))
        
        history_map = History()
        history_map.update(None, start)
        
        cost_map = Cost()
        cost_map.update(start, 0)
        
        processing_order = []
        
        while not min_heap.isEmpty():
            point = min_heap.pop()
            
            cur_cor = point.get_cor()
            cur_cost = cost_map.get_path_cost(cur_cor)
            
            if cur_cor not in [start, end]:
                processing_order.append(cur_cor)

            if cur_cor == end:
                break
            
            for next_cor in self.matrix.get_neighbors(cur_cor):
                path_cost = cur_cost + self.matrix.get_cell(next_cor).get_cost()
                est_cost = self.heuristic(next_cor, end)
                priority = path_cost + est_cost
                
                if not history_map.is_cor_exist(next_cor) or cost_map.compare_cost(next_cor, path_cost):
                    cost_map.update(next_cor, path_cost)
                    history_map.update(cur_cor, next_cor)
                    min_heap.add(Point(next_cor, priority))
    
        if history_map.is_cor_exist(end):
            path = self.gen_path(history_map)
        else:
            path = []
            
        self.update_path(path)
        self.update_processing_order(processing_order)
    
    def heuristic(self, cur_point, end) -> int:
        cur_x, cur_y = cur_point
        end_x, end_y = end
        return abs(end_x - cur_x) + abs(end_y - cur_y)
    
    def update_path(self, path: List[Tuple]):
        self.path = path
        
    def get_path(self) -> List[Tuple]:
        return self.path

    def update_processing_order(self, processing_order: List[Tuple]):
        self.processing_order = processing_order
    
    def get_processing_order(self):
        return self.processing_order