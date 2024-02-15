import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from utils import *

class coordinate_structure:
    def __init__(self) -> None:
        self.transformations = {}

    def print_all(self) -> None:
        for key, value in self.transformations.items():
            print(f'{key}:\n {value}\n')

    def get(self, frame_origin, frame_final) -> np.ndarray:
        transformation_name = "T_" + frame_origin + "_to_" + frame_final
        if transformation_name in self.transformations:
            print("Returned transformation: ", transformation_name)
            return self.transformations[transformation_name]
        else:
            print("Transformation: ", transformation_name, "not found")
            return np.array([])

    def add_transformation(self, frame_origin, frame_final, transformation_matrix, 
                           calculate_inverse = True) -> None:
        T_name = "T_" + frame_origin + "_to_" + frame_final
        self.transformations[T_name] = transformation_matrix
        print("Added transformation: ", T_name)

        if calculate_inverse:
            T_inverse_name = "T_" + frame_final + '_to_' + frame_origin
            inverse_transformation_matrix = np.linalg.inv(transformation_matrix)
            self.transformations[T_inverse_name] = inverse_transformation_matrix
            print("\tAdded transformation: ", T_inverse_name)

    def plot_all(self, frame_for_plot, factor=0.1) -> None:
        # Define the axes vectors
        axes = np.array([[0, 0, 0, 1],  # Origin
                        [factor, 0, 0, 1],  # X-axis
                        [0, factor, 0, 1],  # Y-axis
                        [0, 0, factor, 1]]) # Z-axis

        x_cum, y_cum, z_cum = [], [], []
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

            if frame_origin != frame_for_plot: continue

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

            ax.text(x[0], y[0], z[0], frame_final, verticalalignment='center')

            # Set plot labels
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_zlabel('Z-axis')

        # Set aspect ratio to equal
        ax.set_box_aspect([np.ptp(x_cum), np.ptp(y_cum), np.ptp(z_cum)])
        plt.legend()
        plt.show()