import numpy as np
import traceback
import pandas as pd
from backend.schemas import TransactionInput, PredictionResponse
from backend.model_loader import model_loader
from backend.utils import get_risk_level, generate_explanation
from fastapi import HTTPException

def make_prediction(data: TransactionInput) -> PredictionResponse:
    if model_loader.model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded. Please ensure model files exist in the models/ directory.")

    try:
        # Create a dictionary for the features
        features = {"Time": data.time}
        for i in range(1, 29):
            features[f"V{i}"] = data.v_features[f"V{i}"]

            AMOUNT_THRESHOLD = 274.9

            features["Amount"] = data.amount

            # Feature Engineering (must match training)
            features["Log_Amount"] = np.log1p(data.amount)
            features["High_Amount"] = int(data.amount > AMOUNT_THRESHOLD)

            # Convert to DataFrame
            df = pd.DataFrame([features])

        # Scale 'Time' and 'Amount' if scaler is loaded
        if model_loader.scaler is not None:
            scaled_data = model_loader.scaler.transform(df)
            df = pd.DataFrame(scaled_data, columns=df.columns)

        # Predict probability
        if hasattr(model_loader.model, "predict_proba"):
            probabilities = model_loader.model.predict_proba(df)
            prob = float(probabilities[0][1])  # Probability of class 1 (Fraud)
        else:
            pred = model_loader.model.predict(df)
            prob = 1.0 if pred[0] == 1 else 0.0

        threshold = model_loader.threshold
        
        # Determine class
        is_fraud = prob >= threshold
        
        prediction_label = "Fraudulent" if is_fraud else "Legitimate"
        risk_level = get_risk_level(prob)
        
        # Confidence calculation
        if is_fraud:
            confidence = ((prob - threshold) / (1 - threshold)) * 100 if threshold < 1 else 100
        else:
            confidence = ((threshold - prob) / threshold) * 100 if threshold > 0 else 100
            
        confidence = min(max(confidence, 0), 100)
        if prob < 0.01: confidence = 99.0 + (1 - prob)*0.9
        if prob > 0.99: confidence = 99.0 + prob*0.9

        explanation = generate_explanation(prob, threshold)
        
        model_name = type(model_loader.model).__name__
        if model_name == "Booster" or "XGB" in model_name:
            model_name = "XGBoost"

        return PredictionResponse(
            prediction=prediction_label,
            probability=round(prob, 4),
            risk_level=risk_level,
            confidence=round(confidence, 2),
            threshold=round(threshold, 2),
            model=model_name,
            explanation=explanation
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
