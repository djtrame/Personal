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

tankWidth = 40
tankHeight = 20
turretWidth = 5
wheelWidth = 5

ground_height = 35

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Psyqo Tank')

# imgSnakehead = pygame.image.load('snakehead.png')
# imgApple = pygame.image.load('apple.png')

#pygame.display.set_icon(imgApple)

#pygame.display.flip()
#pygame.display.update()

clock = pygame.time.Clock()

FPS = 30

#not sure how to kill menu loops in game intro and game controls.  this doesn't seem to do it.
inControlsMenu = False
inMainMenu = False

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

def tank(x,y,turretPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x-27,y-2),
                       (x-26,y-5),
                       (x-25,y-8),
                       (x-23,y-12),
                       (x-20,y-14),
                       (x - 18, y - 15),
                       (x - 15, y - 17),
                       (x - 13, y - 19),
                       (x - 11, y - 21)]

    #draw the turret
    pygame.draw.circle(gameDisplay, black, (x,y),int(tankHeight / 2))
    #draw the tank
    pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight))

    #draw the gun
    pygame.draw.line(gameDisplay,black, (x,y), possibleTurrets[turretPos], turretWidth)

    # pygame.draw.circle(gameDisplay, black, (x - 15, y + 20), wheelWidth)

    startWheelX = 15

    #0 thru 6
    for i in range(7):
        pygame.draw.circle(gameDisplay, black, (x-startWheelX,y+21), wheelWidth)
        startWheelX -= 5

    #return the turret position of the tank
    return possibleTurrets[turretPos]

def enemy_tank(x,y,turretPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x+27,y-2),
                       (x+26,y-5),
                       (x+25,y-8),
                       (x+23,y-12),
                       (x+20,y-14),
                       (x + 18, y - 15),
                       (x + 15, y - 17),
                       (x + 13, y - 19),
                       (x + 11, y - 21)]

    #draw the turret
    pygame.draw.circle(gameDisplay, black, (x,y),int(tankHeight / 2))
    #draw the tank
    pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight))

    #draw the gun
    pygame.draw.line(gameDisplay,black, (x,y), possibleTurrets[turretPos], turretWidth)

    # pygame.draw.circle(gameDisplay, black, (x - 15, y + 20), wheelWidth)

    startWheelX = 15

    #0 thru 6
    for i in range(7):
        pygame.draw.circle(gameDisplay, black, (x-startWheelX,y+21), wheelWidth)
        startWheelX -= 5

    #return the turret position of the tank
    return possibleTurrets[turretPos]

#runs once
def game_intro():
    global inMainMenu
    inMainMenu = True
    # intro = True

    while inMainMenu:

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

def game_controls():
    # gameControls = True
    global inControlsMenu
    inControlsMenu = True

    while inControlsMenu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



        gameDisplay.fill(white)

        message_to_screen("Controls",
                          green,
                          y_displace=-100,
                          size="medium")
        message_to_screen("Fire: Spacebar",
                          black,
                          y_displace=-30,
                          size="small")
        message_to_screen("Move Turret: Up and Down Arrows",
                          black,
                          y_displace=10,
                          size="small")
        message_to_screen("Move Tank: Left and Right Arrows",
                          black,
                          y_displace=50,
                          size="small")
        message_to_screen("Pause: P",
                          black,
                          y_displace=90,
                          size="small")

        createButton("Play", 150,500,110,50,darkgreen, green, action="play")
        createButton("Main Menu", 350, 500, 110, 50, yellow, lightyellow, action="mainmenu")
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
    global inMainMenu
    global inControlsMenu
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
                inMainMenu = False
                game_controls()

            if action == "play":
                inMainMenu = False
                inControlsMenu = False
                gameLoop()

            #not working?  we aren't quitting the original loops
            if action == "mainmenu":
                inControlsMenu = False
                game_intro()
    else:
        pygame.draw.rect(gameDisplay, inactiveColor, (x, y, width, height))

    text_to_button(text,black,x,y,width,height)

def roundTo10(number):
    #this places the apple in parts of the screen divisible by 10
    #return round(number/10.0) * 10.0

    #this places the apple on the screen at odd pixel locations
    return round(number)

def barrier(barrierLocationX, randomHeight, barrier_width):
    pygame.draw.rect(gameDisplay, black, [barrierLocationX, display_height-randomHeight, barrier_width, randomHeight])

def explosion(x,y, size=50):
    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        startPoint = x,y

        colorChoices = [red, lightred, yellow, lightyellow]

        magnitude = 1

        while magnitude < size:
            exploding_bit_x = x + random.randrange(-1*magnitude,magnitude)
            exploding_bit_y = y + random.randrange(-1 * magnitude, magnitude)

            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0,4)], (exploding_bit_x,exploding_bit_y),random.randrange(1,5))
            magnitude += 1

            pygame.display.update()
            clock.tick(100)

        explode = False


def fireShell(gunCoordinates, tankX, tankY, turretPos,gun_power,barrierLocationX,barrier_width,randomHeight,enemyTankX,enemyTankY):
    fire = True
    damage = 0

    #can't modify tuples, convert it to a list instead
    startingShell = list(gunCoordinates)
    #print("FIRE!")

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #print(startingShell[0],startingShell[1])
        pygame.draw.circle(gameDisplay,red,(startingShell[0],startingShell[1]),5)

        startingShell[0] -= (12 - turretPos)*2

        #quadratic equation example
        #y = x^2  y = x**2
        startingShell[1] += int((((startingShell[0] - gunCoordinates[0])*0.01/(gun_power/50))**2) - (turretPos + turretPos/(12-turretPos)))

        actual_ground = display_height - ground_height

        #if the shell has hit the ground
        if startingShell[1] > actual_ground:
            print("Last shell:",startingShell[0],startingShell[1])
            #determine estimated spot of last impact
            #cross multiplication
            #(x/600) = (189/618) for instance
            #618x = (600 * 189)
            #x = (113,400) / 618
            #x = 183 <------ estimated last X of impact (when the shell hit the border at 600)
            hit_x = int((startingShell[0]*actual_ground)/startingShell[1])
            hit_y = int(actual_ground)
            if enemyTankX + 15 > hit_x  > enemyTankX - 15:
                print("HIT TARGET!")
                damage = 25
            print ("Impact:",hit_x,hit_y)
            explosion(hit_x , hit_y)
            fire = False

        #do comparisons and store them as booleans
        check_x_1 = startingShell[0] <= barrierLocationX + barrier_width
        check_x_2 = startingShell[0] >= barrierLocationX

        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("Last shell:", startingShell[0], startingShell[1])
            hit_x = int(startingShell[0])
            hit_y = int(startingShell[1])
            print ("Impact:",hit_x,hit_y)
            explosion(hit_x , hit_y)
            fire = False

        pygame.display.update()
        clock.tick(100)

    return damage

def eFireShell(gunCoordinates, tankX, tankY, turretPos,gun_power,barrierLocationX,barrier_width,randomHeight,pTankX,pTankY):
    currentPower = 1
    power_found = False
    damage = 0

    while not power_found:
        currentPower += 1
        if currentPower > 100:
            power_found = True

        fire = True

        # can't modify tuples, convert it to a list instead
        startingShell = list(gunCoordinates)

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            startingShell[0] += (12 - turretPos) * 2

            # quadratic equation example
            # y = x^2  y = x**2
            startingShell[1] += int((((startingShell[0] - gunCoordinates[0]) * 0.01 / (currentPower / 50)) ** 2) - (
            turretPos + turretPos / (12 - turretPos)))

            actual_ground = display_height - ground_height

            # if the shell has hit the ground
            if startingShell[1] > actual_ground:
                # determine estimated spot of last impact
                # cross multiplication
                # (x/600) = (189/618) for instance
                # 618x = (600 * 189)
                # x = (113,400) / 618
                # x = 183 <------ estimated last X of impact (when the shell hit the border at 600)
                hit_x = int((startingShell[0] * actual_ground) / startingShell[1])
                hit_y = int(actual_ground)
                if pTankX + 15 > hit_x > pTankX - 15:
                    print("target acquired!")
                    power_found = True
                fire = False

            # do comparisons and store them as booleans
            check_x_1 = startingShell[0] <= barrierLocationX + barrier_width
            check_x_2 = startingShell[0] >= barrierLocationX

            check_y_1 = startingShell[1] <= display_height
            check_y_2 = startingShell[1] >= display_height - randomHeight

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int(startingShell[0])
                hit_y = int(startingShell[1])
                fire = False

    fire = True

    #can't modify tuples, convert it to a list instead
    startingShell = list(gunCoordinates)
    #print("FIRE!")

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #print(startingShell[0],startingShell[1])
        pygame.draw.circle(gameDisplay,red,(startingShell[0],startingShell[1]),5)

        startingShell[0] += (12 - turretPos)*2

        #quadratic equation example
        #y = x^2  y = x**2
        #y = -x^2 produces an upside down U which is the shape of an arch.  booyah!
        startingShell[1] += int((((startingShell[0] - gunCoordinates[0])*0.01/(currentPower/50))**2) - (turretPos + turretPos/(12-turretPos)))

        actual_ground = display_height - ground_height

        #if the shell has hit the ground
        if startingShell[1] > actual_ground:
            #determine estimated spot of last impact
            #cross multiplication
            #(x/600) = (189/618) for instance
            #618x = (600 * 189)
            #x = (113,400) / 618
            #x = 183 <------ estimated last X of impact (when the shell hit the border at 600)
            hit_x = int((startingShell[0]*actual_ground)/startingShell[1])
            hit_y = int(actual_ground)
            if pTankX + 15 > hit_x  > pTankX - 15:
                print("HIT TARGET!")
                damage = 25
            explosion(hit_x , hit_y)
            fire = False

        #do comparisons and store them as booleans
        check_x_1 = startingShell[0] <= barrierLocationX + barrier_width
        check_x_2 = startingShell[0] >= barrierLocationX

        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight


        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("Last shell:", startingShell[0], startingShell[1])
            hit_x = int(startingShell[0])
            hit_y = int(startingShell[1])
            print ("Impact:",hit_x,hit_y)
            explosion(hit_x , hit_y)
            fire = False

        pygame.display.update()
        clock.tick(100)
    return damage

def power(level):
    text = smallfont.render("Power: " + str(level) + "%", True, black)
    gameDisplay.blit(text,[display_width / 2, 0])

def health_bars(player_health, enemy_health):
    if player_health > 75:
        player_health_color = green
    elif player_health > 50:
        player_health_color = yellow
    else:
        player_health_color = red

    if enemy_health > 75:
        enemy_health_color = green
    elif enemy_health > 50:
        enemy_health_color = yellow
    else:
        enemy_health_color = red

    pygame.draw.rect(gameDisplay, player_health_color, (680,25,player_health,25))
    pygame.draw.rect(gameDisplay, enemy_health_color, (20, 25, enemy_health, 25))

def gameLoop():
    gameExit = False
    gameOver = False

    player_health = 100
    enemy_health = 100


    mainTankX = display_width * 0.9
    mainTankY = display_height * 0.9
    tankMove = 0
    currentTurretPos = 0
    changeTurretPos = 0

    enemyTankX = display_width * 0.1
    enemyTankY = display_height * 0.9

    fire_power = 50
    power_change = 0

    barrierLocationX = (display_width /2) + random.randint(-0.2*display_width,.2*display_width)
    randomHeight = random.randrange(display_height * 0.1, display_height * 0.6)
    barrier_width = 40

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
                    tankMove = -5
                elif event.key == pygame.K_RIGHT:
                    tankMove = 5
                elif event.key == pygame.K_UP:
                    changeTurretPos = 1
                elif event.key == pygame.K_DOWN:
                    changeTurretPos = -1
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_SPACE:
                    damage = fireShell(gun,mainTankX,mainTankY,currentTurretPos,fire_power,barrierLocationX,barrier_width,randomHeight,enemyTankX,enemyTankY)
                    enemy_health -= damage

                    damage = eFireShell(enemy_gun, enemyTankX, enemyTankY, 8, 50, barrierLocationX, barrier_width,
                              randomHeight,mainTankX,mainTankY)
                    player_health -= damage

                elif event.key == pygame.K_a:
                    power_change = -1
                elif event.key == pygame.K_d:
                    power_change = 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankMove = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTurretPos = 0

                if event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0

        mainTankX += tankMove

        currentTurretPos += changeTurretPos

        if currentTurretPos > 8:
            currentTurretPos = 8
        elif currentTurretPos < 0:
            currentTurretPos = 0

        if mainTankX - (tankWidth / 2) < barrierLocationX + barrier_width:
            mainTankX += 5

        # clear the display
        gameDisplay.fill(white)
        health_bars(player_health,enemy_health)

        # draw the tank and store the position of the turret
        gun = tank(mainTankX, mainTankY, currentTurretPos)
        enemy_gun = enemy_tank(enemyTankX,enemyTankY,8)

        fire_power += power_change
        power(fire_power)

        barrier(barrierLocationX, randomHeight, barrier_width)

        #draw the ground over the barrier
        gameDisplay.fill(green, rect=[0,display_height-ground_height, display_width,ground_height])

        pygame.display.update()


        #frames per second (fps)
        #to affect game difficulty always change movement variables first before tinkering with fps
        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
gameLoop()