import pygame
import random

pygame.init()

#set screen size
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Maze')

#define font
font = pygame.font.SysFont(None, 40)

#create the player
player_pos = [[int(screen_width / 2), int(screen_height / 2)]]
player_pos.append([300,310])
direction = 0


#define game variables
cell_size = 10
update_player = 0
new_piece = [0, 0]
game_over = False
clicked = False
score = 0
currand = 0.01
checker = 0

#define colors
bg = (255, 200, 150)
body_inner = (50, 175, 25)
body_outer = (100, 100, 200)
blue = (0, 0, 255)
red = (255, 0, 0)

#generates a maze
def generate_maze(currand):
    maze = [[0 for _ in range(screen_width // cell_size)] for _ in range(screen_height // cell_size)]
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if random.random() < currand:  # Adjust this probability for more or less walls
                maze[row][col] = 1

    return maze

#checks if the created maze touches the starting position of the player
def check_starting_position_collision(maze, player_pos):
    for pos in player_pos:
        if maze[pos[1] // cell_size][pos[0] // cell_size] == 1:
            return True
    return False

#draws the maze to the screen
def draw_maze(maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, red, (col * cell_size, row * cell_size, cell_size, cell_size))

#sets up initial maze
maze = generate_maze(currand)
while check_starting_position_collision(maze, player_pos):
    maze = generate_maze(currand)
maze_values = []
maze_values.append(maze)

#checks if the player touches the maze
def check_collision(player_pos, maze):
    player_head = player_pos[0]
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 1:
                block_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                if block_rect.collidepoint(player_head):
                    return True
    return False

#draws the screen
def draw_screen():
    screen.fill(bg)

#draws the score
def draw_score(score):
    score_txt = 'Score: ' + str(score)
    score_img = font.render(score_txt, True, blue)
    screen.blit(score_img, (0, 0))
    score += 1

#checks if the player meets the conditions to end the game
def check_game_over(game_over):
    head_count = 0
    for x in player_pos:
        if player_pos[0] == x and head_count > 0:
            game_over = True
        elif player_pos[0] == maze_values[0]:
            game_over = True
        head_count += 1
    return game_over

#checks if the player has escaped the maze that helps to establish level variants
def check_next_level(checker):
    if player_pos[0][0] < 0 or player_pos[0][0] > screen_width or player_pos[0][1] < 0 or player_pos[0][1] > screen_height:
        game_over = True 
    checker += 1	  
    return checker

#checks if the player has escaped the maze and uses a bool to determine if the level should increase
next_level = False
def check_next_level(next_level):
    if player_pos[0][0] < 0 or player_pos[0][0] > screen_width or player_pos[0][1] < 0 or player_pos[0][1] > screen_height: 
        next_level += 1	  
    return next_level

# Reads high scores from a file
def read_high_scores():
    with open("high_scores.txt", "r") as file:
        high_scores = [int(score) for score in file.readlines()]
    return high_scores

#checks and adds the highscore to the file
def add_high_score(score):
    highscore = read_high_scores()
    if score > max(highscore):
        highscore.remove(max(highscore))
        highscore.append(score)
        with open("high_scores.txt", "w") as file:
            file.write(str(score))
        return True
    return False    

#displays the end game screen
def draw_game_over(pscore):
    over_text = "Game Over!"
    over_img = font.render(over_text, True, blue)
    pygame.draw.rect(screen, red, (screen_width // 2 - 140, screen_height // 2 - 60, 300, 120))
    screen.blit(over_img, (screen_width // 2 - 80, screen_height // 2 - 50))
    add_high_score(pscore)
    y_offset = 0
    for num, score in enumerate(read_high_scores()):
        score_text = (f"Highest score is: {score}")
        score_img = font.render(score_text, True, blue)
        screen.blit(score_img, (screen_width // 2 - 120, screen_height // 2 + 20 + y_offset))
        y_offset += 30


#game loop
currand = 0.01
run = True
while run:

    #draws our screen
    draw_screen()
    draw_score(score)
    draw_maze(maze)
    
    #determines direction of the player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3:
                direction = 1
            if event.key == pygame.K_RIGHT and direction != 4:
                direction = 2
            if event.key == pygame.K_DOWN and direction != 1:
                direction = 3
            if event.key == pygame.K_LEFT and direction != 2:
                direction  = 4
            if event.key == pygame.K_SPACE:
                direction = 0

    if game_over == False:
        #update player
        if update_player > 99:
            update_player = 0
            player_pos = player_pos[-1:] + player_pos[:-1]
            if check_collision(player_pos, maze):
                game_over = True
            #heading up
            if direction == 1:
                player_pos[0][0] = player_pos[1][0]
                player_pos[0][1] = player_pos[1][1] - cell_size
            #heading down
            if direction == 3:
                player_pos[0][0] = player_pos[1][0]
                player_pos[0][1] = player_pos[1][1] + cell_size
            #heading right
            if direction == 2:
                player_pos[0][1] = player_pos[1][1]
                player_pos[0][0] = player_pos[1][0] + cell_size
            #heading left
            if direction == 4:
                player_pos[0][1] = player_pos[1][1]
                player_pos[0][0] = player_pos[1][0] - cell_size
            game_over = check_game_over(game_over)
            next_level = check_next_level(checker)
            
            if next_level:
                player_pos = [[int(screen_width / 2), int(screen_height / 2)]]
                player_pos.append([300,310])
                currand += 0.01
                direction = 0
                score += 1
                maze = [[0 for _ in range(screen_width // cell_size)] for _ in range(screen_height // cell_size)]
                for row in range(len(maze)):
                    for col in range(len(maze[0])):
                        if random.random() < (currand)+0.01:
                            maze[row][col] = 1
                while check_starting_position_collision(maze, player_pos):
                       maze = generate_maze(currand)
                draw_score(score)
                       
                       
    if game_over == True:
        draw_game_over(score)

    #draw the player
    head = 1
    for x in player_pos:

        if head == 0:
            pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, body_inner, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
        if head == 1:
            pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, (255,0,0), (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
            head = 0

    pygame.display.update()

    update_player += 1

pygame.quit()
