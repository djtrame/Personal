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

imgSnakehead = pygame.image.load('snakehead.png')
imgApple = pygame.image.load('apple.png')

pygame.display.set_icon(imgApple)

#pygame.display.flip()
#pygame.display.update()

clock = pygame.time.Clock()

#thickness of the snake
block_size = 20
appleThickness = 30
FPS = 15

direction = "right"

#font size 25
# smallfont = pygame.font.SysFont("comicsansms", 25)
# mediumfont = pygame.font.SysFont("comicsansms", 50)
# largefont = pygame.font.SysFont("comicsansms", 80)
smallfont = pygame.font.Font("fonts/freesansbold.ttf", 25)
mediumfont = pygame.font.Font("fonts/freesansbold.ttf", 50)
largefont = pygame.font.Font("fonts/freesansbold.ttf", 80)

def pause():
    paused = True

    message_to_screen("Paused...", black, -100, "large")

    message_to_screen("Press C to continue or Q to quit...",
                      black,
                      25)

    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        #gameDisplay.fill(white)

        clock.tick(5)

#weird code to trick cx_Freeze into working
if False:
    import pygame._view

def score(score):
    #score being passed in is snakeLength-1
    if score < 11:
        calcScore = score
    elif score >= 11 and score < 21:
        calcScore = score * 5
    elif score >= 21 and score < 31:
        calcScore = score * 10
    elif score >= 31 and score < 41:
        calcScore = score * 20
    elif score >= 41 and score < 51:
        calcScore = score * 40
    elif score >= 51 and score < 61:
        calcScore = score * 80
    elif score >= 61 and score < 71:
        calcScore = score * 160
    else:
        calcScore = score * 250

    text = smallfont.render("Score: "+str(calcScore), True, black)
    gameDisplay.blit(text, [0,0])

def randAppleCoordinates():
    randAppleX = roundTo10(random.randrange(0, display_width - appleThickness))
    randAppleY = roundTo10(random.randrange(0, display_height - appleThickness))

    #returning a tuple
    return randAppleX, randAppleY

#runs once
def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither",
                          green,
                          y_displace=-100,
                          size="large")
        message_to_screen("The objective of the game is to eat red apples!",
                          black,
                          y_displace=-30,
                          size="small")
        message_to_screen("The more apples you eat the longer you get!",
                          black,
                          y_displace=10,
                          size="small")
        message_to_screen("If you run into yourself or the edge of the window you croak!",
                          black,
                          y_displace=50,
                          size="small")
        message_to_screen("Press C to play, P to pause or Q to quit...",
                          black,
                          y_displace=180,
                          size="small")

        pygame.display.update()
        clock.tick(15)

def snake(block_size, snakeList):
    if direction == "right":
        head = pygame.transform.rotate(imgSnakehead, 270)
    if direction == "down":
        head = pygame.transform.rotate(imgSnakehead, 180)
    if direction == "left":
        head = pygame.transform.rotate(imgSnakehead, 90)
    if direction == "up":
        head = imgSnakehead

    #the head of our snake is the last (-1) element of the list
    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    #loop through everything except the very last element
    for XnY in snakeList[:-1]:
        # x,y,width,height
        # draw the snake
        #pygame.draw.rect(gameDisplay, darkgreen, [lead_x, lead_y, block_size, block_size])
        pygame.draw.rect(gameDisplay, darkgreen, [XnY[0],XnY[1],block_size,block_size])

#return a tuple?
def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
            textSurface = mediumfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0, size="small"):
    textSurface, textRect = text_objects(msg,color,size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurface, textRect)

def roundTo10(number):
    #this places the apple in parts of the screen divisible by 10
    #return round(number/10.0) * 10.0

    #this places the apple on the screen at odd pixel locations
    return round(number)

def gameLoop():
    #this allows us to access and modify direction.  without global you can only access
    global direction

    direction = "right"
    gameExit = False
    gameOver = False

    # leader of the group of blocks.  the head of the snake.
    lead_x = display_width / 2
    lead_y = display_height / 2

    #if these values are 0 the snake does not move at the start
    #values >0 begin moving the snake in a particular direction
    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    #a random number from 0 to 790 could by 113.  that pixel wouldn't line up with our block_size snake head
    #so we round that 113 to something like 110.  or we round 116 to 120.  now it lines up with the snake
    #use tuple unpacking
    randAppleX,randAppleY = randAppleCoordinates()
    # randAppleX = roundTo10(random.randrange(0, display_width-appleThickness))
    # randAppleY = roundTo10(random.randrange(0, display_height-appleThickness))

    #main game loop
    while not gameExit:

        if gameOver == True:
            message_to_screen("Game Over!",
                              red,
                              y_displace=-50,
                              size="large")
            message_to_screen("Press C to play again or Q to quit",
                              black,
                              y_displace=50,
                              size="medium")
            pygame.display.update()

        while gameOver == True:
            #gameDisplay.fill(white)

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
                    #prevent the snake from turning directly around if it is bigger than 2 segments
                    #this also prevents a game crash for doing so
                    if not (direction == "right" and snakeLength > 2):
                        #remove the snakeLength / 10 part if you don't want the snake to speed up as it gets bigger
                        lead_x_change = -block_size
                        lead_y_change = 0
                        direction = "left"
                elif event.key == pygame.K_RIGHT:
                    if not (direction == "left" and snakeLength > 2):
                        lead_x_change = block_size
                        lead_y_change = 0
                        direction = "right"
                elif event.key == pygame.K_UP:
                    if not (direction == "down" and snakeLength > 2):
                        lead_y_change = -block_size
                        lead_x_change = 0
                        direction = "up"
                elif event.key == pygame.K_DOWN:
                    if not (direction == "up" and snakeLength > 2):
                        lead_y_change = block_size
                        lead_x_change = 0
                        direction = "down"
                elif event.key == pygame.K_p:
                    pause()

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

        #draw the apple
        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, block_size, block_size])
        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, appleThickness, appleThickness])
        gameDisplay.blit(imgApple, (randAppleX, randAppleY))


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

        score(snakeLength-1)

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
                randAppleX, randAppleY = randAppleCoordinates()
                snakeLength += 1



        #frames per second (fps)
        #to affect game difficulty always change movement variables first before tinkering with fps
        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
gameLoop()