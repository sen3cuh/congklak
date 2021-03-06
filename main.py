import pygame

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Congklak")
font = pygame.font.Font('freesansbold.ttf',25,)

# Global variable
white = (255, 255, 255)
navy = (0, 0, 128)

### Circle module

# Global variable for circle module
circle_x = [110, 185, 260, 335, 410, 485, 560, 635, 700, 635, 560, 485, 410, 335, 260, 185]
circle_y = [225, 260, 260, 260, 260, 260, 260, 260, 225, 190, 190, 190, 190, 190, 190, 190]
active = 1

def circles():
    """
    Initiate the hole in the board
    """
    circle_num = 16
    circle_radius = 25
    circle_width = 2

    for i in range(circle_num):
        pygame.draw.circle(screen, white, [circle_x[i], circle_y[i]], circle_radius, circle_width)

    return

def select_circle(i):
    circle_radius = 25
    circle_width = 2

    pygame.draw.circle(screen, (0, 0, 0), [circle_x[i], circle_y[i]], circle_radius, circle_width)
    return

def validate_select_circle():
    """
    Checking valid circle position
    """
    global active

    # Player 1 case
    if player == "player1":
        if active > 7:
            active = 7
        elif active < 1:
            active = 1
    
    # Player 2 case
    if player == "player2":
        if active < 9:
            active = 9
        elif active > 15:
            active = 15

### Player module

# Global variable for player module
player = "player1"

def switch_player():
    """
    Change active player
    """
    global player

    if player == "player1":
        player = "player2"
    else:
        player = "player1"
    return

def display_player():
    player_text = font.render(player, True, white)
    screen.blit(player_text, (25, 25))

### Seeds module

# Global variable for seed module
board = [0, 7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7,]
half_total_seeds = sum(board)/2
base1 = 0
base2 = int(len(board)/2)
message = ""

def display_board():
    """
    Display the board inside the circle
    """
    for i in range(len(board)):
        seed_text = font.render(str(board[i]), True, white)
        screen.blit(seed_text, (circle_x[i]-10, circle_y[i]-13))
    
    return

def print_last_hole(last_hole):
    print("The last hole is", str(last_hole))

def print_message():
    message_text = font.render(message, True, white)
    screen.blit(message_text, (15, 575))

def which_side(hole):
    """
    Indicate which side the last hole is
    """
    if hole < len(board)/2:
        return "side1"
    else:
        return "side2"

def game_over():
    """
    Checking if a player wins
    """
    over_text = font.render("GAME OVER", True, navy)
    if board[base1] > half_total_seeds:
        win_text = font.render("Player 1 Wins", True, white)
        screen.blit(over_text, (15, 525))
        screen.blit(win_text, (15, 550))
    elif board[base2] > half_total_seeds:
        win_text = font.render("Player 2 Wins", True, white)
        screen.blit(over_text, (15, 525))
        screen.blit(win_text, (15, 550))
    
    return
    

def move_seeds(hole):
    """
    Perform each move everytime a player choose
    a hole
    """
    global board, message

    # Wrap around index
    if hole < 0:
        hole += len(board)

    # Moving the seeds
    hole_value = board[hole]

    # Checking if the chosen hole is empty
    if hole_value == 0:
        message = "please select a hole with a seed on it"
        return
    elif hole == base1 or hole == base2:
        message = "please select a valid hole"
        return

    i = 1
    # Seeds movement upper-bound range
    hole_range = hole_value + 1
    while i < hole_range:
        # Checking if the hole is an opponent's base
        if player == "player1" and (hole-i) == (len(board)/2):
            hole_range += 1
        elif player == "player2" and (hole-i) == 0:
            hole_range += 1
        else:
            board[hole-i] += 1
            board[hole] -= 1
        i += 1
    
    # Checking if the last hole is base
    if hole-hole_range+1 == 0 or hole-hole_range+1 == (len(board)/2):
        message = "last hole is base, same player"
    # Checking if the last hole is empty
    elif board[hole-hole_range+1] != 1:
        # Continue movement otherwise
        move_seeds(hole-hole_value)
    else:
        # Checking which side is last hole
        last_hole = hole-hole_range+1
        if last_hole < 0:
            last_hole += len(board)
        side = which_side(last_hole)

        # Checking if the hole is opponent's base
        if player == "player1" and side == "side2":
            switch_player()
            message = "The last hole is " + str(last_hole)
        elif player == "player2" and side == "side1":
            switch_player()
            message = "The last hole is " + str(last_hole)
        # Else we check if opponent's adjacent hole is filled
        # If yes, then add all the seed and the seed in our last
        # hole and add it to the base
        else:
            if player == "player1":
                if board[-last_hole] != 0:
                    board[0] += board[last_hole] + board[-last_hole]
                    board[last_hole] = 0
                    board[-last_hole] = 0
            # Opponent's adjacent hole is -(last_hole-len(board))
            elif player == "player2":
                if board[-(last_hole-len(board))] != 0:
                    board[int(len(board)/2)] += board[last_hole] + board[-(last_hole-len(board))]
                    board[last_hole] = 0
                    board[-(last_hole-len(board))] = 0
            switch_player()
            message = "The last hole is " + str(last_hole)
       
    return


def main():
    global active, message
    message = ""

    running = True
    while running:
        # Background
        screen.fill((136, 187, 228))
        pygame.draw.ellipse(screen, white, [50, 100, 700, 250], 25)

        # Evaluating event
        for event in pygame.event.get():

            # Check if window is closed
            if event.type == pygame.QUIT:
                running = False
            
            ## Check if arrow is pressed
            if event.type == pygame.KEYDOWN:
                # Changing position of select circle
                if event.key == pygame.K_RIGHT:
                    active += 1
                if event.key == pygame.K_LEFT:
                    active -= 1
                # Entering select circle value
                if event.key == pygame.K_RETURN:
                    hole = active
                    move_seeds(hole)
                # Testing for active player
                if  event.key == pygame.K_c:
                    switch_player()
        
        # Drawing object
        circles()
        validate_select_circle()
        select_circle(active)
        display_board()
        
        # Drawing text
        display_player()
        print_message()
        game_over()

        
        # Updating the surface
        pygame.display.update()

    return


if __name__ == "__main__":
    main()