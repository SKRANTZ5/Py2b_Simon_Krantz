# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:12:49 2023

@author: SKRANTZ5
"""

#matplotlib inline
import numpy as np
import pandas as pd
import random

from IPython.display import display, HTML

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

class Person:
    def __init__(self):
        self.recover_prob = 0.2
        self.die_prob = 0.05
        self.init_sick_prob = 0.1
        self.infect_others_prob = 0.05
        self.vaccinated = False
        self.recovered = False
        self.dead = False
        self.sick = False
        
        self.average_meetups = 10
        self.days_sick = 0
        self.init_sick_or_not()
        
    def init_sick_or_not(self):
        """When created each person starts as either sick or healthy"""
        prob = random.random()
        if prob <= self.init_sick_prob:
            # This should yield that about 10% of the people created are sick, the rest healthy
            self.sick = True
        else:
            self.sick = False
    
    def day_passes(self, population, init_scenario):
        """This method describes what happends to each person each day"""
        if self.sick == True:
            self.days_sick += 1
            if init_scenario == False:
                self.infect_others(population)
        
        # Will person recover?
        prob = random.random()
        if prob <= self.recover_prob and self.sick == True:
            # Person has rehabilitated and is now healthy!
            self.sick = False
            self.recovered = True 
        
        # If person is still sick they might die
        prob = random.random()
        if prob <= self.die_prob and self.sick == True:
            self.dead = True
            self.sick = False
            
    def infect_others(self, population):
        person_encounters = random.sample(range(population.size), self.average_meetups)
        for person_id in person_encounters:
            prob = random.random()
            person = population[person_id]
            if prob <= self.infect_others_prob and person.dead == False and person.recovered == False and person.vaccinated == False:
                population[person_id].sick = True  

class Village:
    def __init__(self, init_population_size):
        self.population = np.empty(init_population_size, Person)
        self.init_vaccination = 0.2 * init_population_size
        self.daily_vaccination_threshold = 0.04 * init_population_size
        self.vaccination_started = False
        self.generate_inhabitants()
        
        
    def advance_days(self, init_scenario = False):
        """Counts the status of the citizens in the community"""
        people_sick = 0
        people_recovered = 0
        people_dead = 0
        people_vaccinated = 0     
        people_immune = 0
        
        for person in self.population:
            if person.sick == True:
                people_sick += 1
            if person.dead == True:
                people_dead += 1
                
            if person.recovered == True and person.vaccinated == True:
                people_recovered += 1
                people_vaccinated += 1
                people_immune += 1
            elif person.vaccinated == True:
                people_vaccinated += 1
                people_immune += 1
            elif person.recovered == True:
                people_recovered += 1 
                people_immune += 1
            
            person.day_passes(self.population, init_scenario)
        
        people_susceptible = self.population.size - (people_immune + people_dead + people_sick)
        
        if people_sick >= self.init_vaccination and self.vaccination_started == False:
            print(f"Vaccination has started! At the end of the day {people_sick} are sick and the community is on the alert")
            self.vaccination_started = True
            
        if self.vaccination_started == True:
            self.vaccinate_population()
            
        return people_sick, people_recovered, people_dead, people_vaccinated, people_immune, people_susceptible
    
    def generate_inhabitants(self):
        """Generates the population"""
        for i in range(self.population.size):
            self.population[i] = Person()
            
    def vaccinate_population(self):
        people_vaccinated_today = 0
        
        for person in self.population:
            if people_vaccinated_today == self.daily_vaccination_threshold:
                break
            elif person.sick == False and person.dead == False and person.vaccinated == False:
                person.vaccinated = True
                people_vaccinated_today += 1
                
    def gen_df_and_save(self, day_data_arr):
        col = ["Sick", "Recovered", "Deceased", "Vaccinated", "Immune", "Susceptible"]
        df = pd.DataFrame(day_data_arr, columns = col)
        #display(df)
        df.to_csv('my_ass5_dataset.csv', index = False)
    
    def start_simulation(self):
        """This function controls the simulation and what happends in a day"""
        
        current_day = 0
        day_data_list = []
        
    
        people_sick, people_recovered, people_dead, people_vaccinated, people_immune, people_susceptible = self.advance_days(init_scenario = True)

        day_data = [people_sick, people_recovered, people_dead, people_vaccinated, people_immune, people_susceptible]
        day_data_list.append(day_data)
        while people_sick != 0:
            print(f"By day {current_day} {people_sick} people are sick, {people_recovered} has recovered and {people_dead} are dead.")
            current_day += 1
            
            people_sick, people_recovered, people_dead, people_vaccinated, people_immune, people_susceptible = self.advance_days()
            
            day_data = [people_sick, people_recovered, people_dead, people_vaccinated, people_immune, people_susceptible]
            day_data_list.append(day_data)
            
        # The village is free of the virus, simulation ended
        days_sick = [person.days_sick for person in self.population]
        day_data_arr = np.array(day_data_list)
        print(day_data_arr)
        self.gen_df_and_save(day_data_arr)
        
        print("\n-------END OF SIMULATION-------")
        print(f"By day {current_day} {people_sick} people are sick, {people_recovered} has recovered and {people_dead} are dead.")
        print(f"In total {people_vaccinated} people recieved vaccination and {people_susceptible} remain susceptible to the virus.")
        print("--------------")
        print("The village has recovered and the virus is eliminated!")
        print("The longest time an individual was sick is: ", max(days_sick), "days")
        
    # def ploter(self):
    #     df = pd.read_csv('my_ass5_dataset.csv')
    #     rows = len(df)
    #     display(df)
# TODO
def plot_data():
    """This function plots the data of each column in the csv file"""
    df = pd.read_csv('my_ass5_dataset.csv')
    days = len(df)
    x = np.linspace(0, days-1, days)
    plt.xlabel("Day")
    plt.ylabel("Population")
    plt.xlim([-10, days])
    
    for col in df.columns:
        plt.plot(x, df[col])
        plt.legend(df.columns)
    

plot_data() 

       
def main():
    pop_size = 1000
    village = Village(pop_size)
    village.start_simulation()

main()

                
        
        

