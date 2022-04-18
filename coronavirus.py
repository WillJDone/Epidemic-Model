#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:26:22 2022

@author: qa21336
"""

import argparse
import numpy as np
import random as rand
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation       

def main(*args):
    parser = argparse.ArgumentParser(description='Modelling a pandemic with matrices')
    parser.add_argument('--infection', metavar='P', type=int, default=0.1,
                        help='this the chance a person infects an adjacent person in a day')
    parser.add_argument('--duration', metavar='N', type=int, default=14,
                        help='days until removed')
    parser.add_argument('--death', metavar='P', type=float, default=0.2,
                        help='the chance an infected person dies')
    parser.add_argument('--edge', metavar='N', type=float, default=60,
                        help='size of side of square matrix')

    args = parser.parse_args()

    Coronavirus(args.infection, args.duration, args.death, args.edge)        
        
class Coronavirus:
    def __init__(self, r, t, d, edge):
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
                 self.s_grid, self.i_grid, self.r_grid, self.d_grid, self.edge)
        
    def form_matirx(self,edge):
        self.matrix = np.zeros([edge,edge],int)
        infected = ([rand.randint(0,edge-1)],[rand.randint(0,edge-1)])
        self.matrix[infected] = 1
        self.values(self.s_graph,self.i_graph,self.r_graph,self.d_graph)

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
                        self.values(self.s_graph,self.i_graph,self.r_graph,self.d_graph)
                                       
    def values(self,S,I,R,D):               
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
    
class animation():
    def __init__(self,s_graph,i_graph,r_graph,d_graph,s_grid,i_grid,r_grid,d_grid,edge):
         self.s_graph = s_graph
         self.i_graph = i_graph
         self.r_graph = r_graph
         self.d_graph = d_graph
         self.s_grid = s_grid
         self.i_grid = i_grid
         self.r_grid = r_grid
         self.d_grid = d_grid
         self.edge = edge
         self.hex_grid(self.s_graph,self.i_graph,self.r_graph,self.d_graph,
                 self.s_grid, self.i_grid, self.r_grid, self.d_grid, self.edge)
         self.animate(self.s_graph,self.i_graph,self.r_graph,self.d_graph,
                 self.s_grid, self.i_grid, self.r_grid, self.d_grid, self.edge)
        
    def hex_grid(self,s_graph,i_graph,r_graph,d_graph,s_grid,i_grid,r_grid,d_grid,edge):
        for n in range (len(s_grid)):
            for m in range (len(s_grid[n])):
                s_grid[n][m] = (s_grid[n][m][0]  * 0.5 * (3 ** 0.5),s_grid[n][m][1] )
                if round(s_grid[n][m][0] * 2 * (3**-0.5)) %2 == 0:
                    s_grid[n][m] = (s_grid[n][m][0], s_grid[n][m][1] + 0.5)       
                    
            for m in range (len(i_grid[n])):
                i_grid[n][m] = (i_grid[n][m][0]  * 0.5 * (3 ** 0.5),i_grid[n][m][1] )
                if round(i_grid[n][m][0] * 2 * (3**-0.5)) %2 == 0:
                    i_grid[n][m] = (i_grid[n][m][0], i_grid[n][m][1] + 0.5)
                    
            for m in range (len(r_grid[n])):
                r_grid[n][m] = (r_grid[n][m][0]  * 0.5 * (3 ** 0.5),r_grid[n][m][1] )
                if round(r_grid[n][m][0] * 2 * (3**-0.5)) %2 == 0:
                    r_grid[n][m] = (r_grid[n][m][0], r_grid[n][m][1] + 0.5)
                    
            for m in range (len(d_grid[n])):
                d_grid[n][m] = (d_grid[n][m][0]  * 0.5 * (3 ** 0.5),d_grid[n][m][1] )
                if round(d_grid[n][m][0] * 2 * (3**-0.5)) %2 == 0:
                    d_grid[n][m] = (d_grid[n][m][0], d_grid[n][m][1] + 0.5)       
            
    def animate(self,s_graph,i_graph,r_graph,d_graph,s_data,i_data,r_data,d_data,edge):         
        size = 6.7
        fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(14,size))      
    
        ax2.set_xlim([-1, edge])
        ax2.set_ylim([-1, edge])
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['bottom'].set_visible(False)
        ax2.spines['left'].set_visible(False)
        ax2.xaxis.set_ticklabels([])
        ax2.yaxis.set_ticklabels([])
        ax2.set_xticks([])
        ax2.set_yticks([])
    
        s_scat = ax2.scatter(0,0, s= 2540*(size/edge)**2, c='blue', marker='H')
        i_scat = ax2.scatter(0,0, s= 2540*(size/edge)**2, c='red', marker='H')
        r_scat = ax2.scatter(0,0, s= 2540*(size/edge)**2, c='green', marker='H')
        d_scat = ax2.scatter(0,0, s= 2540*(size/edge)**2, c='black', marker='H')
    
        time = list(range(len(s_graph)))             
    
        s_line, = ax1.plot(time,s_graph, color='b',label='Susceptible')
        i_line, = ax1.plot(time,i_graph, color='r',label='Infected')
        r_line, = ax1.plot(time,r_graph, color='g',label='Removed with immunity')
        d_line, = ax1.plot(time,d_graph, color='k', label='Died')
        
        anim = FuncAnimation(fig, self.update, len(s_graph), interval=20, 
                             blit=True, fargs = [time,s_line,i_line,r_line,
                             d_line,s_scat,i_scat,r_scat,d_scat,self.s_graph,
                             self.i_graph,self.r_graph,self.d_graph,self.s_grid,
                             self.i_grid, self.r_grid, self.d_grid],
                                 repeat = False) 
        ax1.set_xlabel('Time /days')
        ax1.set_ylabel('Number of people')
        ax1.legend(frameon=False,loc='upper center')           
        plt.show()

    def update(self,i,time,s_line,i_line,r_line,d_line,s_scat,i_scat,r_scat,d_scat,
               s_graph,i_graph,r_graph,d_graph,s_grid,i_grid, r_grid, d_grid,):
        s_line.set_data(time[:i], s_graph[:i])
        i_line.set_data(time[:i], i_graph[:i])
        r_line.set_data(time[:i], r_graph[:i])
        d_line.set_data(time[:i], d_graph[:i])
        s_scat.set_offsets(s_grid[i])
        r_scat.set_offsets(r_grid[i])
        i_scat.set_offsets(i_grid[i])
        d_scat.set_offsets(d_grid[i])
        return s_line,i_line,r_line,d_line,s_scat,i_scat,r_scat,d_scat,

main()