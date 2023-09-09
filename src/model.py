import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import HistGradientBoostingRegressor
import pickle


def load_and_deduplicate_csvs(folder_path: str) -> pd.DataFrame:
    """Load and concatenate data from CSVs, deduplicating based on 'flatmates_id'."""
    dfs = [
        pd.read_csv(os.path.join(folder_path, file_name))
        for file_name in os.listdir(folder_path)
        if file_name.endswith(".csv")
    ]
    all_data = pd.concat(dfs, ignore_index=True)
    return all_data.drop_duplicates(subset="flatmates_id", keep="first")


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the data for model training."""
    df["date"] = pd.to_datetime(df["date"]).apply(lambda x: x.toordinal())
    return pd.get_dummies(
        df, columns=["suburb", "city", "house_type"], drop_first=False
    )


def train_model(
    X_train: pd.DataFrame, y_train: pd.Series
) -> HistGradientBoostingRegressor:
    """Train and return the regression model."""
    model = HistGradientBoostingRegressor()
    model.fit(X_train, y_train)
    return model


def get_default_prediction_data(X_train: pd.DataFrame) -> dict:
    """Return a default data dictionary."""
    default_data = {col: 0 for col in X_train.columns}

    city = "Adelaide"
    suburb = "Adelaide"
    house_type = "Share House"
    bedroom_count = 3
    bathroom_count = 1
    price_includes_bills = False
    rooms_available = 3

    default_data[f"city_{city}"] = 1
    default_data[f"suburb_{suburb}"] = 1
    default_data[f"house_type_{house_type}"] = 1
    default_data["price_includes_bills"] = price_includes_bills
    default_data["bedroom_count"] = bedroom_count
    default_data["bathroom_count"] = bathroom_count
    default_data["rooms_available"] = rooms_available

    default_data["date"] = pd.Timestamp("2023-12-01").to_julian_date()
    return default_data


def save_model(model: HistGradientBoostingRegressor, model_path: str):
    """Save the model to a pickle file."""

    with open(model_path, "wb") as f:
        pickle.dump(model, f)


def save_columns(X_train: pd.DataFrame):
    with open("models/train_columns.pkl", "wb") as f:
        pickle.dump(X_train.columns.tolist(), f)


def main(folder_path: str):
    """Main execution function."""
    data = load_and_deduplicate_csvs(folder_path)
    data = preprocess_data(data)

    X = data.drop(["flatmates_id", "url", "price"], axis=1)
    y = data["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = train_model(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.2f}")

    save_model(model, "models/model.pkl")
    save_columns(X_train)

    mock_data = get_default_prediction_data(X_train)
    predicted_price = model.predict(pd.DataFrame([mock_data]))

    print(
        f"Predicted rental price in Adelaide on 1st December 2023: ${predicted_price[0]:.2f}"
    )


if __name__ == "__main__":
    FOLDER_PATH = "output"
    main(FOLDER_PATH)
