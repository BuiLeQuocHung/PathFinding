from typing import List, Tuple
from DataSctructure.Heap import MinHeap
from DataSctructure.PathFinding_helper import Cost, History, Point
from Base import Base



class Astar(Base):
    def __init__(self, matrix) -> None:
        super().__init__(matrix)
        
    def path_finding(self):
        start = self.matrix.get_start()
        end = self.matrix.get_end()
        
        min_heap = MinHeap()
        min_heap.add(Point(self, value=0))
        
        history_map = History()
        history_map.update(None, start)
        
        cost_map = Cost()
        
        while not min_heap.isEmpty():
            point = min_heap.pop()
            
            cur_cost = point.get_cost()
            cur_cor = point.get_cor()
            
            if cur_cor == end:
                break
            
            for next_cor in self.matrix.get_neighbors(cur_cor):
                path_cost = cur_cost + self.matrix.get_cell(next_cor).get_cost()
                est_cost = self.heuristic(next_cor, end)
                priority = path_cost + est_cost
                
                if not cost_map.is_cor_exist(next_cor) or cost_map.compare_cost(next_cor, priority):
                    cost_map.update(next_cor, path_cost)
                    history_map.update(cur_cor, next_cor)
                    min_heap.add(Point(next_cor, priority))
    
        if cost_map.is_cor_exist(end):
            path = self.gen_path(history_map)
        else:
            path = []
        self.update_path(path)
    
    def gen_path(self, history_map: History):
        """
            Gen path from start to end using history_map
        """
        path = []
        cor = self.matrix.get_end()
        while cor:
            path = [cor] + path
            cor = history_map.get_parent(cor)
        return path
    
    def heuristic(self, cur_point, end) -> int:
        cur_x, cur_y = cur_point
        end_x, end_y = end
        return abs(end_x - cur_x) + abs(end_y - cur_y)
    
    def update_path(self, path: List[Tuple]):
        self.path = path

    
    