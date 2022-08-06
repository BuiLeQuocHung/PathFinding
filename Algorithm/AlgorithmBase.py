from DataSctructure.Matrix import Matrix
from DataSctructure.PathFinding_helper import History

class AlgorithmBase:
    def __init__(self, matrix: Matrix) -> None:
        self.matrix = matrix
    
    def path_finding():
        """
            find path from start_point to end_point
        """
        raise NotImplementedError('Implement path finding please!!')
    
    def get_path():
        """
            return path from start to end
        """
        raise NotImplementedError('Implement get path please!!')
    
    def gen_path(self, history_map: History):
        """
            Gen path from start to end using history_map
        """
        start = self.matrix.get_start()
        end = self.matrix.get_end()
        
        path = []
        cor = history_map.get_parent(end)
        while cor != start:
            path = [cor] + path
            cor = history_map.get_parent(cor)
        return path
    