from PathFindingAlgorithm.AlgorithmBase import AlgorithmBase
from DataStructure.Heap import MinHeap
from DataStructure.Matrix import Matrix
from PathFindingAlgorithm.Helper.AlgorithmHelper import Cost, History, Point

class Greedy(AlgorithmBase):
    def __init__(self, matrix: Matrix) -> None:
        super().__init__(matrix)
        
    def path_finding(self):
        start_cor = self.matrix.get_start_cor()
        end_cor = self.matrix.get_end_cor()
        
        min_heap = MinHeap([])
        min_heap.add(Point(start_cor, self.matrix.get_cell(start_cor).get_cost()))
        
        history_map = History()
        history_map.update(None, start_cor)
        
        cost_map = Cost()
        cost_map.update(start_cor, self.matrix.get_cell(start_cor).get_cost())
        
        processing_order = []
        
        while not min_heap.isEmpty():
            point = min_heap.pop()
            
            cur_cor = point.get_cor()
            
            if cur_cor not in [start_cor, end_cor]:
                processing_order.append(cur_cor)

            if cur_cor == end_cor:
                break
            
            cur_cost = cost_map.get_path_cost(cur_cor)
            
            for next_cor in self.matrix.get_neighbors(cur_cor):
                path_cost = cur_cost + self.matrix.get_cell(next_cor).get_cost()
                est_cost = self.heuristic(next_cor, end_cor)
                if not history_map.is_cor_exist(next_cor):
                    cost_map.update(next_cor, path_cost)
                    history_map.update(cur_cor, next_cor)
                    min_heap.add(Point(next_cor, est_cost))
    
        if history_map.is_cor_exist(end_cor):
            path = self.gen_path(history_map, start_cor, end_cor)
            cost = cost_map.get_path_cost(end_cor)
        else:
            path = []
            cost = None
            
        self.update_path(path)
        self.update_processing_order(processing_order)
        self.update_cost(cost)
        
    def heuristic(self, cur_point, end_point) -> int:
        cur_x, cur_y = cur_point
        end_x, end_y = end_point
        return abs(end_x - cur_x) + abs(end_y - cur_y)
        