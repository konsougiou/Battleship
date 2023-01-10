import pygame as pg
from buttons import Button
import os
import api

pg.font.init()

WIDTH, HEIGHT = 1200, 800
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 50

key = None
player = None

SCORE_FONT = pg.font.SysFont('comicsans', 20)

WIN = pg.display.set_mode((WIDTH, HEIGHT))

BUTTON_IMAGE = pg.image.load(os.path.join('resources', 'button.jpeg'))
BUTTON = pg.transform.scale(BUTTON_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT) )

BUTTON_2_IMAGE = pg.image.load(os.path.join('resources', 'Color-Green.jpeg'))
BUTTON_2 = pg.transform.scale(BUTTON_2_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT) )


MENU_BG_IMAGE = pg.image.load(os.path.join('resources', 'menu_BG.jpeg'))
MENU_BG = pg.transform.scale(MENU_BG_IMAGE, (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
RED = (255, 0 ,0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GREY = (220, 220, 220)
BLUE = (0, 0, 255)


HOST_BUTTON = Button(BUTTON , pos = [(WIDTH/2), 300], text_input = "HOST", font = SCORE_FONT, base_color = WHITE, hovering_color = PURPLE)
GUEST_BUTTON = Button(BUTTON , pos = [(WIDTH/2), 500], text_input = "GUEST", font = SCORE_FONT, base_color = WHITE, hovering_color = PURPLE)
INPUT_BUTTON = Button(BUTTON , pos = [(WIDTH/2), 560], text_input = "", font = SCORE_FONT, base_color = WHITE, hovering_color = PURPLE)
SUBMIT_BUTTON = Button(BUTTON , pos = [(WIDTH*2/3), 100], text_input = "SUBMIT FORMATION", font = SCORE_FONT, base_color = WHITE, hovering_color = PURPLE)
FIRE_BUTTON = Button(BUTTON , pos = [100, 100], text_input = "FIRE", font = SCORE_FONT, base_color = WHITE, hovering_color = PURPLE)

grid = [[0 for _ in range(20)] for _ in range(10)]




def draw_main(grid, enemy_grid, MENU_MOUSE_POS):

    WIN.blit(MENU_BG, (0, 0))
    FIRE_BUTTON.changeColor(MENU_MOUSE_POS)
    FIRE_BUTTON.update(WIN)

    for i, row in enumerate(enemy_grid):
        for j, tile in enumerate(row):
            if tile == 1:
                colour = GREY
            elif tile == 2:
                colour = RED
            elif tile == 3:
                colour = PURPLE
            else:
                colour = BLUE
            pg.draw.rect(WIN, colour, pg.Rect((j*80) + 405, 80*i + 5, 70, 70))

    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile == 1:
                colour = GREY
            elif tile == 2:
                colour = RED
            elif tile == 3:
                colour = PURPLE
            else:
                colour = BLUE
            pg.draw.rect(WIN, colour, pg.Rect((j*80) + 405, 80*i + 405, 70, 70))





def draw_setup(grid, available_ships, MENU_MOUSE_POS):

    WIN.blit(MENU_BG, (0, 0))

    SUBMIT_BUTTON.changeColor(MENU_MOUSE_POS)
    SUBMIT_BUTTON.update(WIN)

    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile == 1:
                colour = GREY
            elif tile == 2:
                colour = RED
            else:
                colour = BLUE
            pg.draw.rect(WIN, colour, pg.Rect((j*120) + 10, 120*i + 210, 100, 100))




def main(player, key, grid):
    enemy_grid = [[0 for _ in range(20)] for _ in range(10)]
    turn = 1
    pressed = (-1, -1)
    pressed_status = 0
    current_ticks = pg.time.get_ticks()
   
    while True:

        MENU_MOUSE_POS = pg.mouse.get_pos()

        if player == turn:

            if pressed != (-1, -1):
                FIRE_BUTTON.image = BUTTON_2
            else:
                FIRE_BUTTON.image = BUTTON_2


            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:

                    if FIRE_BUTTON.checkForInput(MENU_MOUSE_POS) and pressed != (-1, -1):
                        r = api.fire(player, key, pressed)
                        if r.json()["end"]:
                            pg.quit()
                        enemy_grid[pressed[1]][pressed[0]] = 2 if r.json()["message"] else 3
                        turn = 1 if turn == 2 else 2

                    x_pos = MENU_MOUSE_POS[0] - 400
                    y_pos = MENU_MOUSE_POS[1] 


                    if y_pos <= 400 and x_pos >= 0:
                        x_idx, y_idx = x_pos//80, y_pos//80

                        if pressed == (-1, -1):
                            pressed_status = enemy_grid[y_idx][x_idx]
                            enemy_grid[y_idx][x_idx] = 1
                            pressed = (x_idx, y_idx)
                        elif pressed == (x_idx, y_idx):
                            enemy_grid[y_idx][x_idx] = pressed_status
                            pressed = (-1, -1)
                        else:
                            enemy_grid[pressed[1]][pressed[0]] = pressed_status
                            pressed_status = enemy_grid[y_idx][x_idx]
                            enemy_grid[y_idx][x_idx] = 1
                            pressed = (x_idx, y_idx)

        else:
            new_ticks = pg.time.get_ticks()
            if new_ticks - current_ticks > 5000:
                current_ticks = new_ticks
                r = api.ping_fire(key)
                previous_target =  (r.json()["previous_x"], r.json()["previous_y"])
                turn = r.json()["state"]
                if turn == 3:
                    pg.quit()

                if turn == player:
                    position = grid[previous_target[1]][previous_target[0]]
                    grid[previous_target[1]][previous_target[0]] =  2 if position == 1 else 3
                    pressed = (-1, -1)


            else:
                pg.time.delay(1000)
                pg.display.update()
                continue

        
        draw_main(grid, enemy_grid, MENU_MOUSE_POS)
        pg.display.update()






def setup(player, key, grid):

    available_ships = [2,3,4,5]
    pressed = False
    pivot = [-1, -1]
    waiting = False
    current_ticks = pg.time.get_ticks()

    while True:
        
        if waiting:
            new_ticks = pg.time.get_ticks()
            if new_ticks - current_ticks > 5000:
                current_ticks = new_ticks
                r = api.ping_grid(player, key)
                if r.json()["message"] == "begin":
                    main(player, key, grid)
                else:
                    pg.time.delay(1000)
                    pg.display.update()
                    continue
            else:
                pg.time.delay(1000)
                pg.display.update()
                continue

        MENU_MOUSE_POS = pg.mouse.get_pos()

        if not available_ships:
            SUBMIT_BUTTON.image = BUTTON_2


        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:

                if SUBMIT_BUTTON.checkForInput(MENU_MOUSE_POS) and (not available_ships):
                    r = api.send_grid(player, grid, key)
                    if r.json()["message"] == "begin":
                        main(player, key, grid)
                    else:
                        waiting = True
                    continue

                x_pos = MENU_MOUSE_POS[0] 
                y_pos = MENU_MOUSE_POS[1] - 200


                if y_pos > 0:
                    x_idx, y_idx= x_pos//120, y_pos//120
                    if pressed:

                        if x_idx == pivot[0] and y_idx == pivot[1]:
                            pressed = False
                            grid[y_idx][x_idx] = 0
                            pivot = [-1,-1]
                        elif x_idx == pivot[0]:
                            dist = abs(y_idx - pivot[1]) + 1
                            if dist in available_ships:
                                available_ships.remove(dist)
                                for i in range(min(y_idx, pivot[1]), max(y_idx, pivot[1]) + 1):
                                    grid[i][x_idx] = 1
                                pressed = False
                        elif y_idx == pivot[1]:
                            dist = abs(x_idx - pivot[0]) + 1
                            if dist in available_ships:
                                available_ships.remove(dist)
                                for i in range(min(x_idx, pivot[0]), max(x_idx, pivot[0]) + 1):
                                    grid[y_idx][i] = 1
                                pressed = False
                    else:
                        pivot = [x_pos//120, y_pos//120]
                        grid[y_pos//120][x_pos//120] = 2
                        pressed = True

                    
        draw_setup(grid, available_ships, MENU_MOUSE_POS)
        pg.display.update()


# Function implementing the main menu screen where user selects between 
# hosting and joining a game





def menu(player, key, grid):

    pressed = False
    pg.display.set_caption("Gamemodes")
    current_ticks = pg.time.get_ticks()

    while True:
        
        WIN.blit(MENU_BG, (0, 0))
        if player == 1:
            new_ticks = pg.time.get_ticks()
            if new_ticks - current_ticks > 5000:
                current_ticks = new_ticks
                r = api.ping_initialize(key)
                if r.json()["message"] == 0:
                    setup(player, key, grid)
                else:
                    pg.time.delay(1000)
                    pg.display.update()
                    continue
            else:
                pg.time.delay(1000)
                pg.display.update()
                continue


        MENU_MOUSE_POS = pg.mouse.get_pos()

        
        for button in [HOST_BUTTON, GUEST_BUTTON, INPUT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if HOST_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player = 1
                    r = api.initialize_host()
                    key = r.json()["key"]
                    print(f"The game key is {key}")

                elif GUEST_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player = 2
                    key = input("please enter the game key: ")
                    r = api.initialize_guest(key)
                    if r.json()["message"] == 0:
                        setup(player, key, grid)
                    else:
                        print("Invalid key")

                elif INPUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pressed = True
                else:
                    pressed = False 

            # if event.type == pg.KEYDOWN and pressed:
            #     if event.key == pg.K_0:
            #         INPUT_BUTTON.text_input += "0"
            #     elif event.key == pg.K_1:
            #         INPUT_BUTTON.text_input += "1"
            #     elif event.key == pg.K_2:
            #         INPUT_BUTTON.text_input += "2"
            #     elif event.key == pg.K_3:
            #         INPUT_BUTTON.text_input += "3"
            #     elif event.key == pg.K_BACKSPACE:
            #         INPUT_BUTTON.text_input = INPUT_BUTTON.text_input[:-1]

            
        pg.display.update()
        
        


# Function implementing a the screen where the players set up their grids

    
# Function implemening the main game loop 



if __name__ == "__main__":
    menu(player, key, grid)