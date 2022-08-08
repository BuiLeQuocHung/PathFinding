from PathFindingAlgorithm.AlgorithmBase import AlgorithmBase
from PathFindingAlgorithm.Helper.AlgorithmHelper import Cost, History

class DFS(AlgorithmBase):
    def __init__(self, matrix) -> None:
        super().__init__(matrix)
        
    def path_finding(self):        
        start_cor = self.matrix.get_start_cor()
        end_cor = self.matrix.get_end_cor()
        
        stack = [start_cor]
        
        history_map = History()
        history_map.update(None, start_cor)
        
        cost_map = Cost()
        cost_map.update(start_cor, self.matrix.get_cell(start_cor).get_cost())
        
        processing_order = []
        
        while stack:
            cur_cor = stack.pop()
            
            if cur_cor not in [start_cor, end_cor]:
                processing_order.append(cur_cor)

            if cur_cor == end_cor:
                break
            
            cur_cost = cost_map.get_path_cost(cur_cor)
            
            for next_cor in self.matrix.get_neighbors(cur_cor):
                if not history_map.is_cor_exist(next_cor):
                    history_map.update(cur_cor, next_cor)
                    next_cost = cur_cost + self.matrix.get_cell(next_cor).get_cost()
                    cost_map.update(next_cor, next_cost)
                    stack.append(next_cor)
        
        if history_map.is_cor_exist(end_cor):
            path = path = self.gen_path(history_map, start_cor, end_cor)
            cost = cost_map.get_path_cost(end_cor)
        else:
            path = []
            cost = None
            
        self.update_path(path)
        self.update_processing_order(processing_order)
        self.update_cost(cost)