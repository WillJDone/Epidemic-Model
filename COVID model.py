import turtle
import numpy as np
import matplotlib.pyplot as plt
import random

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Epidemic Model")

def decision(probability):    # returns true or false based on probability
    return random.random() < probability

def rand(x,y): # returns random number between x and y
    return np.random.randint(x,y)

#vaccines
vaccinated = 150
need_vaccine = vaccinated
vaccine_rollout = 10
v = 0

#population stats
population = 170
infected = 20
population_spread = 20  #25 max
Dead = 0
recovered = 0
susceptible = population - infected - Dead

#simulation parameters
simulation_cycles = 40
movement_speed = 0     # 0 = max speed
distance_per_cycle = 10
Infected_arrival_chance = 0
max_potential_infected_visitors = 10

#covid stats
infection_distance = 30
recovery_chance = 1/5    # fractions only
min_recovery_time = 5
Covid_mortality = 0.01
Death_clock = rand(14,32)
Immunity_after_recovery = 0.7
Immunity_after_vaccination = 0.92
Immunity_after_infected_and_vaccinated = 0.97
Immunity_decrease_per_cycle = 0.0



class Ball(turtle.Turtle): #A ball represents a human in our simulation
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color()
        self.penup()
        self.speed(0)
        self.goto(rand(-9,10)*population_spread,rand(-9,10)*population_spread)
        self.infected_time = 0
        self.immunity = 0
        self.vaccinated = False
        self.times_infected = 0


P=[] #list containing all objects in simulation


infected_log = [infected]
susceptible_log = [susceptible]
recovered_log = [0]
sim_log = [0]

print(infected_log,susceptible_log)



for i in range(population-infected):
    i = Ball()
    i.color("green")
    P.append(i)

for i in range(infected):
    i = Ball()
    i.color("red")
    P.append(i)

for x in range(simulation_cycles):
    if decision(Infected_arrival_chance):
        for z in range(rand(1,max_potential_infected_visitors + 1)):
            z = Ball()
            z.color("red")
            P.append(z)
            population += 1
            infected += 1
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
                        if decision(1-k.immunity):
                            k.color("red")
                            infected += 1
                            susceptible -= 1 
                    if k.color() == ("blue","blue") and (j.xcor()-k.xcor())**2 + (j.ycor()-k.ycor())**2 < infection_distance**2:
                        if decision(1-k.immunity):
                            k.color("red")
                            infected += 1
                            susceptible -= 1
                            k.infected_time = 0
                if rand(1,1/recovery_chance) == 1 and j.infected_time >= min_recovery_time:
                    if decision(1-Covid_mortality): 
                            if j.vaccinated:
                                j.color("yellow")
                            else:
                                j.color("blue")
                            if j.times_infected > 0 and j.vaccinated:
                                j.immunity = Immunity_after_infected_and_vaccinated
                            else:
                                j.immunity = Immunity_after_recovery
                            j.times_infected += 1
                            recovered += 1
                            infected -= 1
                        
                    else: 
                        if j.infected_time >= Death_clock:
                            j.color("grey")
                            j.speed(0)
                            P.remove(j)
                            population -= 1
                            infected -= 1
                            Dead += 1
                j.infected_time += 1
                if j.immunity < 0: 
                    j.immunity -= Immunity_decrease_per_cycle
                

            
    if x >= vaccine_rollout and need_vaccine > 0:
        for i in P:
            if i.color() == ("green","green") or i.color() == ("blue","blue") and need_vaccine > 0:
                i.color("yellow")
                i.immunity = Immunity_after_vaccination
                i.vaccinated = True
                need_vaccine -= 1
                v += 1
     
    infected_log.append(infected)
    susceptible_log.append(susceptible)
    recovered_log.append(recovered)
    sim_log.append(sim_log[-1] + 1)
    print("cycle:",sim_log[-1])
    print("S =",susceptible,"I =",infected,"R =",recovered, "P =", population, "D =", Dead, "V =", v)

plt.plot(sim_log,infected_log,label = "infected",color = "red")
plt.plot(sim_log,susceptible_log,label = "susceptible",color = "green")
plt.plot(sim_log,recovered_log,label = "recovered", color = "blue")
plt.legend()
plt.show()

