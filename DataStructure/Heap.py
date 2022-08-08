from typing import List
from DataStructure.AlgorithmHelper import Point


class MinHeap:
    def __init__(self, arr: List[Point]):
        self.n = len(arr)
        self.arr = arr
    
    def build_heap(self) -> None:
        for i in range(self.n//2, -1, -1):
            self.top_down(i)
    
    def top_down(self, i) -> None:
        if i < self.n:
            swap_idx = i
            
            if 2*i + 1 < self.n and self.arr[2*i+1].get_cost() < self.arr[swap_idx].get_cost():
                swap_idx = 2*i+1
            
            if 2*i + 2 < self.n and self.arr[2*i+2].get_cost() < self.arr[swap_idx].get_cost():
                swap_idx = 2*i+2
            
            if swap_idx != i:
                self.swap(i, swap_idx)
                self.top_down(swap_idx)
    
    def bottom_up(self, i) -> None:
        if i > 0:
            swap_idx = (i-1)//2
            if self.arr[i].get_cost() < self.arr[swap_idx].get_cost():
                self.swap(i, swap_idx)
                self.bottom_up(swap_idx)
        
    def swap(self, i, j) -> None:
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
        
    def get_top(self) -> Point:
        return self.arr[0]
    
    def isEmpty(self) -> bool:
        return self.n == 0
    
    def pop(self) -> Point:
        self.n -= 1
        self.swap(0, self.n)
        self.top_down(0)
        return self.arr.pop()
    
    def add(self, node: Point) -> None:
        self.arr.append(node)
        self.bottom_up(self.n)
        self.n += 1
        
    # def print_heap(self):
    #     start = 0
    #     range = 1
    #     while start < self.n:
    #         print(self.arr[start:start+range])
    #         start = start + range
    #         range *= 2
        
