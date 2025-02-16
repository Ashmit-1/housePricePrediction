from flask import Flask, request
from flask import render_template
import joblib
import pandas as pd
 
app = Flask(__name__, template_folder="templates")

def predict_price(latitude, longitude, age, population, households, income, proximity_to_ocean):
    myModel = joblib.load("final_model_random_forest.pkl")
    df = pd.read_csv("housing.csv")
    new_full_pipeline = joblib.load("full_pipeline.joblib")
    total_rooms_median = df["total_rooms"].median()
    total_bed_rooms_median = df["total_bedrooms"].median()
    data = {
        "longitude":[longitude],
        "latitude":[latitude],
        "housing_median_age":[age],
        "total_rooms":[total_rooms_median],
        "total_bedrooms":[total_bed_rooms_median],
        "population":[population],
        "households":[households],
        "median_income":[income],
        "ocean_proximity":[proximity_to_ocean]
    }
    user_data = pd.DataFrame(data)
    user_data["median_income"] = user_data["median_income"]/1000
    user_data["rooms_per_household"] = user_data["total_rooms"] /user_data["households"]
    user_data["population_per_household"] = user_data["population"] /user_data["households"]
    user_data["bedrooms_per_room"] = user_data["total_bedrooms"] /user_data["total_rooms"]
    prepared_data = new_full_pipeline.transform(user_data)
    modelPrediction = myModel.predict(prepared_data)
    return f"{modelPrediction[0]:.2f}"

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        latitude=float(request.form.get("latitude"))
        longitude=float(request.form .get("longitude"))
        households=float(request.form.get("households"))
        age=float(request.form.get("age"))
        population=float(request.form.get("population"))
        proximity=request.form.get("proximity")
        income=float(request.form.get("income"))
        predictions = predict_price(latitude, longitude, age, population, households, income, proximity)
        return render_template("index.html", predictions=predictions)



if __name__ == "__main__":
    app.run()
