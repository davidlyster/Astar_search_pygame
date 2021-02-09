import pygame
from queue import PriorityQueue


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

    def __init__(self, row, col, width, grid_row_count):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.colour = empty_node_colour
        self.neighbours = []
        self.grid_row_count = grid_row_count    # boundary of the grid

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

    def update_neighbours(self, grid):
        """
        Check all neighbouring nodes and at each valid node to this Nodes neighbours list
        i.e. walls are invalid, can't add node that isn't on grid
        """
        # empty this every time as each node will have a new set of neighbours
        self.neighbours = []

        # Check nodes in all 4 directions and add them to neighbours if they are valid
        # NOTE: for the UP and DOWN checks, checking the row below is row+1 and above is -1 which is counterintuitive considering how graphs normally work
        #       but pygame starts with x,y:=0,0 in the left so the oup and down movements are reversed

        # DOWN
        # if the row below is in the grid - if the node below this node is not a barrier
        if self.row < self.grid_row_count-1 and not grid[self.row+1][self.col].is_wall():
            self.neighbours.append(grid[self.row+1][self.col])
            
        # LEFT
        # if the column to the left is in the grid - if the node to the left of this node is not a barrier
        if self.col > 0 and not grid[self.row][self.col-1].is_wall():
            self.neighbours.append(grid[self.row][self.col-1])

        # UP
        # if the row above is in the grid - if the node below this node is not a barrier
        if self.row > 0 and not grid[self.row-1][self.col].is_wall():
            self.neighbours.append(grid[self.row-1][self.col])

        # RIGHT
        # if the column to the right is in the grid - if the node to the right of this node is not a barrier
        if self.col < self.grid_row_count-1 and not grid[self.row][self.col+1].is_wall():
            self.neighbours.append(grid[self.row][self.col+1])

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
            node = Node(x, y, node_width, row_count)
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


def a_star_heuristic(p1, p2):
    """
    function used to make heurisitic guess at distance between two points
    used to guide the A* search
    the points come in as x,y so return the distance between them by comparing x,x and y,y using manhattan ('L') distancing
    we use manhattan instead of euclidian (hypotenuse) as we cannot go sideways on the graph (i.e. moving from 1,1 to 2,2, is 3 steps 1,1, 1,2, 2,2)
    """
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1-x2) + abs(y1-y2)


def reconstruct_path(came_from, current, draw):
    # TODO
    return


# THE VIP
def a_star_search(draw_func, grid, start, end):
    """
    A* Search  Algorithm
    ====================
    A* is an informed Search (the algorithm know the location of the end node when starting) algorithm that is always 
    guaranteed to find the shortest path between a start and end node.
    It does so by making use of a heuristic function (a_star_heuristic) to determine which search path to extend.
    This is based on the current cost of the path plus the expected cost fo the rest of the path (guessed by heuristic).
    This is formulated as:
    f(n) = g(n) + h(n) 
    where g(n) is the cost of the current path from start to the current node, 
    h(n) is the result of the heuristic function used to guess the expected cost of the next node to the end node
    and f(n) ("f score") is the addition of these, the value of which is used to direct the search

    Primary characteristics:
    + Complete solution     - If the solution exist, it is guaranteed to be found
    + Optimal Solution      - Guaranteed to find the shortest path
    - Complexity (O(b^d))   - Stores all observed nodes in memory

    So for each node that is being evaluated we have to record its distance from the start (along the current path) and its f score.
    Each node will also have alist of neighbours that will be evaluated using the above formula until the final node is reached.
    """

    # the open set is the list of discovered nodes that need to be evaluated to see if they are to be expanded further 
    open_set = PriorityQueue()
    # IMPORTANT - the reason we are using the priority queue is that PQ.get() will return the node with the lowest score
    #             i.e. first compares f-score, then compares path_distance
    #             because of this its crucial that the order of the elements in the queue is f-score, path_length, node
    # ALSO, we include the path length because if two nodes have the same f score we can see which has lowest path length and expand into that node
    # open_set.put("f score", "path distance to here", "next nieghbor to evaluate")
    open_set.put((0, 0, start))
    # PriorityQueues have no way to check if an element is contained in them so use open_set_xyxy to keep track of nodes in the PriorityQueue
    open_set_xyxy = {start}

    came_from = {}  # this will contain the previous node along the shortest path

    # make maps of f and g scores for every node with a default of infinity
    g_scores = {node: float('inf') for row in grid for node in row}
    f_scores = {node: float('inf') for row in grid for node in row}

    # define values for starting node
    g_scores[start] = 0
    f_scores[start] = a_star_heuristic(start.get_position(), end.get_position())
    
    # get coordinates of end node which will be used every time the heuristic is called
    end_node_pos = end.get_position()

    # keep track of length of observed path, update on every iteration
    path_length = 0
    while not open_set.empty():

        # let the player quit the game if the want
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = open_set.get()[2]    # last element is the next node
        open_set_xyxy.remove(current_node)  # the node does not need to be re-evaluated later so remove from open_set_xyxy

        if current_node == end:
            # draw the shortest path
            pass  # TODO delete later
            return True

        # get f score for all neighbours
        for neighbour in current_node.neighbours:
            # f(n) = g(n) + h(n) 
            # NOTE: we're adding 1 here because the distance from each node to its neighbour is 1
            # obviously this is not the case normally for this algorithm like in google maps where different roads have different lengths
            g_score = g_scores[current_node] + 1

            # if this path to neighbour is better than any previous one
            if g_score < g_scores[neighbour]:

                came_from[neighbour] = current_node
                g_scores[neighbour] = g_score
                h_score = a_star_heuristic(neighbour.get_position(), end_node_pos)
                f_score = g_score + h_score

                f_scores[neighbour] = f_score

                if neighbour not in open_set_xyxy:
                    path_length += 1
                    # open_set.put("f score", "path distance to here", "next nieghbor to evaluate")
                    open_set.put((f_scores[neighbour], path_length, neighbour))
                    open_set_xyxy.add(neighbour)

                    # change node colour as it is now open/being evaluated
                    neighbour.set_being_searched()

        # now redraw the grid
        draw_func()

        # set the node colour to show it has been searched but do not do it for the start node as we want it to keep its colour as the algorithm progresses
        if current_node != start:
            current_node.set_been_searched()

    return False


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
                pygame.quit()

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
            TODO: let user make changes before running with right click 'deletes'
            # if the user right clicks
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_click_position(pos, row_count, width)
            """

            # if the user pressed a key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not algorithm_running:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    # pass in function as lambda here so within the a_star_search function we can simply call 'draw_func()' (a_star_search argument name)
                    # to run draw_grid(window, grid, row_count, width) which contains variables in the scope of this code block not within a_star_search scope
                    a_star_search(lambda: draw_grid(window, grid, row_count, width), grid, start_node, end_node)

                    algorithm_running = False


##############################################
##############################################
## RUN PROGRAM AFTER INITIALISING VARIABLES ##
##############################################
##############################################

# heading at top of the window
pygame.display.set_caption("A* Search Visualisation")

# set size of output window
game_window_width = 700
game_window = pygame.display.set_mode((game_window_width, game_window_width))

# set dimension of square graph
total_row_count = 50

# RUN THE PROGRAM
run_program(game_window, game_window_width, total_row_count)

# fin
