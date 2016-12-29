import pygame
import random

#this is a psuedo 3d example.  (2.5d)
pygame.init()

#define colors using tuples
white = (255,255,255)
black = (0,0,0)
red = (150,0,0)
lightred = (255,0,0)
green = (0,255,0)
darkgreen = (0,155,0)
blue = (0,0,255)
yellow = (200,200,0)
lightyellow = (255,255,0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('3d demo')

clock = pygame.time.Clock()

FPS = 30


#not sure how to kill menu loops in game intro and game controls.  this doesn't seem to do it.
inControlsMenu = False
inMainMenu = False
inGameOverMenu = False
inWinningMenu = False

#font size 25
# smallfont = pygame.font.SysFont("comicsansms", 25)
# mediumfont = pygame.font.SysFont("comicsansms", 50)
# largefont = pygame.font.SysFont("comicsansms", 80)
smallfont = pygame.font.Font("fonts/freesansbold.ttf", 25)
mediumfont = pygame.font.Font("fonts/freesansbold.ttf", 50)
largefont = pygame.font.Font("fonts/freesansbold.ttf", 80)


def cube(startPoint, fullSize):
    #top left node
    node_1 = [startPoint[0], startPoint[1]]

    #top right
    node_2 = [startPoint[0]+fullSize, startPoint[1]]

    #bottom left
    node_3 = [startPoint[0], startPoint[1]+fullSize]

    #bottom right
    node_4 = [startPoint[0]+fullSize, startPoint[1]+fullSize]

    #give half the offset to x, half to y
    offset = int(fullSize / 2)

    x_mid = int(display_width / 2)

    #distance from the middle of the screen
    x_offset = -1*int(startPoint[0]-x_mid)

    y_mid = int(display_height / 2)
    y_offset = int(startPoint[1] - y_mid)

    print(x_offset)

    if x_offset < -100:
        x_offset = -100
    elif x_offset > 100:
        x_offset = 100

    #add to the x and subtract from y (go up and to the right)
    node_5 = [node_1[0] + x_offset, node_1[1]-y_offset]
    node_6 = [node_2[0] + x_offset, node_2[1]-y_offset]
    node_7 = [node_3[0] + x_offset, node_3[1]-y_offset]
    node_8 = [node_4[0] + x_offset, node_4[1]-y_offset]

    #top line
    pygame.draw.line(gameDisplay, white, node_1, node_2)

    # bottom line
    pygame.draw.line(gameDisplay, white, node_3, node_4)

    # left side line
    pygame.draw.line(gameDisplay, white, node_1, node_3)

    # right side line
    pygame.draw.line(gameDisplay, white, node_2, node_4)

    #top line of 2nd square
    pygame.draw.line(gameDisplay, white, node_5, node_6)

    #bottom line of 2nd square
    pygame.draw.line(gameDisplay, white, node_7, node_8)

    #left side line of 2nd square
    pygame.draw.line(gameDisplay, white, node_5, node_7)

    #right side line of 2nd square
    pygame.draw.line(gameDisplay, white, node_6, node_8)

    #mark the nodes
    pygame.draw.circle(gameDisplay, green, node_1, 5)
    pygame.draw.circle(gameDisplay, green, node_2, 5)
    pygame.draw.circle(gameDisplay, green, node_3, 5)
    pygame.draw.circle(gameDisplay, green, node_4, 5)

    pygame.draw.circle(gameDisplay, green, node_5, 5)
    pygame.draw.circle(gameDisplay, green, node_6, 5)
    pygame.draw.circle(gameDisplay, green, node_7, 5)
    pygame.draw.circle(gameDisplay, green, node_8, 5)


    pygame.draw.line(gameDisplay, white, node_1, node_5)
    pygame.draw.line(gameDisplay, white, node_2, node_6)
    pygame.draw.line(gameDisplay, white, node_3, node_7)
    pygame.draw.line(gameDisplay, white, node_4, node_8)


def gameLoop():

    squareLocation = [300,200]
    squareSize = 100

    squareMove = 0

    z_move = 0
    z_location = 50
    y_move = 0

    gameExit = False

    #main game loop
    while not gameExit:

        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    squareMove = -5
                elif event.key == pygame.K_RIGHT:
                    squareMove = 5
                elif event.key == pygame.K_UP:
                    #moving towards the cube
                    # z_move = -5
                    # squareMove = -1
                    y_move = -5
                elif event.key == pygame.K_DOWN:
                    #moving away from the cube
                    # z_move = 5
                    # squareMove = 1
                    y_move = 5
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_a:
                    power_change = -1
                elif event.key == pygame.K_d:
                    power_change = 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    squareMove = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    #squareMove = 0
                    y_move = 0

                if event.key == pygame.K_a or event.key == pygame.K_d:
                    z_move = 0

        # clear the display
        gameDisplay.fill(black)

        #newSquareSize = int(squareSize / (z_location*0.1))
        newSquareSize = squareSize

        z_location += z_move

        #squareSize += squareMove
        squareLocation[0] += squareMove
        squareLocation[1] += y_move

        cube(squareLocation, newSquareSize)

        pygame.display.update()

        #frames per second (fps)
        #to affect game difficulty always change movement variables first before tinkering with fps
        clock.tick(FPS)

    pygame.quit()
    quit()


gameLoop()