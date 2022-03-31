import random #import random library
import matplotlib.pyplot as plt #import matplotlib library
import numpy as np #import numpy library
from itertools import islice #import itertools library
import math #import math library
import statistics #import statistics library
import time #import time library


class GeneticAlgorithm:
    
    def __init__(self, BeeStart):
        self.Generations=1500 #Number of times that the algorithm will loop
        self.NofTowns=10 #The number of towns that should be visited must be greater than 3
        self.CartesianMax=1000 #The maximum cartesian coordinates to be used 
        self.PopulationSize=50 #Population size 
        self.ElitismRate=0.02 #Top percentage of the population deemed elite
        self.crossoverRate=0.5
        self.MutationRate=0.05 #The percentage chance of an indivdual mutating
        self.Show_Generations= True #Switch to show current generation in Console
        self.convergenceCheck=True #if half the generations have passed and there has been no improvement over a third of the generations terminate the algorithm
        self.NoGenerationalImprovement=200
        self.debugMode=False #keeps the towns the same by setting the same random seed in the population definition function where a random sample of towns is taken
        self.PostProc=True
        self.BeeStart=BeeStart
    
    
    class Flower: #Creating the class flower to store thier respective x and y values 
        
        def __init__(self,x,y): #initialising function with an x and y value
            self.x=x #setting the value to be stored as x
            self.y=y #setting the value to be stored as y
    
    class Paths: #Path class to include methods to create the paths and calculate the distances between the the individual flowers in them.
        
        def PathGeneration(Flowers): #Generating individuals
            path=[] #Blank array to store random list of towns
            path.append(random.sample(Flowers, len(Flowers))) #Appending a random list of towns
            #path.insert(index, object)
            return path #return the path array
         
        def Length(self,Population): #Calculate distance between towns
            PathLengths=[] #empty array to store lengths of the paths
            for i in range(self.PopulationSize): #looping through the population
                    for j in range(self.NofTowns): #looping the same amount of times as the number of towns
                        #print(np.shape(Population)) #used for debugging
                        Length=np.sqrt((Population[i][0][j].x - Population[i][0][j-1].x)**2+(Population[i][0][j].y-Population[i][0][j-1].y)**2) #calculating euclidean distance
                        PathLengths.append(Length) #appending the paths lengths array with the length values
            Routes=np.array_split(np.array(PathLengths),self.PopulationSize) #splitting the Pathslengnths array into the population sizes
            return Routes #return routes
        
    def FitnessFunction(self,Routes): #Fitness funtion takes a variable in the same format as pathslengths
        TotalLengths=[] #Creating an empty list to store the total lengths of each member in the population
        for i in range(self.PopulationSize): #Looping through the population
                x=np.sum(Routes[0][i]) #Using Numpy to sum the individual lengths between the towns
                TotalLengths.append(x) #Appending the sum of the individual lengths to the total lengths list
        return TotalLengths #return the total lengths list
    
    def Elitism(self,FitList,Population):   #takes a fitness list and a Population
        NewPopulation=[] #Creating blank list to store the new population
        RankList=[] #Creating blank list to store the current populations rank in terms of fitness
        for i in range(self.PopulationSize): #loop through the population
            x=(sorted(enumerate(FitList), key=lambda i: i[1]))[i][0] #create a list that shows where the members are in the population and shows thier index
            RankList.append(x) #append ranklist with the x value above
            #print(x) #used in debugging
        for j in range(round(self.ElitismRate*self.PopulationSize)): #taking the percentage defined by the user at on line 13
            NewPopulation.append(Population[RankList[j]]) #appending the new population with the best percentage of the new population
        for i in range(len(NewPopulation)): #looping through the population
            Population.remove(NewPopulation[i]) #anything that is now in the new population is removed from the current one
        return [Population, NewPopulation] #Returning the updated and the current and new populations as a tuple
        
    def RouletteWheelSelection(self,Population, FitList): #Using a roulette wheel where higher fitness individuals have a higher probability of getting picked
        SelectedIndividuals=[] #Creating a blank list to store selected individuals
        InvPercentage=[] #Creating a blank list to store the inverse of the percentage fitness of the corresponding individual
        Wheel=[] #creating a blank list to store members of the population multiple times, with respect to thier percentage score
        for i in range(len(Population)): #looping for the length of the population passed to it, as elitism can change this length
            InvPercentage.append(round((sum(FitList)/FitList[i]))) #calculating the inverse of the percentage, rounding it and then adding to the InvPercentag
            for j in range(InvPercentage[i]): #looping the current element in invpercentage times
                Wheel.append(Population[i]) #append the corresponding member of the population to the wheel list
        for i in range(len(Population)*2): #loop for twice the length of the population passed as with elitism it could change. Twice because crossover reduces 2 members to 1
            y=random.randint(0, len(Wheel)-1) #create a random integer between 0 and the length of the wheel
            SelectedIndividuals.append(Wheel[y]) #'spin the wheel' and append the 
        return SelectedIndividuals #return selected individuals
    
    def Crossover(self,SelectedIndividuals):#Whatever comes out of selection
        NewPopulation=[] #creating a local new population list
        splitters=[2]*int((len(SelectedIndividuals)/2)) #creating a sublist to be used to split the selected individuals list
        x=iter(SelectedIndividuals) #Creating an object that can be iterated one element at a time using the selected individuals list
        Parents=[list(islice(x, elem)) for elem in splitters] #Slicing the x list into groups of 2 using the slitter list
        for i in range(len(Parents)): #Looping through the parents list
            NewMember=[-1]*math.ceil(self.NofTowns*self.crossoverRate) #Creating the new member array with a number of blank elements 
            for j in range(math.ceil(self.NofTowns*self.crossoverRate)): #Looping through the new member list
                NewMember[j]=Parents[i][0][0][j] #Changing the blanks in the array to the genes in the first parent
            for k in range(self.NofTowns): #Looping through the whole array
                if Parents[i][1][0][k] not in NewMember: #If the next parents array is not in the new member
                    Child=[] #Creating a blank array to keep the same formatiing as the original members
                    NewMember.append(Parents[i][1][0][k]) #adding the respective gene to the end of the new member
                    Child.append(NewMember) #adding the new member to the child list
            NewPopulation.append(Child) #adding the children to the new population list
        return NewPopulation #return the new population
    
    def Mutation(self,NewPopulation,MutationRate): #Creating a function to mutate the new population
        for i in range(len(NewPopulation)): #looping through the members of the population not deemed elite as later in the RunGeneticAlgorithm Function the elite members are at the end of the list
            if MutationRate>=random.uniform(0,1): #if the mutation rate is less greater than a randomly generated number between 0 and 1 continue
                x=random.randint(0,self.NofTowns-1) #create a random integer between 0 and the length of the population -1 
                y=random.randint(0,self.NofTowns-1) #create a random integer between 0 and the length of the population -1 
                #print(np.shape(NewPopulation))
                NewPopulation[i][0][x],NewPopulation[i][0][y]=NewPopulation[i][0][y],NewPopulation[i][0][x] #swap the x indexed member with the y indexed member in the population
        return NewPopulation #Return new population
    
    def InitialPopulation(self): #function to generate the towns and subsequent initial population
        global Flowers #creating the global variable towns so it can be seen in the variable explorer
        Flowers=[] #creating a blank list called towns 
        Population=[] #creating a blank list called population
        if self.debugMode == True: # if debug more is on, set the random seed to 1 to ensure that the generated towns are the same each time.
            random.seed(1) #setting the random seed as 1
        for i in range(self.NofTowns): #looping the number of tiems equal to number of towns
            Flowers.append(self.Flower(random.randint(0,self.CartesianMax),random.randint(0,self.CartesianMax))) #using the towns class create towns objects with random x and y values and append them to the towns array
        Flowers[0]=self.Flower(self.BeeStart[0],self.BeeStart[0])
        for i in range(self.PopulationSize): #looping the same amount of times as the population size 
            Population.append(self.Paths.PathGeneration(Flowers)) #appending the population with random orders of towns using the Paths method PathGeneration
        random.seed() #returning the random seed to a blank value so the rest of the random behavior in the algorithm is random
        return Population #Returning population
    
    def RunGeneticAlgorithm(self): #function that runs the genetic algorithm, plots the data and exports it as .csv
        Start_time=time.time() #saving the start time of the algorithm
        Population=self.InitialPopulation() #creating the intitial population
        BestFitness=[] #creating a blank array called best fitness 
        MeanFitness=[] #creating a blank array called mean fitness
        WorstFitness=[] #creating an array called worst fitness
        FinishTime=[] #creating a blank array to store the end times of each generation
        Samples=[]
        ConvChecker=0
        for i in range(self.Generations): #looping the same amount of generations
            ##calculating fitnesses 
            Routes=[] #creating a blank list called routes
            Routes.append(self.Paths.Length(self,Population)) #appending the routes array with the Paths method Lengths
            FitList=self.FitnessFunction(Routes) #using the fitness function to get the overall fitness list
            MeanFitness.append(statistics.mean(FitList))  #calculating the mean fitness at each generation and appending it to the mean fitness list
            BestFitness.append(min(FitList)) #calculating the best fitness at each generation and appending it to the best fitness list
            WorstFitness.append(max(FitList)) #calculating the worst fitness 
            ##Running the algorithm
            [A, B] = self.Elitism(FitList,Population) #create a tuple storing the elite members (B) and the updated current population (A)
            # print(len(B)) #used in debugging
            C = self.RouletteWheelSelection(A, FitList)  # C= the output of the tournament selection function when given the updated population and its fitness list
            D = self.Crossover(C) #D is the output of the crossover function when given C
            F=self.Mutation(D,self.MutationRate) #mutate the crossed over members
            E=F+B #combine with the elite members
            NewPopulation=E #set E as the new population
            if self.Show_Generations==True: # if generation switch is true
                print('Generation',i+1) #printing which generation the algorithm is on
            Population=NewPopulation #Making the Current population the one that has just been made
            FinishTime.append(time.time()) #append the finish time array with the current time
            
            if i%250==0: #every 250 generations
                FitIndex=(sorted(enumerate(FitList), key=lambda i: i[1]))[0] 
                Samples.append(Population[FitIndex[0]])
            if i>10 and i%10==0 and BestFitness[i]-BestFitness[i-10]==0 and self.convergenceCheck==True: #if i is greater than 10, and the 10th previous best fitness is equal to the current, and conv check is on
                ConvChecker=ConvChecker+1 #increase the convchecker by 1
            elif i>10 and i%10==0 and BestFitness[i]-BestFitness[i-10]!=0 and self.convergenceCheck==True:#same check as above 
                ConvChecker=0 #set convcheker as 0
            if ConvChecker>=self.NoGenerationalImprovement and self.convergenceCheck==True: #if convergence criteria has been met
                print('Terminated at Generation',i+1) #print a message to console
                break #exit the for loop
        GenerationTime=[x-Start_time for x in FinishTime] #using list comprehension to get a list with the cumulative time for each generation
        End_time=time.time() #saving the finish time of the whole algorithm
        ElapsedTime=End_time-Start_time #calculating the elapsed time
        ##saving the best ones of the population
        
        BestPopulationSaver=[] #Blank list to store the best member of the population in the last generation
        FinalFitIndex=(sorted(enumerate(FitList), key=lambda i: i[1]))[0] #creating a final fitness index so the best individual can be easily indexed
        #print(np.shape(FinalFitIndex)) #used in debugging
        BestPopulationSaver.append(Population[FinalFitIndex[0]]) #appending the best population saver list with the best member of the last generation
        BestMembx=[] #creating a best membx list to store the x values of the towns in the best member of the population in the last generation
        BestMemby=[] #creating a best memby list to store the x values of the towns in the best member of the population in the last generation
        #print(np.shape(BestPopulationSaver))
        for i in range(self.NofTowns): #looping through the number of towns
            BestMembx.append(BestPopulationSaver[0][0][i].x) #adding the x coordinate of the member to the bestmembx list
            BestMemby.append(BestPopulationSaver[0][0][i].y) #adding the y coordinate of the member to the bestmemby list
        
        BestMembx.append(BestMembx[0]) #adding the first element back to the last to end of the list as to complete the loop
        BestMemby.append(BestMemby[0]) #adding the first element back to the last to end of the list as to complete the loop
        
        SamplesCoordinates=self.Samples(Samples)
        
        
        if self.PostProc==True:
            print('Intial Best Fitness = %0.3f' % BestFitness[0], 'Unit Lengths') #Printing the Intial best fitness to the console
            print('Intial Worst Fitness = %0.3f' % WorstFitness[0], 'Unit Lengths') #Printing the inital worst fitness to the console 
            print('Final Best Fitness = %0.3f' % BestFitness[-1], 'Unit Lengths') #Printing final best fitness to the console
            print('Final Worst Fitness = %0.3f' % WorstFitness[-1], 'Unit Lengths') #Printing final worst fitness to the console
            print('Time Elapsed = %0.3f' % ElapsedTime,'Seconds') #printing the elapsed time to the console
            ##plots
            plt.figure() #Creating new Figure
            plt.plot(BestMembx,BestMemby,color='k',label='Optimum Route') #Plotting the best route through the towns
            plt.plot(BestMembx,BestMemby,color='k', marker='o', mfc='r', label= 'Flowers') #Plotting the best route through the towns
            
            plt.plot(self.BeeStart[0],self.BeeStart[1],marker='o',color='k', mfc='y',markersize=15, label = 'Bee starting position')
            plt.xlim(-self.CartesianMax/5,self.CartesianMax+5) #change the axis limits of the graph
            plt.ylim(-self.CartesianMax/5,self.CartesianMax+50) #change the axis limits of the graph
            plt.xlabel('X Coordinate') #Creating an axis label
            plt.ylabel('Y Coordinate') #Creating an axis label
            plt.legend()
            plt.title('Best Route (%0.3f)' %BestFitness[-1]) #creating a plot title
            plt.grid('on') #adding a grid to the plot for clarity
            
            
            plt.figure() #Creating new Figure
            plt.plot(GenerationTime, BestFitness, color='k', label='Minimum Fitness vs Time') #plotting the best fitness as the generations increase
            plt.xlabel('Time Elapsed (s)') #Creating an axis label
            plt.ylabel('Minimum Fitness') #Creating an axis label
            plt.legend(loc='best')# setting the legend location
            plt.title('Graph of Best Fitness over Time') #creating a plot title
            plt.grid('on') #adding a grid to the plot for clarity
        
        return SamplesCoordinates
        
    def Samples(self, Samples): #function for reordering the sample list
        Samples1=[] #list to store the sample
        for i in range(len(Samples)): #loop through the samples
            X=[] #x coordinates list
            Y=[] #y coordinates list
            for j in range(self.NofTowns): #loop through the towns
                X.append(Samples[i][0][j].x) #append current samples x coordinate to the temp list
                Y.append(Samples[i][0][j].y) #append current samples y coordinate to the temp list
            
            for k in range(len(Y)): #loop through the coordinates 
                if Y[0] != self.BeeStart[1] and X[0] != self.BeeStart[0]: #if the first coordinate isnt the bees starting pos 
                    Y.append(Y[0]) #rearrange list
                    Y.pop(0) #rearrange list
                    X.append(X[0]) #rearrange list
                    X.pop(0) #rearrange list
            Sample = np.c_[X,Y] #concat list
            Samples1.append(Sample) #append new sample
        return Samples1 #return list of samples
        

BeeStart=[100,100] #starting position of the bee

Instance=GeneticAlgorithm(BeeStart) #create instance
Samples = Instance.RunGeneticAlgorithm() #retrieve samples
    
