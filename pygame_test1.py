import pygame
import time

#x = pygame.init()
#print(x)

pygame.init()

#define colors using tuples
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Psyqo Slither')

#pygame.display.flip()
#pygame.display.update()

clock = pygame.time.Clock()

block_size = 10
FPS = 30

#font size 25
font = pygame.font.SysFont(None, 25)

def message_to_screen(msg,color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [display_width/2.5, display_height/2.5])

def gameLoop():
    gameExit = False
    gameOver = False

    # leader of the group of blocks.  the head of the snake.
    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = 0
    lead_y_change = 0

    #main game loop
    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game over, press C to play again or Q to quit", red)
            pygame.display.update()

            for event in pygame.event.get():
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

        #x,y,width,height
        pygame.draw.rect(gameDisplay,black,[lead_x,lead_y,block_size,block_size])
        #pygame.draw.rect(gameDisplay, red, [400, 300, 10, 20])

        #another method for drawing rectangles
        #gameDisplay.fill(red,rect=[200,200,50,50])

        pygame.display.update()

        #frames per second (fps)
        #to affect game difficulty always change movment variables first before tinkering with fps
        clock.tick(FPS)

    pygame.quit()
    quit()

gameLoop()