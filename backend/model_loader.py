import os
import joblib
from dotenv import load_dotenv
from xgboost import XGBClassifier

load_dotenv()


class ModelLoader:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.threshold = 0.5
        self.load_models()

    def load_models(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        model_path = os.getenv("MODEL_PATH", "models/fraud_detector.json")
        scaler_path = os.getenv("SCALER_PATH", "models/scaler.pkl")
        threshold_path = os.getenv("THRESHOLD_PATH", "models/best_threshold.pkl")

        model_full_path = os.path.join(base_dir, model_path)
        scaler_full_path = os.path.join(base_dir, scaler_path)
        threshold_full_path = os.path.join(base_dir, threshold_path)

        try:
            # Load XGBoost model
            self.model = XGBClassifier()
            self.model.load_model(model_full_path)

            # Load scaler
            self.scaler = joblib.load(scaler_full_path)

            # Load threshold
            self.threshold = float(joblib.load(threshold_full_path))

            print("✅ Models loaded successfully!")

        except Exception as e:
            print(f"❌ Error loading models: {e}")
            self.model = None
            self.scaler = None
            self.threshold = 0.5


model_loader = ModelLoader()