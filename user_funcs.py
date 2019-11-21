# user_funcs.py
"""
user-defined functions for the streamlit mohr's circle app
"""

import numpy as np


def mohr_c(stress_x, stress_y, shear):
    """
    This function takes in:
    stress_x: int or float
    stress_y: int or float
    shear: int or float

    and outputs two values for the circle center and radius

    output:
    C, R
    C is x-value of the circle center
    R is the radius of the circle
    """
    C = (stress_x + stress_y) / 2
    R = ((((stress_x - stress_y) / 2) ** 2) + shear ** 2) ** 0.5
    return C, R


def c_array(C, R, n=100):
    """
    This function takes in:
    C: int or float, the x-value of a circle center
    R: int or float, the radius of the circle
    n (optinal): number of points

    and outputs two NumPy arrays of x and y values that will create the circle

    output:
    x, y
    x is a NumPy array with n-values that contains the x-values to build the circle
    y is a NumPy array with n-values that contains the y-value to build the circle
    """
    # build the circle_x and circle_y arrays. They are used to draw the circle
    t = np.linspace(0, 2 * np.pi, n + 1)
    x = R * np.cos(t) + C
    y = R * np.sin(t)
    return x, y


def X_Y(stress_x, stress_y, shear):
    # build the arrays that describe the line X-Y between the known points
    X = np.array([stress_x, stress_y])
    Y = np.array([-shear, shear])
    return X, Y


def max_stress(C, R):
    pass


def min_stress(C, R):
    pass


def max_shear(C, R):
    pass


def mohrs_circle(stress_x=2.0, stress_y=5.0, shear=4.0):
    """
    This function takes in:
    stress_x: int or float
    stress_y: int or float
    shear: int or float

    and outputs a comple NumPy arrays to build a Mohr's Circle

    output:
    circle_x, circle_y, X, Y, R, C
    """
    stress_avg = (stress_x + stress_y) / 2
    stress_max = stress_avg + (((stress_x - stress_y) / 2) ** 2 + shear ** 2) ** 0.5
    stress_min = stress_avg - (((stress_x - stress_y) / 2) ** 2 + shear ** 2) ** 0.5
    R = ((((stress_x - stress_y) / 2) ** 2) + shear ** 2) ** 0.5  # Also max shear
    circle_eqn = ((stress_x - stress_avg) ** 2) - shear ** 2 - R ** 2

    if shear == 0:
        theta_p = 0
        theta_s = 0
    else:
        theta_p = 0.5 * np.degrees(np.arctan((2 * shear) / (stress_x - stress_y)))
        if theta_p <= 0:
            a = -1
        else:
            a = 1
        theta_s = a * 0.5 * np.degrees(np.arctan((stress_x - stress_y) / (2 * shear)))

    if abs(stress_min) > abs(stress_max):
        maxi = stress_min
        mini = stress_max
    elif abs(stress_max) > abs(stress_min):
        maxi = stress_max
        mini = stress_min

    # principle planes

    shear_lim_p = np.arange(0, 0.5 * (R + 1), 1)
    shear_lim_n = np.arange(0, -0.5 * R - 1, -1)

    princ_x_slope = (theta_p / abs(theta_p)) * np.tan(np.radians(theta_p))
    princ_y_slope = (theta_p / abs(theta_p)) * np.tan(np.radians((theta_p + 90)))

    if princ_x_slope < 0:
        range_x = shear_lim_n
        princ_x = princ_x_slope * range_x + stress_avg

    elif princ_x_slope > 0:
        range_x = shear_lim_p
        princ_x = princ_x_slope * range_x + stress_avg

    if princ_y_slope < 0:
        range_y = shear_lim_n
        princ_y = princ_y_slope * range_y + stress_avg

    elif princ_y_slope > 0:
        range_y = shear_lim_p
        princ_y = princ_y_slope * range_y + stress_avg

    # build the circle_x and circle_y arrays. They are used to draw the circle
    n = 100
    t = np.linspace(0, 2 * np.pi, n + 1)
    x = R * np.cos(t) + stress_avg
    y = R * np.sin(t)

    # build the arrays that describe the line X-Y between the known points
    X = np.array([stress_x, stress_y])
    Y = np.array([-shear, shear])

    # the center of Mohr's Circle is the average stress
    C = stress_avg

    return x, y, X, Y, R, C
