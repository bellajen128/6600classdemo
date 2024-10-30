import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

st.title('In class activity')

st.write('Hello world!!')

data = pd.read_csv("https://raw.githubusercontent.com/qurat-azim/instructionaldatasets/refs/heads/main/data/penguins.csv")

st.sidebar.header("Select Options")
selected_category = st.sidebar.selectbox("Select Category", options =['All','Adelie', 'Gentoo', 'Chinstrap'])

if selected_category != 'All':
    filtered_data = data[data['species'] == selected_category]
else: 
    filtered_data = data


# Matplorlib histogram
st.write("#### Matplotlib Histogram")
fig, ax = plt.subplots()
ax.hist(filtered_data['culmen_length_mm'], bins=30, color="skyblue", edgecolor = "black")
ax.set_title("Matplotlib Histogram for Culmen Lengths")
ax.set_xlabel("Value")
ax.set_ylabel ("Frequency")

st.pyplot(fig) ### use streamlit to display the pyplot object

# Seaborn density plot 
st.write('#### Seaborn Density Plot')
fig, ax = plt.subplots()
fig = sns.displot(filtered_data['culmen_depth_mm'], color="black", kind='kde', ax=ax, fill=True)
ax.set_title('Seaborn Desity Plot for Culmen Depths')
ax.set_xlabel("Value")
ax.set_ylabel("Density")
st.pyplot(fig)

# Altair scatter plot
st.write('### Altair Scatter Plot')
scatter_plot = alt.Chart(filtered_data).mark_circle().encode(
    x=alt.X('flipper_length_mm', title='Flipper Length'),
    y=alt.Y('body_mass_g', title='Body Mass'),
    color=alt.Color('island', scale=alt.Scale(scheme='tableau10')),
    tooltip = ['island', 'flipper_length_mm', 'body_mass_g']
).properties(
    width=600,
    height=400,
    title="Scatter Plot of Penguins Data"
).interactive() # Allows zooming and panning
st.altair_chart(scatter_plot, use_container_width =True)



