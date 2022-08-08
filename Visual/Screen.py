import random
import pygame, pygame_gui
import time
import threading

from typing import List, Tuple
from DataStructure.Matrix import Matrix
from config import BLOCK_SIZE, CELL_SIZE


class Screen:
    def __init__(self, size) -> None:
        self.screen = pygame.display.set_mode(size)
        self.matrix_offset_x = 0
        self.matrix_offset_y = 160
        
    def draw_cell(self, rect: pygame.Rect, color: Tuple) -> None:
        pygame.draw.rect(self.screen, color, rect)
        
    def draw_cors(self, cors: List[Tuple], color, delay, event: threading.Event):
        delta = (BLOCK_SIZE - CELL_SIZE) / 2
        for cor in cors:
            x, y = cor
            new_x = y * (BLOCK_SIZE) + self.matrix_offset_x
            new_y = x * (BLOCK_SIZE) + self.matrix_offset_y
            
            rect = pygame.Rect(new_x + delta, new_y + delta, CELL_SIZE, CELL_SIZE)
            self.draw_cell(rect, color)
            
            if event.is_set():
                break

            time.sleep(delay)

    def draw_matrix(self, matrix: Matrix) -> None:
        delta = (BLOCK_SIZE - CELL_SIZE) / 2
        
        for i in range(matrix.get_width()):
            for j in range(matrix.get_height()):
                # pygame is reversed, x is j and y is i
                x = j * (BLOCK_SIZE) + self.matrix_offset_x
                y = i * (BLOCK_SIZE) + self.matrix_offset_y
                
                rect = pygame.Rect(x + delta, y + delta, CELL_SIZE, CELL_SIZE)
                rect_color = matrix.get_color((i,j))
                self.draw_cell(rect, rect_color)
                
    def draw_matrix_animated(self, matrix: Matrix, delay, event: threading.Event) -> None:
        delta = (BLOCK_SIZE - CELL_SIZE) / 2
        
        cors = [(i,j) for i in range(matrix.get_width()) for j in range(matrix.get_height())]
        random.shuffle(cors)
        
        for cor in cors:
            i, j = cor
            x = j * (BLOCK_SIZE) + self.matrix_offset_x
            y = i * (BLOCK_SIZE) + self.matrix_offset_y
            
            rect = pygame.Rect(x + delta, y + delta, CELL_SIZE, CELL_SIZE)
            rect_color = matrix.get_color((i,j))
            self.draw_cell(rect, rect_color)
            
            if event.is_set():
                break

            time.sleep(delay)
    
    def draw_ui_manager(self, ui_manager: pygame_gui.UIManager) -> None:
        ui_manager.draw_ui(self.screen)
        
    def draw_surface(self, surface: pygame.Surface, x, y) -> None:
        self.screen.blit(surface, (x, y))
