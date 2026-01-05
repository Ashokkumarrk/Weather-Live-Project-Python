# IMPORT LIBRARIES

import streamlit as st               ##Imports Streamlit, which is used to build web dashboards using Python.
import requests                      ##Used to call APIs (here, to fetch live weather data).
import pandas as pd                  ##Used for data handling and creating DataFrames 
import matplotlib.pyplot as plt      ##Used to create charts and plots
import seaborn as sns                ##Used for advanced & stylish charts (bar chart in this app).
from datetime import datetime        ##Used to get current date and time (for background color and sunrise/sunset).


# PAGE CONFIGURATION

st.set_page_config(page_title="Weather Dashboard", layout="wide")     ##Browser tab title = Weather Dashboard ,Layout = wide screen (uses full width)


# TIME-BASED BACKGROUND

hour = datetime.now().hour           ##Gets current hour (0–23) from system time.

if 5 <= hour < 12:                   ##Morning → Light blue background.
    page_bg = "#E3F2FD"
elif 12 <= hour < 17:                ##Afternoon → Light yellow background  
    page_bg = "#FFF8E1"
elif 17 <= hour < 20:                ##Evening → Light orange background
    page_bg = "#FFE0B2"
else:                                ##Night → Dark background.    
    page_bg = "#263238"

st.markdown(                        ##Allows HTML & CSS styling inside Streamlit.##Changes the entire app background color dynamically ##Styles KPI cards:Padding ,Rounded corners, Center text, White font color padding: 18px;
    f"""
    <style>
    .stApp {{                        
        background-color: {page_bg};
    }}
    .metric-box {{                   
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);   
        margin-bottom: 20px;   /*  SPACING FIX */
    }}
    </style>
    """,
    unsafe_allow_html=True        ##Allows HTML + CSS inside Streamlit. ##Adds shadow (card effect)
)


# TITLE & SUBTITLE

st.markdown("<h1 style='text-align:center;'>🌦 Live Weather Analytics Dashboard</h1>", unsafe_allow_html=True)         ##Displays main title with emoji and center alignment.
st.markdown("<h4 style='text-align:center;'>Real-time Weather Monitoring using Python</h4>", unsafe_allow_html=True)   ##Displays subtitle


# SLICERS

s1, s2, s3 = st.columns(3)      ##Splits the page into 3 equal columns.

with s1:
    city = st.selectbox("🌍 City", ["Chennai", "Bangalore", "Delhi", "Mumbai", "Hyderabad"])   ##Dropdown to choose temperature unit.

with s2:
    unit = st.selectbox("🌡 Temperature Unit", ["Celsius", "Fahrenheit"])                       ##Dropdown to choose temperature unit.

with s3:
    theme = st.selectbox("🎨 Chart Theme", ["Light", "Dark"])                                  ##Dropdown for theme (future use / UI enhancement)


# API CONFIGURATION

api_key = "e1c0b441e48a22b7f4f55eeabbe21c59"             ##API key for OpenWeatherMap.
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"    ##Builds API URL using selected city
data = requests.get(url).json()                          ## Sends request → converts response into JSON data.


# EXTRACT WEATHER DATA

temp = data["main"]["temp"]                  ##Gets current temperature.
feels_like = data["main"]["feels_like"]      ##Gets feels like temperature.
humidity = data["main"]["humidity"]          ##Gets humidity percentage. 
pressure = data["main"]["pressure"]          ##Gets atmospheric pressure.
wind = data["wind"]["speed"]                 ##Gets wind speed
lat = data["coord"]["lat"]                   ##Gets latitude
lon = data["coord"]["lon"]                    ##Gets longitude

sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")      ##Converts UNIX time → readable time.
sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

if unit == "Fahrenheit":                   ##Checks selected unit.
    temp = (temp * 9/5) + 32               ##Converts Celsius → Fahrenheit.    
    feels_like = (feels_like * 9/5) + 32


# KPI CARDS

k1, k2, k3, k4, k5 = st.columns(5)         ##Creates 5 KPI cards in one row.  
##Displays styled KPI values:Temperature, Feels Like, Humidity, Wind, Pressure
with k1:
    st.markdown(f"<div class='metric-box' style='background:#ef5350;'><h4>Temperature</h4><h2>{round(temp,1)}</h2></div>", unsafe_allow_html=True)
with k2:
    st.markdown(f"<div class='metric-box' style='background:#ab47bc;'><h4>Feels Like</h4><h2>{round(feels_like,1)}</h2></div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='metric-box' style='background:#26a69a;'><h4>Humidity</h4><h2>{humidity}%</h2></div>", unsafe_allow_html=True)
with k4:
    st.markdown(f"<div class='metric-box' style='background:#42a5f5;'><h4>Wind</h4><h2>{wind} m/s</h2></div>", unsafe_allow_html=True)
with k5:
    st.markdown(f"<div class='metric-box' style='background:#ffa726;'><h4>Pressure</h4><h2>{pressure}</h2></div>", unsafe_allow_html=True)

# EXTRA GAP BELOW KPI ROW
st.markdown("")

# DATAFRAME       ##Creates a DataFrame for charts.stores weather metrics and values.
df = pd.DataFrame({
    "Metric": ["Temperature", "Feels Like", "Humidity", "Pressure", "Wind Speed"],
    "Value": [temp, feels_like, humidity, pressure, wind]
})





# MAIN DIVISION (LEFT & RIGHT)

left, right = st.columns([1.5, 2.0])       ##Splits page:Left = map + sun timings, Right = charts

# LEFT SIDE
with left:
    st.markdown("### 🗺️ City Location")     ##Shows city location on map.
    st.map(pd.DataFrame({"lat":[lat], "lon":[lon]}), zoom=4)

    st.markdown(                        ##Displays sun timings in a styled card.
        f"""
        <div class='metric-box' style='background:#ffb300;margin-top:20px;'>
        <h4>🌅 Sun Timings</h4>      
        <h3>Sunrise: {sunrise}</h3>
        <h3>Sunset: {sunset}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

# CHART FUNCTION

def chart(title):    ##Reusable function for charts.
    fig, ax = plt.subplots(figsize=(4,3))     ##Reusable function for charts.
    ax.set_title(title)                       ##Sets chart title. 
    return fig, ax                            ##Returns chart object.




 ##1.Line chart – Trend,2️. Bar chart – Comparison,3️. Pie chart – Proportion,4️. Horizontal bar – Ranking,5️. Area chart – Volume, 6️.Histogram – Distribution

with right:
    st.markdown("### 📊Charts")

     #RIGHT SIDE (6 CHARTS) 
    r1, r2 = right.columns(2)  
    with r1:
        fig, ax = chart("Trend Analysis")
        ax.plot(df["Metric"], df["Value"], marker="o")
        st.pyplot(fig)        ##Renders chart in Streamlit

    with r2:
        fig, ax = chart("Value Comparison")
        sns.barplot(x="Metric", y="Value", data=df, ax=ax)
        st.pyplot(fig)

    st.markdown("")
    

    r3, r4 = right.columns(2)

    with r3:
        fig, ax = chart("Proportion View")
        ax.pie(df["Value"], labels=df["Metric"], autopct="%1.1f%%")
        st.pyplot(fig)

    with r4:
        fig, ax = chart("Rank Comparison")
        ax.barh(df["Metric"], df["Value"])
        st.pyplot(fig)

    st.markdown("")
    

    r5, r6 = right.columns(2)

    with r5:
        fig, ax = chart("Volume Change")
        ax.fill_between(df["Metric"], df["Value"], alpha=0.5)
        st.pyplot(fig)

    with r6:
        fig, ax = chart("Distribution Pattern")
        ax.hist(df["Value"], bins=5)
        st.pyplot(fig)

