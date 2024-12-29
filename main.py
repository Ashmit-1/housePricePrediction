import streamlit as st
st.title("House Price Prediction")
longitude = st.slider("Enter your longitude", min_value=-150.0, max_value=-100.0, step=0.1)
latitude = st.slider("Enter your latitude", min_value=30.0, max_value=50.0, step=0.1)
house_age_slider = st.slider('Enter house age')
population = st.number_input("Enter average population of the area", step=1, min_value=0, placeholder="Population", value=None)
households = st.number_input("Enter average number of households in the area", step=1, min_value=0, placeholder="Households", value=None)
income = st.number_input("Enter your income", step=1, min_value=0, placeholder="Income", value=None)
proximity_to_ocean = st.selectbox("Enter proximity to ocean", options=("Less than one hour from ocean", "Inland", "Near ocean", "Near bay", "Island"), index=None, placeholder="Proximity to ocean")