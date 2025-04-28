import random
import numpy as np
import math


def init (r , L ,  N , v0 ):
    

   # Define the size of the square
    square_size = L

   # Define a list to store the circle positions
    circles = []

   # Define a function to check if two circles overlap
    def circles_overlap(circle1, circle2):
        distance = math.sqrt((circle1[0] - circle2[0])**2 + (circle1[1] - circle2[1])**2)
        return distance < (2*r)

    # Generate random circles until the maximum number of circles is reached
    max_circles = N
    while len(circles) < max_circles:
        # Generate a random position for the circle
        x = random.uniform(r, square_size - r)
        y = random.uniform(r, square_size - r)
        circle = (x, y)

        # Check if the circle overlaps with any existing circles
        overlaps = False
        for existing_circle in circles:
            if circles_overlap(circle, existing_circle):
                overlaps = True
                break

        # Add the circle to the list if it doesn't overlap
        if not overlaps:
            circles.append(circle)
    circles = np.array(circles)
    theta = np.random.uniform(0, 2 * np.pi , size=N)  # angles
    v = np.array([v0 * np.cos(theta), v0 * np.sin(theta)])  # velocities

    return circles , v.T , theta
     

