import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import copy

from utils import *

WIDTH = 800
HEIGHT = 800
BLACK_COLOR = (0, 0, 0)
BLUE_COLOR = (255, 0, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX 
FONT_SCALE = 1
TEXT_THICKNESS = 2

class coordinate_structure:
    def __init__(self) -> None:
        self.transformations = {}

    def print_all(self) -> None:
        for key, value in self.transformations.items():
            print(f'{key}:\n {value}\n')

    def get(self, frame_origin, frame_final) -> np.ndarray:
        transformation_name = "T_" + frame_origin + "_to_" + frame_final
        if transformation_name in self.transformations:
            #print("Returned transformation: ", transformation_name)
            return self.transformations[transformation_name]
        else:
            print("Transformation: ", transformation_name, "not found")
            return np.array([])

    def add_transformation(self, origin_frame, final_frame, transformation_matrix) -> None:
        origin_a = origin_frame
        final_a = final_frame
        T_a = transformation_matrix

        T_name_a = "T_" + origin_a + "_to_" + final_a
        self.transformations[T_name_a] = T_a
        print("Added transformation: ", T_name_a)

        final_b = origin_a
        origin_b = final_a
        T_name_b = "T_" + origin_b + '_to_' + final_b
        T_b = np.linalg.inv(T_a)
        self.transformations[T_name_b] = T_b
        print("\tAdded transformation: ", T_name_b)

        T_names_to_be_added = []
        T_to_be_added = []
        for transformation_name_st, transformation_matrix_st in self.transformations.items():
            origin_st, final_st = get_frame_names(transformation_name_st)
        
            if(origin_st == final_a and origin_a != final_st):
                new_T = transformation_matrix_st @ T_a
                T_name = "T_" + origin_a + "_to_" + final_st
                T_names_to_be_added.append(T_name)
                T_to_be_added.append(new_T)
                print("\tAdded transformation: ", T_name, "case a")

                new_T_inv = np.linalg.inv(new_T)
                T_name_inv = "T_" + final_st + "_to_" + origin_a
                T_names_to_be_added.append(T_name_inv)
                T_to_be_added.append(new_T_inv)
                print("\tAdded transformation: ", T_name_inv, "case a - inverse")

            if(origin_st == final_b and origin_b != final_st):
                new_T = transformation_matrix_st @ T_b
                T_name = "T_" + origin_b + "_to_" + final_st
                T_names_to_be_added.append(T_name)
                T_to_be_added.append(new_T)
                print("\tAdded transformation: ", T_name, "case b")

                new_T_inv = np.linalg.inv(new_T)
                T_name_inv = "T_" + final_st + "_to_" + origin_b
                T_names_to_be_added.append(T_name_inv)
                T_to_be_added.append(new_T_inv)
                print("\tAdded transformation: ", T_name_inv, "case b - inverse")

        for i in range(len(T_to_be_added)):
            self.transformations[T_names_to_be_added[i]] = T_to_be_added[i]

        print()

    def plot_all(self, frame_for_plot, factor=0.1) -> None:
        # Define the axes vectors
        axes = np.array([[0, 0, 0, 1],  # Origin
                        [factor, 0, 0, 1],  # X-axis
                        [0, factor, 0, 1],  # Y-axis
                        [0, 0, factor, 1]]) # Z-axis

        x_cum, y_cum, z_cum = [np.array([factor, 0, 0, 0])], [np.array([0, factor, 0, 0])], [np.array([0, 0, factor, 0])]
        # Plot the axes
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot origin
        ax.quiver(0, 0, 0, factor, 0, 0, color='r')#, label='X-axis')
        ax.quiver(0, 0, 0, 0, factor, 0, color='g')#, label='Y-axis')
        ax.quiver(0, 0, 0, 0, 0, factor, color='b')#, label='Z-axis')

        ax.text(0, 0, 0, frame_for_plot, verticalalignment='center')

        for transformation_name, transformation_matrix in self.transformations.items():
            
            frame_origin, frame_final = get_frame_names(transformation_name)

            if frame_final != frame_for_plot: continue

            print(transformation_name, "added to the plot")

            # Apply the transformation matrix to the axes vectors
            transformed_axes = np.dot(transformation_matrix, axes.T).T

            # Extract the transformed coordinates
            x = transformed_axes[:, 0]
            y = transformed_axes[:, 1]
            z = transformed_axes[:, 2]

            x_cum.append(x)
            y_cum.append(y)
            z_cum.append(z)

            # Plot arrows for X, Y, and Z axes
            ax.quiver(x[0], y[0], z[0], x[1]-x[0], y[1]-y[0], z[1]-z[0], color='r')#, label='X-axis')
            ax.quiver(x[0], y[0], z[0], x[2]-x[0], y[2]-y[0], z[2]-z[0], color='g')#, label='Y-axis')
            ax.quiver(x[0], y[0], z[0], x[3]-x[0], y[3]-y[0], z[3]-z[0], color='b')#, label='Z-axis')

            ax.text(x[0], y[0], z[0], frame_origin, verticalalignment='center')

            # Set plot labels
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_zlabel('Z-axis')

        # Set aspect ratio to equal
        ax.set_box_aspect([np.ptp(x_cum), np.ptp(y_cum), np.ptp(z_cum)])
        plt.show()

    def draw_diagram(self) -> None:
        nodes_list = []
        for transformation_name, transformation_matrix in self.transformations.items():
            frame_origin, frame_final = get_frame_names(transformation_name)
            if frame_origin not in nodes_list:
                nodes_list.append(frame_origin)
            if frame_final not in nodes_list:
                nodes_list.append(frame_final)

        image = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8)*255
        center = (WIDTH // 2, HEIGHT // 2)
        radius = min(WIDTH, HEIGHT) // 3
        n_points = len(nodes_list)

        points = draw_equidistant_points_on_circle(image, center, radius, n_points, BLACK_COLOR)

        nodes = {}
        for i in range(len(nodes_list)):
            nodes[nodes_list[i]] = points[i]
            cv2.putText(image, nodes_list[i], points[i], FONT,  
                   FONT_SCALE, BLACK_COLOR, TEXT_THICKNESS, cv2.LINE_AA)

        for transformation_name, transformation_matrix in self.transformations.items():
            frame_origin, frame_final = get_frame_names(transformation_name)
            cv2.arrowedLine(image, nodes[frame_origin], nodes[frame_final], BLUE_COLOR, 2)
        cv2.imshow('Coordinate Frames Structure ', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

