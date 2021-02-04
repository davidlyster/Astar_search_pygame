import pygame

# set size of output window
game_window_width = 500
game_window = pygame.display.set_mode((game_window_width, game_window_width))

# game name
pygame.display.set_caption("A* Search Visualisation")

# set colours for different node types
wall_node = (0, 0, 0)               # black
empty_node = (255, 255, 255)        # white
searched_node = (0, 255, 255)       # 'aqua'

searching_node = (102, 255, 102)    # light green searching node = node being searched
start_node = (0, 0, 255)            # blue
end_node = (255, 51, 0)             # red
final_path_node = (255, 0, 255)     # purple

# NEXT - define node class
