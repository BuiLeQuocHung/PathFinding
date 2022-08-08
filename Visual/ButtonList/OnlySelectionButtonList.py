import pygame

from typing import List
from Visual.Button.Button import BaseButton
from Visual.ButtonList.BaseButtonList import BaseButtonList


class OnlySelectionButtonList(BaseButtonList):
    def __init__(self, list_buttons: List[BaseButton]) -> None:
        super().__init__(list_buttons)
        
    def unselect(self):
        for i in range(len(self.list_buttons)):
            button = self.list_buttons[i]
            button.unselect()
    
    def select(self, event: pygame.event.Event) -> BaseButton:
        selected_button = None
        if event.ui_element in self.list_buttons:
            selected_button = event.ui_element
                
        if not selected_button:
            return selected_button
        
        self.unselect()
        
        selected_button.select()
        return selected_button