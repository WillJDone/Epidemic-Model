import turtle
import numpy as np
import matplotlib.pyplot as plt
import random

def open_window():    # opens an animation window in the turtle module titled "epidemic model"
    wn = turtle.Screen()
    wn.bgcolor("black")
    wn.title("Epidemic Model")
    return wn

def decision(probability):    # returns true or false based on probability
    return random.random() < probability #random.random() prints a random floating point value between 0 and 1



def rand(x,y): # returns random number between x and y-1
    return np.random.randint(x,y)



def determine_survival(x):      # determines whether an individual will survive based on mortality
        return decision(1-x.mortality)



def generate_population(human,susceptible,infected): # will generate a population of susceptible and infected humans and return a list of the population
        P = []
        for i in range(susceptible):
            i = human()
            i.color("green")
            P.append(i)
    
        for i in range(infected):
            i = human()
            i.color("red")
            determine_survival(i)
            P.append(i)
        return P
    



def infected_visitors(population,infected,Infected_arrival_chance,max_potential_infected_visitors,pop_list,human): # will cause a random number infected visitors to arrive every cycle based on the inputed variables
        if decision(Infected_arrival_chance):
            for z in range(rand(1,max_potential_infected_visitors + 1)): 
                z = human()
                z.color("red")
                pop_list.append(z)
                population += 1
                infected += 1
        return pop_list,population,infected
  
    
  
def move_all(pop_list,movement_speed,distance_per_cycle): # will cause all objects in the population list to move the inputed distance at the inputed speed each cycle
        for i in pop_list:
            i.speed(movement_speed)
            i.goto(i.xcor() + rand(-1,2)*distance_per_cycle,i.ycor() + rand(-1,2)*distance_per_cycle)




def cure_or_kill(pop_list,population,infected,recovered,dead,vaccinated_pop,recovery_chance,min_recovery_time,min_death_time,Full_immunity_period,Immunity_after_recovery,Immunity_after_infected_and_vaccinated,j): # will either cause an individual to recover or die if the requirements for either are met
                        if j.survives == "undetermined":     
                            j.survives = determine_survival(j)
                        if j.survives == True: # will recover if individual does survive, has been infected longer than the minimum recovery time and the random output based on recovery chance is true
                            if decision(recovery_chance) and j.infected_time >= min_recovery_time:
                                        if j.vaccinated:
                                            j.color("yellow")
                                        else:
                                            if Full_immunity_period > 0:
                                             j.color("blue")
                                             j.Full_immunity_period = Full_immunity_period
                                            else:
                                                 j.color("green")
                                        if j.times_infected > 0 and j.vaccinated:
                                            j.immunity = Immunity_after_infected_and_vaccinated
                                        else:
                                            j.immunity = Immunity_after_recovery
                                        j.times_infected += 1
                                        recovered += 1
                                        infected -= 1
                                
                        elif j.survives == False: # will kill individal if it does not survive and has been infected longer than the minimum death time
                                if j.infected_time >= min_death_time:
                                    j.color("grey")
                                    pop_list.remove(j)
                                    population -= 1
                                    infected -= 1
                                    dead += 1
                                    if j.vaccinated:
                                        vaccinated_pop -= 1
                        return pop_list,population,infected,recovered,dead,vaccinated_pop



def within_infection_distance(j,k,infection_distance): # will output True if object j and k are within infection distance of eachother and ouput false if not
    if (j.xcor()-k.xcor())**2 + (j.ycor()-k.ycor())**2 < infection_distance**2:
        return True
    else:
        return False
  
    
def lose_full_immunity(susceptible,recovered,j): # will cause the full immunity period of any recovered individual to decrease by one each cycle and make them susceptible again once that hits 0
                if j.color() == ("blue","blue"):                
                             if j.Full_immunity_period == 0:
                                    j.color("green")
                                    susceptible += 1
                                    recovered -= 1                
                             j.Full_immunity_period -= 1
                return susceptible,recovered
            


def infect_if_exposed(infected,susceptible,Mortality_after_infection,Mortality_after_vaccination,Mortality_after_infection_and_vaccination,infection_distance,j,k): # will infect a susceptible individual if they are within infection distance of an infected individual and the random output based on infectiousness is true
                            
                            if k.color() == ("green","green") and within_infection_distance(j,k,infection_distance) and decision(k.infectiosness): #infects non vaccinated
                                if decision(k.immunity):
                                  k.color("red")                   
                                  k.mortality = Mortality_after_infection
                                  determine_survival(k)
                                  infected += 1
                                  susceptible -= 1
                                  
                                  
                            if k.color() == ("yellow","yellow") and within_infection_distance(j,k,infection_distance) and decision(k.infectiosness): #infects vaccinated
                                    if decision(1-k.immunity):
                                        k.color("red")
                                        infected += 1
                                        susceptible -= 1 
                                        if k.times_infected == 0:
                                            k.mortality = Mortality_after_vaccination
                                        else: 
                                            k.mortality = Mortality_after_infection_and_vaccination
                                        determine_survival(k)
                            return infected,susceptible            
            
def vaccinate(i,Immunity_after_vaccination): # will vaccinate an individual by turning it yellow and increasing its immunity
                            i.color("yellow")
                            i.immunity = Immunity_after_vaccination
                            i.vaccinated = True

def vaccinate_pop(vaccinated_pop,need_vaccine,Total_to_be_vaccinated,vaccine_rollout_time,vaccine_development_time,cycle,pop_list,Immunity_after_vaccination): # will vaccinated a certain number of individuals each cycle until all vaccines have been distributed
            
            vaccinated_per_cycle = round(Total_to_be_vaccinated/vaccine_rollout_time) 
            daily_need_vaccine = vaccinated_per_cycle              
            if cycle >= vaccine_development_time and need_vaccine > 0: 
                for i in pop_list:
                    if i.color() == ("green","green") and need_vaccine > 0 and daily_need_vaccine > 0:
                        vaccinate(i,Immunity_after_vaccination)                                               
                        need_vaccine -= 1
                        daily_need_vaccine -= 1
                        vaccinated_pop += 1
                
            return vaccinated_pop,need_vaccine
        
        
def update_infected_stats(j,Immunity_decrease_per_cycle): # will update instance variables each cycle 
                        j.infected_time += 1
                        if j.immunity > 0: 
                            j.immunity -= Immunity_decrease_per_cycle
                            

def log_data(infected,susceptible,vaccinated_pop,dead,recovered,infected_log,susceptible_log,vaccinated_log,dead_log,recovered_log,sim_log): # will log the data each cycle that will be used to create the graph at the end of the simulation 
            infected_log.append(infected)
            susceptible_log.append(susceptible)        
            vaccinated_log.append(vaccinated_pop)
            dead_log.append(dead)
            recovered_log.append(recovered)
            sim_log.append(sim_log[-1] + 1)
            return infected_log,susceptible_log,vaccinated_log,dead_log,recovered_log,sim_log

def print_data(susceptible,infected,recovered,population,dead,vaccinated_pop,sim_log): # will print simulation data each cycle
            print("cycle:",sim_log[-1])
            print("S =",susceptible,"I =",infected,"R =",recovered, "P =", population, "D =", dead, "V =", vaccinated_pop)
  
            
  
    
  
    
def plot_graph(sim_log,infected_log,susceptible_log,recovered_log,vaccinated_log,dead_log): # will plot a graph of the cycle on the x axis and simulation data on the y aixis
    plt.plot(sim_log,infected_log,label = "infected",color = "red")
    plt.plot(sim_log,susceptible_log,label = "susceptible",color = "green")
    plt.plot(sim_log,recovered_log,label = "recovered", color = "blue")
    plt.plot(sim_log,vaccinated_log,label = "vaccinated", color = "yellow")
    plt.plot(sim_log,dead_log,label = "dead", color = "black")
    plt.legend()
    plt.show() 
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
def run_simulation():  # runs the entire simulation
    #vaccines
    
    need_vaccine = 10                    # the number of people who will be eventually vaccinated or number of available vaccines
    vaccine_development_time = 2         # the number of cycles before individuals get vaccinated
    vaccine_rollout_time = 10            # the time over which all vaccines are distributed
    
    
    
    #population stats
    population = 100                      # the initial population
    infected = 2                          # initial number of infected people
    population_spread = 15                # multiplier the distance over which individuals are able to spawn, 25 max for individuals to be remain within animation window
     
    
    
    
    
    #simulation parameters
    simulation_cycles = 20                # number of times each individual will move once in simulation
    movement_speed = 0                    # 0 = max speed
    distance_per_cycle = 10               # max distance moved by individuals each cycle
    Infected_arrival_chance = 0.01        # the probability that each cycle, additional infected individuals will be added the population
    max_potential_infected_visitors = 10  # the maximum number of infected individuals 
    
    
    #covid stats
    infection_distance = 30                                  # distance that susceptible individuals have to be within an infected one in order to get infected
    infectiosness = 0.8                                      # probability of transmitting virus if in range
    recovery_chance = 1/3                                    # the chance that an infected person will recover each cycle
    min_recovery_time = 5                                    # mininum number of cycles after infection that an infected individual can recover
    Covid_mortality = 0.02                                   # probability an infected individual will die
    Mortality_after_infection = 0.001                        # probability a recovered individual will die when reinfected
    Mortality_after_vaccination = 0.0005                     # probability a vaccinated infected individual will die
    Mortality_after_infection_and_vaccination = 0.0001       # probability a recovered vaccinated individual will die after reinfection
    min_death_time = 5                                       # minimum number of cycles after being infected that an individual can die
    Full_immunity_period = 20                                # amount of time that a recovered individual will have full immunity
    Immunity_after_recovery = 0.7                            # probability that a recovered individual will get infected if exposed to the virus
    Immunity_after_vaccination = 0.92                        # probability that a vaccinated individual will get infected if exposed to the virus
    Immunity_after_infected_and_vaccinated = 0.97            # probability that a recovered and vaccinated individual will get infected if exposed to the virus
    Immunity_decrease_per_cycle = 0.002                      # the amount that immunity decreases by each cycle
    
    
    
    
    
    susceptible = population - infected # these variables and lists are being assigned their default values
    infected_log = [infected]
    susceptible_log = [susceptible]
    recovered_log = [0]
    vaccinated_log = [0]
    dead_log = [0]    
    sim_log = [0]
    vaccinated_pop = 0
    Total_to_be_vaccinated = need_vaccine
    recovered = 0
    dead = 0
    
    
    class human(turtle.Turtle): #A ball represents a human in our simulation
        def __init__(self): 
            turtle.Turtle.__init__(self)
            
            self.shape("circle")
            self.color()
            self.penup() # stops balls from leaving a line when moving
            self.speed(0) # speed of 0 moves ball instantly
            self.goto(rand(-9,10)*population_spread,rand(-9,10)*population_spread) # balls sent to random location when generated
            
            self.infected_time = 0              # time that an individual has been infected for
            self.immunity = 0                   # all individuals start off with no immunity
            self.vaccinated = False              
            self.times_infected = 0             # number of times an individual has been infected
            self.infectiosness = infectiosness   
            self.mortality = Covid_mortality
            self.Full_immunity_period = 0
            self.survives = "undetermined"
    
    wn = open_window()
    
    

    pop_list = generate_population(human,susceptible,infected)    #pop_list  = list containing all objects in simulation

    print("Initial infected:",infected_log,"Population:",population)
    
    
    
    
    
    
    for cycle in range(simulation_cycles):
        
        pop_list,population,infected = infected_visitors(population,infected,Infected_arrival_chance,max_potential_infected_visitors,pop_list,human)   
        move_all(pop_list,movement_speed,distance_per_cycle)                                                                                                            
                 
        for j in pop_list:  # runs through each member of population
            if j.color() == ("red","red"):  
                
                    for k in pop_list:   # compares each infected individual to each member of the population
                        infected,susceptible = infect_if_exposed(infected,susceptible,Mortality_after_infection,Mortality_after_vaccination,Mortality_after_infection_and_vaccination,infection_distance,j,k)
                        
                    pop_list,population,infected,recovered,dead,vaccinated_pop = cure_or_kill(pop_list,population,infected,recovered,dead,vaccinated_pop,recovery_chance,min_recovery_time,min_death_time,Full_immunity_period,Immunity_after_recovery,Immunity_after_infected_and_vaccinated,j)              
                    update_infected_stats(j,Immunity_decrease_per_cycle)
                    
            susceptible,recovered = lose_full_immunity(susceptible,recovered,j)
        
        
        vaccinated_pop,need_vaccine = vaccinate_pop(vaccinated_pop,need_vaccine,Total_to_be_vaccinated,vaccine_rollout_time,vaccine_development_time,cycle,pop_list,Immunity_after_vaccination)
        infected_log,susceptible_log,vaccinated_log,dead_log,recovered_log,sim_log = log_data(infected,susceptible,vaccinated_pop,dead,recovered,infected_log,susceptible_log,vaccinated_log,dead_log,recovered_log,sim_log)         
        print_data(susceptible,infected,recovered,population,dead,vaccinated_pop,sim_log)
        
    plot_graph(sim_log, infected_log, susceptible_log, recovered_log,vaccinated_log,dead_log)
    wn.mainloop()  # causes program to only terminate when window closes
    
    
