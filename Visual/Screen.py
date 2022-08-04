import pygame, pygame_gui

from typing import Tuple
from DataSctructure.Matrix import Matrix


class Screen:
    block_size = 18
    
    def __init__(self, size) -> None:
        self.screen = pygame.display.set_mode(size)
        
        
    def draw_cell(self, rect: pygame.Rect, color: Tuple[int, int, int]) -> None:
        pygame.draw.rect(self.screen, color, rect)
    
    def draw_matrix(self, matrix: Matrix) -> None:
        offset_x = 100
        offset_y = 200
        
        cell_size = matrix.get_cell_size()
        delta = (self.block_size - cell_size) // 2
        
        for i in range(matrix.get_width()):
            for j in range(matrix.get_height()):
                # pygame is reversed, x is j and y is i
                x = j * (self.block_size) + offset_x
                y = i * (self.block_size) + offset_y
                
                rect = pygame.Rect(x + delta, y + delta, cell_size, cell_size)
                rect_color = matrix.get_color((i,j))
                self.draw_cell(rect, rect_color)
    
    def draw_ui_manager(self, ui_manager: pygame_gui.UIManager) -> None:
        ui_manager.draw_ui(self.screen)
        
    def draw_surface(self, surface: pygame.Surface) -> None:
        self.screen.blit(surface, (0, 0))
