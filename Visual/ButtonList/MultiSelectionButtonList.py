import pygame

from typing import List, Dict
from Visual.Button.Button import BaseButton
from Visual.ButtonList.BaseButtonList import BaseButtonList

class  MultiSelectionButtonList(BaseButtonList):
    def __init__(self, list_buttons: List[BaseButton]) -> None:
        super().__init__(list_buttons)
    
    def unselect(self):
        for i in range(len(self.list_buttons)):
            button = self.list_buttons[i]
            button.unselect()
    
    def select(self, event: pygame.event.Event) -> BaseButton:
        for i in range(len(self.list_buttons)):
            button = self.list_buttons[i]
            if event.ui_element == button:
                button.select()
                return button
            
