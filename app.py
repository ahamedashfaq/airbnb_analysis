import pandas as pd
import pymongo as pygo
import urllib.parse
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sn
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
from pathlib import Path



#connecting to mongodb
connection_string = f"mongodb+srv://ashfaq:ashfaq@airbnbcluster.zjyuv.mongodb.net/?retryWrites=true&w=majority&appName=airbnbcluster"
client = MongoClient(connection_string)
db = client['AirbnbDB']
col = db['airbnb']

#reading preprocced csv data
csvpath = Path(__file__).parent / 'airbnb_DATA.csv'
df = pd.read_csv(csvpath)

#setting page configuration
st.set_page_config(page_title="Airbnb Data Visualization",layout="wide")




# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top 10s","Explore"],
                           #icons=["house","graph-up-arrow","bar-chart-line"],
                           menu_icon="menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "18px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#6495ED"}}
                           )

# -------------------------------Home page
if selected == "Home":
       
    st.image("data:image/png;base64,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")
    st.markdown("## :blue[Airbnb data] refers to a wide range of information related to the listings, bookings, and user activity on the Airbnb platform. Airbnb is a popular online marketplace that connects people who want to rent out their homes with those looking for short-term accommodations. The platform collects and stores massive amounts of data, which can provide valuable insights for hosts, guests, and researchers alike.")
    #st.markdown("## :violet[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")
    #st.markdown("## :blue[Overview] : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")

# -------------------------------Overview page
if selected == "Overview":
    
        # GETTING USER INPUTS
        country = st.sidebar.multiselect('Select a country', sorted(df.country.unique()), sorted(df.country.unique()))
        prop = st.sidebar.multiselect('Select property_type', sorted(df.property_type.unique()),
                                      sorted(df.property_type.unique()))
        room = st.sidebar.multiselect('Select room_type', sorted(df.room_type.unique()), sorted(df.room_type.unique()))
        price = st.slider('Select price', df.price.min(), df.price.max(), (df.price.min(), df.price.max()))

        # CONVERTING THE USER INPUT INTO QUERY
        query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'

        # CREATING COLUMNS
        col1, col2 = st.columns(2, gap='medium')
        with col1:
            # TOP 10 PROPERTY TYPES BAR CHART
            df1 = df.query(query).groupby(["property_type"]).size().reset_index(name="listings").sort_values(
                by='listings', ascending=False)[:10]
            fig = px.bar(df1,
                         title='Top 10 Property Types',
                         x='listings',
                         y='property_type',
                         orientation='h',
                         color='property_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

            # TOP 10 HOSTS BAR CHART
            df2 = df.query(query).groupby(["host_name"]).size().reset_index(name="listings").sort_values(by='listings', ascending=False)[:10]
            fig = px.bar(df2,
                         title='Top 10 Hosts with Highest number of Listings',
                         x='listings',
                         y='host_name',
                         orientation='h',
                         color='host_name',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
    
            df1 = df.query(query).groupby(["room_type"]).size().reset_index(name="counts")
            fig = px.pie(df1,
                         title='Total Listings in each Room_types',
                         names='room_type',
                         values='counts',
                         color_discrete_sequence=px.colors.sequential.Rainbow
                         )
            fig.update_traces(textposition='outside', textinfo='value+label')
            st.plotly_chart(fig, use_container_width=True)

            
            country_df = df.query(query).groupby(['country'], as_index=False)['name'].count().rename(
                columns={'name': 'total_Listings'})
            fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='country',
                                locationmode='country names',
                                color='total_Listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                                )
            st.plotly_chart(fig, use_container_width=True)

# -------------------------------Explore page
if selected == "Explore":
    st.markdown("## Explore more about the Airbnb data")


    country = st.sidebar.multiselect('Select a country', sorted(df.country.unique()), sorted(df.country.unique()))
    prop = st.sidebar.multiselect('Select property_type', sorted(df.property_type.unique()),
                                  sorted(df.property_type.unique()))
    room = st.sidebar.multiselect('Select room_type', sorted(df.room_type.unique()), sorted(df.room_type.unique()))
    price = st.slider('Select price', df.price.min(), df.price.max(), (df.price.min(), df.price.max()))

    # CONVERTING THE USER INPUT INTO QUERY
    query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'

    # HEADING 1
    st.markdown("## Price Analysis")

    # CREATING COLUMNS
    col1, col2 = st.columns(2, gap='medium')
    with col1:
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('room_type', as_index=False)['price'].mean().sort_values(by='price')
        fig = px.bar(data_frame=pr_df,
                     x='room_type',
                     y='price',
                     color='price',
                     title='Avg Price in each Room type'
                     )
        st.plotly_chart(fig, use_container_width=True)

        # HEADING 2
        st.markdown("## Availability Analysis")

        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=df.query(query),
                     x='room_type',
                     y='availability_365',
                     color='room_type',
                     title='Availability by Room_type'
                     )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('country', as_index=False)['price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                             locations='country',
                             color='price',
                             hover_data=['price'],
                             locationmode='country names',
                             size='price',
                             title='Avg Price in each Country',
                             color_continuous_scale='agsunset'
                             )
        col2.plotly_chart(fig, use_container_width=True)

        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")

        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('country', as_index=False)['availability_365'].mean()
        country_df.availability_365 = country_df.availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                             locations='country',
                             color='availability_365',
                             hover_data=['availability_365'],
                             locationmode='country names',
                             size='availability_365',
                             title='Avg Availability in each Country',
                             color_continuous_scale='agsunset'
                             )
        st.plotly_chart(fig, use_container_width=True)