import pygame

from typing import List, Dict
from Visual.Button.RadioButton import RadioButton
from Visual.ButtonList.MultiSelectionButtonList import MultiSelectionButtonList

class RadioButtonList(MultiSelectionButtonList):
    def __init__(self, list_buttons: List[RadioButton]) -> None:
        super().__init__(list_buttons)
        
    def get_status(self):
        return {
            button.get_text(): button.get_is_selected()\
                for button in self.list_buttons
        }