# Libraries

import random
import mesa
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid
import numpy as np
import pandas as pd
import matplotlib


# Rules definition.
# The rules of Conway's game of life are defined based on four numbers: Death, Survival, Reproduction, Overpopulation, grouped as (D, S, R, O) Cells die if the number of their living neighbors is <D or >O, survive if the number of their living neighbors is ≤S, come to life if their living neighbors are ≥R and ≤O.

rules = (3, 10, 1, 6) # (D, S, R, O)

"""  """

class Automaton(Agent):
    def __init__(self, pos, model, isAlive=False):
        super().__init__(pos, model)
        self.pos = pos
        self.isAlive = isAlive

    def alive_neighbors(self):
        neighbors = self.model.grid.iter_neighbors(self.pos, moore=True, include_center=False)
        return sum([1 for n in neighbors if n.isAlive])

    def step(self):
        n = self.alive_neighbors()
        # continuar ahorita que sepa qp

class Build_Model(Model):
    def __init__(self, rules, alive_probability = 0.5, dims=(50,50), seed=313):
        self.rules = rules
        self.dims = dims
        self.schedule = SimultaneousActivation(self)
        self.grid = Grid(dims[0], dims[1], torus=True)
        self.grid_new = 

"""  """

class buildModel(Model):
    
    def __init__(self, N, rules, aliveProbability=0.5, dims=(50, 50), seedRNG=123):
        super().__init__()
        self.num_agents = N
        self.width, self.height = dims
        self.grid = mesa.space.MultiGrid(self.width, self.height, True)
        self.schedule = mesa.time.RandomActivation(self)

        for i in range(self.num_agents):
            a =  Automaton(i, self)
            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self, pos):
        #First check if alive
        live = self.isAlive
        preLive = self.isAlive

        # Count alive neighbors
        n = self.alive_neighbors(pos)
        
        # Apply the Game of Life rules
        if live and self.rules[0] <= n <= self.rules[1]:
            self.isAlive[pos] = True
        elif not live and self.rules[2] <= n <= self.rules[3]:
            self.isAlive[pos] = True
        else:
            self.isAlive[pos] = False

        self.schedule.step()


