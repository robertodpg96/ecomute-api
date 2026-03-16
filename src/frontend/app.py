import streamlit as st
import requests

st.title("Ecomute Trip Planner")
st.write("Calculate how long your trip will take using our ML model!")

#1. Inputs
distance = st.slider("Distance (km)", 1.0, 20.0, 5.0)
battery = st.slider("Battery Level (%)", 10.0, 100.0, 50.0)

#2. Button to trigger prediction
if st.button("Predict Trip Duration"):
    #Call our own API
    payload = {
        "distance_km": distance,
        "battery_level": battery
    }
    try:
        response = requests.post("http://localhost:8000/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            minutes = result.get("estimated_minutes")
            st.metric("Estimated Trip Duration", f"{minutes} minutes")
        
        else:
            st.error("Error connecting to API.")

    except Exception as e:
        st.error(f"Failed to connect to API: {e}")

