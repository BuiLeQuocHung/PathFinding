import pygame, pygame_gui

from DataStructure.Matrix import Cell
from Visual.Button.Button import BaseButton
from config import CELL_SIZE

class CellButton(BaseButton):
    def __init__(self, cell: Cell, rect: pygame.Rect, text: str, manager: pygame_gui.UIManager) -> None:
        super().__init__(rect, text, manager)
        self.cell = cell
        self.cursor = self.create_cursor()
    
    def create_cursor(self):
        size = CELL_SIZE *2
        surface = pygame.Surface((size, size))
        color = self.cell.get_color()
        surface.fill(color)
        return pygame.cursors.Cursor((0,0), surface)
            
    def select(self):
        if not self.is_selected:
            super().select()
            pygame.mouse.set_cursor(self.cursor)
    
    def unselect(self):
        if self.is_selected:
            super().unselect()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    def get_cell(self):
        return self.cell