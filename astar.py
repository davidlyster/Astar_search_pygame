import pygame


# set colours for different node types
# decided with descriptive names rather than RED,BLUE etc.
# so it'll be easier to keep track of later in script when assigning colours to nodes
wall_node_colour = (0, 0, 0)               # black
empty_node_colour = (255, 255, 255)        # white
searched_node_colour = (0, 255, 255)       # 'aqua'
searching_node_colour = (102, 255, 102)    # green - searching node = node being searched
start_node_colour = (0, 0, 255)            # blue
end_node_colour = (255, 51, 0)             # red
final_path_node_colour = (255, 0, 255)     # purple
gridline_colour = (128, 128, 128)          # grey


class Node:
    """
    Each node/square in the window needs the following characteristics
    - its starting axes' location on the graph (i.e. row,col * width)
    - its colour/status
    - list of it's neighbours
    """

    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.colour = empty_node_colour
        self.neighbours = []

    def get_position(self):
        return self.row, self.col

    def draw(self, window):
        """
        This method actually draws the node onto the screen using a rectangle of width, height = window_width / rows
        """
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.width))

    #######################################
    ## METHODS TO SET NODE STATUS/COLOUR ##
    #######################################

    def set_been_searched(self):
        """
        indicate that node has been searched by setting colour to searched_node_colour/aqua
        """
        self.colour = searched_node_colour

    def set_being_searched(self):
        """
        set node to being searched (colour)
        """
        self.colour = searching_node_colour

    def set_wall(self):
        """
        set node to be a wall (colour)
        """
        self.colour = wall_node_colour

    def set_start_node(self):
        """
        set node to be the start node (colour)
        """
        self.colour = start_node_colour

    def set_end_node(self):
        """
        set node to be the end node (colour)
        """
        self.colour = end_node_colour

    def set_final_path_node(self):
        """
        set node to be a final path node (colour)
        """
        self.colour = final_path_node_colour

    #########################################
    ##### END STATUS/COLOUR SET METHODS #####
    #########################################

    #########################################
    ## METHODS TO CHECK NODE STATUS/COLOUR ##
    #########################################

    def has_been_searched(self):
        """
        if the node colour is aqua/searched_node_colour, it has been searched so return true
        """
        return self.colour == searched_node_colour

    def is_being_searched(self):
        """
        if the node colour is green/searching_node_colour, it is being searched so return true
        """
        return self.colour == searching_node_colour

    def is_wall(self):
        """
        if the node colour is black/wall_node_colour, it is a wall so return true
        """
        return self.colour == wall_node_colour

    def is_start_node(self):
        """
        if the node colour is blue/start_node_colour, its the start node so return true
        """
        return self.colour == start_node_colour

    def is_end_node(self):
        """
        if the node colour is red/end_node_colour, its the end node so return true
        """
        return self.colour == end_node_colour

    #########################################
    #### END STATUS/COLOUR CHECK METHODS ####
    #########################################


def make_grid(row_count, width):
    """
    making a square (ie. width = columns and rows) grid of new Nodes
    """
    grid = []

    # have to assign a width(=height) to each node based on the
    # window size divided by the amount of row(=columns) in the grid
    node_width = width // row_count

    for x in range(row_count):
        grid.append([])
        for y in range(row_count):
            node = Node(x, y, node_width)
            grid[x].append(node)

    return grid


def draw_grid(window, grid, row_count, width):
    """
    draw the actual grid
    """
    window.fill(empty_node_colour)  # initialise the grid to be white

    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid_lines(window, row_count, width)
    pygame.display.update()


def draw_grid_lines(window, row_count, width):
    """
    draw the actually grid 'lines' - the outline of the nodes/squares
    again, the grid is square and has 'width' number of nodes so width gives us the range for our loop
    """

    # again,
    # have to assign a width(=height) to each node based on the
    # window size divided by the amount of row(=columns) in the grid
    node_width = width // row_count
    # this is used here to define where to start drawing a gridline

    for x in range(row_count):
        pygame.draw.line(window, gridline_colour, (0, x * node_width), (width, x * node_width))

        for y in range(row_count):
            pygame.draw.line(window, gridline_colour, (y * node_width, 0), (y * node_width, width))


def get_click_position(position, row_count, width):
    """
    turn clicked x,y, position into the grid equivalent row,column
    """

    # again,
    # have to assign a width(=height) to each node based on the
    # window size divided by the amount of row(=columns) in the grid
    node_width = width // row_count

    y, x = position

    col = x // node_width
    row = y // node_width

    return row, col


def run_program(window, width, row_count):
    """
    This is the main function that runs the program and tracks interaction with the game window
    """

    grid = make_grid(row_count, width)

    # active = the game's status
    active = True

    start_node = None
    end_node = None

    # when the search starts this gets sets to true and will disable the user from clicking anything but the exit button
    algorithm_running = False

    # continue to draw the window until a breaking condition is reached, at which stage quit the game
    while active:
        draw_grid(window, grid, row_count, width)

        for event in pygame.event.get():

            # if the exit button is pressed
            if event.type == pygame.QUIT:
                active = False

            # if the user left clicks
            if pygame.mouse.get_pressed()[0]:

                # get the node the user clicked on
                pos = pygame.mouse.get_pos()
                row, col = get_click_position(pos, row_count, width)
                clicked_node = grid[row][col]

                # if theres no start node selected, the clicked node is the new start node
                if not start_node:
                    start_node = clicked_node
                    clicked_node.set_start_node()

                # if there is a start and no end, and the user didn't click the start node, the click is the end node
                elif not end_node and clicked_node != start_node:
                    end_node = clicked_node
                    clicked_node.set_end_node()

                # if there is a start and end, any other node clicked will become a wall
                elif clicked_node != start_node and clicked_node != end_node:
                    clicked_node.set_wall()


            """
            xyxy let user make changes before running with right click 'deletes'
            # if the user right clicks
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_click_position(pos, row_count, width)
            """

            # if the user pressed a key
            # if event.type == pygame.KEYDOWN:
    pygame.quit()


##############################################
##############################################
## RUN PROGRAM AFTER INITIALISING VARIABLES ##
##############################################
##############################################

# heading at top of the window
pygame.display.set_caption("A* Search Visualisation")

# set size of output window
game_window_width = 800
game_window = pygame.display.set_mode((game_window_width, game_window_width))

# set dimension of square graph
total_row_count = 40

# RUN THE PROGRAM
run_program(game_window, game_window_width, total_row_count)

# fin
