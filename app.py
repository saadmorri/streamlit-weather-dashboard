import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Live Weather Dashboard", layout="wide")

st.title("🌦️ Live Weather Dashboard")
st.write("This dashboard shows live weather forecast data for a selected city.")

@st.cache_data
def get_coordinates(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        return None

    result = data["results"][0]
    return {
        "name": result["name"],
        "country": result.get("country", ""),
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "timezone": result.get("timezone", "auto")
    }

@st.cache_data
def get_weather_data(latitude, longitude, timezone="auto", forecast_days=3):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation",
        "current": "temperature_2m,wind_speed_10m,relative_humidity_2m",
        "forecast_days": forecast_days,
        "timezone": timezone
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def convert_to_dataframe(weather_json):
    hourly = weather_json["hourly"]
    df = pd.DataFrame({
        "time": hourly["time"],
        "temperature_2m": hourly["temperature_2m"],
        "relative_humidity_2m": hourly["relative_humidity_2m"],
        "wind_speed_10m": hourly["wind_speed_10m"],
        "precipitation": hourly["precipitation"]
    })
    df["time"] = pd.to_datetime(df["time"])
    return df

st.sidebar.header("Controls")

city = st.sidebar.selectbox(
    "Choose a city",
    ["Bishkek", "Osh", "Almaty", "Astana", "Tashkent"]
)

forecast_days = st.sidebar.slider("Forecast days", 1, 7, 3)

selected_variables = st.sidebar.multiselect(
    "Select variables",
    ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "precipitation"],
    default=["temperature_2m", "wind_speed_10m", "precipitation"]
)

location = get_coordinates(city)

if location is None:
    st.error("City not found.")
    st.stop()

weather_json = get_weather_data(
    latitude=location["latitude"],
    longitude=location["longitude"],
    timezone=location["timezone"],
    forecast_days=forecast_days
)

df = convert_to_dataframe(weather_json)

current = weather_json.get("current", {})

st.subheader(f"Current Weather in {location['name']}, {location['country']}")

col1, col2, col3 = st.columns(3)
col1.metric("Current Temperature (°C)", current.get("temperature_2m", "N/A"))
col2.metric("Wind Speed (km/h)", current.get("wind_speed_10m", "N/A"))
col3.metric("Humidity (%)", current.get("relative_humidity_2m", "N/A"))

with st.expander("View processed data"):
    st.dataframe(df, use_container_width=True)

st.subheader("Weather Trends")

if "temperature_2m" in selected_variables:
    fig_temp = px.line(df, x="time", y="temperature_2m", title="Temperature Over Time")
    st.plotly_chart(fig_temp, use_container_width=True)

if "relative_humidity_2m" in selected_variables:
    fig_humidity = px.line(df, x="time", y="relative_humidity_2m", title="Humidity Over Time")
    st.plotly_chart(fig_humidity, use_container_width=True)

if "wind_speed_10m" in selected_variables:
    fig_wind = px.line(df, x="time", y="wind_speed_10m", title="Wind Speed Over Time")
    st.plotly_chart(fig_wind, use_container_width=True)

if "precipitation" in selected_variables:
    fig_rain = px.bar(df, x="time", y="precipitation", title="Precipitation Over Time")
    st.plotly_chart(fig_rain, use_container_width=True)

st.subheader("Summary Statistics")

summary = pd.DataFrame({
    "Metric": [
        "Average Temperature",
        "Maximum Temperature",
        "Average Wind Speed",
        "Total Precipitation"
    ],
    "Value": [
        round(df["temperature_2m"].mean(), 2),
        round(df["temperature_2m"].max(), 2),
        round(df["wind_speed_10m"].mean(), 2),
        round(df["precipitation"].sum(), 2)
    ]
})

st.table(summary)