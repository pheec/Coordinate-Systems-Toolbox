import cv2
import numpy as np

def get_frame_names(transformation_name):
    str1, str2 = transformation_name.split('_to_')
    prefix = "T_"
    if str1.startswith(prefix):
        str1 = str1[len(prefix):]
    else:
        str1 = str1
    return str1, str2

def draw_equidistant_points_on_circle(img, center, radius, n_points, color):
    points = []
    for i in range(n_points):
        x = int(center[0] + radius * np.cos(2 * np.pi * i / n_points))
        y = int(center[1] + radius * np.sin(2 * np.pi * i / n_points))
        points.append((x, y))
        cv2.circle(img, (x, y), 10, color, -1)  # Draw the point
    return points
