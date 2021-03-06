#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:26:22 2022

@author: qa21336
"""

import argparse
from simulation import simulation
import billiard_model

def main(*args):
    """
    The main function is where the whole program operates out of; relevant
    variables are set using argarse for either CLI entry or default values. In
    the case of the hexagonal grid model the simulation class is called with
    its relevant inputs. If the user choses, they can input a name for either
    a gif of the animation or a pdf of the graph
    Consider that some combinations of values can easily result in maximum
    recursion depth

    """
    parser = argparse.ArgumentParser(description='Modelling a pandemic with matrices')
    parser.add_argument('--infection', metavar='P', type=float, default=0.1,
                        help='this the chance a person infects an adjacent person in a day')
    parser.add_argument('--duration', metavar='N', type=int, default=14,
                        help='days until removed')
    parser.add_argument('--death', metavar='P', type=float, default=0.2,
                        help='the chance an infected person dies')
    parser.add_argument('--edge', metavar='N', type=int, default=40,
                        help='size of each side of the hexagonal grid')
    parser.add_argument('--file_1', metavar='N', type=str, default=None,
                        help='Filename to be saved of the SIRD graph of the last day')
    parser.add_argument('--file_2', metavar='N', type=str, default=None,
                        help='Filename to be saved instead of the animation')

    args = parser.parse_args()

    simulation(args.infection, args.duration, args.death, args.edge, args.file_1,args.file_2)
    #call the simulation class in simulation.py with respective inputs
    
main()

billiard_model.run_simulation()