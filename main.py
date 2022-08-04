import pygame, pygame_gui
from DataSctructure.Matrix import Matrix
from Visual.Screen import Screen


pygame.init()
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

class MainProgram:
    def __init__(self) -> None:
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.algorithm_selection = pygame_gui.elements.UIDropDownMenu(['Astar'], 'Astar', pygame.Rect(10, 10, 120, 30), self.ui_manager)
        
        self.screen = Screen((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.matrix = Matrix(20, 30)
        
        self.clock = pygame.time.Clock()
        
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(pygame.Color('#000000'))
    
    def run(self):
        is_running= True
        while is_running:
            time_delta = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == self.algorithm_selection:
                        print("dcm")
                
                self.ui_manager.process_events(event)
            self.ui_manager.update(time_delta)


            self.screen.draw_surface(self.background)
            self.screen.draw_matrix(self.matrix)
            self.screen.draw_ui_manager(self.ui_manager)
            
            pygame.display.update()
            
            
program = MainProgram()
program.run()
pygame.quit()


# import pygame
# import pygame_gui


# pygame.init()

# pygame.display.set_caption('Quick Start')
# window_surface = pygame.display.set_mode((800, 600))

# background = pygame.Surface((800, 600))
# background.fill(pygame.Color('#000000'))

# manager = pygame_gui.UIManager((800, 600))

# hello_button = pygame_gui.elements.UIDropDownMenu(['Astar'], 'Astar', pygame.Rect(10, 10, 120, 30), manager)

# clock = pygame.time.Clock()
# is_running = True

# while is_running:
#     time_delta = clock.tick(60)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             is_running = False

#         if event.type == pygame_gui.UI_BUTTON_PRESSED:
#             if event.ui_element == hello_button:
#                 print('Hello World!')

#         manager.process_events(event)

#     manager.update(time_delta)

#     window_surface.blit(background, (0, 0))
#     manager.draw_ui(window_surface)

#     pygame.display.update()