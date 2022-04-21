# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 16:48:35 2022

@author: qa21336
"""

from matplotlib import pyplot as plt

def plot(s_graph,i_graph,r_graph,d_graph,file):
    """
    If the user has decided to input a file name, the data of the frame of the 
    graph animation is plotted and saved with the respective name as a pdf
    """
    if file != None:
        fig = plt.figure()
        ax = plt.axes()
        ax.plot(s_graph,color='b',label='Susceptible')
        ax.plot(i_graph,color='r',label='Infected')
        ax.plot(r_graph,color='g',label='Removed with immunity')
        ax.plot(d_graph,color='k', label='Died')
        ax.set_xlabel('Time /days')
        ax.set_ylabel('Number of people')
        ax.legend(frameon=False,loc='right',prop={'size':6})
        fig.savefig(file+'.pdf')
        plt.close()