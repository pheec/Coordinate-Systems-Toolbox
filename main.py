import numpy as np
from coordinate_structure_toolbox import coordinate_structure

coord_structure = coordinate_structure()

T_world_to_base = np.array([
                        [1, 0, 0, 1],
                        [0, 1, 0, 2],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]
                            ])

T_asd_to_world = np.array([
                        [1, 0, 0, 2],
                        [0, 1, 0, 1],
                        [0, 0, 1, 1],
                        [0, 0, 0, 1]
                            ])

T_base_to_camera = np.array([
                        [0, 1, 0, 0],
                        [1, 0, 0, 0],
                        [0, 0, 1, 3],
                        [0, 0, 0, 1]
                            ])

coord_structure.add_transformation('world', 'base', T_world_to_base)
coord_structure.add_transformation('base', 'camera', T_base_to_camera)
coord_structure.add_transformation('asd', 'world', T_asd_to_world)

#coord_structure.print_all()

# T = coord_structure.get('base', 'world')
# print(T)

coord_structure.plot_all('world')
