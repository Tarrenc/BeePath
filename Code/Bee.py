import pygame #import pygame 
from BeePath import GeneticAlgorithm #import the GA
import numpy as np #import numpy
 
BeeStart=[375,375] #bees starting position
GA = GeneticAlgorithm(BeeStart) #Instance of GA class
Samples=GA.RunGeneticAlgorithm() #retrieve the route samples

pygame.init() #initialise pygame 

dimension=750 #how big  the window is
win = pygame.display.set_mode((dimension, dimension)) #create a pygame window
  
# set the pygame window name 
pygame.display.set_caption("Bee Simulation")
  
# bee start co-ordinates 
x = BeeStart[0]
y = BeeStart[1]

# dimensions of the bee and flower 
width = 50
height = 50
Bwidth = 50
Bheight = 50

#importing and resizing the bee and flower and creating background image
bg = pygame.image.load("Grass.png")
BeePic=pygame.image.load('BeePic.png')
BeePic = pygame.transform.scale(BeePic, (Bwidth, Bheight))
FlowerPic=pygame.image.load('Flower.png')
FlowerPic = pygame.transform.scale(FlowerPic, (width, height))

#Game variables
counter=0 #counter to loop through routes

vel = 5 #bee velocity

run = True #start the games loop



def create_best_path(Sample): #unfinished
    x=Sample[:,0] 
    y=Sample[:,1]

    return [x,y]
global best_path
best_path=create_best_path(Samples[-1])


while run: #start the game
    pygame.time.delay(10) #delay the game update
    win.blit(bg, (0,0)) #set the background
    for event in pygame.event.get(): #retrieve user actions
        if event.type == pygame.QUIT: #if window is closed 
            run = False #stop running the game
            
        if event.type == pygame.KEYDOWN: #if a key has been pressed, up here to debounce the button
            if event.key == pygame.K_p: #if p is pressed
                if counter<len(Samples)-1: #if counter isnt max
                    counter+=1 #increase the counter
                else: #if max is reached
                    counter=len(Samples)-1 #set the counter as the max 
                #print(counter)
   

    keys = pygame.key.get_pressed() #from the event queue retrieve the key presses and save them as keys
    if keys[pygame.K_LEFT] and x>0: #left key and still in window
        x -= vel #move left
    if keys[pygame.K_RIGHT] and x<dimension-width*1: #if right pressed and still in window
        x += vel  #move right
    if keys[pygame.K_UP] and y>0: #if up pressed and still in window 
        y -= vel  #move up
    if keys[pygame.K_DOWN] and y<dimension-height*1: #if the down key is pressed 
        y += vel #move down

    
    for i in range(1,len(Samples[0]),1): #loop through the samples starting at one 
        win.blit(FlowerPic, (Samples[0][i][0], Samples[0][i][1])) #draw the flowers
    if  keys[pygame.K_SPACE]: #if space is pressed 
        for i in range(1,len(Samples[0]),1): #loop through the flowers 
            pygame.draw.line(win,(0,0,255),(x+Bwidth/2,y+Bwidth/2),(Samples[0][i][0]+width/2,Samples[0][i][1]+width/2)) #draw lines from the bee to the flower
    
    
    if keys[pygame.K_h]: #if h is pressed move the bee back to the start
        x=BeeStart[0] #x = bee start
        y=BeeStart[1] #y = bee start
    

    if keys[pygame.K_RETURN]: #if enter is pressed 
        for i in range(len(Samples[0])-1): #loop through the samples again 
            #print(i)
            #two lines below draw the routes from the starting bee pos depending on what counter is on
            pygame.draw.line(win,(0,0,0),(Samples[counter][i][0]+width/2,Samples[counter][i][1]+width/2),(Samples[counter][i+1][0]+width/2,Samples[counter][i+1][1]+width/2))
            pygame.draw.line(win,(0,0,0),(Samples[counter][0][0]+width/2,Samples[counter][0][1]+width/2),(Samples[counter][-1][0]+width/2,Samples[counter][-1][1]+width/2))
        
        
    if keys[pygame.K_a]: #hopefully this be the animation function
        pass
    
    win.blit(BeePic, (x,y)) #draw bee at x,y
    
    pygame.display.update()  #update the window
    
pygame.quit() #quit the game