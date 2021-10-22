import pygame
pygame.init()

clock = pygame.time.Clock()

size = 600
menu_height = 80
num_rows = 20
line_width = size // num_rows
white = (255, 255, 255)
mat_white = (230, 230, 230)
black = (0, 0, 0)
green = (0, 255, 0)
mat_green = (46, 184, 46)
blue = (0, 0, 255)
mat_blue = (0, 102, 255)
child_node_blue = (70, 104, 163, 50)
path_cell_yellow = (203, 212, 40)
mat_red = (255, 80, 80)
bot = None
# destination = None
open_queue = []
close_queue = []
wall_cells = []
goal_cells = []
path = []
found_goal_cell = None
bot_init_cell = None
window = None 
play_area_rect = None
menu_area_rect = None
run_button = None
wall_button = None
bot_button = None
goal_button = None
clicked_button = None

def create_play_and_menu_area_sections():
    global play_area_rect, menu_area_rect
    play_area_rect = pygame.draw.rect(window, black, pygame.Rect(0, 0, size, size))
    menu_area_rect = pygame.draw.rect(window, black, pygame.Rect(0, size, size, menu_height))

def draw_menus():
    global run_button, wall_button, bot_button, goal_button
    # defining a font
    smallfont = pygame.font.SysFont('arial',20) # font face, and size

    run_text = smallfont.render('RUN' , True , white) # Creating the text object
    wall_text = smallfont.render('WALL' , True , black) # Creating the text object
    bot_text = smallfont.render('BOT' , True , white) # Creating the text object
    goal_text = smallfont.render('GOAL' , True , white) # Creating the text object

    # run button
    run_button = pygame.draw.rect(window, mat_red, [10, size + menu_height // 3, 80, 30]) # a box around text to look like a button
    window.blit(run_text, (10+15+3, size + menu_height // 3 + 4))

    # wall button
    wall_button = pygame.draw.rect(window, mat_white, [110, size + menu_height // 3, 80, 30]) # a box around text to look like a button
    window.blit(wall_text, (110+15, size + menu_height // 3 + 4))

    # bot button
    bot_button = pygame.draw.rect(window, mat_blue, [210, size + menu_height // 3, 80, 30]) # a box around text to look like a button
    window.blit(bot_text, (210+15+3, size + menu_height // 3 + 4))

    # goal button
    goal_button = pygame.draw.rect(window, mat_green, [310, size + menu_height // 3, 80, 30]) # a box around text to look like a button
    window.blit(goal_text, (310+15-3, size + menu_height // 3 + 4))

    # pygame.draw.rect(window,color_dark,[100,100,80,30]) # a box around text to look like a button
    

def main():
    global window, size, num_rows, bot, play_area_rect, menu_area_rect, clicked_button

    window = pygame.display.set_mode((size, size + menu_height))
    window.fill(black) # fill windows with black color
    create_play_and_menu_area_sections()
    draw_grid(window, size, num_rows) # grid will not change (no need to redraw)
    draw_menus()

    
    white = (255,255,255) # white color
    color_light = (170,170,170) # light shade of the button
    color_dark = (100,100,100) # dark shade of the button

    pygame.display.update() # update display

    exit = False
    while not exit: # main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    x, y = pygame.mouse.get_pos()
                    if menu_area_rect.collidepoint(pygame.mouse.get_pos()):
                        check_if_menu_button_pressed(x, y)
                        if clicked_button == 'run':
                            cliked_button = None
                            print("run clicked")
                            if(len(goal_cells) > 0 and bot is not None):
                                print("calling breadh firs search")
                                search_in_breadth_first_approach()
                    elif play_area_rect.collidepoint(pygame.mouse.get_pos()):
                        if clicked_button == 'wall':
                            create_wall_cell(x, y)
                        elif clicked_button == 'goal':
                            create_goal_cell(x, y)
                        elif clicked_button == 'bot':
                            create_bot(x, y)                          
        
        pygame.display.update()


def search_in_breadth_first_approach():
    global bot, goal_cells, path
    print("x is: ", bot.x, "y is: ", bot.y)
    bot_current_cell_number = get_cell_number(bot.x, bot.y)
    
    # putting the intial bot position to open queue
    open_queue.append(bot_current_cell_number)

    processing = True
    find_path = False
    while processing: # main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
    
        if len(open_queue) > 0 :
            current_node_cell = open_queue.pop(0) # remove and get first element of open_queue
            
            # check if this cell allready processed
            if(current_node_cell in close_queue):
                continue

            print("current cell number is: ", current_node_cell)
            print("goal cell/s is/are at: ", goal_cells)

            # cheking for goal
            if (current_node_cell in goal_cells):
                # add the goal cell to close queue too, this is helpfull to find the path
                close_queue.append(current_node_cell)
                found_goal_cell = current_node_cell # there can be many goal cell, this is the one found first.
                print("goal found, now find the path from close_queue, close_queue is:", close_queue)
                processing = False
                find_path = True
                clock.tick(2) # stay some time here without closing the windoew
            else:
                # goal not found, continue processing
                child_node_cells = get_child_nodes(current_node_cell) # find possible child cells nodes to process
                close_queue.append(current_node_cell) # putting the processed node to closed queue

                # add child nodes to open queue only if they are already not in both open_queue and close_queue
                print("childe nodes: ", child_node_cells)
                for child_node in child_node_cells:
                    if child_node not in open_queue and child_node not in close_queue:
                        open_queue.append(child_node) # add children to END OF THE OPEN QUEUE (BFS)
                print("open queue: ", open_queue, "open_queue length: ", len(open_queue), "\n")

                paint_child_node_cells(child_node_cells)
            

        else:
            print("no nodes to processe, open_queue length: ", len(open_queue), ", open queue: ", open_queue)
            print("closed queue (processed nodes) : ", close_queue)
            return close_queue
    
    dead_end_nodes = []
    while find_path:
        path.append(close_queue[0]) # put the bot starting cell to path.

        for i in range(len(close_queue) -1):
            from_cell = path[-1]
            to_cell = close_queue[i+1]

            if to_cell in dead_end_nodes:
                continue

            print("finding path, from_Cell: ", from_cell, ", try to_cell: ", to_cell)
            if verify_to_cell_is_navigatable_from_from_cell(from_cell, to_cell):
                path.append(to_cell)
        
        if path[-1] == found_goal_cell:
            find_path = False
        else:
            # a dead end has occured, start finding path avoiding this dead end cell
            dead_end_nodes.append(path[-1])
            path = [] # to start again

        
    paint_path(path)


def get_cell_number(x, y):
    print("get_cell_number, x:", x, " y: ", y)
    cell_number = None
    for i in range(num_rows):  # columns
        for j in range(num_rows):  # rows
            if (x == j * line_width) and (y == i * line_width): # exact cell top left coordinates
                cell_number = (i * num_rows) + (j)
                print("i :", i, ", j :", j)
                return cell_number
            
            elif (x < (j+1) * line_width) and (y < (i+1) * line_width): # soon as conditions met, that is the cell no. return
                # here j+1 and i+1 is because now need to consider the bottom right corner of the cell.
                cell_number = (i * num_rows) + (j)
                print("i :", i, ", j :", j, ", cell number is: ", cell_number)
                return cell_number


def check_if_menu_button_pressed(x, y):
    global run_button, wall_button, bot_button, goal_button, clicked_button

    if run_button.collidepoint(pygame.mouse.get_pos()):
        clicked_button = 'run'
        print("run clicccc")
    elif wall_button.collidepoint(pygame.mouse.get_pos()):
        clicked_button = 'wall'
    elif bot_button.collidepoint(pygame.mouse.get_pos()):
        clicked_button = 'bot'
    elif goal_button.collidepoint(pygame.mouse.get_pos()):
        clicked_button = 'goal'


def create_wall_cell(x, y):
    global window
    print("create_wall_Cell, x:", x, " y: ", y)
    cell_no = get_cell_number(x, y) # get the cell number which mouse was clicked on
    cell_x, cell_y = get_top_left_cordinates_given_cell_number(cell_no)
    if not cell_no in wall_cells:
        wall_cells.append(cell_no)
        print("cell number is: ", cell_no, ", type is: ", type(cell_no))
        pygame.draw.rect(window, white, pygame.Rect(cell_x, cell_y, line_width, line_width))
    else:
        wall_cells.remove(cell_no)
        pygame.draw.rect(window, black, pygame.Rect(cell_x, cell_y, line_width, line_width))
        draw_grid(window, size, num_rows) # adjust grid lines disapear, hence redraw


def create_goal_cell(x, y):
    global window
    cell_no = get_cell_number(x, y) # get the cell number which mouse was clicked on
    cell_x, cell_y = get_top_left_cordinates_given_cell_number(cell_no)
    if not cell_no in goal_cells:
        goal_cells.append(cell_no)
        print("cell number is: ", cell_no, ", type is: ", type(cell_no))
        pygame.draw.rect(window, mat_green, pygame.Rect(cell_x, cell_y, line_width, line_width))
    else:
        goal_cells.remove(cell_no)
        pygame.draw.rect(window, black, pygame.Rect(cell_x, cell_y, line_width, line_width))
        draw_grid(window, size, num_rows) # adjust grid lines disapear, hence redraw


def create_bot(x, y):
    global window, bot_init_cell, bot
    if bot_init_cell is not None: # remove allready place bot
        cell_x, cell_y = get_top_left_cordinates_given_cell_number(bot_init_cell)
        pygame.draw.rect(window, black, pygame.Rect(cell_x, cell_y, line_width, line_width))   
    cell_no = get_cell_number(x, y) # get the cell number which mouse was clicked on
    cell_x, cell_y = get_top_left_cordinates_given_cell_number(cell_no)
    print("cell number is: ", cell_no, ", type is: ", type(cell_no))   
    bot_init_cell = cell_no   
    bot = pygame.draw.rect(window, mat_blue, pygame.Rect(cell_x, cell_y, line_width, line_width))
    draw_grid(window, size, num_rows) # adjacent grid lines disapear, hence redraw


def get_child_nodes(cell_number):
    children = []
    up = get_up_cell(cell_number)
    if up is not None and up not in wall_cells:
        children.append(up)

    right = get_right_cell(cell_number)
    if right is not None and right not in wall_cells:
        children.append(right)

    down = get_down_cell(cell_number)
    if down is not None and down not in wall_cells:
        children.append(down)

    left = get_left_cell(cell_number)
    if left is not None and left not in wall_cells:
        children.append(left)
    
    return children

    

def get_up_cell(cell_number):
    cell_row_number = cell_number // num_rows # current row number of bot
    if (cell_row_number - 1 < 0):  # above /up row number of bot
        return None
    else:
        return (cell_number - num_rows)


def get_right_cell(cell_number):
    cell_column_number = cell_number % num_rows # current column number of bot
    if (cell_column_number + 1 >= num_rows): 
        # current cell is at the right edge, so no rigth child / right cell available
        return None
    else:
        return (cell_number + 1) # else return next cell number


def get_down_cell(cell_number):
    cell_row_number = cell_number // num_rows # current row number of bot
    if (cell_row_number + 1 >= num_rows):  # down / next row number of bot
        return None
    else:
        return (cell_number + num_rows)


def get_left_cell(cell_number):
    cell_column_number = cell_number % num_rows # current column number of bot
    if (cell_column_number - 1 < 0): 
        # current cell is at the left edge, so no left child / right cell available
        return None
    else:
        return (cell_number - 1) # else return previous cell number


def paint_child_node_cells(child_node_cells):
    for child_node_cell in child_node_cells:
        if child_node_cell is not bot_init_cell and child_node_cell not in goal_cells:
            cell_x, cell_y = get_top_left_cordinates_given_cell_number(child_node_cell)
            pygame.draw.rect(window, child_node_blue, pygame.Rect(cell_x, cell_y, line_width, line_width))
            draw_grid(window, size, num_rows) # because adjust grid lines disappear, so redraw it again
            pygame.display.update()
            clock.tick(60)

def paint_path(path):
    print("path is: ", path)
    for path_node_cell in path:
        if path_node_cell is not bot_init_cell and path_node_cell not in goal_cells:
            cell_x, cell_y = get_top_left_cordinates_given_cell_number(path_node_cell)
            pygame.draw.rect(window, path_cell_yellow, pygame.Rect(cell_x, cell_y, line_width, line_width))
            draw_grid(window, size, num_rows) # because adjust grid lines disappear, so redraw it again
            pygame.display.update()
            clock.tick(15)


def move_bot(cell_to_move):
    global window, bot, close_queue

    # clearing or painint another color for last cell
    if(len(close_queue) > 0):
        last_cell = close_queue[-1]
        last_x, last_y = get_top_left_cordinates_given_cell_number(last_cell)
        pygame.draw.rect(window, (50, 50, 50), pygame.Rect(last_x, last_y, line_width, line_width))

    x, y = get_top_left_cordinates_given_cell_number(cell_to_move)
    print("moving to cell : ", cell_to_move, " of cordinates x: ", x, ", y: ", y, ",  line_width: ", line_width)
    bot = pygame.draw.rect(window, blue, pygame.Rect(x, y, line_width, line_width))
    print("moved bot attributes: bot.x: ", bot.x, ", bot.y: ", bot.y)



def get_top_left_cordinates_given_cell_number(cell_to_move):
    cell_row_number = cell_to_move // num_rows # cell row number
    cell_column_number = cell_to_move % num_rows # cell column number

    y = cell_row_number * line_width
    x = cell_column_number * line_width
    return x, y


def verify_to_cell_is_navigatable_from_from_cell(from_cell, to_cell):
    if (to_cell in wall_cells): # if to_cell is a wall cell, return False
        return False

    if(from_cell + 1 == to_cell): # check to_cell is the right cell
        return True

    if(from_cell - 1 == to_cell): # check to_cell is the left cell
        return True
    
    if(from_cell - num_rows == to_cell): # check to_cell is the top / up cell
        return True

    if(from_cell + num_rows == to_cell): # check to_cell is the down / bottom cell
        return True
    
    return False # Else not navigatable, return False


def draw_grid(window, size, num_rows):
    x = 0
    y = 0

    for l in range(num_rows):
        x += line_width
        y += line_width

        pygame.draw.line(window, white, (x, 0), (x, size)) # drawing columns
        pygame.draw.line(window, white, (0, y), (size, y)) # drawing rows

main()