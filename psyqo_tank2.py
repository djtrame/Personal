import pygame
import random

pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
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

difficulties = ["Easy", "Medium", "Hard"]
difficulty_selected = 0

ground_height = 35

gameDisplay = pygame.display.set_mode((display_width,display_height))

#pygame doesn't seem to like files over 500kb ??
fire_sound = pygame.mixer.Sound("boom.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

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
inGameOverMenu = False
inWinningMenu = False

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

    #offset of first wheel drawing
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
    global difficulty_selected
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
                if event.key == pygame.K_1:
                    difficulty_selected = 0
                if event.key == pygame.K_2:
                    difficulty_selected = 1
                if event.key == pygame.K_3:
                    difficulty_selected = 2

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
        message_to_screen("Press 1 for Easy, 2 for Medium and 3 for Hard Difficulty",
                          black,
                          y_displace=50,
                          size="small")
        # message_to_screen("Press C to play, P to pause or Q to quit...",
        #                   black,
        #                   y_displace=180,
        #                   size="small")

        message_to_screen("Difficulty Selected = " + difficulties[difficulty_selected],
                          black,
                          y_displace=90,
                          size="small")

        createButton("Play", 150,500,110,50,darkgreen, green, action="play")
        createButton("Controls", 350, 500, 110, 50, yellow, lightyellow, action="controls")
        createButton("Quit", 550, 500, 110, 50, red, lightred, action="quit")


        pygame.display.update()
        clock.tick(15)

def game_over():
    global inGameOverMenu
    global difficulty_selected
    inGameOverMenu = True

    while inGameOverMenu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty_selected = 0
                if event.key == pygame.K_2:
                    difficulty_selected = 1
                if event.key == pygame.K_3:
                    difficulty_selected = 2

        gameDisplay.fill(white)
        message_to_screen("Game Over!",
                          green,
                          y_displace=-100,
                          size="medium")
        message_to_screen("You died!",
                          black,
                          y_displace=-30,
                          size="small")
        message_to_screen("Press 1 for Easy, 2 for Medium and 3 for Hard Difficulty",
                          black,
                          y_displace=50,
                          size="small")

        message_to_screen("Difficulty Selected = " + difficulties[difficulty_selected],
                          black,
                          y_displace=90,
                          size="small")


        createButton("Play Again", 150,500,150,50,darkgreen, green, action="play")
        createButton("Controls", 350, 500, 110, 50, yellow, lightyellow, action="controls")
        createButton("Quit", 550, 500, 110, 50, red, lightred, action="quit")


        pygame.display.update()
        clock.tick(15)

def winning_menu():
    global inWinningMenu
    global difficulty_selected
    inWinningMenu = True

    while inWinningMenu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty_selected = 0
                if event.key == pygame.K_2:
                    difficulty_selected = 1
                if event.key == pygame.K_3:
                    difficulty_selected = 2

        gameDisplay.fill(white)
        message_to_screen("You won!",
                          green,
                          y_displace=-100,
                          size="medium")
        message_to_screen("Congrats!",
                          black,
                          y_displace=-30,
                          size="small")
        message_to_screen("Press 1 for Easy, 2 for Medium and 3 for Hard Difficulty",
                          black,
                          y_displace=50,
                          size="small")

        message_to_screen("Difficulty Selected = " + difficulties[difficulty_selected],
                          black,
                          y_displace=90,
                          size="small")


        createButton("Play Again", 150,500,150,50,darkgreen, green, action="play")
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

def barrier(barrierLocationX, randomHeight, barrier_width):
    pygame.draw.rect(gameDisplay, black, [barrierLocationX, display_height-randomHeight, barrier_width, randomHeight])

def explosion(x,y, size=50):
    pygame.mixer.Sound.play(explosion_sound)
    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        startPoint = x,y

        colorChoices = [red, lightred, yellow, lightyellow]

        magnitude = 1

        #draw random sized circles of random color that get bigger and bigger up to 50 pixels
        while magnitude < size:
            exploding_bit_x = x + random.randrange(-1*magnitude,magnitude)
            exploding_bit_y = y + random.randrange(-1 * magnitude, magnitude)

            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0,4)], (exploding_bit_x,exploding_bit_y),random.randrange(1,5))
            magnitude += 1

            pygame.display.update()
            clock.tick(100)

        explode = False


def fireShell(gunCoordinates, tankX, tankY, turretPos,gun_power,barrierLocationX,barrier_width,randomHeight,enemyTankX,enemyTankY):
    pygame.mixer.Sound.play(fire_sound)
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

        #our tank is firing left so subtract from the x coordinate each frame
        startingShellXAdjustment = (12 - turretPos) * 2
        startingShell[0] -= startingShellXAdjustment

        turretPosAdjustment = turretPos + turretPos/(12-turretPos)

        #quadratic equation example
        #y = x^2  y = x**2
        startingShellYAdjustment = int((((startingShell[0] - gunCoordinates[0])*0.01/(gun_power/50))**2) - turretPosAdjustment)
        startingShell[1] += startingShellYAdjustment

        # print("---------------------------------")
        # print("StartingShell X Adjustment: " + str(startingShellXAdjustment))
        # print("StartingShell X: " + str(startingShell[0]))
        # print("TurretPosAdjustment: " + str(turretPosAdjustment))
        # print("gunCoordinates X: " + str(gunCoordinates[0]))
        # print("StartingShell Y Adjustment: " + str(startingShellYAdjustment))
        # print("StartingShell Y: " + str(startingShell[1]))

        actual_ground = display_height - ground_height

        #if the shell has hit the ground
        if startingShell[1] > actual_ground:
            #print("Last shell:",startingShell[0],startingShell[1])
            #determine estimated spot of last impact
            #cross multiplication
            #(x/600) = (189/618) for instance
            #618x = (600 * 189)
            #x = (113,400) / 618
            #x = 183 <------ estimated last X of impact (when the shell hit the border at 600)
            hit_x = int((startingShell[0]*actual_ground)/startingShell[1])
            hit_y = int(actual_ground)
            if enemyTankX + 10 > hit_x  > enemyTankX - 10:
                print("Player CRITICALLY HIT TARGET!")
                damage = 25
            elif enemyTankX + 15 > hit_x  > enemyTankX - 15:
                print("Player Hard HIT TARGET!")
                damage = 18
            elif enemyTankX + 25 > hit_x  > enemyTankX - 25:
                print("Player Medium HIT TARGET!")
                damage = 10
            elif enemyTankX + 35 > hit_x  > enemyTankX - 35:
                print("Player Light HIT TARGET!")
                damage = 5

            #print ("Impact:",hit_x,hit_y)
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

#simulate a shot many times until the CPU finds the right target
#then randomize that power level so it doesn't always hit
#another path to CPU behavior is to have it take a shot, then measure whether it was short or long and adjust accordingly
def eFireShell(gunCoordinates, tankX, tankY, turretPos,gun_power,barrierLocationX,barrier_width,barrierHeight,pTankX,pTankY):
    pygame.mixer.Sound.play(fire_sound)
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

                #if the shell hits 10 pixels to the left or right of the tank
                if pTankX + 10 > hit_x > pTankX - 10:
                    #print("target acquired!")
                    power_found = True
                fire = False

            # do comparisons and store them as booleans
            check_x_1 = startingShell[0] <= barrierLocationX + barrier_width
            check_x_2 = startingShell[0] >= barrierLocationX

            check_y_1 = startingShell[1] <= display_height
            check_y_2 = startingShell[1] >= display_height - barrierHeight

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int(startingShell[0])
                hit_y = int(startingShell[1])
                fire = False

    fire = True

    #can't modify tuples, convert it to a list instead
    startingShell = list(gunCoordinates)
    #print("FIRE!")

    #this is where the enemy tank difficulty comes in
    #give a random factor to the shot after it has "found its mark" in the loop above
    #a dumber tank gets a higher randomness, a better tank gets a lower
    randomPowerRange = 0.0001

    if difficulties[difficulty_selected] == "Easy":
        randomPowerRange = 0.2
    elif difficulties[difficulty_selected] == "Medium":
        randomPowerRange = 0.1
    elif difficulties[difficulty_selected] == "Hard":
        randomPowerRange = 0.05

    randomized_power = random.randrange(int(currentPower * (1-randomPowerRange)), int(currentPower * (1+randomPowerRange)))
    randomized_power += 1


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
        startingShell[1] += int((((startingShell[0] - gunCoordinates[0])*0.01/(randomized_power/50))**2) - (turretPos + turretPos/(12-turretPos)))

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
            if pTankX + 10 > hit_x  > pTankX - 10:
                print("CPU CRITICALLY HIT TARGET!")
                damage = 25
            elif pTankX + 15 > hit_x  > pTankX - 15:
                print("CPU Hard HIT TARGET!")
                damage = 18
            elif pTankX + 25 > hit_x  > pTankX - 25:
                print("CPU Medium HIT TARGET!")
                damage = 10
            elif pTankX + 35 > hit_x  > pTankX - 35:
                print("CPU Light HIT TARGET!")
                damage = 5

            explosion(hit_x , hit_y)
            fire = False

        #do comparisons and store them as booleans
        check_x_1 = startingShell[0] <= barrierLocationX + barrier_width
        check_x_2 = startingShell[0] >= barrierLocationX

        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - barrierHeight


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

def checkWinner(pHealth, eHealth):
    if pHealth < 1:
        game_over()
    elif eHealth < 1:
        winning_menu()

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

    #create randomized starting locations
    #enemyTankX = display_width * 0.1
    enemyTankX = display_width * (random.randint(1,35)/100)
    enemyTankY = display_height * 0.9

    fire_power = 50
    power_change = 0

    barrierLocationX = (display_width /2) + random.randint(-0.1*display_width,.1*display_width)
    barrierHeight = random.randrange(display_height * 0.1, display_height * 0.4)
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
                    #player fires
                    damage = fireShell(gun,mainTankX,mainTankY,currentTurretPos,fire_power,barrierLocationX,barrier_width,barrierHeight,enemyTankX,enemyTankY)
                    enemy_health -= damage
                    checkWinner(player_health,enemy_health)

                    #move the enemy tank after we fire
                    possibleMovement = ['f','r']
                    moveIndex = random.randrange(0,2)
                    eTankRightBoundary = display_width * 0.4
                    eTankLeftBoundary = 16

                    #randomize how far the tank moves
                    for x in range(random.randrange(0,10)):
                        #if the left edge of the tank is to the left of 320 pixels and if the tank is to the right of 32 pixels then move it
                        #if eTankRightBoundary > enemyTankX > eTankLeftBoundary:
                        if possibleMovement[moveIndex] == "f":
                            #if the tank has gone too far forward
                            if enemyTankX >= eTankRightBoundary:
                                enemyTankX -= 10
                                moveIndex = 1
                            else:
                                enemyTankX += 10
                        elif possibleMovement[moveIndex] == "r":
                            #if the tank has gone too far backward
                            if enemyTankX <= eTankLeftBoundary:
                                enemyTankX += 10
                                moveIndex = 0
                            else:
                                enemyTankX -= 10

                        # clear the display
                        gameDisplay.fill(white)
                        health_bars(player_health, enemy_health)

                        # draw the tank and store the position of the turret
                        gun = tank(mainTankX, mainTankY, currentTurretPos)
                        enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)

                        barrier(barrierLocationX, barrierHeight, barrier_width)

                        # draw the ground over the barrier
                        gameDisplay.fill(green,
                                         rect=[0, display_height - ground_height, display_width, ground_height])

                        pygame.display.update()
                        clock.tick(FPS)


                    #cpu fires
                    damage = eFireShell(enemy_gun, enemyTankX, enemyTankY, 8, 50, barrierLocationX, barrier_width,barrierHeight,mainTankX,mainTankY)
                    player_health -= damage
                    checkWinner(player_health, enemy_health)

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

        if fire_power > 100:
            fire_power = 100
        elif fire_power < 1:
            fire_power = 1

        power(fire_power)

        barrier(barrierLocationX, barrierHeight, barrier_width)

        #draw the ground over the barrier
        gameDisplay.fill(green, rect=[0,display_height-ground_height, display_width,ground_height])

        pygame.display.update()

        #frames per second (fps)
        #to affect game difficulty always change movement variables first before tinkering with fps
        clock.tick(FPS)

    pygame.quit()
    quit()

#game_over()
#winning_menu()
game_intro()
gameLoop()