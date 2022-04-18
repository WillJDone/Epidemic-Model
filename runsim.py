#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:26:22 2022

@author: qa21336
"""

import argparse
from simulation import simulation

def main(*args):
    parser = argparse.ArgumentParser(description='Modelling a pandemic with matrices')
    parser.add_argument('--infection', metavar='P', type=int, default=0.1,
                        help='this the chance a person infects an adjacent person in a day')
    parser.add_argument('--duration', metavar='N', type=int, default=14,
                        help='days until removed')
    parser.add_argument('--death', metavar='P', type=float, default=0.2,
                        help='the chance an infected person dies')
    parser.add_argument('--edge', metavar='N', type=float, default=40,
                        help='size of side of square matrix')
    parser.add_argument('--file_1', metavar='N', type=str, default=None,
                        help='Filename to be saved of the SIRD graph of the last day')
    parser.add_argument('--file_2', metavar='N', type=str, default=None,
                        help='Filename to be saved instead of the animation')

    args = parser.parse_args()

    simulation(args.infection, args.duration, args.death, args.edge, args.file_1,args.file_2)
    
main()