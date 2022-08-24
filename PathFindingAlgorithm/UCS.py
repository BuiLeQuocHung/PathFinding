from PathFindingAlgorithm.AlgorithmBase import AlgorithmBase
from DataStructure.Heap import MinHeap
from DataStructure.Matrix import Matrix
from PathFindingAlgorithm.Helper.AlgorithmHelper import Cost, History, Point


class UCS(AlgorithmBase):
    def __init__(self, matrix: Matrix) -> None:
        super().__init__(matrix)
    
    def path_finding(self):
        start_cor = self.matrix.get_start_cor()
        end_cor = self.matrix.get_end_cor()
        
        visited = {}
        
        min_heap = MinHeap([Point(start_cor, self.matrix.get_cell(start_cor).get_cost())])
        
        history_map = History()
        history_map.update(None, start_cor)
        
        cost_map = Cost()
        cost_map.update(start_cor, self.matrix.get_cell(start_cor).get_cost())
        
        processing_order = []
        visited = {}
        
        while not min_heap.isEmpty():
            point = min_heap.pop()
            
            cur_cor = point.get_cor()
            
            
            if cur_cor not in [start_cor, end_cor] and cur_cor not in visited:
                processing_order.append(cur_cor)
                visited[cur_cor] = True

            if cur_cor == end_cor:
                break
            
            cur_cost = cost_map.get_path_cost(cur_cor)
            
            visited[point] = True
            
            for next_cor in self.matrix.get_neighbors(cur_cor):
                if next_cor not in visited:
                    next_cost = cur_cost + self.matrix.get_cell(next_cor).get_cost()
                    if not history_map.is_cor_exist(next_cor) or cost_map.compare_cost(next_cor, next_cost):
                        history_map.update(cur_cor, next_cor)
                        cost_map.update(next_cor, next_cost)
                        min_heap.add(Point(next_cor, next_cost))
        
        if history_map.is_cor_exist(end_cor):
            path = path = self.gen_path(history_map, start_cor, end_cor)
            cost = cost_map.get_path_cost(end_cor)
        else:
            path = []
            cost = None
            
        self.update_path(path)
        self.update_processing_order(processing_order)
        self.update_cost(cost)
            
        
    