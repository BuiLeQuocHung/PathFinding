import pygame, pygame_gui

from typing import Dict, List

class BaseButton(pygame_gui.elements.UIButton):
    def __init__(self, relative_rect: pygame.Rect, text: str, manager: pygame_gui.UIManager):
        super().__init__(relative_rect, text, manager)