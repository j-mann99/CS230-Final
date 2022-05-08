"""
Class: CS230--Section 3
Name: Jack Manning
Description: Final version 2.0
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""
import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk

default_countries = ["us", "au", "gb"]
default_shapes = ["circle", "oval", "disk"]
default_duration = 50

# reading in the data
def read_data():
    return pd.read_csv("UFO Sightings.csv", low_memory=False).set_index("date posted")


#showing the original data
@st.cache
def load_data(nrows):
    data = pd.read_csv('UFO Sightings.csv', nrows=nrows)
    return data

data_load_state = st.text('Loading data...')
ufo_data = load_data(1000)

# filtering data
def filter_data(selected_countries, selected_shapes, min_duration):
    df = read_data()
    df = df.loc[df['country'].isin(selected_countries)]
    df = df.loc[df['shape'].isin(selected_shapes)]
    df = df.loc[df['duration (seconds)'].astype(float) > min_duration]
    return df


#count frequency of countries

def all_countries():
    df = read_data()
    lst = []
    for ind, row in df.iterrows():
        if row['country'] not in lst:
            lst.append(row['country'])

    return lst


def count_countries(countries, df):
    lst = [df.loc[df['country'].isin([country])].shape[0] for country in countries]

    return(lst)


def all_shapes():
    df = read_data()
    lst = []
    for ind, row in df.iterrows():
        if row['shape'] not in lst:
            lst.append(row['shape'])

    return lst


#Generate map - I did my best here - I could not debug it to get it to populate on streamlit
#def generate_map(df):
 #   map_df = df.filter(['shape', 'latitude', 'longitude'])

  #  view_state = pdk.ViewState(lattitude=map_df["latitude"].astype(float).mean(),
   #                            longitude=map_df["longitude"].astype(float).mean(),
    #                           zoom=2)
    #layer = pdk.Layer('ScatterplotLayer',
     #                 data=map_df,
      #                get_position='[latitude, longitude]',
       #               get_radius=5000000,
        #              get_color=[50, 150, 220],
         #             pickable=True)

   # tool_tip = {'html': 'Listing:<br/> <b>{name}</b>', 'style': {'backgroundColor': 'steelblue', 'color': 'white'}}

   # map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
    #               initial_view_state=view_state,
     #              layers=[layer],
      #             tooltip=tool_tip)
    #st.pydeck_chart(map)


  #  data = filter_data(default_countries)

   # generate_map(data)


# bar chart for sighting durations -
# This one was also difficult, I was attempting to find the average duration
# of the sighting for each shape to give viewers a better understanding of which shapes were more "legitimate"
#def sighting_durations(df):
 #   durations = [row['duration (seconds)'].astype(float) for ind, row in df.iterrows()]
  #  shapes = [row['shape'] for ind, row in df.iterrows()]

   # dict = {}
    #for shape in shapes:
     #   dict[shape] = []

    #for i in range(len(durations)):
     #   dict[shapes[i]].append(durations[i])

    #return dict


#def shape_average(dict_durations):
 #   dict1 = {}
  #  for key in dict_durations.keys():
   #     dict1[key] = np.meam(dict_durations[key])

    #return dict1


#def bar_chart(dict_averages):
 #   plt.figure()
  #  x = dict_averages.keys()
   # y = dict_averages.values()
    #plt.bar(x, y)
   # plt.xticks(rotation=45)
    #plt.ylabel("Shape")
    #plt.xlabel("Average Duration")
    #plt.title(f"Average duration by shape: {', '.join(dict_averages.keys())}")

    #return plt


# pie chart for countries
def pie_chart(counts, selected_countries):
    plt.figure()
    explodes = [0 for i in range(len(counts))]
    maximum = counts.index(np.max(counts))
    explodes[maximum] = 0.25

    plt.pie(counts, labels=selected_countries, explode=explodes, autopct="%.2f")
    plt.title(f"UFO sightings in each country(expressed as a %): {','.join(default_countries)}")
    plt.show()

def main():
    st.title("Data analytics and visualization with Python")
    st.write("UFO Sightings! Open the sidebar to begin")
    st.sidebar.write("Please choose your options to display data.")
    countries = st.sidebar.multiselect("Select a country: ", all_countries())
    shapes = st.sidebar.multiselect("Select the shape of the sighting: ", all_shapes())
    duration = st.sidebar.slider("Duration(in seconds): ", 0, 10000)

    data = filter_data(countries, shapes, duration)
    series = count_countries(countries, data)

    st.subheader('UFO Sighting information')
    st.write(ufo_data)
    st.set_option('deprecation.showPyplotGlobalUse', False)

    #st.write("View a Bar Chart")
    #st.pyplot(bar_chart(shape_average(sighting_durations(data))))

    st.write("View a Pie Chart")
    st.pyplot(pie_chart(series, countries))
    st.set_option('deprecation.showPyplotGlobalUse', False)

    #st.write("View a map of the sightings")
    #generate_map(data)



main()

data = filter_data(default_countries, default_shapes, default_duration)
counts = count_countries(default_countries, data)

#duration = sighting_durations(data)
#averages = shape_average(duration)




