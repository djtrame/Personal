import pygame
import time
import random

#x = pygame.init()
#print(x)

pygame.init()

#define colors using tuples
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
darkgreen = (0,155,0)
blue = (0,0,255)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Psyqo Slither')

#pygame.display.flip()
#pygame.display.update()

clock = pygame.time.Clock()

#thickness of the snake
block_size = 20

FPS = 20

#font size 25
font = pygame.font.SysFont(None, 25)

def snake(block_size, snakeList):
    for XnY in snakeList:
        # x,y,width,height
        # draw the snake
        #pygame.draw.rect(gameDisplay, darkgreen, [lead_x, lead_y, block_size, block_size])
        pygame.draw.rect(gameDisplay, darkgreen, [XnY[0],XnY[1],block_size,block_size])

def message_to_screen(msg,color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [display_width/2.5, display_height/2.5])

def roundTo10(number):
    #this places the apple in parts of the screen divisible by 10
    #return round(number/10.0) * 10.0

    #this places the apple on the screen at odd pixel locations
    return round(number)

def gameLoop():
    gameExit = False
    gameOver = False

    # leader of the group of blocks.  the head of the snake.
    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    #a random number from 0 to 790 could by 113.  that pixel wouldn't line up with our block_size snake head
    #so we round that 113 to something like 110.  or we round 116 to 120.  now it lines up with the snake
    randAppleX = roundTo10(random.randrange(0, display_width-block_size))
    randAppleY = roundTo10(random.randrange(0, display_height-block_size))

    #main game loop
    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game over, press C to play again or Q to quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                #handle the user clicking the X on the window during the game over sequence
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    #in a snake game the user pressed a direction and the snake continues moving in that direction
                    #for other game types we want the movement to stop when the key is released
                    #this handles that scenario but we are leaving it commented for the snake game
                    #lead_x_change = 0
                    pass

        #boundaries
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change



        gameDisplay.fill(white)

        appleThickness = 30

        #draw the apple
        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, block_size, block_size])
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, appleThickness, appleThickness])


        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        #if length of the snake is bigger than the allowed length then remove the 1st element
        if len(snakeList) > snakeLength:
            del snakeList[0]

        #check if we're crashing into ourselves
        #list comprehension
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        #snakeList[1:] would get us anything after the 1st element
        #snakeList[-1] is the last element

        #draw the snake
        snake(block_size, snakeList)


        #pygame.draw.rect(gameDisplay, red, [400, 300, 10, 20])

        #another method for drawing rectangles
        #gameDisplay.fill(red,rect=[200,200,50,50])

        pygame.display.update()

        #check exact crossover of snake and apple (works as long as they have the same size)
        # if lead_x == randAppleX and lead_y == randAppleY:
        #     randAppleX = roundTo10(random.randrange(0, display_width - block_size))
        #     randAppleY = roundTo10(random.randrange(0, display_height - block_size))
        #     snakeLength += 1

        #handle a bigger apple crossover
        # if lead_x >= randAppleX and lead_x <= randAppleX + appleThickness:
        #     if lead_y >= randAppleY and lead_y <= randAppleY + appleThickness:
        #         randAppleX = roundTo10(random.randrange(0, display_width - block_size))
        #         randAppleY = roundTo10(random.randrange(0, display_height - block_size))
        #         snakeLength += 1

        #handle more exact partial crossovers
        if (lead_x > randAppleX and lead_x < randAppleX+appleThickness) or (lead_x+block_size > randAppleX and lead_x+block_size < randAppleX + appleThickness):
            if (lead_y > randAppleY and lead_y < randAppleY+appleThickness) or (lead_y+block_size > randAppleY and lead_y+block_size < randAppleY+appleThickness):
                randAppleX = roundTo10(random.randrange(0, display_width - block_size))
                randAppleY = roundTo10(random.randrange(0, display_height - block_size))
                snakeLength += 1



        #frames per second (fps)
        #to affect game difficulty always change movement variables first before tinkering with fps
        clock.tick(FPS)

    pygame.quit()
    quit()

gameLoop()