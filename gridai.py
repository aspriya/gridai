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
mat_red = (255, 80, 80)
player = None
destination = None
open_queue = []
close_queue = []
wall_cells = []
goal_cells = []
bot_init_cell = None
window = None 
play_area_rect = None
menu_area_rect = None
run_button = None
wall_button = None
bot_button = None
goal_button = None
cliked_button = None

def initialize_player(window, cell_x, cell_y):
    global player
    player = pygame.draw.rect(window, blue, pygame.Rect(cell_x * line_width, cell_y * line_width, line_width, line_width))

def draw_destination(window, cell_x, cell_y):
    global destination
    destination = pygame.draw.rect(window, green, pygame.Rect(cell_x * line_width, cell_y * line_width, line_width, line_width))

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
    global window, size, num_rows, player, destination, play_area_rect, menu_area_rect

    window = pygame.display.set_mode((size, size + menu_height))
    window.fill(black) # fill windows with black color
    create_play_and_menu_area_sections()
    draw_grid(window, size, num_rows) # grid will not change (no need to redraw)
    # draw_destination(window, 3, 3) # destination does not change (no need to redraw)
    # initialize_player(window, 0, 0)
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
                    elif play_area_rect.collidepoint(pygame.mouse.get_pos()):
                        if cliked_button == 'wall':
                            create_wall_cell(x, y)
                        elif cliked_button == 'goal':
                            create_goal_cell(x, y)
                        elif cliked_button == 'bot':
                            create_bot(x, y)
                        elif cliked_button == 'run':
                            create_wall_cell(x, y)
        
        pygame.display.update()


    # pygame.display.update() # update display
    # R, G, B, Alpha = window.get_at((126,126))
    # print("Red: ", R, ", Green: ", G, ", Blue: ", B, ", Alpha: ", Alpha)
    # clock.tick(1)
    # clock.tick(1)
    # clock.tick(1)
    # clock.tick(1)
    # clock.tick(1)
    # clock.tick(1)
    # clock.tick(1)
    # clock.tick(1)




    # search_in_breadth_first_approach()


def search_in_breadth_first_approach():
    print("x is: ", player.x, "y is: ", player.y)
    bot_current_cell_number = get_cell_number(player.x, player.y)
    destination_cell_number = get_cell_number(destination.x, destination.y)

    open_queue.append(bot_current_cell_number) # putting the intial bot position to open queue

    play = True
    while play: # main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    create_wall_cell(pygame.mouse.get_pos())
    
        bot_current_cell_number = open_queue.pop(0) # remove and get first element of open_queue

        if(len(close_queue) > 0):  # check if atleast one time moved
            can_go = verify_can_navigate_to_this_from_previous_cell(close_queue[-1], bot_current_cell_number) # end of close_queue is previous cell  
        else:
            can_go = True

        if (can_go):
            # check if this cell allready visited
            if(bot_current_cell_number in close_queue):
                continue

            print("current cell number is: ", bot_current_cell_number)

            # move the bot to this new current cell
            move_bot(bot_current_cell_number)
            clock.tick(1)
            pygame.display.update() # update display

            # cheking for goal
            if (bot_current_cell_number == destination_cell_number):
                print("yeeeeeey, came to destination!!")
                clock.tick(1)
                # stay some time here without closing the windoew 
                return close_queue # returning close queue because from that we can get the trace / path
        else:
            continue

        # goal not found, continue processing
        sorrounding_cells = get_child_nodes(bot_current_cell_number) # find next possible cells to move
        open_queue.extend(sorrounding_cells) # add children to END OF THE OPEN QUEUE (BFS)
        close_queue.append(bot_current_cell_number) # putting the processed node to closed queue
        print("open queue: ", open_queue, "\n")


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
    global run_button, wall_button, bot_button, goal_button, cliked_button

    if run_button.collidepoint(pygame.mouse.get_pos()):
        cliked_button = 'run'
    elif wall_button.collidepoint(pygame.mouse.get_pos()):
        cliked_button = 'wall'
    elif bot_button.collidepoint(pygame.mouse.get_pos()):
        cliked_button = 'bot'
    elif goal_button.collidepoint(pygame.mouse.get_pos()):
        cliked_button = 'goal'


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
    global window, bot_init_cell
    if bot_init_cell is not None: # remove allready place bot
        cell_x, cell_y = get_top_left_cordinates_given_cell_number(bot_init_cell)
        pygame.draw.rect(window, black, pygame.Rect(cell_x, cell_y, line_width, line_width))   
    cell_no = get_cell_number(x, y) # get the cell number which mouse was clicked on
    cell_x, cell_y = get_top_left_cordinates_given_cell_number(cell_no)
    print("cell number is: ", cell_no, ", type is: ", type(cell_no))   
    bot_init_cell = cell_no   
    pygame.draw.rect(window, mat_blue, pygame.Rect(cell_x, cell_y, line_width, line_width))
    draw_grid(window, size, num_rows) # adjust grid lines disapear, hence redraw


def get_child_nodes(cell_number):
    children = []
    up = get_up_cell(cell_number)
    if up is not None:
        children.append(up)

    right = get_right_cell(cell_number)
    if right is not None:
        children.append(right)

    down = get_down_cell(cell_number)
    if down is not None:
        children.append(down)

    left = get_left_cell(cell_number)
    if left is not None:
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


def move_bot(cell_to_move):
    global window, player, close_queue

    # clearing or painint another color for last cell
    if(len(close_queue) > 0):
        last_cell = close_queue[-1]
        last_x, last_y = get_top_left_cordinates_given_cell_number(last_cell)
        pygame.draw.rect(window, (50, 50, 50), pygame.Rect(last_x, last_y, line_width, line_width))

    x, y = get_top_left_cordinates_given_cell_number(cell_to_move)
    print("moving to cell : ", cell_to_move, " of cordinates x: ", x, ", y: ", y, ",  line_width: ", line_width)
    player = pygame.draw.rect(window, blue, pygame.Rect(x, y, line_width, line_width))
    print("moved player attributes: player.x: ", player.x, ", player.y: ", player.y)



def get_top_left_cordinates_given_cell_number(cell_to_move):
    cell_row_number = cell_to_move // num_rows # cell row number
    cell_column_number = cell_to_move % num_rows # cell column number

    y = cell_row_number * line_width
    x = cell_column_number * line_width
    return x, y


def verify_can_navigate_to_this_from_previous_cell(from_cell, to_cell):
    if(from_cell + 1 == to_cell): # check to_cell is the right cell
        return True

    if(from_cell - 1 == to_cell): # check to_cell is the left cell
        return True
    
    if(from_cell - 4 == to_cell): # check to_cell is the top / up cell
        return True

    if(from_cell + 4 == to_cell): # check to_cell is the down / bottom cell
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