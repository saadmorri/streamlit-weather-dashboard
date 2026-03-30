# 🌦️ Live Weather Dashboard (Streamlit)

## 📌 Project Overview
This project is an interactive dashboard built using Streamlit that displays live weather data for selected cities using the Open-Meteo API.

## ⚙️ Features
- Select city from dropdown
- Choose forecast days
- Select weather variables
- Filter by date range
- Interactive charts (line + bar)
- Summary statistics
- Live API data

## 🛠️ Technologies Used
- Python
- Streamlit
- Pandas
- Plotly
- Requests

## 🌍 Data Source
- Open-Meteo API (live weather data)
- Open-Meteo Geocoding API

## 🧠 Why I Chose This Dataset
I chose live weather data because it changes continuously and is useful for real-world analysis. The Open-Meteo API provides free public data without requiring an API key, making it ideal for building an interactive dashboard.

## ▶️ How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py