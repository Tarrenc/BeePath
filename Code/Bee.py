# import pygame module in this program 
import pygame
import numpy as np
import random 
from BeePath import GeneticAlgorithm
# activate the pygame library .  
# initiate pygame and give permission  
# to use pygame's functionality.  

toggle=False
pygame.init()
  
# create the display surface object  
# of specific dimension..e(500, 500).  
win = pygame.display.set_mode((500, 500))
  
# set the pygame window name 
pygame.display.set_caption("Moving rectangle")
  
# object current co-ordinates 
x = 0
y = 0
  
# dimensions of the object 
width = 20
height = 20
  
# velocity / speed of movement
vel = 5
  
# Indicates pygame is running
run = True
flowersx = random.sample(range(10, 495), 5)
flowersy = random.sample(range(10, 495), 5)
#print(flowersx)
for i in range(len(flowersx)):
    pygame.draw.rect(win, (255,0,0), (flowersx[i], flowersy[i], width, height))
    pygame.display.update()
# infinite loop 
while run:
    # creates time delay of 10ms 
    pygame.time.delay(10)
    # iterate over the list of Event objects  
    # that was returned by pygame.event.get() method.  
    for event in pygame.event.get():
          
        # if event object type is QUIT  
        # then quitting the pygame  
        # and program both.  
        if event.type == pygame.QUIT:
              
            # it will make exit the while loop 
            run = False
    # stores keys pressed 
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_q]:
        # if left arrow key is pressed
        if keys[pygame.K_LEFT] and x>0:
            # decrement in x co-ordinate
            x -= vel
        # if left arrow key is pressed
        if keys[pygame.K_RIGHT] and x<500-width:
            # increment in x co-ordinate
            x += vel
        # if left arrow key is pressed   
        if keys[pygame.K_UP] and y>0:
            # decrement in y co-ordinate
            y -= vel
        # if left arrow key is pressed   
        if keys[pygame.K_DOWN] and y<500-height:
            # increment in y co-ordinate
            y += vel

    else:
        # if left arrow key is pressed
        if x>0:
            # decrement in x co-ordinate
            x -= vel
        # if left arrow key is pressed
        elif x<500-width:
            # increment in x co-ordinate
            x += vel
        # if left arrow key is pressed   
        elif y>0:
            # decrement in y co-ordinate
            y -= vel
        # if left arrow key is pressed   
        elif y<500-height:
            # increment in y co-ordinate
            y += vel
    win.fill((0,255,0))
      
    # drawing object on screen which is rectangle here 
    pygame.draw.rect(win, (255,255,0), (x, y, width, height))
    for i in range(len(flowersx)):
        pygame.draw.rect(win, (255,0,0), (flowersx[i], flowersy[i], width, height))
    if  keys[pygame.K_SPACE]:
        for i in range(len(flowersx)):
            pygame.draw.line(win,(255,255,255),(x+width/2,y+width/2),(flowersx[i]+width/2,flowersy[i]+width/2))
        #pygame.display.update()
    
    # it refreshes the window

    
    pygame.display.update() 
  
# closes the pygame window 
pygame.quit()