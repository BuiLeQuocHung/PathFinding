import enum
from Algorithm.Astar import Astar
from Algorithm.BFS import BFS
from Algorithm.BidirectionalSearch import BidirectionalSearch
from Algorithm.DFS import DFS
from Algorithm.Greedy import Greedy
from Algorithm.UCS import UCS
from DataStructure.Matrix import Matrix

class AlgorithmOption(enum.Enum):
    ASTAR = 'Astar'
    BFS = 'BFS'
    DFS = 'DFS'
    UCS = "UCS"
    BIDIRECTION = "Bidirection"
    GREEDY = "Greedy"
    
    @classmethod
    def to_list(cls):
        return list(map(lambda x: x.value, cls))
    
    @classmethod
    def default_value(cls):
        return cls.ASTAR.value

class AlgorithmSelection:
    def __init__(self) -> None:
        self.current_algorithm = None
        
    def load_algorithm(self, matrix: Matrix, algorithm_name):
        if algorithm_name == AlgorithmOption.ASTAR.value:
            return Astar(matrix)
        elif algorithm_name == AlgorithmOption.BFS.value:
            return BFS(matrix)
        elif algorithm_name == AlgorithmOption.DFS.value:
            return DFS(matrix)
        elif algorithm_name == AlgorithmOption.UCS.value:
            return UCS(matrix)
        elif algorithm_name == AlgorithmOption.BIDIRECTION.value:
            return BidirectionalSearch(matrix)
        elif algorithm_name == AlgorithmOption.GREEDY.value:
            return Greedy(matrix)
        
        raise ValueError("Algorithm not exists")
        
            
    def run_algorithm(self, matrix: Matrix, algorithm_name):
        self.current_algorithm = self.load_algorithm(matrix, algorithm_name)
        self.current_algorithm.path_finding()
        
    def get_path(self):
        return self.current_algorithm.get_path()
    
    def get_processing_order(self):
        return self.current_algorithm.get_processing_order()
    
    def get_cost(self):
        return self.current_algorithm.get_cost()