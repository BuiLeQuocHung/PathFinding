import pygame, pygame_gui
import threading

from PathFindingAlgorithm.AlgorithmSelection import AlgorithmOption, AlgorithmSelection
from DataStructure.Matrix import Cell, Matrix, Special_Cell
from Maze.MazeGenerator import MazeGenerator

from Visual.Button.CellButton import CellButton
from Visual.Button.RadioButton import RadioButton
from Visual.ButtonList.RadioButtonList import RadioButtonList
from Visual.ButtonList.OnlySelectionButtonList import OnlySelectionButtonList
from Visual.Screen import Screen
from config import SCREEN_WIDTH, SCREEN_HEIGHT, MATRIX_COL, MATRIX_ROW, \
    PROCESSING_ORDER_COLOR, PATH_COLOR, BLOCK_SIZE

pygame.init()
pygame.display.set_caption("Path Finding")

class MainProgram:
    def __init__(self) -> None:
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.algorithm_selection_dropdown = pygame_gui.elements.UIDropDownMenu(
            AlgorithmOption.to_list(), AlgorithmOption.default_value(), 
            pygame.Rect(10, 5, 120, 30), self.ui_manager,
            expansion_height_limit=127
            )
        self.algorithm_selection_dropdown.set_dimensions((150, 30))
        
        self.list_cell_buttons = OnlySelectionButtonList([
            CellButton(Cell(can_move = False), pygame.Rect(250, 5, 120, 30), "Wall", self.ui_manager), 
            CellButton(Cell(cost = 1), pygame.Rect(250, 35, 120, 30), "Street: 1", self.ui_manager),
            CellButton(Cell(cost = 2), pygame.Rect(250, 65, 120, 30), "Mud: 2", self.ui_manager),
            CellButton(Cell(cost = 3), pygame.Rect(250, 95, 120, 30), "Forest: 3", self.ui_manager), 
            CellButton(Cell(cost = 4), pygame.Rect(250, 125, 120, 30), "River: 4", self.ui_manager)
        ])
        
        
        self.gen_new_matrix_button = pygame_gui.elements.UIButton(pygame.Rect(600, 25, 120, 30), "New matrix", self.ui_manager)
        self.list_matrix_status_buttons = RadioButtonList([
            RadioButton(pygame.Rect(750, 10, 120, 30), "Walls", self.ui_manager),
            RadioButton(pygame.Rect(750, 40, 120, 30), "Uniform cost", self.ui_manager)
        ])
        
        self.gen_maze_button = pygame_gui.elements.UIButton(pygame.Rect(480, 25, 120, 30), "New maze", self.ui_manager)
        
        self.cost_textbox = pygame_gui.elements.UITextBox("Cost: ", pygame.Rect(1250, 10, 120, 30), self.ui_manager)
        self.processing_count_textbox = pygame_gui.elements.UITextBox("Visited: ", pygame.Rect(1250, 40, 120, 30), self.ui_manager)
        
        self.screen = Screen((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.upper_background = pygame.Surface((SCREEN_WIDTH, self.screen.matrix_offset_y))
        self.upper_background.fill(pygame.Color('#202020'))
        
        self.lower_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - self.screen.matrix_offset_y))
        self.lower_background.fill(pygame.Color('#202020'))
        
        self.matrix = Matrix.instance(MATRIX_ROW, MATRIX_COL)
        self.maze_generator = MazeGenerator.instance(MATRIX_ROW, MATRIX_COL)
        
        self.clock = pygame.time.Clock()
        
        self.algorithm_selection = AlgorithmSelection()
        
        self.event= threading.Event()
        self.thread = None
    
    def run(self):
        is_running = True
        
        dragging = False
        dragging_cell: Special_Cell = None
        button_select: CellButton = None
        
        current_algo = AlgorithmOption.default_value()
        
        
        self.init_draw()
        
        while is_running:      
            time_delta = self.clock.tick(120)
        
            self.screen.draw_surface(self.upper_background, 0, 0)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == self.algorithm_selection_dropdown:                      
                        if self.thread:
                            self.reset_thread()
                        
                        self.screen.draw_matrix(self.matrix)
                        
                        current_algo = event.text
                        
                        self.run_algorithm(current_algo, 0.001, 0.01)
                
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:     
                    # Select target cell button
                    button_select = (self.list_cell_buttons.select(event) or button_select)
                    
                    # Select target radio buttons
                    self.list_matrix_status_buttons.select(event)
                    
                    # Select gen new matrix
                    if event.ui_element == self.gen_new_matrix_button:
                        if self.thread:
                            self.reset_thread()

                        status = self.list_matrix_status_buttons.get_status()
                        uniform_cost = status['Uniform cost']
                        can_move = status['Walls']
                        self.matrix.gen_matrix(uniform_cost, can_move)
                        self.screen.draw_matrix(self.matrix)
                        
                        self.cost_textbox.set_text("Cost: {}".format(''))
                        self.processing_count_textbox.set_text("Visited: {}".format(''))
                        
                    elif event.ui_element == self.gen_maze_button:
                        if self.thread:
                            self.reset_thread()
                        
                        self.matrix.update_matrix(self.maze_generator.gen_maze())
                        
                        args = ( 
                                (self.screen.draw_matrix_animated, (self.matrix, 0.0007, self.event)),
                            )
                        self.thread = threading.Thread(target=self.threading_multi_functions, args=(args, self.event) )
                        self.thread.start()
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicks = pygame.mouse.get_pressed()
                    l_click, m_click, r_click = mouse_clicks
                    
                    if r_click:
                        button_select = None
                        # Unselect all buttons
                        self.list_cell_buttons.unselect()
                    
                    elif l_click:
                        dragging = True
                        if not any([dragging_cell, button_select]):
                            mpos = pygame.mouse.get_pos()
                            start = self.matrix.get_cell(self.matrix.get_start_cor())
                            end = self.matrix.get_cell(self.matrix.get_end_cor())
                            
                            for cell in [start, end]:
                                obj_cor = self.matrix_cor_to_screen_cor(cell.get_cor())
                                if self.mouse_collide_rect(mpos, obj_cor, BLOCK_SIZE, BLOCK_SIZE):
                                    dragging_cell = cell
                        
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                    dragging_cell = None
                    
                self.ui_manager.process_events(event)
                

            if dragging:
                if dragging_cell:
                    mpos = pygame.mouse.get_pos()
                    matrix_cor = self.screen_cor_to_matrix_cor(mpos)

                    if self.is_valid_matrix_cor(matrix_cor) and matrix_cor != dragging_cell.get_cor():
                        if self.thread and self.thread.is_alive():
                            self.reset_thread()
                            
                        dragging_cell.update_cor(matrix_cor)
                        self.screen.draw_matrix(self.matrix)
                        
                        self.run_algorithm(current_algo, 0, 0)
                    
                elif button_select:
                    mpos = pygame.mouse.get_pos()
                    matrix_cor = self.screen_cor_to_matrix_cor(mpos)
                    
                    if self.is_valid_matrix_cor(matrix_cor):
                        if self.thread and self.thread.is_alive():
                            self.reset_thread()

                        cell = button_select.get_cell()
                        self.matrix.get_cell(matrix_cor).update_cell(cell.can_move(), cell.get_cost())
                        self.screen.draw_matrix(self.matrix)
                        
                        self.run_algorithm(current_algo, 0.001, 0.01)
                    
            self.screen.draw_ui_manager(self.ui_manager)
            pygame.display.update()
            self.ui_manager.update(time_delta)
    


    def init_draw(self):
        self.screen.draw_surface(self.upper_background, 0, 0)
        self.screen.draw_surface(self.lower_background, 0, self.screen.matrix_offset_y)
        self.screen.draw_matrix(self.matrix)
        self.screen.draw_ui_manager(self.ui_manager)
        
    def run_algorithm(self, current_algo: str, processing_draw_delay, path_draw_delay):
        """
            run algorithm and update screen
        """
        # Run algo
        self.algorithm_selection.run_algorithm(self.matrix, current_algo)
        
        # Update screen by creatring new thread
        processing_order = self.algorithm_selection.get_processing_order()
        path = self.algorithm_selection.get_path()
        cost = self.algorithm_selection.get_cost()
        
        args = ( 
                (self.screen.draw_cors, (processing_order, PROCESSING_ORDER_COLOR, processing_draw_delay, self.event)),
                (self.screen.draw_cors, (path, PATH_COLOR, path_draw_delay, self.event)),
                (self.cost_textbox.set_text, ["Cost: {}".format(cost)]),
                (self.processing_count_textbox.set_text, ["Visited: {}".format(len(processing_order))])
            )
        self.thread = threading.Thread(target=self.threading_multi_functions, args=(args, self.event) )
        self.thread.start()
            
    def threading_multi_functions(self, args, event: threading.Event):
        for each in args:
            func, arg = each
            func(*arg)
            
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
        offset_x = self.screen.matrix_offset_x
        offset_y = self.screen.matrix_offset_y
        return (y*BLOCK_SIZE + offset_x, x*BLOCK_SIZE + offset_y)
    
    def screen_cor_to_matrix_cor(self, screen_cor):
        x, y = screen_cor
        offset_x = self.screen.matrix_offset_x
        offset_y = self.screen.matrix_offset_y
        
        new_x = (y - offset_y) // BLOCK_SIZE
        # new_x = max(new_x, 0)
        # new_x = min(new_x, MATRIX_ROW -1)
        
        new_y = (x - offset_x) // BLOCK_SIZE
        # new_y = max(new_y, 0)
        # new_y = min(new_y, MATRIX_COL - 1)
        return (new_x, new_y)
    
    def is_valid_matrix_cor(self, cor):
        x, y = cor
        if 0 <= x < MATRIX_ROW and 0 <= y < MATRIX_COL:
            return True
        return False

    
        
            
program = MainProgram()
program.run()
pygame.quit()