import pygame
from BeePath import GeneticAlgorithm
import numpy as np
 
BeeStart=[375,375]
GA = GeneticAlgorithm(BeeStart)
Samples=GA.RunGeneticAlgorithm()

pygame.init()

dimension=750
win = pygame.display.set_mode((dimension, dimension))
  
# set the pygame window name 
pygame.display.set_caption("Moving rectangle")
  
# object current co-ordinates 
x = BeeStart[0]
y = BeeStart[1]
# dimensions of the object 
width = 50
height = 50
Bwidth = 50
Bheight = 50

BeePic=pygame.image.load('BeePic.png')
BeePic = pygame.transform.scale(BeePic, (Bwidth, Bheight))
bg = pygame.image.load("Grass.png")
FlowerPic=pygame.image.load('Flower.png')
FlowerPic = pygame.transform.scale(FlowerPic, (width, height))
counter=0

vel = 5

run = True



def create_best_path(Sample):
    x=Sample[:,0]
    y=Sample[:,1]

    return [x,y]



global best_path
best_path=create_best_path(Samples[-1])
while run:
    pygame.time.delay(10) 
    win.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if counter<len(Samples)-1:
                    counter+=1
                else:
                    counter=len(Samples)-1
                print(counter)
   

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x>0:
        x -= vel
    if keys[pygame.K_RIGHT] and x<dimension-width*1:
        x += vel 
    if keys[pygame.K_UP] and y>0:
        y -= vel  
    if keys[pygame.K_DOWN] and y<dimension-height*1:
        y += vel

    
    for i in range(1,len(Samples[0]),1):
        win.blit(FlowerPic, (Samples[0][i][0], Samples[0][i][1]))
    if  keys[pygame.K_SPACE]:
        for i in range(1,len(Samples[0]),1):
            pygame.draw.line(win,(0,0,255),(x+Bwidth/2,y+Bwidth/2),(Samples[0][i][0]+width/2,Samples[0][i][1]+width/2))
    
    
    if keys[pygame.K_h]:
        x=BeeStart[0]
        y=BeeStart[1]
    

    if keys[pygame.K_RETURN]:
        for i in range(len(Samples[0])-1):
            #print(i)
            pygame.draw.line(win,(0,0,0),(Samples[counter][i][0]+width/2,Samples[counter][i][1]+width/2),(Samples[counter][i+1][0]+width/2,Samples[counter][i+1][1]+width/2))
            pygame.draw.line(win,(0,0,0),(Samples[counter][0][0]+width/2,Samples[counter][0][1]+width/2),(Samples[counter][-1][0]+width/2,Samples[counter][-1][1]+width/2))
        
        
    if keys[pygame.K_a]:
        pass
    
    win.blit(BeePic, (x,y)) 
    
    pygame.display.update() 

pygame.quit()