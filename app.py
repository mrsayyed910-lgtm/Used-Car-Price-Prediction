
import sqlite3
from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import json

app = Flask(__name__)

# ===========================
# Load Trained Model
# ===========================

model = pickle.load(open("model/car_price_model.pkl", "rb"))

# ===========================
# Load Label Encoders
# ===========================

le_brand = pickle.load(open("model/le_brand.pkl", "rb"))
le_model = pickle.load(open("model/le_model.pkl", "rb"))
le_fuel = pickle.load(open("model/le_fuel.pkl", "rb"))
le_transmission = pickle.load(open("model/le_transmission.pkl", "rb"))
le_seller = pickle.load(open("model/le_seller.pkl", "rb"))

le_owner = pickle.load(open("model/le_owner.pkl", "rb"))
le_condition = pickle.load(open("model/le_condition.pkl", "rb"))
le_insurance = pickle.load(open("model/le_insurance.pkl", "rb"))
le_accident = pickle.load(open("model/le_accident.pkl", "rb"))
le_city = pickle.load(open("model/le_city.pkl", "rb"))

# Optional
model_columns = pickle.load(open("model/model_columns.pkl", "rb"))
    
def get_dropdown_data():

    df = pd.read_csv("dataset/car data.csv")

    brands = sorted(df["brand"].unique())

    transmissions = sorted(df["transmission_type"].unique())
    seller_types = sorted(df["seller_type"].unique())
    fuel_types = sorted(df["fuel_type"].unique())

    owner_types = sorted(df["owner_type"].unique())
    conditions = sorted(df["car_condition"].unique())
    insurance_status = sorted(df["insurance_status"].unique())
    accident_history = sorted(df["accident_history"].unique())
    cities = sorted(df["city"].unique())

    brand_model = {}
    brand_model_details = {}

    for brand in brands:

        models = sorted(df[df["brand"] == brand]["model"].unique())

        brand_model[brand] = models
        brand_model_details[brand] = {}

        for model_name in models:

            row = df[
                (df["brand"] == brand) &
                (df["model"] == model_name)
            ].iloc[0]

            brand_model_details[brand][model_name] = {

                "engine": int(row["engine"]),
                "max_power": float(row["max_power"]),
                "mileage": float(row["mileage"]),
                "seats": int(row["seats"])

            }

    return (
        brands,
        brand_model,
        brand_model_details,
        transmissions,
        seller_types,
        fuel_types,
        owner_types,
        conditions,
        insurance_status,
        accident_history,
        cities
    )

@app.route("/")
def home():

    (
        brands,
        brand_model,
        brand_model_details,
        transmissions,
        seller_types,
        fuel_types,
        owner_types,
        conditions,
        insurance_status,
        accident_history,
        cities
    ) = get_dropdown_data()

    return render_template(
        "index.html",

        brands=brands,
        transmissions=transmissions,
        seller_types=seller_types,
        fuel_types=fuel_types,

        owner_types=owner_types,
        conditions=conditions,
        insurance_status=insurance_status,
        accident_history=accident_history,
        cities=cities,

        brand_model=json.dumps(brand_model),
        brand_model_details=json.dumps(brand_model_details)
    )

@app.route("/predict", methods=["POST"])
def predict():

    (
        brands,
        brand_model,
        brand_model_details,
        transmissions,
        seller_types,
        fuel_types,
        owner_types,
        conditions,
        insurance_status,
        accident_history,
        cities
    ) = get_dropdown_data()

    # ========= Form Data =========

    brand = request.form["brand"]
    model_name = request.form["model"]
    fuel = request.form["fuel_type"]
    transmission = request.form["transmission_type"]
    seller = request.form["seller_type"]

    owner = request.form["owner_type"]
    condition = request.form["car_condition"]
    insurance = request.form["insurance_status"]
    accident = request.form["accident_history"]
    city = request.form["city"]

    registration_year = int(request.form["registration_year"])
    vehicle_age = int(request.form["vehicle_age"])
    km_driven = int(request.form["km_driven"])
    mileage = float(request.form["mileage"])
    engine = int(request.form["engine"])
    max_power = float(request.form["max_power"])
    seats = int(request.form["seats"])

    # ========= Encode =========

    brand_encoded = le_brand.transform([brand])[0]
    model_encoded = le_model.transform([model_name])[0]
    fuel_encoded = le_fuel.transform([fuel])[0]
    transmission_encoded = le_transmission.transform([transmission])[0]
    seller_encoded = le_seller.transform([seller])[0]

    owner_encoded = le_owner.transform([owner])[0]
    condition_encoded = le_condition.transform([condition])[0]
    insurance_encoded = le_insurance.transform([insurance])[0]
    accident_encoded = le_accident.transform([accident])[0]
    city_encoded = le_city.transform([city])[0]

    # ========= Feature Order =========
    # Must match the training notebook

    features = np.array([[
        brand_encoded,
        model_encoded,
        vehicle_age,
        km_driven,
        seller_encoded,
        fuel_encoded,
        transmission_encoded,
        mileage,
        engine,
        max_power,
        seats,
        registration_year,
        owner_encoded,
        condition_encoded,
        insurance_encoded,
        accident_encoded,
        city_encoded
    ]])

    prediction = round(model.predict(features)[0])

    conn = sqlite3.connect("car_prediction.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO prediction_history(
            brand,
            model,
            predicted_price,
            registration_year,
            vehicle_age,
            km_driven,
            fuel_type,
            transmission_type,
            seller_type,
            owner_type,
            car_condition,
            insurance_status,
            accident_history,
            city,
            engine,
            mileage,
            max_power,
            seats
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        brand,
        model_name,
        prediction,
        registration_year,
        vehicle_age,
        km_driven,
        fuel,
        transmission,
        seller,
        owner,
        condition,
        insurance,
        accident,
        city,
        engine,
        mileage,
        max_power,
        seats
    ))

    conn.commit()
    conn.close()

    return render_template(
        "index.html",
prediction=f"{prediction:,}",
        brands=brands,
transmissions=transmissions,
        seller_types=seller_types,
        fuel_types=fuel_types,
        owner_types=owner_types,
        conditions=conditions,
insurance_status=insurance_status,
accident_history=accident_history,
        cities=cities,
brand_model=json.dumps(brand_model),
brand_model_details=json.dumps(brand_model_details)
    )
if __name__ == "__main__":
    app.run(debug=True)
    