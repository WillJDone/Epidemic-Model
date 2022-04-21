# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 12:23:43 2022

@author: qa21336
"""

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

class animation:
    """
    This class displays an animation of the hexagonal grid and a SIRD on the 
    same figure. In total their are 8 lists of data: SIRD for each the grid
    and graph that are named appropriately. 
    """
    def __init__(self,s_graph,i_graph,r_graph,d_graph,s_grid,i_grid,r_grid,d_grid,edge,file):
        self.s_graph = s_graph
        self.i_graph = i_graph
        self.r_graph = r_graph
        self.d_graph = d_graph
        self.s_grid = s_grid
        self.i_grid = i_grid
        self.r_grid = r_grid
        self.d_grid = d_grid
        self.edge = edge #this is the size of the matrix
        self.hex_grid(self.s_grid, self.i_grid, self.r_grid, self.d_grid, self.edge)
        self.animate(self.s_graph,self.i_graph,self.r_graph,self.d_graph,
                     self.s_grid, self.i_grid, self.r_grid, self.d_grid, self.edge,file)
        
    def hex_grid(self,s_grid,i_grid,r_grid,d_grid,edge):
        """
        This function creates offsets in the data to convert from square
        coordinates to hexagonal data for each: SIRD
        """
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
            
    def animate(self,s_graph,i_graph,r_graph,d_graph,s_data,i_data,r_data,d_data,edge,file):  
        """
        This function plots two separate axes on the same figure: ax1 is the
        animation, a2 is the grid. Then the animation is made using
        FuncAnimation
        """
        fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(14,6.7)) #create figure
    
        ax2.set_xlim([-1, edge]) #set x axis limts
        ax2.set_ylim([-1, edge]) #set y axis limits
        
        #removing unnecessary axes properties for the grid
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['bottom'].set_visible(False)
        ax2.spines['left'].set_visible(False)
        ax2.set_xticks([])
        ax2.set_yticks([])
        
        # set properties of the axes for the SIRD graph
        ax1.set_xlabel('Time /days')
        ax1.set_ylabel('Number of people')
        ax1.legend(frameon=False,loc='upper center')
        
        #set properties of scatter for the grid
        s_scat = ax2.scatter(0,0, s= 85500*(1/edge)**2, c='blue', marker='H')
        i_scat = ax2.scatter(0,0, s= 85500*(1/edge)**2, c='red', marker='H')
        r_scat = ax2.scatter(0,0, s= 85500*(1/edge)**2, c='green', marker='H')
        d_scat = ax2.scatter(0,0, s= 85500*(1/edge)**2, c='black', marker='H')
    
        time = list(range(len(s_graph)))#list of days created for simulation        
    
        #set properties of scatter for the grid
        s_line, = ax1.plot(time,s_graph, color='b',label='Susceptible')
        i_line, = ax1.plot(time,i_graph, color='r',label='Infected')
        r_line, = ax1.plot(time,r_graph, color='g',label='Removed with immunity')
        d_line, = ax1.plot(time,d_graph, color='k', label='Died')
        
        # call FuncAnimation with relevant figure, function, frames and extra arguments 
        anim = FuncAnimation(fig, self.update, len(s_graph), interval=10, 
                             fargs = [time,s_line,i_line,r_line,
                             d_line,s_scat,i_scat,r_scat,d_scat,self.s_graph,
                             self.i_graph,self.r_graph,self.d_graph,self.s_grid,
                             self.i_grid, self.r_grid, self.d_grid]) 

        if file != None:
            anim.save(file+'.gif', fps = 30) #save animation the file name if given
        plt.show()

    def update(self,i,time,s_line,i_line,r_line,d_line,s_scat,i_scat,r_scat,d_scat,
               s_graph,i_graph,r_graph,d_graph,s_grid,i_grid, r_grid, d_grid,):
        """
        For each SIRD of the grid and graph, the next element of the set of 
        data is returned. Moreover, the value of i represents the day. 
        i itself increases by one each time this function is called
        """
        s_line.set_data(time[:i], s_graph[:i])
        i_line.set_data(time[:i], i_graph[:i])
        r_line.set_data(time[:i], r_graph[:i])
        d_line.set_data(time[:i], d_graph[:i])
        s_scat.set_offsets(s_grid[i])
        r_scat.set_offsets(r_grid[i])
        i_scat.set_offsets(i_grid[i])
        d_scat.set_offsets(d_grid[i])
        return s_line,i_line,r_line,d_line,s_scat,i_scat,r_scat,d_scat,