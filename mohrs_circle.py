# mohrs_circle.py
"""
A Python and Bokeh App that builds a Mohr's circle based on user input.

To run the app from a terminal

 > bokeh serve mohrs_cirle.py

Browse to http://8000:5006
"""

import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure


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

#For now make dummy data to plot
x, y, X, Y, R, C = mohrs_circle()

# Create the Bokeh Column Data Source Object from the mohrs_circle() output arrays
circle_source = ColumnDataSource(data=dict(x=x, y=y))
line_source = ColumnDataSource(data=dict(x=X, y=Y))

# Set up the Bokeh Plot
plot = figure(plot_height=400,plot_width=400, title="Mohr's Circle",
              tools="pan,reset,save,wheel_zoom")
plot.xaxis.fixed_location = 0
plot.yaxis.fixed_location = 0
plot.line('x','y', source=circle_source, line_width=3, line_alpha=0.6)
plot.line('x','y', source=line_source, line_width=3, line_alpha=0.8)

# Set up the input widgets
stress_x_input = TextInput(title="stress in x", value="2.0")
stress_y_input = TextInput(title="sress in y", value="5.0")
shear_input = TextInput(title="shear xy", value="4.0")

# Set up the callback function

def update_data(attrname, old, new):

    # Get the current slider values
    s_x = float(stress_x_input.value)
    s_y = float(stress_y_input.value)
    v = float(shear_input.value)

    # Generate the new circle
    x, y, X, Y, R, C = mohrs_circle(s_x,s_y,v)

    circle_source.data = dict(x=x, y=y)
    line_source.data = dict(x=X,y=Y)

for w in [stress_x_input, stress_y_input,shear_input]:
    w.on_change('value', update_data)

# Set up layouts and add to document
inputs = column(stress_x_input, stress_y_input, shear_input)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Mohr's Circle"
