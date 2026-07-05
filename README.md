# FraudGuard AI

A production-ready full-stack web application for real-time Machine Learning Fraud Detection.

## Project Overview

FraudGuard AI leverages a pre-trained machine learning model (e.g., XGBoost) to classify transactions as legitimate or fraudulent in milliseconds. The system includes a modern, responsive frontend built with Vanilla HTML/CSS/JS and a scalable FastAPI backend that serves both the UI and the prediction endpoints.

## Features
- **Real-Time Prediction**: Instantaneous fraud probability calculation.
- **Responsive UI**: Pixel-perfect design that works across Desktop, Tablet, and Mobile.
- **FastAPI Backend**: High-performance asynchronous API for ML inference.
- **Modular Architecture**: Clean separation of routes, schemas, and model loading.
- **Robust Validation**: Both frontend and backend data validation.

## Folder Structure

```
MLProject/
├── backend/               # FastAPI Server & Logic
│   ├── app.py             # Main FastAPI application
│   ├── predict.py         # Prediction pipeline logic
│   ├── schemas.py         # Pydantic validation models
│   ├── model_loader.py    # Singleton model loader
│   ├── requirements.txt   # Python dependencies
│   ├── .env               # Environment configuration
│   └── utils.py           # Helper functions
├── frontend/              # Static Frontend Assets
│   ├── index.html         # Main Landing Page
│   ├── css/               # Stylesheets
│   ├── js/                # Modular JavaScript
│   └── assets/            # Images and Icons
├── models/                # Trained ML Models (User must add)
│   ├── fraud_detector.json
│   ├── scaler.pkl
│   └── best_threshold.pkl
└── README.md
```

## Installation & Setup

### 1. Requirements
- Python 3.9+
- A trained XGBoost model file (`.json`) plus scaler and threshold pickle files.

### 2. How to Add the ML Model
Place your trained model files exactly in the `models/` directory at the root of the project:

- `models/fraud_detector.json`
- `models/scaler.pkl`
- `models/best_threshold.pkl`

### 3. Install Dependencies
Navigate to the project root and install the required Python packages:
```bash
pip install -r backend/requirements.txt
```

### 4. Start the Application
Run the FastAPI server using Uvicorn:
```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

### 5. Access the Website
Open your browser and navigate to:
[http://localhost:8000](http://localhost:8000)

## API Documentation

FastAPI automatically generates interactive API documentation. You can view it by starting the server and navigating to:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Endpoint: `POST /predict`
Evaluates a transaction payload.

**Request JSON:**
```json
{
    "time": 482.0,
    "amount": 124.50,
    "v_features": {
        "V1": -1.2, "V2": 0.5, "V3": 1.1, "V4": 0.0, "V5": 0.0, "V6": 0.0, "V7": 0.0, "V8": 0.0, "V9": 0.0, "V10": 0.0, "V11": 0.0, "V12": 0.0, "V13": 0.0, "V14": 0.0, "V15": 0.0, "V16": 0.0, "V17": 0.0, "V18": 0.0, "V19": 0.0, "V20": 0.0, "V21": 0.0, "V22": 0.0, "V23": 0.0, "V24": 0.0, "V25": 0.0, "V26": 0.0, "V27": 0.0, "V28": 0.01
    }
}
```

**Response JSON:**
```json
{
    "prediction": "Legitimate",
    "probability": 0.0023,
    "risk_level": "Low",
    "confidence": 99.77,
    "threshold": 0.5,
    "model": "XGBoost",
    "explanation": "Transaction appears legitimate. The anomaly score is below the threshold."
}
```

## Deployment
For production deployment, use a process manager like Gunicorn with Uvicorn workers:
```bash
gunicorn backend.app:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

Ensure you set appropriate environment variables (see `backend/.env`) to configure the file paths if the model location changes in production.

## License
MIT License.
