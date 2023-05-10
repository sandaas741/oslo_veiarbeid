import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

#Cache function
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)  
    return df

st.title("Oslo Vårrengjøring 2023")

#Load data
df = load_data('vaarengjoring.csv')

# Find max and min date for date filter
min_date = pd.to_datetime(df['Dato'], format='%d.%m.%Y').min()
max_date = pd.to_datetime(df['Dato'], format='%d.%m.%Y').max()

# Filter the data based on the date range
filter_street = st.sidebar.checkbox('Filtrer på addresse:')

if filter_street:
    search_term = st.sidebar.text_input('Addresse: ')
    if search_term:
        df = df.loc[df['Gatenavn'].str.contains(search_term, case=False)]
    else:
        df = df

# Filter the data based on the date
filter_date = st.sidebar.checkbox('Filtrer på dato: ')

if filter_date:
    date_range = st.sidebar.date_input('Dato:', max_date, min_value=min_date, max_value=max_date)
    df = df[(pd.to_datetime(df['Dato'], format='%d.%m.%Y').dt.date == date_range)]
else:
    df = df

# Update the map with the filtered data
fig1 = px.scatter_mapbox(df, lat='lat', lon='lon', hover_name='Gatenavn', hover_data =["Kommentar", "Tidpunkt"], zoom=10, color_discrete_sequence=["fuchsia"])
fig1.update_layout(mapbox_style="open-street-map")
fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Display the updated map in Streamlit
st.plotly_chart(fig1)
st.write(df.iloc[:,0:4])