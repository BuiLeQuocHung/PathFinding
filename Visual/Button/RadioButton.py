import pygame, pygame_gui

from Visual.Button.Button import BaseButton

class RadioButton(BaseButton):
    def __init__(self, relative_rect: pygame.Rect, text: str, manager: pygame_gui.UIManager):
        super().__init__(relative_rect, text, manager)

    def select(self):
        if not self.is_selected:
            super().select()
        else:
            super().unselect()
    
    def unselect(self):
        if self.is_selected:
            super().unselect()
    
    def get_text(self):
        return self.text
    
    def get_is_selected(self):
        return self.is_selected