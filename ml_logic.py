import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'mock_historical_orders.csv')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'vendor_recommender_model.joblib')

def load_data()-> pd.DataFrame :
    if not os.path.exists(DATA_PATH) :
        raise FileNotFoundError(f"Data file not found in {DATA_PATH}. Please run the script to generate data .")
    
    print(f"Loading data from the path - {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    
    # data casting fix
    df['outcome_score'] = pd.to_numeric(df['outcome_score'], errors='coerce')
    df['outcome_score'].fillna(0, inplace=True)

    print("Data loaded successfully ")

    print(df.head())    
    return df


def preprocess_data(df) :
    """
    Preprocesses the historical data for ML model training.
    Selects features and target variable.
    """

    features : list[str] = [
        'unit_price',
        'quality_rating',
        'avg_delivery_days'
    ]

    target =  'outcome_score'
    X = df[features]
    y = df[target]

    print(f"Features (X) shape : {X.shape}")
    print(f"Target (y) shape : {y.shape}" )
    print(f"Features used: {features}")
    return X,y,features


def train_model (X, y) :
    print("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training RandomForestRegressor model...")

    # good choice for robustness and understand non-linear patterns
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=1)

    model.fit(X=X_train, y=y_train)
    print("Model training complete !")

    y_pred = model.predict(X=X_test)
    mse = mean_squared_error(y_true=y_test, y_pred= y_pred)
    r2 = r2_score(y_true=y_test, y_pred=y_pred)

    print(f"Mean squared error (MSME) : { mse:.4f}")
    print(f"R-squared (R2) score : {r2:.4f}")
    return model


def save_model(model, features):
    """Saves the trained model and feature list using joblib."""
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({'model' : model, 'features' : features}, MODEL_PATH)
    print(f"Model and features saved to : {MODEL_PATH}")


def load_model() :
    """Loads the trained model and feature list from joblib file."""
    if not os.path.exists(MODEL_PATH) :
        raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}. Please train and save the model first.")
    
    print(f"loading model from : {MODEL_PATH}")
    data = joblib.load(MODEL_PATH)
    print("Model loaded successfully !")
    return data['model'], data['features']


def predict_outcome_score(model ,features, input_data) :
    input_df = pd.DataFrame([input_data], columns=features)
    prediction = model.predict(input_df)
    return prediction[0]
'''
if __name__ == "__main__":
    try:    
        df = load_data()
        if (df.empty == False) :
            
            X, y, features = preprocess_data(df=df)
            model = train_model(X=X, y=y)
            save_model(model=model, features=features)



                # checking the score :
                # --- Test prediction-
            print("\n--- Testing Model Prediction ---")
            loaded_model, loaded_features = load_model()

            example_input = {
                'supply_id': 1,              # Disposable Gloves
                'vendor_id': 101,            # MediCare Direct
                'unit_price': 450,
                'quality_rating': 5,
                'avg_delivery_days': 2
            }
            predicted_score = predict_outcome_score(loaded_model, loaded_features, example_input)
            print(f"Predicted outcome score for example input: {predicted_score:.4f}")

            # Example for a potentially lower score vendor
            example_input_low_score = {
                'supply_id': 1,              # Disposable Gloves
                'vendor_id': 103,            # Budget Pharma Solutions
                'unit_price': 380,
                'quality_rating': 3,
                'avg_delivery_days': 3
            }
            predicted_score_low = predict_outcome_score(loaded_model, loaded_features, example_input_low_score)
            print(f"Predicted outcome score for low-score example: {predicted_score_low:.4f}")

        else :
            print("something went wrong while loading data from csv !")
    except FileNotFoundError as e:
        print(f"Error : {e}. Please ensure 'mock_historical_orders.csv' is in 'ml_service/data/' ")
    except Exception as e:
        print(f"An unexpected error occured : {e}")
'''