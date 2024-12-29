import streamlit as st
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

myModel = joblib.load("final_model_random_forest.pkl")
df = pd.read_csv("housing.csv")
total_rooms_median = df["total_rooms"].median()
total_bed_rooms_median = df["total_bedrooms"].median()
st.title("House Price Prediction")
longitude = st.slider("Enter your longitude", min_value=-150.0, max_value=-100.0, step=0.1, value=None)
latitude = st.slider("Enter your latitude", min_value=30.0, max_value=50.0, step=0.1,value=None)
house_age_slider = st.slider('Enter house age',value=None)
population = st.number_input("Enter average population of the area", step=1, min_value=0, placeholder="Population...", value=None)
households = st.number_input("Enter average number of households in the area", step=1, min_value=0, placeholder="Households...", value=None)
income = st.number_input("Enter your income", step=1, min_value=0, placeholder="Income...", value=None)
proximity_to_ocean = st.selectbox("Enter proximity to ocean", options=("Less than one hour from ocean", "Inland", "Near ocean", "Near bay", "Island"), index=None, placeholder="Proximity to ocean...")

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

st.subheader("The data entered", divider=True)
st.dataframe(user_data_to_show, hide_index=True)

user_data["median_income"] = user_data["median_income"]/1000
user_data["rooms_per_household"] = user_data["total_rooms"] /user_data["households"]
user_data["population_per_household"] = user_data["population"] /user_data["households"]
user_data["bedrooms_per_room"] = user_data["total_bedrooms"] /user_data["total_rooms"]

num_attributes = []
cat_attributes = ["ocean_proximity"]
for i in data:
    num_attributes.append(i)
num_attributes.pop()

numerical_pipeline = Pipeline([
 ('imputer', SimpleImputer(strategy="median")),
 ('std_scaler', StandardScaler()),
])
full_pipeline = ColumnTransformer([
 ("num", numerical_pipeline, num_attributes),
 ("cat", OneHotEncoder(), cat_attributes),
])


