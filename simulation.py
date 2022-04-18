# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 12:23:44 2022

@author: dmall
"""

import numpy as np
import random as rand  
from animation import animation
from plot import plot

class simulation:
    def __init__(self, r, t, d, edge, file_1,file_2):
        self.s_grid = [] #list containing data for grid animation of susceptible people
        self.i_grid = [] #list containing data for grid animation of infected people
        self.r_grid = [] #list containing data for grid animation of revovered people
        self.d_grid = []#list containing data for grid animation of dead people
        self.r  = r#infection rate, this the chance a person infects an adjacent person in a day
        self.t = t#days until removed 
        self.d = d #death rates, the chance an infected person dies   
        self.edge = edge #size of matrix
        self.s_graph = [] #list containing number of susceptible people on each day
        self.i_graph = [] #list containing number of infected people on each day
        self.r_graph = [] #list containing number of recovered people on each day
        self.d_graph = [] #list containing number od dead people on each day
        self.form_matirx(self.edge)
        animation(self.s_graph,self.i_graph,self.r_graph,self.d_graph,
                        self.s_grid, self.i_grid, self.r_grid, self.d_grid, self.edge, file_2)
        plot(self.s_graph,self.i_graph,self.r_graph,self.d_graph,file_1)
  
    def form_matirx(self,edge):
        self.matrix = np.zeros([edge,edge],int)
        infected = ([rand.randint(0,edge-1)],[rand.randint(0,edge-1)])
        self.matrix[infected] = 1
        self.values()

    def new_cases(self,matrix,edge):
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
            for x in range(edge):
                for y in range(edge):
                    if matrix[y][x] > 0:
                        matrix[y][x] = matrix[y][x] + 1
                    if matrix[y][x] == self.t+1:
                        if rand.randint(1, 10) >= 10 * self.d:                            
                            matrix[y][x] = -1
                        else:
                            matrix[y][x] = -2
                          
    def infection(self,matrix,edge):
            for x in range(edge):
                for y in range(edge):
                    if matrix[y][x] != -1 and matrix[y][x] != 0 and matrix[y][x] != -2:
                        self.new_cases(matrix,edge)
                        self.time(matrix,edge)                       
                        # print(matrix,'\n') #uncomment this line to print each matrix - use low edge number e.g. 4
                        self.s_graph.append(np.count_nonzero(matrix == 0))
                        self.i_graph.append(np.count_nonzero(matrix > 0))
                        self.r_graph.append(np.count_nonzero(matrix == -1))
                        self.d_graph.append(np.count_nonzero(matrix == -2))
                        self.values()                    
                                       
    def values(self):               
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