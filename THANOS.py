import pygame
import time
import random
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 4096)

pygame.mixer.init()
pygame.init()

# loads up all the images into the variables

boat = pygame.image.load("Boat Background.png")
bossbg = pygame.image.load("Bossback.png")

bulletSound = pygame.mixer.Sound("Bullet Sound.wav")
music = pygame.mixer.music.load("Halotheme1.wav")
pygame.mixer.music.play(-1)

smallText = pygame.font.Font("freesansbold.ttf", 20)
img = pygame.image.load('skullwall.jpeg')

keyboard = pygame.image.load("Keyboard.png")

intermission = pygame.image.load("intermission.png")

win = pygame.display.set_mode((1250,720))
pygame.display.set_caption("Game ting")
gameoverscreen = pygame.image.load("GAMEOVER.png")
finalwinscreen1 = pygame.image.load("FinalBg.jpg")


goldmedal = pygame.image.load("Gold_Medal.png")
silvermedal = pygame.image.load("Silver_Medal.png")
bronzemedal = pygame.image.load("Bronze_Medal.png")

import sys

# colour variables



Black=(0,0,0)
White = (255,255,255)
Green = (0,255,0)
Red = (200,0,0)
Purple = (128,0,128)
Bright_Red= (255,0,0)
Bright_Green = (0,255,0)


#images for the sprites

walkRight = [pygame.image.load('PL1 copy 2.png'), pygame.image.load('PL2 copy 2.png'),pygame.image.load('PL3 copy 2.png'),
             pygame.image.load('PL4 copy 2.png'), pygame.image.load('PL5 copy 2.png'),pygame.image.load('PL6 copy 2.png'),
             pygame.image.load('PL7 copy 2.png'), pygame.image.load('PL8 copy 2.png'),pygame.image.load('PL9 copy 2.png'),
             pygame.image.load('PL10 copy 2.png'),pygame.image.load('PL11 copy 2.png'),pygame.image.load('PL12 copy 2.png')]
walkLeft = [pygame.image.load('PL1 copy.png'), pygame.image.load('PL2 copy.png'), pygame.image.load('PL3 copy.png'),
            pygame.image.load('PL4 copy.png'), pygame.image.load('PL5 copy.png'), pygame.image.load('PL6 copy.png'),
            pygame.image.load('PL7 copy.png'), pygame.image.load('PL8 copy.png'), pygame.image.load('PL9 copy.png'),
            pygame.image.load('PL10 copy.png'),pygame.image.load('PL11 copy.png'),pygame.image.load('PL12 copy.png')]

background_level2 = pygame.image.load("Battleground2 copy.png")

clock=pygame.time.Clock()


def text_objects(text, font):
    textSurface = font.render(text, True, Black)
    return textSurface, textSurface.get_rect()

#class for the player, This makes the code easeier to navigate

class player(object):
    def __init__ (self,x,y,width,height):
        self.x=x
        self.y= y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x, self.y, 31, 52)
        self.health = 15

        #this draws the frames of the character
    def draw(self, win):
        if self.walkCount + 1 >= 36:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))


        #health bar
        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
        self.hitbox = (self.x , self.y, 31, 52)
        #hitbox
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


    #if the player is hit, -5 of his health

    def hit(self):
        if self.health >0:
            self.health -=5
        pygame.display.update()

#class for the BigEnemy (BULL)

class BigEnemy(object):
    walkRight = [pygame.image.load('BER1.png'), pygame.image.load('BER2.png'), pygame.image.load('BER3.png')]
    walkLeft = [pygame.image.load('BEL1.png'), pygame.image.load('BEL2.png'), pygame.image.load('BEL3.png')]

    def __init__(self,x,y,width,height,end,vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = vel
        self.hitbox = (self.x +4, self.y, 90, 106)
        self.health = 20
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:

            if self.walkCount + 1 >= 9:#frames
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount +=1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            #health bar
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 100, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

            self.hitbox = (self.x + 4, self.y, 90, 106)
            #hitbox
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel*-1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
    def hit(self):
        if self.health>0:
            self.health -=1
        else:
            self.visible =False
        print("Hit")

class BossEnemey(object):
    walkRight = [pygame.image.load('BossR1.png'), pygame.image.load('BossR2.png'), pygame.image.load('BossR3.png'),
                 pygame.image.load('BossR4.png'), pygame.image.load('BossR5.png'), pygame.image.load('BossR6.png'),
                 pygame.image.load('BossR7.png'), pygame.image.load('BossR8.png')]


    walkLeft = [pygame.image.load('BossL1.png'), pygame.image.load('BossL2.png'), pygame.image.load('BossL3.png'),
                pygame.image.load('BossL4.png'), pygame.image.load('BossL5.png'), pygame.image.load('BossL6.png'),
                pygame.image.load('BossL7.png'), pygame.image.load('BossL8.png')]

    def __init__(self,x,y,width,height,pathend,vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pathend = pathend
        self.path = [self.x, self.pathend]
        self.walkCount = 0
        self.vel = vel
        self.hitbox = (self.x, self.y, 300, 350)
        self.health = 75
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:

            if self.walkCount + 1 >= 24:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount +=1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 356, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

            self.hitbox = (self.x + 4, self.y, 300, 350)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel*-1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
    def hit(self):
        if self.health>0:
            self.health -=1
        else:
            self.visible =False
            #self.pop = True
        print("Hit")

class horseenemy(object):
    walkRight = [pygame.image.load('BKR1.png'), pygame.image.load('BKR2.png'), pygame.image.load('BKR3.png'),
                 pygame.image.load('BKR4.png'), pygame.image.load('BKR5.png'), pygame.image.load('BKR6.png'),
                 pygame.image.load('BKR7.png'), pygame.image.load('BKR8.png'), pygame.image.load('BKR9.png'),
                 pygame.image.load('BKR10.png'),pygame.image.load('BKR11.png'),pygame.image.load('BKR12.png')]


    walkLeft = [pygame.image.load('BKL1.png'), pygame.image.load('BKL2.png'), pygame.image.load('BKL3.png'),
                pygame.image.load('BKL4.png'), pygame.image.load('BkL5.png'), pygame.image.load('BkL6.png'),
                pygame.image.load('BKL7.png'), pygame.image.load('BKL8.png'), pygame.image.load('BKL9.png'),
                pygame.image.load('BKL10.png'),pygame.image.load('BKL11.png'),pygame.image.load('BKL12.png')]

    def __init__(self,x,y,width,height,pathend,vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pathend = pathend
        self.path = [self.x, self.pathend]
        self.walkCount = 0
        self.vel = vel
        self.hitbox = (self.x +4, self.y, 50, 100)
        self.health = 50
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:

            if self.walkCount + 1 >= 36:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount +=1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 250, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

            self.hitbox = (self.x + 4, self.y, 50, 100)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel*-1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
    def hit(self):
        if self.health>0:
            self.health -=1
        else:
            self.visible =False
            #self.pop = True
        print("Hit")


class enemy(object):
    walkRight = [pygame.image.load('ER1.png'), pygame.image.load('ER2.png'), pygame.image.load('ER3.png'),
                 pygame.image.load('ER4.png'), pygame.image.load('ER5.png'), pygame.image.load('ER6.png'),
                 pygame.image.load('ER7.png'), pygame.image.load('ER8.png'), pygame.image.load('ER9.png')]
    walkLeft = [pygame.image.load('EL1.png'), pygame.image.load('EL2.png'), pygame.image.load('EL3.png'),
                pygame.image.load('EL4.png'), pygame.image.load('EL5.png'), pygame.image.load('EL6.png'),
                pygame.image.load('EL7.png'), pygame.image.load('EL8.png'), pygame.image.load('EL9.png')]

    def __init__(self,x,y,width,height,end,vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.end, self.x]
        self.walkCount = 0
        self.vel = vel
        self.hitbox = (self.x +4, self.y, 32, 52)
        self.health = 10
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:

            if self.walkCount + 1 >= 27:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount +=1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

            self.hitbox = (self.x + 4, self.y, 32, 52)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel*-1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
    def hit(self):
        if self.health>0:
            self.health -=1
        else:
            self.visible =False
            #self.pop = True
        print("Hit")

class projectile(object):
    def __init__ (self,x,y,radius,colour,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.colour=colour
        self.facing=facing
        self.vel=12 * facing
    def draw(self,win):
        pygame.draw.circle(win,self.colour,(self.x,self.y), self.radius)


#button function
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(mouse)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(win, ac, (x, y, w, h))
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        win.blit(textSurf, textRect)
        if click[0] == 1 and action != None:
            if action == "Start":
                story_screen()
            elif action == "Quit":
                pygame.quit()
                quit()
            elif action == "Back":
                story_screen()
            elif action == "Home":
                game_intro()
            elif action == 'Go':
                level_1()
            elif action == " ":
                controlscreen()

    else:
        pygame.draw.rect(win, ic, (x, y, w, h))
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        win.blit(textSurf, textRect)

#screen for controls
def controlscreen():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        win.fill(White)
        win.blit(keyboard,(275,100))
        button("Home", 1120, 30, 100, 50, White, Bright_Red, "Home")

        storyfont = pygame.font.SysFont("returnofganonregular", 45)
        storytextsurface = storyfont.render("Press W to Jump", False, Black)
        win.blit(storytextsurface, (625 - (storytextsurface.get_width() / 2), 375))

        storytextsurface = storyfont.render("Press A and D to Move", False, Black)
        win.blit(storytextsurface, (625 - (storytextsurface.get_width() / 2), 425))

        storytextsurface = storyfont.render("Press SPACE to Shoot", False, Black)
        win.blit(storytextsurface, (625 - (storytextsurface.get_width() / 2), 475))

        storytextsurface = storyfont.render("EASY Mode makes You faster, and the Enemies Slower.", False, Black)
        win.blit(storytextsurface, (625 - (storytextsurface.get_width() / 2), 525))

        storytextsurface = storyfont.render("HARD Mode makes You Slower, and the Enemies Faster.", False, Black)
        win.blit(storytextsurface, (625 - (storytextsurface.get_width() / 2), 575))

        pygame.display.update()


#first screen when you load up
def game_intro():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        win.fill(Black)

        win.blit(img, (0,0))

        myfont = pygame.font.SysFont('comicsans', 75)
        textsurface = myfont.render('THE', False, (255, 255, 255))
        win.blit(textsurface, (450, 43))

        myfont = pygame.font.SysFont('comicsans', 100)
        textsurface = myfont.render('PUNISHER', False, (255, 255, 255))
        win.blit(textsurface, (450, 100))

        #buttons for the start of the game, quit, and controls
        button("Start",562,250,225,100,White,Bright_Green, "Start")
        button("Quit",562,375,225,100,White,Bright_Red, "Quit")
        button(" ",437,250,100,225, White,Purple, " " )

        #rotating text for the control button
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render("Controls", True, Black)
        text = pygame.transform.rotate(text, 90)
        win.blit(text, (487 - (text.get_width() / 2), 330))

        pygame.display.update()

score= 0


#print(pygame.font.get_fonts())
#retganonttf

#screen after the game loop
def story_screen():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        win.fill(Black)
        win.blit(intermission ,(0,0))
        #win.blit(Round1_Screen ,(184,50) )

        storyfont = pygame.font.SysFont("returnofganonregular", 60)
        storytextsurface = storyfont.render("Press Space to Start", False, Black)
        win.blit(storytextsurface, (625 - (storytextsurface.get_width() / 2), 375 ))

        storytextsurface = storyfont.render("Fight your way to Defeat Kurse; the Dark Elf.", False, Black)
        win.blit(storytextsurface, (625 - (storytextsurface.get_width() / 2), 200))


        storyfont1 = pygame.font.SysFont("returnofganonregular", 45)
        storytextsurface1 = storyfont1.render("Press H to Activate EASY mode", False, Black)
        win.blit(storytextsurface1, (625 - (storytextsurface1.get_width() / 2), 250))

        storytextsurface1 = storyfont1.render("Press J to Activate HARD mode", False, Black)
        win.blit(storytextsurface1, (625 - (storytextsurface1.get_width() / 2), 300))

        #press space to start
        if keys[pygame.K_SPACE]:
            level_1()

        #easy mode - This changes the player's velocity, and the enemies velocity
        if keys[pygame.K_h]:
            Punish.vel = 15
            BigBoi.vel = 15
            Skeleton.vel = 15
            BlackKnight.vel = 15
            Boss.vel = 1
        #hard mode - PLayer is slower and enemy is faster
        if keys[pygame.K_j]:
            Punish.vel = 5
            BigBoi.vel = 20
            Skeleton.vel = 20
            BlackKnight.vel = 35
            Boss.vel = 2

        pygame.display.update()


########################################################################################################################
#classes - Turning them into variables with sizes, velocity
Punish = player(625,535,64,64)
Skeleton = enemy(1200,570, 64,64, 100,20)
BigBoi = BigEnemy(100,510,98,106,1200,20)
BlackKnight = horseenemy (100,525,80,98,1200,35)
Boss = BossEnemey(1,250,80,98,1200,2)
bullets = []
scorefont = pygame.font.SysFont("comicsans", 50)

########################################################################################################################

#LEVEL 1
def level_1():
    shootloop = 0
    run = False
    gameOver = False
    while not run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        global score
        while gameOver == True:
            win.blit(gameoverscreen, (0, 0))
            font1 = pygame.font.SysFont('returnofganonregular', 50)
            text = font1.render('Press q to quit, Press r to Restart', 1, White)
            win.blit(text, (625 - (text.get_width() / 2), 500))
            pygame.display.update()
            #if player is dead, and r key is pressed, reset everything - PLayer health, enemy, x and y positions, etc.
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_r:
                        Punish.isJump = False
                        Punish.jumpCount = 10
                        Punish.health = 15
                        Punish.x = 625
                        Punish.y = 535
                        Skeleton.x = 1200
                        Skeleton.y =570
                        Skeleton.health =10
                        BigBoi.x = 100
                        BigBoi.y = 510
                        BigBoi.health = 20
                        score=0
                        level_1()
        if Punish.health == 0:
            gameOver =True
        #if player health is = to 0, run the while loop

        #this draws the buttons ,the score, the player and enemies, and the bullets.
        keys = pygame.key.get_pressed()
        win.blit(boat, (0, 0))
        text = scorefont.render("Score: " + str(score), False, White)
        win.blit(text, (625 - (text.get_width() / 2), 10))
        button("Back", 1120, 30, 100, 50, White, Bright_Red, "Back")
        button("Home", 1120, 90, 100, 50, White, Bright_Green, "Home")
        Punish.draw(win)
        Skeleton.draw(win)
        BigBoi.draw(win)
        for bullet in bullets:
            bullet.draw(win)


        #if both enemies are dead, draw the intermission screen, and load up the next level
        if BigBoi.visible == False and Skeleton.visible == False:
            win.blit(intermission, (0, 0))
            #win.blit(Round2_Screen, (229, 176))
            keys = pygame.key.get_pressed()

            font1 = pygame.font.SysFont('returnofganonregular', 50)
            text = font1.render('Round 1 Completed', 1, Black)
            win.blit(text, (625 - (text.get_width() / 2), 200))
            text1 = font1.render("Press g to Fight!", 1, Black)

            win.blit(text1, (625 - (text1.get_width() / 2), 300))
            text1 = font1.render("The Black Knight Awaits...", 1, Black)

            win.blit(text1, (625 - (text1.get_width() / 2), 250))

            Punish.isJump = False
            Punish.jumpCount = 10
            Punish.x = 625
            Punish.y = 535

            if keys[pygame.K_g]:
                level_2() # level 2
            pygame.display.update()

        #if the player colliedes with the skeleton, -5 score
        if Skeleton.visible == True:
            if Punish.hitbox[1] < Skeleton.hitbox[1] + Skeleton.hitbox[3] and Punish.hitbox[1] + Punish.hitbox[3] > Skeleton.hitbox[1]:
                if Punish.hitbox[0] + Punish.hitbox[2] > Skeleton.hitbox[0] and Punish.hitbox[0] < Skeleton.hitbox[0] + Skeleton.hitbox[2]:
                    Punish.hit()
                    score -= 5
        # if player collides with bull, - 10 score
        if BigBoi.visible == True:
            if Punish.hitbox[1] < BigBoi.hitbox[1] + BigBoi.hitbox[3] and Punish.hitbox[1] + Punish.hitbox[3] > BigBoi.hitbox[1]:
                if Punish.hitbox[0] + Punish.hitbox[2] > BigBoi.hitbox[0] and Punish.hitbox[0] < BigBoi.hitbox[0] + BigBoi.hitbox[2]:
                    Punish.hit()
                    score -= 10

        #this is so the bullets dont stack on each other, this seperates them
        clock.tick(27)
        if shootloop > 0:
            shootloop +=1
        if shootloop > 3:
            shootloop =0

        #if the bullets collide with the enemies, +3 score
        for bullet in bullets:
            if Skeleton.visible == True:
                if bullet.y - bullet.radius < Skeleton.hitbox[1] + Skeleton.hitbox[3] and bullet.y + bullet.radius > Skeleton.hitbox[1]:
                    if bullet.x + bullet.radius > Skeleton.hitbox[0] and bullet.x - bullet.radius<Skeleton.hitbox[0] + Skeleton.hitbox[2]:
                        Skeleton.hit()
                        score += 3
                        bullets.pop(bullets.index(bullet)) #then remove bullets once they collided

            #if they go out of bounds, remove them
            if bullet.x < 1250 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

            #if bullets collide with the bull, +1 score
            if BigBoi.visible == True:
                if bullet.y - bullet.radius < BigBoi.hitbox[1] + BigBoi.hitbox[3] and bullet.y + bullet.radius > BigBoi.hitbox[1]:
                    if bullet.x + bullet.radius > BigBoi.hitbox[0] and bullet.x - bullet.radius<BigBoi.hitbox[0] + BigBoi.hitbox[2]:
                        BigBoi.hit()
                        score += 1
                        bullets.pop(bullets.index(bullet))

            # if bullets collides with both enemies at the same time, remove bullets
            if BigBoi.visible == True and Skeleton.visible == True:
                if bullet.y - bullet.radius < Skeleton.hitbox[1] + Skeleton.hitbox[3] and bullet.y + bullet.radius >Skeleton.hitbox[1]:
                    if bullet.x + bullet.radius > Skeleton.hitbox[0] and bullet.x - bullet.radius < Skeleton.hitbox[0] + Skeleton.hitbox[2]:
                        if bullet.y - bullet.radius < BigBoi.hitbox[1] + BigBoi.hitbox[3] and bullet.y + bullet.radius > BigBoi.hitbox[1]:
                            if bullet.x + bullet.radius > BigBoi.hitbox[0] and bullet.x - bullet.radius < BigBoi.hitbox[0] + BigBoi.hitbox[2]:
                                bullets.pop(bullets.index(bullet))


        #shoot with space
        if keys[pygame.K_SPACE] and shootloop == 0:
            bulletSound.play()
            if Punish.left:
                facing = - 1
            else:
                facing = 1
            if len(bullets) < 10:
                bullets.append(projectile(round(Punish.x + Punish.width//2), round(Punish.y + Punish.height//2), 4, (0,0,0), facing))
            shootloop = 1
        #move left
        if keys[pygame.K_a] and Punish.x > Punish.vel:
            Punish.x -= Punish.vel
            Punish.left=True
            Punish.right=False
            Punish.standing = False
        #move right
        elif keys[pygame.K_d] and Punish.x < 1250 -Punish.vel - Punish.width:
            Punish.x += Punish.vel
            Punish.left=False
            Punish.right=True
            Punish.standing = False
        else:
            Punish.standing = True
            Punish.walkCount= 0

        #jumping with w
        if not(Punish.isJump):
            if keys[pygame.K_w]:
                Punish.isJump = True
                Punish.right = False
                Punish.left = False
                Punish.walkCount = 0
        else:
            if Punish.jumpCount >= -10:
                Punish.y -= (Punish.jumpCount * abs(Punish.jumpCount)) * 0.5
                Punish.jumpCount -= 1
            else:
                Punish.jumpCount = 10
                Punish.isJump = False


        pygame.display.update()
        #redrawGameWindow()

########################################################################################################################


def level_2():
    shootloop = 0
    run = False
    gameOver=False
    while not run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        global score
        while gameOver == True:
            win.blit(gameoverscreen, (0, 0))
            win.blit(gameoverscreen, (0, 0))
            font1 = pygame.font.SysFont('returnofganonregular', 50)
            text = font1.render('Press q to quit, Press r to Restart', 1, White)
            win.blit(text, (625 - (text.get_width() / 2), 500))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_r:
                        Punish.isJump = False
                        Punish.jumpCount = 10
                        Punish.health = 15
                        Punish.x = 625
                        Punish.y = 535
                        BlackKnight.x = 100
                        BlackKnight.y = 525
                        BlackKnight.health = 50
                        score=0
                        level_2()
        #if player is dead, and player presses r, reset everyhthing and run the function again

        if Punish.health == 0:
            gameOver =True

        keys = pygame.key.get_pressed()
        win.blit(background_level2, (0, 0))
        text = scorefont.render("Score: " + str(score), False, White)
        win.blit(text, (625 - (text.get_width() / 2), 10))
        button("Back", 1120, 30, 100, 50, White, Bright_Red, "Back")
        button("Home", 1120, 90, 100, 50, White, Bright_Green, "Home")
        Punish.draw(win)
        BlackKnight.draw(win)
        for bullet in bullets:
            bullet.draw(win)

        #if enemy is dead, go on to the final level
        if BlackKnight.visible == False:
            win.blit(intermission, (0, 0))
            #win.blit(intermission, (178, 217))
            keys = pygame.key.get_pressed()
            font1 = pygame.font.SysFont('returnofganonregular', 50)
            text = font1.render('Round 2 Completed', 1, Black)
            win.blit(text, (625 - (text.get_width() / 2), 200))
            text1 = font1.render("Press g to Fight!", 1, Black)

            win.blit(text1, (625 - (text1.get_width() / 2), 300))
            text1 = font1.render("You Approach the Final Temple... Kurse Awaits your presence...", 1, Black)
            win.blit(text1, (625 - (text1.get_width() / 2), 250))

            Punish.isJump = False
            Punish.jumpCount = 10
            Punish.x = 625
            Punish.y = 535

            if keys[pygame.K_g]:
                level_3()
            pygame.display.update()

        #if player collides with enenmy, -10 score
        if BlackKnight.visible == True:
            if Punish.hitbox[1] < BlackKnight.hitbox[1] + BlackKnight.hitbox[3] and Punish.hitbox[1] + Punish.hitbox[3] > BlackKnight.hitbox[1]:
                if Punish.hitbox[0] + Punish.hitbox[2] > BlackKnight.hitbox[0] and Punish.hitbox[0] < BlackKnight.hitbox[0] + BlackKnight.hitbox[2]:
                    Punish.hit()
                    score -= 10

        clock.tick(27)
        if shootloop > 0:
            shootloop +=1
        if shootloop > 3:
            shootloop =0

        #if bullets hit enenmy +3 score
        for bullet in bullets:
            if BlackKnight.visible == True:
                if bullet.y - bullet.radius < BlackKnight.hitbox[1] + BlackKnight.hitbox[3] and bullet.y + bullet.radius > BlackKnight.hitbox[1]:
                    if bullet.x + bullet.radius > BlackKnight.hitbox[0] and bullet.x - bullet.radius<BlackKnight.hitbox[0] + BlackKnight.hitbox[2]:
                        BlackKnight.hit()
                        score += 3
                        bullets.pop(bullets.index(bullet))

            #if out of bounds, remove bullets
            if bullet.x < 1250 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
        #shoot
        if keys[pygame.K_SPACE] and shootloop == 0:
            bulletSound.play()
            if Punish.left:
                facing = - 1
            else:
                facing = 1
            if len(bullets) < 10:
                bullets.append(projectile(round(Punish.x + Punish.width//2), round(Punish.y + Punish.height//2), 4, (0,0,0), facing))
            shootloop = 1
        #move left
        if keys[pygame.K_a] and Punish.x > Punish.vel:
            Punish.x -= Punish.vel
            Punish.left=True
            Punish.right=False
            Punish.standing = False
        #move right
        elif keys[pygame.K_d] and Punish.x < 1250 -Punish.vel - Punish.width:
            Punish.x += Punish.vel
            Punish.left=False
            Punish.right=True
            Punish.standing = False
        else:
            Punish.standing = True
            Punish.walkCount= 0
        #jump with w
        if not(Punish.isJump):
            if keys[pygame.K_w]:
                Punish.isJump = True
                Punish.right = False
                Punish.left = False
                Punish.walkCount = 0
        else:
            if Punish.jumpCount >= -10:
                Punish.y -= (Punish.jumpCount * abs(Punish.jumpCount)) * 0.5
                Punish.jumpCount -= 1
            else:
                Punish.jumpCount = 10
                Punish.isJump = False
        pygame.display.update()


########################################################################################################################


def level_3():
    shootloop = 0
    run = False
    gameOver = False
    while not run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        global score
        while gameOver == True:
            win.blit(gameoverscreen, (0, 0))
            win.blit(gameoverscreen, (0, 0))
            font1 = pygame.font.SysFont('returnofganonregular', 50)
            text = font1.render('Press q to quit, Press r to Restart', 1, White)
            win.blit(text, (625 - (text.get_width() / 2), 500))
            pygame.display.update()
            #if player dies, and presses r, reset all the positions, and health, and restart function
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_r:
                        Punish.isJump = False
                        Punish.jumpCount = 10
                        Punish.health = 15
                        Punish.x = 625
                        Punish.y = 535
                        Boss.x = 1
                        Boss.y = 250
                        Boss.health = 75
                        score=0
                        level_3()
        

        if Punish.health == 0:
            gameOver =True

        keys = pygame.key.get_pressed()
        win.blit(bossbg, (0, 0))
        text = scorefont.render("Score: " + str(score), False, (0, 0, 0))
        win.blit(text, (625 - (text.get_width() / 2), 10))
        button("Back", 1120, 30, 100, 50, White, Bright_Red, "Back")
        button("Home", 1120, 90, 100, 50, White, Bright_Green, "Home")
        Punish.draw(win)
        Boss.draw(win)
        for bullet in bullets:
            bullet.draw(win)

        # if player has killed the boss, display the final victory screen
        if Boss.visible == False:
            win.blit(finalwinscreen1, (0, 0))
            # pygame.draw.rect(win, White, (325,100,300,100))
            keys = pygame.key.get_pressed()
            pygame.draw.rect(win, Red, (440, 40, 370, 520))
            pygame.draw.rect(win, White, (450, 50, 350, 500,))

            font1 = pygame.font.SysFont('comicsans', 40)

            text = font1.render('VICTORY!', 1, Black)
            win.blit(text, (625 - (text.get_width() / 2), 100))

            text1 = font1.render("Press R to Play Again", 1, Black)
            win.blit(text1, (625 - (text1.get_width() / 2), 450))

            text1 = font1.render("Press Q to Quit", 1, Black)
            win.blit(text1, (625 - (text1.get_width() / 2), 500))

            text2 = scorefont.render("Score:" + str(score), 1, Black)
            win.blit(text2, (625 - (text.get_width() / 2), 400))

            #if the score is equal to or more than 400, give gold medal
            if score >= 400:
                win.blit(goldmedal, (542, 150))
            #if the score is equal to or more than 300 but less than 400, give silver medal
            if score >= 300 and score < 400:
                win.blit(silvermedal, (542, 150))
            #if score is equal to and more than 100, but less than 300, give bronze medal
            if score >= 100 and score < 300:
                win.blit(bronzemedal, (542, 150))
            #press q to quit
            if keys[pygame.K_q]:
                pygame.quit()
                quit()
            #restart - Reset health, positions, and restart
            if keys[pygame.K_r]:
                Punish.isJump = False
                Punish.jumpCount = 10
                Punish.health = 15
                Punish.x = 625
                Punish.y = 535

                Skeleton.visible = True
                Skeleton.x = 1200
                Skeleton.y = 570
                Skeleton.health = 10

                BigBoi.visible = True
                BigBoi.x = 100
                BigBoi.y = 510
                BigBoi.health = 20

                BlackKnight.visible = True
                BlackKnight.x = 100
                BlackKnight.y = 525
                BlackKnight.health = 50

                Boss.visible = True
                Boss.x = 1
                Boss.y = 250
                Boss.health = 75

                score = 0
                game_intro()
                story_screen()
                level_1()
                level_2()
                level_3()

            pygame.display.update()
        #boss colliding with player = -100 score
        if Boss.visible == True:
            if Punish.hitbox[1] < Boss.hitbox[1] + Boss.hitbox[3] and Punish.hitbox[1] + Punish.hitbox[3] > Boss.hitbox[1]:
                if Punish.hitbox[0] + Punish.hitbox[2] > Boss.hitbox[0] and Punish.hitbox[0] < Boss.hitbox[0] + Boss.hitbox[2]:
                    Punish.hit()
                    score -= 100

        clock.tick(27)
        if shootloop > 0:
            shootloop +=1
        if shootloop > 3:
            shootloop =0
        # if bullets collide with boss, +3 score
        for bullet in bullets:
            if Boss.visible == True:
                if bullet.y - bullet.radius < Boss.hitbox[1] + Boss.hitbox[3] and bullet.y + bullet.radius > Boss.hitbox[1]:
                    if bullet.x + bullet.radius > Boss.hitbox[0] and bullet.x - bullet.radius<Boss.hitbox[0] + Boss.hitbox[2]:
                        Boss.hit()
                        score += 3
                        bullets.pop(bullets.index(bullet))

            if bullet.x < 1250 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        if keys[pygame.K_SPACE] and shootloop == 0:
            bulletSound.play()
            if Punish.left:
                facing = - 1
            else:
                facing = 1
            if len(bullets) < 20:
                bullets.append(projectile(round(Punish.x + Punish.width//2), round(Punish.y + Punish.height//2), 4, (0,0,0), facing))
            shootloop = 1

        if keys[pygame.K_a] and Punish.x > Punish.vel:
            Punish.x -= Punish.vel
            Punish.left=True
            Punish.right=False
            Punish.standing = False

        elif keys[pygame.K_d] and Punish.x < 1250 -Punish.vel - Punish.width:
            Punish.x += Punish.vel
            Punish.left=False
            Punish.right=True
            Punish.standing = False
        else:
            Punish.standing = True
            Punish.walkCount= 0

        if not(Punish.isJump):
            if keys[pygame.K_w]:
                Punish.isJump = True
                Punish.right = False
                Punish.left = False
                Punish.walkCount = 0
        else:
            if Punish.jumpCount >= -10:
                Punish.y -= (Punish.jumpCount * abs(Punish.jumpCount)) * 0.5
                Punish.jumpCount -= 1
            else:
                Punish.jumpCount = 10
                Punish.isJump = False
        pygame.display.update()

game_intro()
story_screen()
level_1()
level_2()
level_3()
pygame.quit()
quit()
