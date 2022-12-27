import streamlit as st
import plotly.express as px
import pandas as pd
import pycountry

def get_iso_alpha(country):
    try:
        country_obj = pycountry.countries.get(name=country)
        return country_obj.alpha_3
    except:
        return None

def chart_general():
    # Get the user input
    year_col, continent_col, log_x_col = st.columns([5, 5, 5])
    with year_col:
        year_choice = st.slider(
            "What year would you like to examine?",
            min_value=1952,
            max_value=2007,
            step=5,
            value=2007,
        )
    with continent_col:
        continent_choice = st.selectbox(
            "What continent would you like to look at?",
            ("All", "Asia", "Europe", "Africa", "Americas", "Oceania"),
        )
    with log_x_col:
        log_x_choice = st.checkbox("Log X Axis?")

    # Apply the year filter given by the user
    filtered_df = df[(df.year == year_choice)]
    # Apply the continent filter
    if continent_choice != "All":
        filtered_df = filtered_df[filtered_df.continent == continent_choice]
        
    fig = px.scatter( # Create the figure in Plotly
        filtered_df,
        x="gdp_cap",
        y="life_exp",
        size="population",
        color="continent", 
        hover_name="country",
        log_x=log_x_choice,
        size_max=60,
    )
    fig.update_layout(title="GDP per Capita vs. Life Expectancy")
    st.plotly_chart(fig, use_container_width=True) # Input the Plotly chart to the Streamlit interface

def map_general():
    fig = px.choropleth(df, locations='iso_alpha', color='life_exp', hover_name='country', 
                        animation_frame='year', color_continuous_scale=px.colors.sequential.Plasma, projection='natural earth')
    fig.update_layout(title="Life Expectancy over time")
    st.plotly_chart(fig, use_container_width=True)

def chart_spain_pop():
    fig = px.bar(spain_data, x='year', y='population', height=400)
    fig.update_layout(title="Population of Spain over time")
    st.plotly_chart(fig, use_container_width=True)

def chart_spain_life_exp():
    fig = px.bar(spain_data, x='year', y='population', color='life_exp', labels={'population': 'Population of Spain'}, height=400)
    fig.update_layout(title="Life Expectancy of Spain over time")
    st.plotly_chart(fig, use_container_width=True)

def chart_spain_gdp():
    fig = px.bar(spain_data, x='year', y='population', color='gdp_cap', labels={'population': 'Population of Spain'}, height=400)
    fig.update_layout(title="GDP per Capita of Spain over time")
    st.plotly_chart(fig, use_container_width=True)

st.set_page_config(layout="wide")
col1, col2, col3 = st.columns([5, 5, 20])
st.title("Streamlit Gapminder Storytelling")

df = pd.read_csv("gapminder_full.csv") #https://www.kaggle.com/datasets/tklimonova/gapminder-datacamp-2007?resource=download
df['iso_alpha'] = df['country'].apply(get_iso_alpha)
spain_data = df.query("country == 'Spain' ")

chart_spain_pop()
chart_spain_life_exp()
chart_spain_gdp()
chart_general()
map_general()
