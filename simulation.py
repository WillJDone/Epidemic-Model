# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 12:23:44 2022

@author: qa21336
"""

import numpy as np
import random as rand  
from animation import animation
from plot import plot

class simulation:
    """
    From the attriubtes inputted from runsim.py this class forms an n by n
    zeros matrix. This each element of the matrix represents a person, and the
    value of the element represents their state:
        0  --  susceptible
        >1 -- infected: value - 1 is the number of days a person is infected 
        -1 -- recovered (with immunity)
        -2 -- dead
        
    A randomly selected element of the matrix is selected and assigned a value 
    of 1 - this is patient 0 on day 0. Each day an infected person has a chance 
    of infcted adjacent people. After a person has been infected for a
    specifiied amount of days they become either recovered or dead - based on
    chance. Note; the value '1' itself is used a placeholder for people who are
    infected but not infectous the instant they become infected. 
    
    e.g.    
    [[0 0 0 0]
     [0 0 0 0]
     [0 2 0 0]
     [0 0 0 0]] 

    [[0 0 0 0]
     [0 2 0 0]
     [2 3 0 0]
     [0 2 0 0]] 

    [[0 2 0 0]
     [0 3 0 0]
     [3 4 0 0]
     [2 3 2 0]] 
    
    (... until everybody is suscepbtilbe, recovered or dead)
    
    From this sequence of matrices, two sets of data are collected: the grid
    animation and the animated SIRD graph. The set of data for the grid 
    animation is s 4 list (one for each:SIRD) of lists (containing the
    coordinates of all the people in each state). The set of data for the 
    animated SIRD graph is a list containing the number of each state of people
    on each day. The animation class in animation.py and the plot function in
    plot.py are called with their respective attirbutes/inputs.
    """
    def __init__(self, r, t, d, edge, file_1,file_2):
        self.s_grid = [] #list containing data for grid animation of susceptible people
        self.i_grid = [] #list containing data for grid animation of infected people
        self.r_grid = [] #list containing data for grid animation of revovered people
        self.d_grid = []#list containing data for grid animation of dead people
        self.r  = r#infection rate, this the chance a person infects an adjacent person in a day
        self.t = t#days until removed 
        self.d = d #death rates, the chance an infected person dies   
        self.edge = edge #size of edge by edge dimension matrix
        self.s_graph = [] #list containing number of susceptible people on each day
        self.i_graph = [] #list containing number of infected people on each day
        self.r_graph = [] #list containing number of recovered people on each day
        self.d_graph = [] #list containing number od dead people on each day
        self.form_matirx(self.edge) #this function starts the set up of the matrices
        
        animation.hex_grid(self.s_grid, self.i_grid, self.r_grid, self.d_grid, self.edge)
        
        # animation(self.s_graph,self.i_graph,self.r_graph,self.d_graph,
        #                 self.s_grid, self.i_grid, self.r_grid, self.d_grid, self.edge, file_2, 1/4)
        # animation(self.s_graph,self.i_graph,self.r_graph,self.d_graph,
        #                 self.s_grid, self.i_grid, self.r_grid, self.d_grid, self.edge, file_2, 1/2)
        # animation(self.s_graph,self.i_graph,self.r_graph,self.d_graph,
        #                 self.s_grid, self.i_grid, self.r_grid, self.d_grid, self.edge, file_2, 3/4)
        
        #To end the animation at 0.25,0.5 and 0.75  through the epidemic uncomment lines 73-78.
        # This was used to save the figures for the report writing
        
        animation(self.s_graph,self.i_graph,self.r_graph,self.d_graph,
                        self.s_grid, self.i_grid, self.r_grid, self.d_grid, self.edge, file_2, 1)
        
        plot(self.s_graph,self.i_graph,self.r_graph,self.d_graph,file_1)
         #animation in animation.py and plot in plot.py are called here once the sequence of
         # matrices are finished
  
    def form_matirx(self,edge):
        """
        The zero matrix is created and patient 0 is assigned. Then 
        salf.values() is called to carry on the simulation
        """
        self.matrix = np.zeros([edge,edge],int)
        infected = ([rand.randint(0,edge-1)],[rand.randint(0,edge-1)]) #random coorinate found
        self.matrix[infected] = 1 #patient 0 assigned value 1
        self.values()
                                                                               
    def values(self):   
        """
        This function creates the lists of data for the grid animation.
        For each SIRD the coordinates of each state are found e.g. self.s_cords
        The coordinated are zipped and added to a list e.g. self.s_grid
        Note;some days may have an empty set of coordinates, so the coordinate 
        (-1,-2) is added as a placeholder.
        At the end self.infection() is called to continue the simulation
        """           
        self.s_coords = np.where(self.matrix == 0)
        if list(zip(self.s_coords[0], self.s_coords[1])) != []:
            self.s_grid.extend([list(zip(self.s_coords[0], self.s_coords[1]))])        
        else:
              self.s_grid.extend([[(-1,-2)]])
             
        self.i_coords = np.where(self.matrix > 1)     
        if list(zip(self.i_coords[0], self.i_coords[1])) != []:
            self.i_grid.extend([list(zip(self.i_coords[0], self.i_coords[1]))])
        else:
              self.i_grid.extend([[(-1,-2)]]) 

        self.r_coords = np.where(self.matrix == -1)      
        if list(zip(self.r_coords[0], self.r_coords[1])) != []:
            self.r_grid.extend([list(zip(self.r_coords[0], self.r_coords[1]))])
        else:
              self.r_grid.extend([[(-1,-2)]]) 
             
        self.d_coords = np.where(self.matrix == -2)      
        if list(zip(self.d_coords[0], self.d_coords[1])) != []:
            self.d_grid.extend([list(zip(self.d_coords[0], self.d_coords[1]))])
        else:
              self.d_grid.extend([[(-1,-2)]])
                      
        self.infection(self.matrix, self.edge)
        
    def infection(self,matrix,edge):
        """
        As long as one person is infected the simulation must carry on until
        the disease is essentially extinct. All the values of the matrix are 
        iteratedthrough, if at least 1 peron is found to be infected, the 
        simulation is allowed to carry on; self.new_cases, self.time and 
        self.values are called. In addition the number of people in eash state
        that day for the SIRD graph.
            
        self.new_cases gives the 6 adjcent spaces a chance to be come infected
            from the adjecnt infected person
        self.time progresses to the next day. The number of days that a person
            is infected for is increased by 1 and if a person comes to the 
            duration of the disease they either die or recover with immunity
        self.values adds to values for the grid for the now new day
        
        self.infection and self.values continue to call each other (adding data
        to list for each day) until the simulation is finished whereby nobody 
        is no longer infected and the virus can no longer spread. At this point
        the lists of data for the plots and animation are completed and their
        relevant functions are called in __init__
        """
        for x in range(edge):
            for y in range(edge):
                if matrix[y][x] > 0:                      
                    # print(matrix,'\n') #uncomment this line to print each matrix - use low edge number e.g. 4
                    self.s_graph.append(np.count_nonzero(matrix == 0))
                    self.i_graph.append(np.count_nonzero(matrix > 0))
                    self.r_graph.append(np.count_nonzero(matrix == -1))
                    self.d_graph.append(np.count_nonzero(matrix == -2))
                    self.new_cases(matrix,edge)
                    self.time(matrix,edge)
                    self.values()  
                        
    def new_cases(self,matrix,edge):        
        """
        The first two lines of this function loop through all elements of the
        matrix. If the element's state is greater than 1 (for infected) each
        adjacent hexagon is given a chance for the infection to spread to. 
        For an infected person, six people are given the chance to become 
        infected from 6 if statements:        
            The first four positions are irrespective of the hexagon's column. 
            The other two depend on the infected person's column. As the gif 
            of the animation demonstrates, the odd columns and odd rows are 
            offset from each because of how hexagons tesselate.
                    
        """
        for x in range(edge):
            for y in range(edge):
                if matrix[y][x] >= 2 :
                    if 0<x and matrix[y][x-1] == 0 and rand.randint(1,10) <= 10 * self.r:
                        matrix[y][x-1] = 1
                    if x<edge-1 and matrix[y][x+1] == 0 and rand.randint(1,10) <= 10 * self.r:
                        matrix[y][x+1] = 1
                    if 0<y and matrix[y-1][x] == 0 and rand.randint(1,10) <= 10 * self.r:                    
                        matrix[y-1][x] = 1
                    if y<edge-1 and matrix[y+1][x] == 0 and rand.randint(1,10) <= 10 * self.r:
                        matrix[y+1][x] = 1
                    if y % 2 == 1:
                        if x<edge-1 and y<edge-1 and matrix[y+1][x+1] == 0 and rand.randint(1,10) <= 10 * self.r == 0:
                            matrix[y+1][x+1] = 1
                        if x<edge-1 and 0<y and matrix[y-1][x+1] == 0 and rand.randint(1,10) <= 10 * self.r == 0:
                            matrix[y-1][x+1] = 1
                    else:        
                        if x>0 and y>0 and matrix[y-1][x-1] == 0 and rand.randint(1,10) <= 10 * self.r == 0:
                            matrix[y-1][x-1] = 1
                        if x>0 and y<edge-1 and matrix[y+1][x-1] == 0 and rand.randint(1,10) <= 10 * self.r == 0:
                            matrix[y+1][x-1] = 1  
                                                 
    def time(self,matrix,edge):
        """
        Similar to self.new_cases each element is iterated through. This 
        functions If the person falls under the 'infected' state the number of
        days they have been infected for increases by one day. Additionally,
        if the number of days a person has been infected equals the duration of
        the virus, the person either becomes recovered (-1) or dead (-2)
        """
        for x in range(edge):
            for y in range(edge):
                if matrix[y][x] > 0:
                    matrix[y][x] = matrix[y][x] + 1
                if matrix[y][x] == self.t+1:
                    if rand.randint(1, 10) >= 10 * self.d:                            
                        matrix[y][x] = -1
                    else:
                        matrix[y][x] = -2