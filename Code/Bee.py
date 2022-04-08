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

# dimensions of the bee and flower 
width = 50
height = 50
Bwidth = 50
Bheight = 50

#importing and resizing images
bg = pygame.image.load("Images/Grass.png")
BeePic=pygame.image.load('Images/BeePic.png')
BeePic = pygame.transform.scale(BeePic, (Bwidth, Bheight))
BeePicRect = BeePic.get_rect(center=[BeeStart[0]+width/2,BeeStart[1]+width/2])
FlowerPic=pygame.image.load('Images/Flower2.png')
FlowerPic = pygame.transform.scale(FlowerPic, (width, height))
BeeHivePic= pygame.image.load('Images/BeeHive.png')
BeeHivePic = pygame.transform.scale(BeeHivePic, (100, 100))

#Game variables
counter=0 #counter to loop through routes
counter1=0 #used in making the bee fly around the route
run = True #start the games loop
polly_time = 250 #time spent at each flower


def create_best_path(Sample): #creates a route for the bee to follow
    Vscale=4 #Higher this higher bee speed
    xs=Sample[:,0] #taking x location of flowers in order of best route
    ys=Sample[:,1] #taking x location of flowers in order of best route

    xroute=[] #making an array to store the travel between flowers in x
    yroute=[] #making an array to store the travel between flowers in y
    
    for i in range(len(xs)-1): #loop through the samples
        length=(((xs[i+1]-xs[i])**2+(ys[i+1]-ys[i])**2)**0.5)/Vscale #allows for the same speed along all length of lines
        
        xroute.append(list(np.linspace(xs[i],xs[i+1],int(np.round(length))))) #create a linear spaces array between the two points of size step
        yroute.append(list(np.linspace(ys[i],ys[i+1],int(np.round(length))))) #create a linear spaces array between the two points of size step
    length=(((xs[-1]-xs[0])**2+(ys[-1]-ys[0])**2)**0.5)/Vscale #allows for the same speed along all length of lines
    xroute.append(list(np.linspace(xs[-1],xs[0],int(np.round(length))))) #return to the start
    yroute.append(list(np.linspace(ys[-1],ys[0],int(np.round(length))))) #return to the start
    xroute = np.array([item for sublist in xroute for item in sublist]) #flatten the list
    yroute = np.array([item for sublist in yroute for item in sublist]) #flatten the list
    route=np.column_stack((xroute, yroute)) #zip list together
    return route #return the route
 
    
best_path=create_best_path(Samples[-1]) #retrieve the path that the bee will take in x and y coords


while run: #start the game
    pygame.time.delay(10) #delay the game update
    win.blit(bg, (0,0)) #set the background
    win.blit(BeeHivePic, (BeeStart[0]-25,BeeStart[1]-25))
    for i in range(1,len(Samples[0]),1): #loop through the samples starting at one 
        win.blit(FlowerPic, (Samples[0][i][0], Samples[0][i][1])) #draw the flowers
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
            elif event.key == pygame.K_q:
                if counter>0: #if counter isnt max
                    counter=counter-1 #increase the counter
                else: #if max is reached
                    counter=0 #set the counter as the max 
                #print(counter)
   

    keys = pygame.key.get_pressed() #from the event queue retrieve the key presses and save them as keys

    if  keys[pygame.K_SPACE]: #if space is pressed 
        for i in range(1,len(Samples[0]),1): #loop through the flowers 
            pygame.draw.line(win,(0,0,255),(BeeStart[0]+Bwidth/2,BeeStart[1]+Bwidth/2),(Samples[0][i][0]+width/2,Samples[0][i][1]+width/2)) #draw lines from the bee to the flower
    
    
    if keys[pygame.K_h]: #if h is pressed move the bee back to the start
        x=BeeStart[0] #x = bee start
        y=BeeStart[1] #y = bee start
    

    if keys[pygame.K_RETURN]: #if enter is pressed 
        for i in range(len(Samples[0])-1): #loop through the samples again 
            #print(i)
            #two lines below draw the routes from the starting bee pos depending on what counter is on
            pygame.draw.line(win,(0,0,0),(Samples[counter][i][0]+width/2,Samples[counter][i][1]+width/2),(Samples[counter][i+1][0]+width/2,Samples[counter][i+1][1]+width/2))
            pygame.draw.line(win,(0,0,0),(Samples[counter][0][0]+width/2,Samples[counter][0][1]+width/2),(Samples[counter][-1][0]+width/2,Samples[counter][-1][1]+width/2))
        
        
    if keys[pygame.K_a]: #function to update the bee rectangle position 
        if counter1<len(best_path)-1: #counter to loop through the points 
            counter1+=1 #update the counter
            BeePicRect.center=[best_path[counter1][0]+width/2, best_path[counter1][1]+width/2] #change location
            for i in range(len(Samples[-1])): #loop through the samples
                c=0 #counter = 0
                if best_path[counter1-2][0] and best_path[counter1-1][0] == Samples[-1][i][0]: #because of repeats if the bee is at the flower is defined like this
                    c+=1 #up the count
                    if c == 1: #if the count is 1
                        pygame.time.delay(polly_time) #delay the game update aka stop at flower
                        c=0  #set counter back to 0
        else: #if counter is at the end
            pass #skip
    
    
    if keys[pygame.K_r]: #reset function
        counter=0 #set counter back to 0
        counter1=0 #set counter1 back to 0
        BeePicRect.center=[BeeStart[0]+width/2,BeeStart[1]+width/2] #return the bee to the starting position
        
    
    if keys[pygame.K_ESCAPE]: #if the escape key is pressed
        break #quit the game
            
    win.blit(BeePic,BeePicRect)  #draw bee at bee rectangle position
    pygame.display.update()  #update the window
    
pygame.quit() #quit the game