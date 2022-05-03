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
                        if j.survives == "undetermined":      #will decide whether an individual will survive if its survival is undetermined
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
            
def vaccinate(i,Immunity_after_vaccination):
                            i.color("yellow")
                            i.immunity = Immunity_after_vaccination
                            i.vaccinated = True

def vaccinate_pop(vaccinated_pop,need_vaccine,Total_to_be_vaccinated,vaccine_rollout_time,vaccine_development_time,cycle,pop_list,Immunity_after_vaccination):
            
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
        
        
def update_infected_stats(j,Immunity_decrease_per_cycle):
                        j.infected_time += 1
                        if j.immunity > 0: 
                            j.immunity -= Immunity_decrease_per_cycle
                            

def log_data(infected,susceptible,vaccinated_pop,dead,recovered,infected_log,susceptible_log,vaccinated_log,dead_log,recovered_log,sim_log):
            infected_log.append(infected)
            susceptible_log.append(susceptible)        
            vaccinated_log.append(vaccinated_pop)
            dead_log.append(dead)
            recovered_log.append(recovered)
            sim_log.append(sim_log[-1] + 1)
            return infected_log,susceptible_log,vaccinated_log,dead_log,recovered_log,sim_log

def print_data(susceptible,infected,recovered,population,dead,vaccinated_pop,sim_log):
            print("cycle:",sim_log[-1])
            print("S =",susceptible,"I =",infected,"R =",recovered, "P =", population, "D =", dead, "V =", vaccinated_pop)
            
def run_simulation():
    #vaccines
    need_vaccine = 10
    
    vaccine_development_time = 2
    vaccine_rollout_time = 10
    vaccinated_pop = 0
    
    
    
    #population stats
    population = 50
    infected = 2
    dead = 0
    recovered = 0 
    
    
    
    
    #simulation parameters
    simulation_cycles = 20
    movement_speed = 0     # 0 = max speed
    distance_per_cycle = 10
    Infected_arrival_chance = 0.01
    max_potential_infected_visitors = 10
    population_spread = 15  #25 max
    
    #covid stats
    infection_distance = 30
    infectiosness = 0.8 #probability of transmitting it if in range
    recovery_chance = 1/3    
    min_recovery_time = 5
    Covid_mortality = 0.02
    Mortality_after_infection = 0.001
    Mortality_after_vaccination = 0.0005
    Mortality_after_infection_and_vaccination = 0.0001
    min_death_time = 5
    Full_immunity_period = 20 
    Immunity_after_recovery = 0.7
    Immunity_after_vaccination = 0.92
    Immunity_after_infected_and_vaccinated = 0.97
    Immunity_decrease_per_cycle = 0.002
    
    
    
    
    
    susceptible = population - infected
    infected_log = [infected]
    susceptible_log = [susceptible]
    recovered_log = [0]
    vaccinated_log = [0]
    dead_log = [0]    
    sim_log = [0]
    vaccinated_pop = 0
    Total_to_be_vaccinated = need_vaccine
    
    
    class human(turtle.Turtle): #A ball represents a human in our simulation
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
            
        
        
        
        
        
        for j in pop_list:
            if j.color() == ("red","red"):                
                    for k in pop_list:
                        infected,susceptible = infect_if_exposed(infected,susceptible,Mortality_after_infection,Mortality_after_vaccination,Mortality_after_infection_and_vaccination,infection_distance,j,k)
                        
                    pop_list,population,infected,recovered,dead,vaccinated_pop = cure_or_kill(pop_list,population,infected,recovered,dead,vaccinated_pop,recovery_chance,min_recovery_time,min_death_time,Full_immunity_period,Immunity_after_recovery,Immunity_after_infected_and_vaccinated,j)              
                                    
                    
                                    
                    
                    
                    update_infected_stats(j,Immunity_decrease_per_cycle)



            susceptible,recovered = lose_full_immunity(susceptible,recovered,j)
        
        
        vaccinated_pop,need_vaccine = vaccinate_pop(vaccinated_pop,need_vaccine,Total_to_be_vaccinated,vaccine_rollout_time,vaccine_development_time,cycle,pop_list,Immunity_after_vaccination)
        

        
        
    
    
        infected_log,susceptible_log,vaccinated_log,dead_log,recovered_log,sim_log = log_data(infected,susceptible,vaccinated_pop,dead,recovered,infected_log,susceptible_log,vaccinated_log,dead_log,recovered_log,sim_log)
        
        
        print_data(susceptible,infected,recovered,population,dead,vaccinated_pop,sim_log)
    plot_graph(sim_log, infected_log, susceptible_log, recovered_log,vaccinated_log,dead_log)
    wn.mainloop()
    
    
    
    
    
    
    
    
    
def plot_graph(sim_log,infected_log,susceptible_log,recovered_log,vaccinated_log,dead_log):
    plt.plot(sim_log,infected_log,label = "infected",color = "red")
    plt.plot(sim_log,susceptible_log,label = "susceptible",color = "green")
    plt.plot(sim_log,recovered_log,label = "recovered", color = "blue")
    plt.plot(sim_log,vaccinated_log,label = "vaccinated", color = "yellow")
    plt.plot(sim_log,dead_log,label = "dead", color = "black")
    plt.legend()
    plt.show()

run_simulation()


