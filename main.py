# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:27:03 2024

@author: rodo1
"""

from aco import ACO
import robot_ant as r_ant
# ----------------------------- ACO example ----------------------------- #
initial_point = [0, 0]
final_point = [9, 8]
n_ants = 350
n_iterations = 10
size = 10

aco = ACO(initial_point, final_point, n_ants, n_iterations, size)
ants = aco.run_ACO()
best_path, best_length = aco.best_path, aco.best_length

aco.draw_ACO2D()
robots = r_ant.robot_ant(0.1, initial_point, final_point, size)
robots.draw_path(best_path)