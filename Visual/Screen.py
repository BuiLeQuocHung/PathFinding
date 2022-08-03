from typing import Tuple
import pygame
from pygame import Rect
from DataSctructure.Matrix import Matrix


class Screen:
    block_size = 30
    
    width_block = 50
    height_block = 30
    block_space = 1
    
    width = (block_size + 1) * width_block + 300
    height = (block_size + 1) * height_block
    
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
    def draw_cell(self, rect: Rect, color: Tuple[int, int, int]) -> None:
        pygame.draw.rect(self.screen, color, rect)
    
    def draw_matrix(self, matrix: Matrix) -> None:
        for i in range(self.width_block):
            for j in range(self.height_block):
                # pygame is reversed, x is j and y is i
                x = j * (self.block_size + self.block_space)
                y = i * (self.block_size + self.block_space)
                
                rect = Rect(x, y, self.block_size, self.block_size)
                rect_color = matrix.get_color((i,j))
                self.draw_cell(rect, rect_color)