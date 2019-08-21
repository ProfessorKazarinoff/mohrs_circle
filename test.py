# test.py
"""
Test script for bokeh applications
"""

import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

# Set up data
n=100
R=1
t = np.linspace(0, 2 * np.pi, n + 1)
x = R * np.cos(t)
y = R * np.sin(t)
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[-2.5, 2.5], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

def R_input_handler(attr, old, new):
    print("Previous label: " + old)
    print("Updated label: " + new)
    R = (float(new))
    x = R * np.cos(t)
    y = R * np.sin(t)
    source.data = dict(x=x, y=y)

def x_input_handler(attr, old, new):
    x = R * np.cos(t) + float(new)
    y = R * np.sin(t)
    source.data = dict(x=x, y=y)

def y_input_handler(attr, old, new):
    x = R * np.cos(t)
    y = R * np.sin(t) + float(new)
    source.data = dict(x=x, y=y)

R_input = TextInput(value="1", title="R:")
x_input = TextInput(value="0", title="x:")
y_input = TextInput(value="0", title="y:")

R_input.on_change("value", R_input_handler)
x_input.on_change("value", x_input_handler)
y_input.on_change("value", y_input_handler)

inputs = column(R_input, x_input, y_input)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "circle"
