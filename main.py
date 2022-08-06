import pygame, pygame_gui
import threading

from Algorithm.AlgorithmSelection import AlgorithmOption, AlgorithmSelection
from DataSctructure.Matrix import Matrix
from Visual.Screen import Screen


pygame.init()
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

MATRIX_ROW = 30
MATRIX_COL = 60

PROCESSING_ORDER_COLOR = (16,78,139) # blue
PATH_COLOR = (255,255,0) # yellow


    

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
        
        dragging = False
        dragging_cell = None
        
        self.init_draw()
        
        while is_running:      
            time_delta = self.clock.tick(60)
        
            self.screen.draw_surface(self.background)
            
            mouse_clicks = pygame.mouse.get_pressed()
            l_click, w_click, r_click = mouse_clicks
            
                
                
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
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mpos = pygame.mouse.get_pos()
                    
                    start = self.matrix.get_cell(self.matrix.get_start_cor())
                    end = self.matrix.get_cell(self.matrix.get_end_cor())
                    
                    block_size = self.screen.block_size
                    
                    for cell in [start, end]:
                        obj_cor = self.matrix_cor_to_screen_cor(cell.get_cor())
                        if self.mouse_collide_rect(mpos, obj_cor, block_size, block_size):
                            dragging = True
                            dragging_cell = cell
                    
                            if self.thread and self.thread.is_alive():
                                self.reset_thread()
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                    dragging_cell = None
                    
                self.ui_manager.process_events(event)
                

            if dragging:
                mpos = pygame.mouse.get_pos()
                matrix_cor = self.screen_cor_to_matrix_cor(mpos)

                if matrix_cor != dragging_cell.get_cor():
                    dragging_cell.update_cor(matrix_cor)
                    self.screen.draw_matrix(self.matrix)
                    

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
                break
    
    def reset_thread(self):
        self.event.set()
        self.thread.join()
        self.event.clear()
        self.thread = None
    
    def mouse_collide_rect(self, mouse_cor, obj_cor, obj_w, obj_h):
        x, y = mouse_cor
        obj_x, obj_y = obj_cor
        
        if x < obj_x or x > obj_x + obj_w:
            return False
        
        if y < obj_y or y > obj_y + obj_h:
            return False
        
        return True

    def matrix_cor_to_screen_cor(self, matrix_cor):
        x, y = matrix_cor
        block_size = self.screen.block_size
        offset_x = self.screen.matrix_offset_x
        offset_y = self.screen.matrix_offset_y
        return (y*block_size + offset_x, x*block_size + offset_y)
    
    def screen_cor_to_matrix_cor(self, screen_cor):
        x, y = screen_cor
        block_size = self.screen.block_size
        offset_x = self.screen.matrix_offset_x
        offset_y = self.screen.matrix_offset_y
        
        new_x = (y - offset_y) // block_size
        new_x = max(new_x, 0)
        new_x = min(new_x, MATRIX_ROW -1)
        
        new_y = (x - offset_x) // block_size
        new_y = max(new_y, 0)
        new_y = min(new_y, MATRIX_COL - 1)
        return (new_x, new_y)
    
    
        
            
program = MainProgram()
program.run()
pygame.quit()