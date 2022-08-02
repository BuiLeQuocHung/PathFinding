from DataSctructure.Heap import MinHeap
from DataSctructure.Others import Cost, History, Point
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
            x, y = cur_cor
            
            for next_cor in self.matrix.get_neighbors(cur_cor):
                path_cost = cur_cost + self.matrix.get_cell(next_cor).get_cost()
                est_val = self.heuristic(next_cor)
                next_cost = path_cost + est_val
                
                if not cost_map.is_cor_exist(next_cor) or cost_map.compare_cost(next_cor, next_cost):
                    cost_map.update(next_cor, next_cost)
                    history_map.update(cur_cor, next_cor)
                    
                    
                    
                    
                    
                    pass
    
    def heuristic(self, cur_point):
        cur_x, cur_y = cur_point
        end_x, end_y = self.end_point
        return abs(end_x - cur_x) + abs(end_y - cur_y)

    
    