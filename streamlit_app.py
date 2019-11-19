# streamlit_app.py
"""
A streamlit app to draw a Mohr's Circle based on user input
"""

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from user_funcs import mohrs_circle

st.title("Mohr's Circle App")

stress_x = st.sidebar.number_input('stress in x', value=2.0, step=0.1)
stress_y = st.sidebar.number_input('stress in y', value=5.0, step=0.1)
shear = st.sidebar.number_input('shear xy', value=4.0, step=0.1)

circle_x, circle_y, X, Y, R, C = mohrs_circle(stress_x=stress_x, stress_y = stress_y, shear = shear)

st.sidebar.markdown(f'max stress = {round(C+R,2)}')
st.sidebar.markdown(f'min stress = {round(C-R,2)}')
st.sidebar.markdown(f'max shear = {round(R,2)}')

fig, ax = plt.subplots()

ax.plot(circle_x,circle_y)
ax.plot(X,Y,'r')
ax.axis('equal')
ax.axvline(0, color='black', alpha=0.2)
ax.axhline(0, color='black', alpha=0.2)

ax.annotate(s=f'$+\sigma$ = {round(C+R,2)}',
            xy=(C+R,0),
            xytext=(C+R,0),
            arrowprops=dict(facecolor='blue', shrink=0.05))
ax.annotate(s=f'$-\sigma$ = {round(C-R,2)}',
            xy=(C-R,0),
            xytext=(C-R,0),
            arrowprops=dict(facecolor='blue', shrink=0.05))

st.pyplot()
