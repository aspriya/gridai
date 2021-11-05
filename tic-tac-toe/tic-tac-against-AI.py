import pygame
pygame.init()

clock = pygame.time.Clock()

# window configurations
size = 600
menu_height = 80
num_rows = 3
line_width = size // num_rows

# colors
white = (255, 255, 255)
mat_white = (230, 230, 230)
black = (0, 0, 0)
green = (0, 255, 0)
mat_green = (46, 184, 46)
blue = (0, 0, 255)
mat_blue = (0, 102, 255)
yellow = (203, 212, 40, 50)
mat_red = (255, 80, 80)

# surfaces
window = None 
play_area_rect = None
menu_area_rect = None

# images
circle = pygame.image.load('circle.png')
circle = pygame.transform.scale(circle, (100, 100)) # resizing

cross = pygame.image.load('cross.png')
cross = pygame.transform.scale(cross, (100, 100)) # resizing

# menu buttons and icons
restart_button = None

# player_1 and player_2 clicked lists
player_1_clicked = []
player_2_clicked = []

# Goal or winning states of the game
winnig_states = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

#### game related global variables ###
# whose turn to play. 
# 1 indicates player 1 (or machine.)
# 2 indicates player 2
turn = 1 # when playing against machine, machine will act as player 1.
won_player = 0

def main():
    global window, size, num_rows, play_area_rect, menu_area_rect, turn, won_player

    window = pygame.display.set_mode((size, size + menu_height))
    window.fill(black) # fill windows with black color
    create_play_and_menu_area_sections()
    draw_grid(window, size, num_rows) # grid will not change (no need to redraw)
    draw_menus()

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
                    if restart_button.collidepoint(pygame.mouse.get_pos()):
                        reset_everything()
                elif play_area_rect.collidepoint(pygame.mouse.get_pos()):
                    clicked_cell = get_cell_number(x, y)

                    # check if no one has already filled that cell
                    if (clicked_cell not in player_1_clicked) and (clicked_cell not in player_2_clicked):
                        if turn == 1:
                            player_1_clicked.append(clicked_cell)
                            turn = 2 # switching turn
                        else:
                            player_2_clicked.append(clicked_cell)
                            turn = 1 # switching turn
            # clock.tick(60)
                    
        if won_player == 0: # meaning no player won yet
            # repaint play area with new updates
            repaint_play_area()

            # checking for win of a player
            won_player = check_for_win()

            if won_player == 1:
                print("Machine Won!! Try again next time")
            elif won_player == 2:
                print("Congratulations, you won!!!")
            else:
                # no one won yet.
                pass
        else:
            # someone won, display player lose or win message
            draw_win_or_lose_msg(won_player)
            pygame.display.update() # update display
                   
                


def create_play_and_menu_area_sections():
    global play_area_rect, menu_area_rect
    play_area_rect = pygame.draw.rect(window, black, pygame.Rect(0, 0, size, size))
    menu_area_rect = pygame.draw.rect(window, black, pygame.Rect(0, size, size, menu_height))


def draw_menus():
    global  restart_button
    # defining a font
    smallfont = pygame.font.SysFont('arial',20) # font face, and size

    restart_text = smallfont.render('RESTART' , True , white) # Creating the text object
    wall_text = smallfont.render('MACHINE' , True , black) # Creating the text object
    bot_text = smallfont.render('YOU' , True , black) # Creating the text object

    # restart button
    restart_button = pygame.draw.rect(window, mat_red, [10, size + menu_height // 3, 100, 30]) # a box around text to look like a button
    window.blit(restart_text, (10+5, size + menu_height // 3 + 4))

    # Player 1 Icon
    cross_icon = pygame.transform.scale(cross, (25, 25)) # resizing
    window.blit(cross_icon, (200, size + menu_height // 3, 80, 30))
    machine_box = pygame.draw.rect(window, mat_white, [240, size + menu_height // 3, 100, 30]) # a box around text to look like a button
    window.blit(wall_text, (240+5, size + menu_height // 3 + 4))

    # Player 2 Icon
    circle_icon = pygame.transform.scale(circle, (25, 25)) # resizing
    window.blit(circle_icon, (440, size + menu_height // 3, 80, 30))
    player_box = pygame.draw.rect(window, mat_white, [480, size + menu_height // 3, 60, 30]) # a box around text to look like a button
    window.blit(bot_text, (480+5, size + menu_height // 3 + 4))


def draw_grid(window, size, num_rows):
    x = 0
    y = 0

    for l in range(num_rows):
        x += line_width
        y += line_width

        pygame.draw.line(window, white, (x, 0), (x, size)) # drawing columns
        pygame.draw.line(window, white, (0, y), (size, y)) # drawing rows



# numbering the cell grid for ease of reference:
'''
---- --- ----
| 0 | 1 | 2 |
---- --- ----
| 3 | 4 | 5 | 
---- --- ----
| 6 | 7 | 8 |
---- --- ----
'''
# Below function helps to consider the grid env as a numbered cell enviorenment 
# as shown above. Given a x, y cordinate, followign function will return the 
# respective cell number.

def get_cell_number(x, y):
    cell_number = None
    for i in range(num_rows):  # columns
        for j in range(num_rows):  # rows
            if (x == j * line_width) and (y == i * line_width): # exact cell top left coordinates
                cell_number = (i * num_rows) + (j)
                return cell_number
            
            elif (x < (j+1) * line_width) and (y < (i+1) * line_width): # soon as conditions met, that is the cell no. return
                # here j+1 and i+1 is because now need to consider the bottom right corner of the cell.
                cell_number = (i * num_rows) + (j)
                return cell_number


# This functions returns the start (top left)
# cordinates of a cell given the cell number
def get_top_left_cordinates_given_cell_number(cell_no):
    cell_row_number = cell_no // num_rows # cell row number
    cell_column_number = cell_no % num_rows # cell column number

    y = cell_row_number * line_width
    x = cell_column_number * line_width
    return x, y


def repaint_play_area():
    global turn, window

    for cell in player_1_clicked:
        paint_icon_in_cell(cell, 1)

    for cell in player_2_clicked:
        paint_icon_in_cell(cell, 2)

    pygame.display.update() # update display


def paint_icon_in_cell(cell, player_number):
    if(player_number == 1):
        # painting player 1 (machine) icon which is the cross.png
        x, y = get_top_left_cordinates_given_cell_number(cell)
        window.blit(cross, (x + 50, y + 50))
    else:
        # painting payer (plaer 2) icon which is the cirlce.png
        x, y = get_top_left_cordinates_given_cell_number(cell)
        window.blit(circle, (x + 50, y + 50))


def check_for_win():
    global winnig_states
    # if a wining state is a subset of plaer_queue, then he is the winner.

    # print("Player 1 clicked: ", player_1_clicked)
    # print("Player 2 clicked: ", player_2_clicked)
    
    for x in winnig_states:
        if set(x).issubset(player_1_clicked):
            # player 1 (machine) won
            return 1
        elif set(x).issubset(player_2_clicked):
            # player 2 (human) won
            return 2
    else:
        return 0

def draw_win_or_lose_msg(won_player):
    global  window
    # defining fonts
    Win_loose_font = pygame.font.SysFont('arial',35) # font face, and size
    retry_font = pygame.font.SysFont('arial',25) # font face, and size

    human_win_message = Win_loose_font.render('Congratulations! You Won!' , True , mat_blue) # Creating the text object
    machine_win_message = Win_loose_font.render('You were defeated by a Machine!' , True , mat_red) # Creating the text object
    restart_message = retry_font.render('Play Again? click the restart button' , True , black) # Creating the text object

    # win or defeat label and box
    if won_player == 1: # machine won
        win_defeat_box = pygame.draw.rect(window, yellow, [10, 5, size - 20, 60]) # a box around text to look like a button
        window.blit(machine_win_message, (40, 15))
    else:
        win_defeat_box = pygame.draw.rect(window, yellow, [10, 5, size - 20, 60]) # a box around text to look like a button
        window.blit(human_win_message, (100, 15))

    # restart label and box
    restart_label_box = pygame.draw.rect(window, mat_white, [10, 70, size - 20, 30]) # a box around text to look like a button
    window.blit(restart_message, (100, 71))

def reset_everything():
    global window, player_1_clicked, player_2_clicked, won_player, turn

    player_1_clicked = []
    player_2_clicked = []
    won_player = 0
    turn = 2

    window.fill(black) # fill windows with black color
    create_play_and_menu_area_sections()
    draw_grid(window, size, num_rows) # grid will not change (no need to redraw)
    draw_menus()


main()