import random

class Biot:

    def __init__(self, speed, amb, sense):
        """Spawn in with a handful of genes"""
        self.speed = speed
        self.ambition = amb
        self.sense = sense
        """Non-genetic attributes"""
        self.coords = (0, 0)
        self.food_gathered = 0
        self.metabolism = self.speed * self.ambition

    def __str__(self):
        return("Biot with genes %d %d %d" % (self.speed, self.ambition, self.sense))

    def place(self, coords):
        """Places a Biot somewhere"""
        self.coords = coords

    def does_survive(self):
        """Biot gets to survive if it finds the food it costs to live"""
        return self.food_gathered > self.metabolism

    def does_reproduce(self):
        """Biot gets to reproduce if it's strong enough to find double
        the needed survival food."""
        return self.food_gathered > 2*self.metabolism

    def mutate(self):
        """All genes have a chance of changing by a small amount"""
        "TODO"
        return



class Field:
    """The environment that the Neets live and compete in. Sized 100x100."""

    def __init__(self, population):
        self.population = []
        self.current_time = 0
        self.foods = [] #list of tuples, will dissapear when eaten

    def food_within_view(self, neet):
        """returns the X and Y of a food, or None if none are within sense range"""
        return

    def first_place_population():
        """randomly place all the neets on the edge of the map"""
        return


    def create_food(self):
        """Randomly place food pellets on the map"""
        return

    def step(self):
        """every Biot makes a move, random order, and will eat if possible"""
        return

    def day(self):
        """Run through a day, making 30 steps, then killing the weak and
        mutating the survivors."""
        for r in range(0, 30):
            self.step()

        survivors = [g if g.does_survive() else None for g in self.population]
        mutants = [mutate(g) for g in survivors]
        self.population = mutants

    def simulate(self, days):
        """Run the simulation forward for some number of days, or generations"""
        for r in range(0, days):
            self.day()

        return

    def population_report(self):
        print(self.population)


species = [Biot(1, 1, 1)] * 40 #start with a simple group
environment = Field(species)

environment.simulate(30)
print(environment.population_report())
