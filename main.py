import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
        page_title="Predict Prices",
        page_icon="house.png",
)

myModel = joblib.load("final_model_random_forest.pkl")
df = pd.read_csv("housing.csv")

total_rooms_median = df["total_rooms"].median()
total_bed_rooms_median = df["total_bedrooms"].median()

st.title("House Price Prediction", anchor=False)
st.divider()

st.markdown("##### Enter your longitude")
longitude = st.slider("Enter your longitude", min_value=-150.0, max_value=-100.0, step=0.1, value=None, label_visibility="collapsed")

st.markdown("##### Enter your latitude")
latitude = st.slider("Enter your latitude", min_value=30.0, max_value=50.0, step=0.1,value=None, label_visibility="collapsed")

st.markdown("##### Enter house age")
house_age_slider = st.slider('Enter house age',value=None, label_visibility="collapsed")

column1, column2 = st.columns(2)

with column1:
    st.markdown("##### Enter average population of the area")
    population = st.number_input("Enter average population of the area", step=1, min_value=0, placeholder="Population...", value=None, label_visibility="collapsed")

    st.markdown("##### Enter average number of households")
    households = st.number_input("Enter average number of households in the area", step=1, min_value=0, placeholder="Households...", value=None, label_visibility="collapsed")

with column2:
    st.markdown("##### Enter your income")
    income = st.number_input("Enter your income", step=1, min_value=0, placeholder="Income...", value=None, label_visibility="collapsed")

    st.markdown("##### Enter proximity to ocean")
    proximity_to_ocean = st.selectbox("Enter proximity to ocean", options=("<1H OCEAN", "INLAND", "NEAR OCEAN", "NEAR BAY", "ISLAND"), index=None, placeholder="Proximity to ocean...", label_visibility="collapsed")

data = {
    "longitude":[longitude],
    "latitude":[latitude],
    "housing_median_age":[house_age_slider],
    "total_rooms":[total_rooms_median],
    "total_bedrooms":[total_bed_rooms_median],
    "population":[population],
    "households":[households],
    "median_income":[income],
    "ocean_proximity":[proximity_to_ocean]
}
user_data = pd.DataFrame(data)
user_data_to_show = user_data.drop(columns=["total_rooms", "total_bedrooms"])

def isFilled(dataframe) -> bool:
    attributes = list(dataframe)
    for attribute in attributes:
        if dataframe[attribute][0] == None:
            return False
    return True

st.subheader("The data entered", divider=True, anchor=False)
st.dataframe(user_data_to_show, hide_index=True)

user_data["median_income"] = user_data["median_income"]/1000
user_data["rooms_per_household"] = user_data["total_rooms"] /user_data["households"]
user_data["population_per_household"] = user_data["population"] /user_data["households"]
user_data["bedrooms_per_room"] = user_data["total_bedrooms"] /user_data["total_rooms"]

col1, col2, col3 = st.columns([2.5,1,2.5], border=False)
with col2:
    predict = st.button("Predict", type="primary")
if predict:
    if isFilled(user_data_to_show):
        new_full_pipeline = joblib.load("full_pipeline.joblib")
        prepared_data = new_full_pipeline.transform(user_data)
        modelPrediction = myModel.predict(prepared_data)
        for i in modelPrediction:
            st.subheader(f"The predicted house price is ${i:.2f}", anchor=False)
            break
    else:
        st.warning("Oops you missed some information !")
       