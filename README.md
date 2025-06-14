# MediStock AI: Machine Learning Service


## 📦 Project Overview
This repository contains the Machine Learning (ML) service component for MediStock AI, designed to provide intelligent vendor recommendations based on historical performance data. The service trains a regression model to predict an `outcome_score` for supply-vendor combinations, indicating the expected quality, efficiency, and cost-effectiveness.

<br/>

## ✨ Key Components
Our ML service is structured into three main Python scripts:

1.  **`generate_data.py`**:
    * **Purpose**: Creates synthetic, realistic historical order data (`mock_historical_orders.csv`). This data simulates past transactions, including various vendor-supply attributes and their resulting "outcome scores."
    * **Data Generated**: Includes fields like `supply_id`, `vendor_id`, `unit_price`, `quality_rating`, `avg_delivery_days`, `actual_price_paid`, `actual_delivery_days`, and the calculated `outcome_score`.

2.  **`ml_logic.py`**:
    * **Purpose**: Houses the core Machine Learning pipeline.
    * **Functionality**:
        * Loads the generated historical data.
        * Preprocesses the data by selecting relevant features.
        * Trains a **RandomForestRegressor** model to predict the `outcome_score`.
        * Evaluates the model's performance (MSE, R2 score).
        * Saves the trained model and its expected features to a `.joblib` file for later use.

3.  **`main.py`**:
    * **Purpose**: Exposes the trained ML model as a RESTful API service using FastAPI.
    * **Functionality**:
        * Loads the pre-trained model once when the service starts.
        * Provides a `/predict` API endpoint that accepts input features (price, quality, delivery days).
        * Uses the loaded ML model to return a predicted `outcome_score` for the given input.
        * Includes a health check (`/`).

<br/>

## 🧠 How the ML Model Works
The `RandomForestRegressor` model is trained on historical data to learn the relationship between vendor/supply attributes and the `outcome_score`.

* **Features Used for Prediction**:
    * `unit_price` (of the supply from a specific vendor)
    * `quality_rating` (of the vendor for that supply)
    * `avg_delivery_days` (for that supply from that vendor)

* **Target Variable**: `outcome_score` (a composite score from 0.05 to 1.0, indicating overall satisfaction/suitability).

The model learns how different combinations of these features historically led to certain `outcome_score` values, allowing it to predict a suitability score for new, unseen vendor-supply combinations.

<br/>

## 📊 Current Model Performance
After our latest refinements and data generation, the model demonstrates strong performance on the synthetic dataset:

* **Mean Squared Error (MSE):** `0.0061`
    * A very low value, indicating that the model's predictions are, on average, very close to the actual `outcome_score` values. The non-zero value accounts for the inherent noise introduced during data generation, which prevents perfect prediction and simulates real-world conditions.
* **R-squared (R2) Score:** `0.7599`
    * This is an excellent R2 score. It means approximately **76% of the variance** in the `outcome_score` can be explained and predicted by our model using the selected features. This confirms the model has effectively learned the underlying patterns and relationships we built into the data generation process.


<br/>

## 🌐 API Endpoints
The FastAPI service exposes the following endpoints:

1.  **Health Check**
    * **Endpoint**: `/`
    * **Method**: `GET`
    * **Description**: A simple endpoint to verify that the service is running and responsive.
    * **Expected Response (JSON)**:
        ```json
        {
          "status": "ok",
          "message": "MediStock AI ML Service is running!"
        }
        ```

2.  **Predict Vendor Outcome Score**
    * **Endpoint**: `/predict`
    * **Method**: `POST`
    * **Description**: Predicts an `outcome_score` for a given supply-vendor scenario based on the provided features.
    * **Request Body (JSON)**:
        ```json
        {
          "unit_price": 450.0,
          "quality_rating": 5,
          "avg_delivery_days": 2
        }
        ```
        * `unit_price`: The price of the supply from the vendor.
        * `quality_rating`: The vendor's quality rating for this supply (e.g., 1-5).
        * `avg_delivery_days`: The average delivery time in days for this supply from this vendor.
    * **Expected Response (JSON)**:
        ```json
        {
          "predicted_outcome_score": 0.7808
        }
        ```
        * `predicted_outcome_score`: A float representing the predicted suitability score between 0.05 and 1.0.
