import pygame
import random
import math
from pygame import mixer
#init
pygame.init()
screen=pygame.display.set_mode((900,600))
bang=mixer.Sound("shot.mp3")
bullet=mixer.Sound("bulletshot.mp3")
loser=mixer.Sound("lose.mp3")



#icon name
pygame.display.set_caption("infinity shot")

#load images player
ship=pygame.image.load("ship.png")
x=450
y=550
PX=0
PY=0

#asteroids

astr1=[]
ox=[]
oy=[]
oyp=[]
for i in range(0, 20):
    astr1.append(pygame.image.load("asteroid2.png"))
    ox.append(random.randint(10,590))
    oy.append(random.randint(-80, -40))
    oyp.append(1)

#bullet
bll=pygame.image.load("bullets.png")
bx=0
by=558
constant=0
byp=0


#score
scv=0
scfont=pygame.font.SysFont("start", 40)

#game over
overf=pygame.font.SysFont("over",80)

#backound
space=pygame.image.load("space.png")
mixer.music.load("bcsound1.mp3")
mixer.music.play(4)




#main
running=True
while running:    
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    if event.type ==pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            PX=-3
            PY=0
        elif event.key == pygame.K_RIGHT:
            PX=3
            PY=0
        elif event.key == pygame.K_TAB:
            if constant==0:
                bx=x
                constant=1
                byp=-20
                    


    if event.type ==pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            PX=0
            PY=0

        


    x=x + PX 
    by=by+byp


    if x>875:
        x=875
    if x<=0:
        x=0


#1
    screen.blit(space,(0,0))

#2
    if constant==1:
        screen.blit(bll,(bx+7, by))        
        if by<=0:
            by=558
            constant=0
  
    #3

    for i in range(0,20):
        if oy[i]>=590:
            ox[i]=random.randint(10,890)
            oy[i]=random.randint(-80,-40)

        d=math.sqrt((bx-ox[i])**2+(by-oy[i])**2)
        dis=math.sqrt((ox[i]-x)**2+(oy[i]-y)**2)

        if d<20:
            bang.play()
            ox[i]=random.randint(10,890)
            oy[i]=random.randint(-80,-40)            
            scv+=1
        oy[i]=oy[i]+oyp[i]
        score=scfont.render("SCORE: "+str(scv),True, (255,255,0))
        screen.blit(score,(20,20))
        screen.blit(astr1[i], (ox[i], oy[i] ))

        if dis<35:
            over=overf.render("GAME OVER",True,(255,255,0))
            screen.blit(over,(300,300))
            loser.play(1)
        
           
#4
    screen.blit(ship, (x, y))
    pygame.display.update()
pygame.quit()
