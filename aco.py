# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:25:12 2024

@author: Rodolfo Alberto Reyes Corona
"""

import numpy as np

class Ant:
    def __init__(self, initial_point):
        self.initial_point = initial_point
        self.reset()
        
    def move_to(self, new_node, distance):
        self.path.append(new_node)
        self.cost += distance

    def reset(self):
        self.path = [self.initial_point]
        self.cost = 0

    def get_path(self):
        return self.path

    def get_cost(self):
        return self.cost

class ACO:
    def __init__(self, initial_point, final_point, n_ants, n_iterations, size):
        """
        Args:
            initial_point (list): Bidimensional initial point
            final_point (list): Bidimensional final point
            n_ants (int): Number of ants running per iteration
            n_iterations (int): Maximum number of iterations
            learning_rate (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, 
                    so 0.95 will lead to decay, 0.5 to much faster decay.
            size (int): This number provide the size of the resolution space in a quad area.
            alpha (int or float): Exponenet on pheromone, higher alpha gives pheromone more weight. Default=random
            beta (int or float): Exponent on distance, higher beta give distance more weight. Default=random
        Example:
            ant_colony = ACO([0,0], [5,5], 100, 10, 10)          
        """        
        self.initial_point = initial_point
        self.final_point = final_point
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.learning_rate = 0.95
        self.alpha = np.random.uniform(0,1)
        self.beta = np.random.uniform(0,1)
        self.table = {}
        self.best_path = None
        self.best_length = np.inf
        self.size = size

        x_i, x_f = 0, self.size + 1
        x = list(np.linspace(x_i, x_f, self.size + 2, dtype=int))
        y = x.copy()
        self.X, self.Y = np.meshgrid(x, y)
    
    # Euclidean distance function between two points.
    def euclidean_distance(self, point_1, point_2):
        x_1, y_1 = point_1
        x_2, y_2 = point_2
        d = (x_2 - x_1) ** 2 + (y_2 - y_1) ** 2
        return np.sqrt(d)
    
    # This function provide the possibles nodes in a ratio of 1.4142 = sqrt(2)
    def possible_options_nodes(self, node):
        min_distance = np.sqrt(2)
        options = []
        for i in range(self.size + 1):
            for j in range(self.size + 1):
                possible_new_node = [self.X[i, j], self.Y[i, j]]
                distance = self.euclidean_distance(node, possible_new_node)
                if 0 < distance <= min_distance:
                    options.append(possible_new_node)
        return options
    
    # Choose new node function provide a new node based in the probability equation.
    def choose_new_node(self, node, nodes_options, pheromones, alpha, beta):
        probabilities = []
        for i, node_option in enumerate(nodes_options):
            distance = self.euclidean_distance(node, node_option)
            visibility = 1 / distance
            pheromone = pheromones[i]
            probabilities.append((pheromone ** beta) * (visibility ** alpha))

        probabilities = np.array(probabilities)
        probabilities /= probabilities.sum()
        cumulative_prob = np.cumsum(probabilities)
        rng = np.random.uniform(0, 1)
        return nodes_options[np.searchsorted(cumulative_prob, rng)]

    
    def get_pheromones(self, options, node):
        pheromones = []
        for option in options:
            possible_route = (tuple(node), tuple(option))
            pheromones.append(self.table.get(possible_route, 0.01))
        return pheromones

    def actualization(self, pheromones, ants):
        rho = 0.1
        for route, pheromone in self.table.items():
            new_pheromone = (1 - rho) * pheromone
            for ant in ants:
                ant_path = ant.get_path()
                for j in range(len(ant_path) - 1):
                    route_aux = (tuple(ant_path[j]), tuple(ant_path[j + 1]))
                    if route == route_aux:
                        new_pheromone += self.learning_rate / ant.get_cost()
            self.table[route] = new_pheromone

    def initialize_ants(self):
        self.ants = [Ant(self.initial_point) for _ in range(self.n_ants)]

    def run_ACO(self):
        # Max step allowed for a better time response, this parameter you can modify.
        max_step = 50
        self.initialize_ants()
        
        for it in range(self.n_iterations):
            for h, ant in enumerate(self.ants):
                print(f'\rExecuting the iteration {(it + 1):04} of {str(self.n_iterations).zfill(4)}. Ant: {str(h + 1).zfill(4)} / {str(self.n_ants).zfill(4)}', end='')            
                ant.reset()
                actual_node = self.initial_point
                step = 0
                
                while True:
                    # Search possible options nodes
                    options = self.possible_options_nodes(actual_node)
                    # Get the value of the pheromones
                    pheromones = self.get_pheromones(options, actual_node)
                    # Choose a new node using the possible optines and values
                    new_node = self.choose_new_node(actual_node, options, pheromones, self.beta, self.alpha)
                    distance = self.euclidean_distance(actual_node, new_node)
                    ant.move_to(new_node, distance)
                    actual_node = new_node
                    step += 1

                    if actual_node == self.final_point or step == max_step:
                        break
                
                # We verify the best cost based on path and lenght
                if ant.get_cost() < self.best_length:
                    self.best_length = ant.get_cost()
                    self.best_path = ant.get_path()

            # Actualization of the values.
            self.actualization(self.table, self.ants)
        return self.ants
    
    def draw_ACO2D(self):
        aux = [self.initial_point, self.final_point]
        import matplotlib.pyplot as plt

        x = [p[0] for p in self.best_path]
        y = [p[1] for p in self.best_path]

        plt.figure('ACO', figsize=(6, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='b')
        for i, point in enumerate(aux):
            plt.text(point[0], point[1], f'{point}', fontsize=8, ha='right')

        plt.xlim(- 1, self.size + 1)
        plt.ylim(- 1, self.size + 1)
        plt.grid(True)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Metaheuristic path lenght ' + str(round(self.best_length,2)))
        plt.show()