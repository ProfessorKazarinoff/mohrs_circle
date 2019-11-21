# streamlit_app.py
"""
A streamlit app to draw a Mohr's Circle based on user input\
using the Bokeh plotting library
"""

import numpy as np
import streamlit as st
from bokeh.plotting import figure
from user_funcs import mohrs_circle

st.title("Mohr's Circle App")

stress_x = st.sidebar.number_input("stress in x", value=2.0, step=0.1)
stress_y = st.sidebar.number_input("stress in y", value=5.0, step=0.1)
shear = st.sidebar.number_input("shear xy", value=4.0, step=0.1)

circle_x, circle_y, X, Y, R, C = mohrs_circle(
    stress_x=stress_x, stress_y=stress_y, shear=shear
)

st.sidebar.markdown(f"max stress = {round(C+R,2)}")
st.sidebar.markdown(f"min stress = {round(C-R,2)}")
st.sidebar.markdown(f"max shear = {round(R,2)}")

p = figure(
    title="Mohr's Circle",
    x_axis_label="stress",
    y_axis_label="shear",
    match_aspect=True,
    tools="pan,reset,save,wheel_zoom",
)

p.line(circle_x, circle_y, color="#1f77b4", line_width=3, line_alpha=0.6)
p.line(X, Y, color="#ff7f0e", line_width=3, line_alpha=0.6)

p.xaxis.fixed_location = 0
p.yaxis.fixed_location = 0

st.bokeh_chart(p)
