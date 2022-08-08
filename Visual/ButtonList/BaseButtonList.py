from typing import Dict, List
import pygame

from Visual.Button.Button import BaseButton

class BaseButtonList:
    def __init__(self, list_buttons: List[BaseButton]) -> None:
        self.list_buttons = list_buttons
        