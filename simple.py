import random
import math
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def av(a, b):
    return((a+b)/2)

def mate(a, b):
    """Reproduce two biots by averaging their traits!"""
    name = (a.name) #sorry parent 2
    return(Biot(name, av(a.speed, b.speed), av(a.amb, b.amb), av(a.sense, b.sense)).mutateBiot())

class Biot:

    def __init__(self, name, speed, amb, sense):
        """Spawn in with a handful of genes"""
        self.name = name #for debugging
        self.speed = speed*5 #Distance covered in 1 step
        self.amb = amb #Ambition is the probability that biot will go for reproduction
        self.sense = sense #how many steps away can food be seen from
        """Non-genetic attributes"""
        self.coords = (0, 0)
        self.eaten = 0
        self.mtb = (self.speed/5 * self.sense) + 1
        """Behavioral Flags"""
        self.searching = False #Looking for Food #2
        self.retreating = False #Done eating, retreating to safe area
        self.done = False #Biot has made it's moves for this day

    def __str__(self):
        return("Biot named %s, genes (%.2lf %.2lf %.2lf), fd/mtb = (%.2lf/%.2lf)" % (self.name, self.speed, self.amb, self.sense, self.eaten, self.mtb))

    def debug(self):
        return ("COORDS: " + str(self.coords))

    def place(self, coords):
        """Places a Biot somewhere"""
        self.coords = coords

    def move(self, move):
        """ADD distance, not PLACE!"""
        self.place((self.coords[0] + move[0], self.coords[1]+move[1]))
        return

    def step_searching(self, foods):
        """Make a move either towards food or nowhere"""
        for r in foods:
            if (distance(self.coords, r) < self.sense*5) and (self.eaten < self.mtb * 2):
                ate = True
                self.place(r)
                self.eaten += 1
                return r

        #No food discovered, random step - but INSIDE the play area
        rads = random.random() * 2 * math.pi
        x, y = self.coords

        dx, dy = (math.cos(rads)*self.speed, math.sin(rads)*self.speed)
        while not (0 <= x+dx <= 100 and 0 <= y+dy <= 100):
            rads = random.random() * 2 * math.pi
            dx, dy = (math.cos(rads)*self.speed, math.sin(rads)*self.speed)
        self.move((dx, dy))
        return None

    def step_retreating(self):
        """Steps in the best direction towards the edge of the map.
        Label the edges: Top=1, Right=2, Low=3, Left=4"""
        if self.done:
            return
        x, y = self.coords

        if (y>x and y > 100-x): #top edge
            target = (x, 100)
        elif (y>x and y < 100-x): #left edge
            target = (0, y)
        elif (y < x and y > 100-x): #right edge
            target = (100, y)
        else:
            target = (x, 0)

        #If we're within one step of the edge
        if distance(self.coords, target) < 5*self.speed:
            self.move(target)
            self.done = True
            return
        else:
            if target == (x, 100):
                self.move(0, 5*self.speed)
            if target == (0, y):
                self.move(((-5*self.speed), 0))
            if target == (x, 0):
                self.move((0, (-5*self.speed)))
            if target == (100, y):
                self.move(((5*self.speed), 0))
            return

    def roam(self, foods):
        """
        -IF no survival food yet:
            survival search
            IF we eat:
                roll for ambition
                IF ambitious:
                    flag: ambitious search
                ELSE
                    flag: retreat
            IF we don't:
                flag: survive
        -IF survival food met:
            IF ambitious:
                search
                IF food nearby:
                    Eat
                    flag: go home
        Return coords of food eaten OR None if none eaten
        """

        if (self.done):
            return None

        if self.eaten < self.mtb: #IF we won't survive yet
            e = self.step_searching(foods)
            if not e == None: #IF we eat
                if (random.random() < self.amb):
                    self.searching = True
                    return e
                    #print("Biot %s is ambitious, searches for more food" % (self.name))
                else:
                    self.retreating = True
                    return e
                    #print("Biot %s is not ambitious, retreats to edge" % (self.name))
            else:
                return None
        elif self.searching:
            e = self.step_searching(foods)
            if not e == None:
                self.retreating = True
                return e
            else:
                return None
        elif self.retreating:
            self.step_retreating()
            return None

    def does_survive(self):
        """Biot gets to survive if it finds the food it costs to live"""
        #return (self.on_edge() and not self.does_starve())
        return not self.does_starve()

    def on_edge(self):
        x, y = self.coords
        return (x % 100 == 0 or y % 100 == 0)

    def does_starve(self):
        return self.eaten < self.mtb

    def does_reproduce(self):
        """Biot gets to reproduce if it's strong enough to find double
        the needed survival food."""
        return self.eaten >= 2*self.mtb

    def mutateTrait(self, trait):
        return max(0, np.random.normal(trait, trait/15, 1)) #normal dist chance of moving by SD 1/10th from current spot

    def mutateBiot(self):
        """All genes have a chance of changing by a small amount"""
        "TODO"
        newSpeed =  self.mutateTrait(self.speed)
        newAmb =    self.mutateTrait(self.amb)
        newSense =  self.mutateTrait(self.sense)
        offspring = Biot(self.name, newSpeed, newAmb, newSense)
        return offspring

    def refresh(self):
        """Reset searching variables for a new day of foraging"""
        self.eaten = 0
        self.searching = False
        self.done = False
        self.retreating = False
        return

class Field:
    """The environment that the Neets live and compete in. Sized 100x100."""

    def __init__(self, population):
        self.population = population
        self.current_time = 0
        self.foods = []

        """Historical values: for plotting"""
        self.t_pop = []
        self.t_speed = []
        self.t_sense = []
        self.t_mtb = []

    def first_place_population(self):
        """randomly place all the neets on the edge of the map"""
        for r in range(0, len(self.population)):
            edge = random.randint(0, 3)
            if edge == 0:
                self.population[r].place((0, random.randint(0, 100)))
            elif edge == 1:
                self.population[r].place((100, random.randint(0, 100)))
            elif edge == 2:
                self.population[r].place((random.randint(0, 100), 0))
            elif edge == 3:
                self.population[r].place((random.randint(0, 100), 100))
        return

    def create_food(self):
        """Randomly place food pellets on the map"""
        self.foods = [(random.randint(1, 99), random.randint(1,99)) for g in range(0, 200)]
        return

    def refresh_all(self):
        "Re-place and re-starve all beings"
        for r in range(0, len(self.population)):
            self.population[r].refresh()
        return

    def step(self):
        """every Biot makes a move, random order, and will eat if possible"""
        random.shuffle(self.population)

        for r in range(0, len(self.population)):
            eaten = self.population[r].roam(self.foods)
            if not (eaten == None):
                self.foods.remove(eaten)
                #print("Food eaten, %d remaining" % (len(self.foods)))
            """This should remove any eaten food"""
        return

    def day(self):
        """Run through a day, making some steps, then killing the weak and
        mutating the survivors."""
        self.refresh_all()
        self.create_food()
        self.t_pop.append(len(self.population))
        for r in range(0, 20):
            self.step()

        #These 6 lines need reworking, something's off

        survivors = []

        for z in self.population:
            if z.does_survive():
                survivors.append(z)
            else:
                print("Biot died, food %lf/%lf" % (z.eaten, z.mtb))

        offspring = []

        for r in range(0, len(survivors), 2):
            offspring.append(mate(self.population[r], self.population[r+1]))

        children = list(np.repeat(offspring, 2)) #double the offspring
        self.population = survivors + children

    def simulate(self, days):
        self.first_place_population()
        """Run the simulation forward for some number of days, or generations"""

        for r in range(1, days):
            self.day()
            print(("Day %3d | Population %3d | %s") % (r, len(self.population), self.population_report()))

        return

    def population_report(self):
        if (len(self.population) > 0):
            av_speed = 0
            av_amb = 0
            av_mtb = 0
            av_sense = 0
            for r in self.population:
                av_speed += r.speed
                av_amb += r.amb
                av_mtb += r.mtb
                av_sense += r.sense
            av_speed /= len(self.population)
            av_amb /= len(self.population)
            av_mtb /= len(self.population)
            av_sense /= len(self.population)

            self.t_mtb.append(av_mtb)
            self.t_speed.append(av_speed)
            self.t_sense.append(av_sense)

            return ("MSpeed %5.02lf | MAmb %5.02lf | MMtb %5.02lf | MSense %5.02lf" % (av_speed, av_amb, av_mtb, av_sense))
        else:
            return("Biots Extinct")


species = [Biot(str(t), 1, .8, 3) for t in range(0, 20)] #start with a simple group
environment = Field(species)
environment.simulate(100)

f, axarr = plt.subplots(2, 2)
axarr[0, 0].plot(environment.t_speed)
axarr[0, 0].set_title('Speed')
axarr[0, 1].plot(environment.t_sense)
axarr[0, 1].set_title('Sense')
axarr[1, 0].plot(environment.t_mtb)
axarr[1, 0].set_title('Metabolism')
axarr[1, 1].plot(environment.t_pop)
axarr[1, 1].set_title('Population')

plt.show()
