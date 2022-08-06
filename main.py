from concurrent.futures import thread
from tkinter import N
import pygame, pygame_gui
import threading

from Algorithm.AlgorithmBase import AlgorithmBase
from Algorithm.Astar import Astar
from Algorithm.AlgorithmSelection import AlgorithmOption, AlgorithmSelection
from DataSctructure.Matrix import Matrix
from Visual.Screen import Screen


pygame.init()
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

MATRIX_ROW = 30
MATRIX_COL = 60

PROCESSING_ORDER_COLOR = (16,78,139) # blue
PATH_COLOR = (255,255,0) # grey


    

class MainProgram:
    def __init__(self) -> None:
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.algorithm_selection_dropdown = pygame_gui.elements.UIDropDownMenu(AlgorithmOption.to_list(), AlgorithmOption.default_value(), pygame.Rect(10, 10, 120, 30), self.ui_manager)
        
        self.screen = Screen((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.background = pygame.Surface((SCREEN_WIDTH, self.screen.matrix_offset_y))
        self.background.fill(pygame.Color('#000000'))
        
        self.matrix = Matrix(MATRIX_ROW, MATRIX_COL)
        
        self.clock = pygame.time.Clock()
        
        self.algorithm_selection = AlgorithmSelection()
        
        self.event= threading.Event()
        self.thread = None
    
    
        
    def run(self):
        is_running = True
        
        self.init_draw()
        
        while is_running:      
            time_delta = self.clock.tick(60)
        
            self.screen.draw_surface(self.background)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == self.algorithm_selection_dropdown:                      
                        if self.thread:
                            self.reset_thread()
                        
                        self.screen.draw_matrix(self.matrix)
                            
                        self.algorithm_selection.run_algorithm(self.matrix, event.text)
                        processing_order = self.algorithm_selection.get_processing_order()
                        path = self.algorithm_selection.get_path()
                        
                        args = ( 
                                (self.screen.draw_cors, (processing_order, PROCESSING_ORDER_COLOR, 0.01)),
                                (self.screen.draw_cors, (path, PATH_COLOR, 0.01)),
                            )
                        self.thread = threading.Thread(target=self.threading_multi_functions, args=(self.event, args) )
                        self.thread.start()

                self.ui_manager.process_events(event)
                
            self.screen.draw_ui_manager(self.ui_manager)
            pygame.display.update()
            self.ui_manager.update(time_delta)
        
    def init_draw(self):
        self.screen.draw_surface(self.background)
        self.screen.draw_matrix(self.matrix)
        self.screen.draw_ui_manager(self.ui_manager)
            
    def threading_multi_functions(self, event: threading.Event, args):
        for each in args:
            func, arg = each
            func(*arg, event)
            
            if event.is_set():
                return
    
    def reset_thread(self):
        self.event.set()
        self.thread.join()
        self.event.clear()
        self.thread = None
            
            
program = MainProgram()
program.run()
pygame.quit()