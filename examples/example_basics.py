#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from coordinate_systems_toolbox import CoordinateStructure


if __name__ == '__main__':
    coord_structure = CoordinateStructure()

    T_robot_to_world = np.array([
                            [1, 0, 0, 1],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]
                                ])

    T_world_to_base = np.array([
                            [1, 0, 0, 0],
                            [0, 1, 0, 1],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]
                                ])

    T_camera_to_robot = np.array([
                            [1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 1],
                            [0, 0, 0, 1]
                                ])

    T_camera_to_holder = np.array([
                            [1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0.8],
                            [0, 0, 0, 1]
                                ])

    coord_structure.add_transformation('robot', 'world', T_robot_to_world)
    coord_structure.add_transformation('world', 'base', T_world_to_base)
    coord_structure.add_transformation('camera', 'robot', T_camera_to_robot)
    coord_structure.add_transformation('camera', 'holder', T_camera_to_holder)

    coord_structure.plot_all('world')
    coord_structure.draw_diagram()

    coord_structure.print_all()

    #T = coord_structure.get('base', 'world')
    #print(T)


