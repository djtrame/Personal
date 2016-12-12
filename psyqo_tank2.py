import pygame
import time
import random



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
pygame.display.set_caption('Psyqo Tank')

# imgSnakehead = pygame.image.load('snakehead.png')
# imgApple = pygame.image.load('apple.png')

#pygame.display.set_icon(imgApple)

#pygame.display.flip()
#pygame.display.update()

clock = pygame.time.Clock()

#thickness of the snake
block_size = 20
appleThickness = 30
FPS = 15

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
        message_to_screen("Welcome to PsyqoTank",
                          green,
                          y_displace=-100,
                          size="medium")
        message_to_screen("The objective is to shoot and destroy",
                          black,
                          y_displace=-30,
                          size="small")
        message_to_screen("the enemy tank before they destroy you.",
                          black,
                          y_displace=10,
                          size="small")
        message_to_screen("The more enemies you destroy, the harder they get!",
                          black,
                          y_displace=50,
                          size="small")
        # message_to_screen("Press C to play, P to pause or Q to quit...",
        #                   black,
        #                   y_displace=180,
        #                   size="small")

        createButton("Play", 150,500,110,50,darkgreen, green, action="play")
        createButton("Controls", 350, 500, 110, 50, yellow, lightyellow, action="controls")
        createButton("Quit", 550, 500, 110, 50, red, lightred, action="quit")


        pygame.display.update()
        clock.tick(15)

#return a tuple?
def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
            textSurface = mediumfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonX, buttonY, buttonWidth, buttonHeight, size="small"):
    textSurface, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonX+(buttonWidth/2)), buttonY+(buttonHeight/2))
    gameDisplay.blit(textSurface, textRect)

def message_to_screen(msg,color,y_displace=0, size="small"):
    textSurface, textRect = text_objects(msg,color,size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurface, textRect)

def createButton(text, x, y, width, height, inactiveColor, activeColor,action=None):
    cursor = pygame.mouse.get_pos()
    #print (cursor)

    click = pygame.mouse.get_pressed()
    #print(click)
    #tuple of (0,0,0), left number is left mouse, then middle, then right

    #if statement with simultaneous conditions
    #highlight the button with a lighter color on mouseover
    if x+width > cursor[0] > x and y+height > cursor[1] > y:
        # draw a button with x,y,width,height
        pygame.draw.rect(gameDisplay, activeColor, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()

            if action == "controls":
                pass

            if action == "play":
                gameLoop()
    else:
        pygame.draw.rect(gameDisplay, inactiveColor, (x, y, width, height))

    text_to_button(text,black,x,y,width,height)

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
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_p:
                    pause()

        gameDisplay.fill(white)

        pygame.display.update()


        #frames per second (fps)
        #to affect game difficulty always change movement variables first before tinkering with fps
        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
gameLoop()