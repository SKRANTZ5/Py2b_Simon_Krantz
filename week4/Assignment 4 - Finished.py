# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 08:38:23 2023

@author: SKRANTZ5
"""

import numpy as np
import random


class Person:
    def __init__(self):
        self.recover_prob = 0.2
        self.die_prob = 0.05
        self.infect_other_prob = 0.05  # Prop of spreading the varus
        self.average_meetups = 10  # Avg people you meet in a day
        self.init_sick_prob = 0.1
        self.days_sick = 0  # Counter for amount of days spent sick, init 0
        self.vaccinated = False  # Flag if person has gotten vacced
        self.recovered = False
        self.dead = False
        self.sick = False

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

        if self.sick == True:  # Sick person
            self.days_sick += 1  # Increment days spent sick
            if init_scenario == False:  # Not first day
                self.infect_others(population)  # Spread the varus

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
        person_encounters = random.sample(
            range(population.size), self.average_meetups
        )
        for person_id in person_encounters:
            prob = random.random()  # Gen a prob
            if (
                prob <= self.infect_other_prob
                and population[person_id].dead == False
                and population[person_id].recovered == False
                and population[person_id].sick == False
                and population[person_id].vaccinated == False
            ):
                population[person_id].sick = True  # Person gets infected


class Village:
    def __init__(self, init_population_size):
        self.population = np.empty(init_population_size, Person)
        self.init_vaccination = (
            0.2 * init_population_size
        )  # How many sick until vac starts
        self.vaccination_started = False  # Flag for when vacc starts going out
        self.daily_vaccination_threshold = (
            0.04 * init_population_size
        )  # How many that can get vacced per day
        self.generate_inhabitants()

    def generate_inhabitants(self):
        """Generates the population"""
        for i in range(self.population.size):
            self.population[i] = Person()

    def vaccinate_population(self):
        people_vaccinated_today = 0  # Init counter for the day
        for person_id in range(self.population.size):
            if people_vaccinated_today == self.daily_vaccination_threshold:  # No more vacc today
                break
            elif self.population[person_id].sick == False and self.population[person_id].dead == False and self.population[person_id].vaccinated == False:
                self.population[person_id].vaccinated = True  # Set flag to true
                people_vaccinated_today += 1  # Inc count
    
    def advance_days(self, init_scenario=False):
        """Counts the status of the citizens in the community"""
        people_sick = 0
        people_recovered = 0
        people_dead = 0
        people_vaccinated = 0  # Counter for amount vacced
        for person in self.population:
            if person.sick == True:
                people_sick += 1
            elif person.recovered == True:
                people_recovered += 1
            elif person.dead == True:
                people_dead += 1
            elif person.vaccinated == True:  # Person is vacced
                people_vaccinated += 1  # Inc count

            person.day_passes(self.population, init_scenario)
            
        if (
            people_sick >= self.init_vaccination and self.vaccination_started == False
        ):  # Threshold for started vacc reached
            self.vaccination_started = True  # set flag to true
            print(
                f"At the end of the day {people_sick} people were sick, and vaccination has started"
            )
        if self.vaccination_started == True:  # Threshold reached
            self.vaccinate_population()  # Vaccinate people

        return people_sick, people_recovered, people_dead, people_vaccinated

    def start_simulation(self):
        """This function controls the simulation and what happends in a day"""
        current_day = 0

        people_sick, people_recovered, people_dead, people_vaccinated = self.advance_days(
            init_scenario=True
        )
        while people_sick != 0:
            print(
                f"By day {current_day}: {people_sick} people are sick, {people_dead} are dead and {people_recovered} has recovered"
            )
            current_day += 1
            people_sick, people_recovered, people_dead, people_vaccinated = self.advance_days()

        days_sick_list = []  # Init empty list
        for person_id in range(self.population.size):  # Loop through the pop
            days_sick_list.append(self.population[person_id].days_sick)
        people_unaffected = self.population.size - (
            people_sick + people_recovered + people_dead
        )
        print(
            f"\nBy day {current_day}: {people_sick} people are sick, {people_dead} are dead and {people_recovered} has recovered. {people_unaffected} people were never in contact with the virus"
        )
        print("The village has recovered and the virus is eliminated!")
        print(
            f"\nThe most amount of days spent sick is: {max(days_sick_list)} days"
        )
        print(
            f"\nThe average days spent sick is {sum(days_sick_list)/len(days_sick_list)}"
        )


def main():
    pop_size = 1000
    village = Village(pop_size)
    village.start_simulation()


main()
