import pygame
import math
import sys
from tetris_pieces import *
from pygame.locals import *

pygame.init()

pygame.mixer.music.load("Tetris.ogg")
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)


# Colours
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
purple = (160,32,240)
cyan = (0,255,255)
orange = (255,100,10)
yellow = (255,255,0)
grey = (190,190,190)

#Colours list

colours = [black, cyan, blue, orange, yellow, green, purple, red]

# User Interface variables
clock = pygame.time.Clock()
fps = 60
width = 640
height = 480
tile_size = 20
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")


def clear_board():
    return [[0 for _ in range(cols)] for _ in range(rows)]

#function that calculates drop time
def calculate_drop_time(level):
   return math.floor(math.pow((0.8 - ((level - 1) * 0.007)), level-1) * 60)

# Draw board function

def draw_board(board, board_surface):
    for row in range(rows):
        for col in range (cols):
            current_tile = board[row][col]
            tile_x = col*tile_size
            tile_y = row * tile_size
            draw_tile(tile_x, tile_y,current_tile, board_surface)

# Draw board title
def draw_tile(pos_x, pos_y, tile, surface):
    tile_colour = colours[tile]
    rect = pygame.Rect((pos_x, pos_y), (tile_size, tile_size))
    pygame.draw.rect(surface, tile_colour, rect)
    pygame.draw.rect(surface, grey, rect.inflate(1,1),1)

# Draw play area

def draw_play_area(screen_position, screen_surface, board_surface):
    rows_to_show = 20.5
    top_y = board_surface.get_height()-rows_to_show * tile_size
    screen_surface.blit(board_surface,screen_position,pygame.Rect((0,top_y), (board_surface.get_width(), rows_to_show * tile_size)))

# Draw Tetriminion

def draw_tetrimino(pos_x, pos_y,tetrimino, board_surface):
    top_x = pos_x
    top_y = pos_y
    rows = len(tetrimino)
    cols = len(tetrimino[0])
    for row in range(rows):
        for col in range(cols):
            tile = tetrimino[row][col]
            if tile != 0:
                tile_x= (top_x + col)*tile_size
                tile_y = (top_y + row)* tile_size
                draw_tile(tile_x, tile_y, tile, board_surface)



# lOCK FUNC

def lock(x_pos, y_pos,grid,tetrimino):

    top_x = x_pos
    top_y = y_pos
    tetrimino_height = len(tetrimino)
    tetrimino_width = len(tetrimino[0])
    for y in range(tetrimino_height):
        for x in range(tetrimino_width):
            tile = tetrimino[y][x]
            if tetrimino[y][x] != 0:
                grid[top_y+y][top_x+x] = tile




# clear
def check_and_clear_lines(grid):
    lines_cleared = 0
    full_lines = []
    for y,line in enumerate (grid):
        if 0 not in line:
            lines_cleared += 1
            full_lines.append(y)

    if lines_cleared > 0:
        for y in full_lines:
            grid.pop(y)
            grid.insert(0, [0 for _ in range (cols)])
    return lines_cleared
# Score lines

def score_lines(lines_cleared):
    if 1 < lines_cleared < 4:
        lines_cleared += 2
    elif lines_cleared == 4:
        lines_cleared += 4
    return lines_cleared

def check_lockout(position, grid, tetrimino):
    top_x = position[0]
    top_y = position[1]
   # print("TOP Y:" +str(top_y))
    tetrimino_height =len(tetrimino)
    tetrimino_width = len(tetrimino[0])
    out_of_bounds_y = 20
    max_y = 0
    for y in range(tetrimino_height):
        if not all(tetrimino[y]):
            max_y = top_y + y
    print(max_y)
    return max_y <= out_of_bounds_y


# Player info
level = 1
score = 0
scores = 5
next_level = 5 * level
drop_clock = 0
current_droptime = base_droptime = calculate_drop_time(level)

# Vars for board

rows = 40
cols = 10
board = [[0 for _ in range(cols)] for _ in range(rows)]
board_surface = pygame.Surface((cols * tile_size, rows * tile_size))
locking = False
lock_clock = 0
lock_delay = 30

font = pygame.font.Font(None, 24)

# Game States
RESTART = -1
PLAYING = 0
GAME_OVER = 1
game_state = PLAYING


def refill_bag():
    everything_bag = ["I", "J", "L", "O", "S", "T", "Z"]
    final_bag= []
    while len(everything_bag) > 0:
        final_bag.append(everything_bag.pop(random.randrange(0, len(everything_bag))))
    return final_bag


random_bag = refill_bag()
print(random_bag)
active_tetrimino = Tetrimino()
active_tetrimino.grid_ref = board
active_tetrimino.reset(random_bag.pop(0))

next_tetrimino = Tetrimino()
next_tetrimino.reset(random_bag[0])

held_tetrimino = ""

swapping = False
can_swap = True



# Game loops
while True:
    game_over = False
    print(game_state)
    while game_state == RESTART:
        print("Restatrinf")
        board = clear_board()
        random_bag = refill_bag()
        active_tetrimino.reset(random_bag.pop(0))
        next_tetrimino.reset(random_bag[0])
        held_tetrimino = ""

        score = 0
        level = 1
        next_level =5 * level
        current_droptime = base_droptime = calculate_drop_time(level)
        game_state = PLAYING
        swapping = False
        can_swap = True

    while game_state == PLAYING:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    active_tetrimino.move(1,0)

                elif event.key == pygame.K_a:
                    active_tetrimino.move(-1,0)

                elif event.key == pygame.K_RIGHT:
                    active_tetrimino.rotate(1)

                elif event.key == pygame.K_LEFT:
                    active_tetrimino.rotate(-1)

                elif event.key == pygame.K_SPACE:
                    swapping = True


                elif event.key == pygame.K_s:
                    current_droptime = base_droptime//20

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    current_droptime = base_droptime

        if swapping and can_swap:
            if held_tetrimino == '':
                held_tetrimino = active_tetrimino.type
                active_tetrimino.reset(random_bag.pop(0))
                if random_bag == []:
                    random_bag = refill_bag()
                next_tetrimino.type = random_bag[0]

            else:
                current_tetrimino = active_tetrimino.type
                active_tetrimino.reset(held_tetrimino)
                held_tetrimino = current_tetrimino

            swapping = False
            can_swap = False
            locking = False
            lock_clock = 0


        drop_clock += 1
        if drop_clock >= current_droptime:
            move = active_tetrimino.move(0,1)
            if not move:
                if not locking:
                    locking = True
                    lock_clock = 0
            else:
                locking = False


            drop_clock = 0
        if locking:
            lock_clock += 1
            if lock_clock >= lock_delay:
                if not active_tetrimino.move(0,1):

                    lock(active_tetrimino.x, active_tetrimino.y, board,
                         pieces[active_tetrimino.type][active_tetrimino.rotation])
                    drop_clock = base_droptime
                    game_over = check_lockout((active_tetrimino.x, active_tetrimino.y), board,
                                              pieces[active_tetrimino.type][active_tetrimino.rotation])

                    active_tetrimino.reset(random_bag.pop(0))
                    game_over = active_tetrimino.collision_check(active_tetrimino.x, active_tetrimino.y)




                    if random_bag == []:
                        random_bag = refill_bag()

                    if game_over:
                        game_state = GAME_OVER
                        pass

                    # print("This did not work")

                    next_tetrimino.reset(random_bag[0])
                    lock_clock = 0
                    locking = False
                    swapping = False
                    can_swap = True
                    lines_cleared = check_and_clear_lines(board)

                    if lines_cleared > 0:

                        scores = scores - lines_cleared
                        score += score_lines(lines_cleared)

                        if score >= next_level:
                            level += 1
                            next_level = 5 * level
                            base_droptime = calculate_drop_time(level)
                        if scores == 0:
                            scores += 5



        screen.fill(grey)
        draw_board(board,board_surface)
        draw_tetrimino(active_tetrimino.x, active_tetrimino.y,pieces[active_tetrimino.type][active_tetrimino.rotation], board_surface)
        draw_tetrimino(22, 5,pieces[next_tetrimino.type][0], screen)

        if held_tetrimino != "":
            draw_tetrimino(7, 2, pieces[held_tetrimino][0], screen)

        draw_play_area(((640/2)- board_surface.get_width()/2,10),screen, board_surface)

# do this but for level and next level
        score_surface = font.render("Score: " + str(10 * score), False, pygame.Color("black"))
        score_surface1 = font.render("Next level: " + str(next_level*10), False, pygame.Color("black"))
        score_surface2 = font.render("Level: " + str(level), False, pygame.Color("black"))
        held_surface = font.render("Held: " , False, pygame.Color("black"))

        screen.blit(score_surface, (640/2 + board_surface.get_width()/2 +10, 10))
        screen.blit(score_surface1, (640/2 + board_surface.get_width()/2 + 10, 10 + score_surface.get_height() + 10))
        screen.blit(score_surface2, (640/2 + board_surface.get_width()/2 + 10, 10 + score_surface.get_height() + 10 + score_surface1.get_height() + 10))
        screen.blit(held_surface, (140, 20))
        pygame.display.update()
    while game_over == GAME_OVER:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = RESTART


        screen.fill(red)
        draw_board(board, board_surface)
        draw_tetrimino(active_tetrimino.x, active_tetrimino.y, pieces[active_tetrimino.type][active_tetrimino.rotation],
                       board_surface)
        draw_tetrimino(22, 5, pieces[next_tetrimino.type][0], screen)

        if held_tetrimino != "":
            draw_tetrimino(7, 2, pieces[held_tetrimino][0], screen)

        draw_play_area(((640 / 2) - board_surface.get_width() / 2, 10), screen, board_surface)

        # do this but for level and next level
        score_surface = font.render("Score: " + str(10 * score), False, pygame.Color("white"))
        score_surface1 = font.render("Next level: " + str(next_level * 10), False, pygame.Color("white"))
        score_surface2 = font.render("Level: " + str(level), False, pygame.Color("white"))
        game_over_surface = font.render("GAME OVER PRESS THE SPACEBAR TO ReStArT",False, pygame.Color("white") )
        held_surface = font.render("Held: ", False, pygame.Color("white"))

        screen.blit(score_surface, (640 / 2 + board_surface.get_width() / 2 + 10, 10))
        screen.blit(score_surface1,
                    (640 / 2 + board_surface.get_width() / 2 + 10, 10 + score_surface.get_height() + 10))
        screen.blit(score_surface2, (640 / 2 + board_surface.get_width() / 2 + 10,
                                     10 + score_surface.get_height() + 10 + score_surface1.get_height() + 10))
        game_over_rect = Rect(640/2 - game_over_surface.get_width() / 2, 200, game_over_surface.get_width(), game_over_surface.get_height() )
        pygame.draw.rect(screen, black,game_over_rect.inflate(10,10))
        screen.blit(game_over_surface, ((640/2)-game_over_surface.get_width()/2, 200))
        screen.blit(held_surface, (140, 20))
        pygame.display.update()


