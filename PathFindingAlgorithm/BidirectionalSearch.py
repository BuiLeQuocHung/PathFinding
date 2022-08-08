from PathFindingAlgorithm.AlgorithmBase import AlgorithmBase
from DataStructure.Matrix import Matrix
from PathFindingAlgorithm.Helper.AlgorithmHelper import Cost, History

class BidirectionalSearch(AlgorithmBase):
    def __init__(self, matrix: Matrix) -> None:
        super().__init__(matrix)
        
    def path_finding(self):
        start_cor = self.matrix.get_start_cor()
        end_cor = self.matrix.get_end_cor()
        
        queue_start = [start_cor]
        queue_end = [end_cor]
        
        history_map_start = History()
        history_map_start.update(None, start_cor)
        
        history_map_end = History()
        history_map_end.update(None, end_cor)
        
        cost_map_start = Cost()
        cost_map_start.update(start_cor, self.matrix.get_cell(start_cor).get_cost())
        
        cost_map_end = Cost()
        cost_map_end.update(end_cor, self.matrix.get_cell(end_cor).get_cost())
        
        processing_order = []
        
        dictionary = {
            0: {
                'begin_cor': start_cor,
                'queue': queue_start,
                'history_map': history_map_start,
                'cost_map': cost_map_start,
                'visited': {}
            },
            1: {
                'begin_cor': end_cor,
                'queue': queue_end,
                'history_map': history_map_end,
                'cost_map': cost_map_end,
                'visited': {}
            }
        }
        
        flag = False
        
        count = 0
        next_count = (count + 1) % 2
        while queue_start and queue_end:
            visited_next = dictionary[next_count]['visited']
            
            queue_cur = dictionary[count]['queue']
            history_map_cur = dictionary[count]['history_map']
            cost_map_cur = dictionary[count]['cost_map']
            visited_cur = dictionary[count]['visited']
            
            cur_cor = queue_cur.pop(0)
            visited_cur[cur_cor] = True
            
            if cur_cor in visited_next:
                flag = True
                break
            
            if cur_cor not in [start_cor, end_cor]:
                processing_order.append(cur_cor)

            cur_cost = cost_map_cur.get_path_cost(cur_cor)
            
            for next_cor in self.matrix.get_neighbors(cur_cor):
                if not history_map_cur.is_cor_exist(next_cor):
                    history_map_cur.update(cur_cor, next_cor)
                    next_cost = cur_cost + self.matrix.get_cell(next_cor).get_cost()
                    cost_map_cur.update(next_cor, next_cost)
                    queue_cur.append(next_cor)
            
            count = next_count
            next_count = (next_count + 1) % 2
        
        if start_cor == end_cor:
            path = []
            cost = None
        elif flag:
            history_map_next = dictionary[next_count]['history_map']
            begin_cor_next = dictionary[next_count]['begin_cor']
            first_path = self.gen_path(history_map_next, begin_cor_next, history_map_cur.get_parent(cur_cor))
            
            begin_cor_cur = dictionary[count]['begin_cor']
            second_path = self.gen_path(history_map_cur, begin_cor_cur, cur_cor)
            
            path = first_path + list(reversed(second_path))
            
            cost_map_cur = dictionary[count]['cost_map']
            cost_map_next = dictionary[next_count]['cost_map']
            cost = cost_map_cur.get_path_cost(history_map_cur.get_parent(cur_cor)) \
                + cost_map_next.get_path_cost(cur_cor)
        else:
            path = []
            cost = None
        
        self.update_path(path)
        self.update_processing_order(processing_order)
        self.update_cost(cost)