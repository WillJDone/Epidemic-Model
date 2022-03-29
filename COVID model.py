# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 13:33:49 2022

@author: Lox Tyrrell
"""

# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 13:33:49 2022
@author: Lox Tyrrell
"""

import turtle
import numpy as np
import matplotlib.pyplot as plt
import random


wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Epidemic Model")

population = 50
vaccinated = 5
vaccine_protection = 0
infected = 1
infection_distance = 30
population_spread = 15   #25 max
simulation_cycles = 20
recovery_chance = 1/5    # fractions only
min_recovery_time = 5
distance_per_cycle = 10
movement_speed = 0     # 0 = max speed
vaccine_rollout = 5



def decision(probability):    # returns true or false based on probability
    return random.random() < probability

def rand(x,y):
    return np.random.randint(x,y)


class Ball(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("green")
        self.penup()
        self.speed(0)
        self.goto(rand(-9,10)*population_spread,rand(-9,10)*population_spread)
        self.infection_time = 0
        


P=[]
recovered = 0
need_vaccine = vaccinated

susceptible = population - infected

infected_log = [infected]
susceptible_log = [susceptible]
recovered_log = [0]
sim_log = [0]

print(infected_log,susceptible_log)

inf = infected

for i in range(population-infected):
    i = Ball()
    P.append(i)

for i in range(infected):
    i = Ball()
    P.append(i)
    i.color("red")

for x in range(simulation_cycles):
    for i in P:
        i.speed(movement_speed)
        i.goto(i.xcor() + rand(-1,2)*distance_per_cycle,i.ycor() + rand(-1,2)*distance_per_cycle)
    for j in P:
        if j.color() == ("red","red"):
                for k in P:
                    if k.color() == ("green","green") and (j.xcor()-k.xcor())**2 + (j.ycor()-k.ycor())**2 < infection_distance**2:
                      k.color("red")
                      infected += 1
                      susceptible -= 1
                    if k.color() == ("yellow","yellow") and (j.xcor()-k.xcor())**2 + (j.ycor()-k.ycor())**2 < infection_distance**2:
                        if decision(1-vaccine_protection):
                            k.color("red")
                            infected += 1
                            susceptible -= 1    
                if rand(1,1/recovery_chance) == 1 and j.infection_time >= min_recovery_time:
                            j.color("blue")
                            recovered += 1
                            infected -= 1
                j.infection_time += 1
    if x > vaccine_rollout and need_vaccine>0:
        for i in P:
            if i.color() == ("green","green") and need_vaccine > 0:
             i.color("yellow")
             need_vaccine -= 1
     
    infected_log.append(infected)
    susceptible_log.append(susceptible)
    recovered_log.append(recovered)
    sim_log.append(sim_log[-1] + 1)
    print("cycle:",sim_log[-1])
    print("S =",susceptible,"I =",infected,"R =",recovered)

plt.plot(sim_log,infected_log,label = "infected",color = "red")
plt.plot(sim_log,susceptible_log,label = "susceptible",color = "green")
plt.plot(sim_log,recovered_log,label = "recovered", color = "blue")
plt.legend()
plt.show()
