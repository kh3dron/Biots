import random
import math

def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

class Biot:

    def __init__(self, speed, amb, sense):
        """Spawn in with a handful of genes"""
        self.speed = speed
        self.amb = amb #Ambition is the probability that biot will go for reproduction
        self.sense = sense
        """Non-genetic attributes"""
        self.coords = (0, 0)
        self.eaten = 0
        self.mtb = self.speed * self.amb
        """Behavioral Flags"""
        self.searching = False #Looking for Food #2
        self.retreating = False #Done eating, retreating to safe area
        self.done = False #Biot has made it's moves for this day

    def __str__(self):
        return("Biot with genes %d %d %d" % (self.speed, self.amb, self.sense))

    def place(self, coords):
        """Places a Biot somewhere"""
        self.coords = coords

    def step_searching(self, foods):
        ate = False
        """Make a move either towards food or nowhere"""
        for r in foods:
            if (distance(self.coords, r) < self.sense*5) and (self.eaten < self.mtb * 2):
                ate = True
                self.place(r)
                self.eaten += 1
                return r

        #No food discovered, random step - but INSIDE the play area
        rads = random.random() * 2 * math.pi
        x, y = (math.cos(rads)*self.speed*5, math.sin(rads)*self.speed*5)
        while not (0 <= x <= 100 and 0 <= y <= 100):
            rads = random.random() * 2 * math.pi
            x, y = (math.cos(rads)*self.speed*5, math.sin(rads)*self.speed*5)
        self.place((x, y))
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
            self.place(target)
            self.done = True
            return
        else:
            if target == (x, 100):
                self.place((x, y+(5*self.speed)))
            if target == (0, y):
                self.place((x-(5*self.speed), y))
            if target == (x, 0):
                self.plce((x, y-(5*self.speed)))
            if target == (100, y):
                self.place((x+(5*self.speed), y))
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
            return

        if self.eaten < self.mtb: #IF we won't survive yet
            e = self.step_searching(foods)
            if not e == None: #IF we eat
                if (random.random() < self.amb):
                    self.searching = True
                else:
                    self.retreating = True
        elif self.searching:
            e = self.step_searching(foods)
            if not e == None:
                self.retreating = True
        elif self.retreating:
            self.step_retreating()

        return



    def does_survive(self):
        """Biot gets to survive if it finds the food it costs to live"""
        return self.eaten > self.mtb

    def does_reproduce(self):
        """Biot gets to reproduce if it's strong enough to find double
        the needed survival food."""
        return self.eaten > 2*self.mtb

    def mutate(self):
        """All genes have a chance of changing by a small amount"""
        "TODO"
        return self



class Field:
    """The environment that the Neets live and compete in. Sized 100x100."""

    def __init__(self, population):
        self.population = population
        self.current_time = 0
        self.foods = [(random.randint(1, 99), random.randint(1,99)) for g in range(0, 100)]

    def food_within_view(self, neet):
        """returns the X and Y of a food, or None if none are within sense range"""
        return

    def first_place_population():
        """randomly place all the neets on the edge of the map"""
        for r in range(0, len(population)):
            edge = random.randint(0, 3)
            if edge == 0:
                return (0, random.randint(0, 100))
            elif edge == 1:
                return (100, random.randint(0, 100))
            elif edge == 2:
                return (random.randint(0, 100), 0)
            elif edge == 3:
                return (random.randint(0, 100), 100)

        return


    def create_food(self):
        """Randomly place food pellets on the map"""
        self.foods = [(random.randint(1, 99), random.randint(1,99)) for g in range(0, 100)]
        return

    def step(self):
        """every Biot makes a move, random order, and will eat if possible"""
        random.shuffle(self.population)

        for r in range(0, len(self.population)):
            eaten = self.population[r].roam(self.foods)
            if not eaten == None:
                self.foods.remove(eaten)
            """This should remove any eaten food"""
        return

    def day(self):
        """Run through a day, making 30 steps, then killing the weak and
        mutating the survivors."""
        self.create_food()
        for r in range(0, 30):
            self.step()

        survivors = [g for g in self.population if g.does_survive()]
        print("SURVIVORS: ", len(survivors))
        mutants = [g.mutate() for g in survivors]
        self.population = mutants

    def simulate(self, days):
        """Run the simulation forward for some number of days, or generations"""
        for r in range(0, days):
            print("New day, Biot count %d" % len(self.population))
            self.day()

        return

    def population_report(self):
        print(self.population)


species = [Biot(1, .5, 1)] * 40 #start with a simple group

environment = Field(species)

environment.simulate(30)
print(environment.population_report())
