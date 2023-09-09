from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import model as model_py
import pandas as pd
from datetime import datetime
import sqlite3

app = Flask(__name__)
CORS(app)

# Load the model
with open("models/model.pkl", "rb") as file:
    model = pickle.load(file)

with open("models/train_columns.pkl", "rb") as file:
    training_columns = pickle.load(file)


def process_input_for_prediction(input_data, training_columns):
    if "date" not in input_data.keys():
        input_data["date"] = datetime.now().toordinal()
    else:
        input_data["date"] = datetime.strptime(
            input_data["date"], "%Y-%m-%d"
        ).toordinal()

    df = pd.DataFrame([input_data])
    df = model_py.preprocess_data(df)  # This function is from your code

    # Identify missing columns
    missing_cols = list(set(training_columns) - set(df.columns))

    # Create a DataFrame with the missing columns filled with zeros
    missing_df = pd.DataFrame(0, index=df.index, columns=missing_cols)

    # Concatenate the original DataFrame with the missing columns
    df = pd.concat([df, missing_df], axis=1)

    # Ensure the order of columns matches the training data
    df = df[training_columns]

    return df


def get_unique_locations():
    connection = sqlite3.connect("src/db/flatmates_data.db")
    cursor = connection.cursor()

    # Fetch unique cities
    cursor.execute("SELECT DISTINCT city FROM flatmates_rent_listings")
    cities = [row[0] for row in cursor.fetchall()]

    # Fetch unique suburbs
    cursor.execute("SELECT DISTINCT suburb FROM flatmates_rent_listings")
    suburbs = [row[0] for row in cursor.fetchall()]

    # Assuming your table has a 'house_type' column.
    cursor.execute("SELECT DISTINCT house_type FROM flatmates_rent_listings")
    house_types = [row[0] for row in cursor.fetchall()]

    data = {"cities": cities, "suburbs": suburbs, "house_types": house_types}

    connection.close()
    return data


@app.route("/predict", methods=["POST"])
def predict():
    # Extract data from the JSON payload
    data = request.json
    data_for_prediction = {
        "city": data["city"],
        "suburb": data["suburb"],
        "house_type": data["houseType"],
        "bedroom_count": data["bedroomCount"],
        "bathroom_count": data["bathroomCount"],
        "price_includes_bills": data["priceIncludesBills"],
        "rooms_available": data["roomsAvailable"],
    }

    print(f"data: {data_for_prediction}")

    # Process data for prediction
    processed_data = process_input_for_prediction(data_for_prediction, training_columns)

    print(f"processed_data: {process_input_for_prediction}")

    prediction = model.predict(processed_data)

    print(f"Prediction: {prediction}")
    # Return the prediction as JSON
    return jsonify(
        {"prediction": float(prediction[0])}
    )  # Convert numpy float to native Python float


@app.route("/get-locations", methods=["GET"])
def get_locations():
    data = get_unique_locations()
    return jsonify(data)


if __name__ == "__main__":
    app.run(port=5000)
