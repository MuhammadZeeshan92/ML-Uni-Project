from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, List

class TransactionInput(BaseModel):
    time: float = Field(..., description="Seconds elapsed between this transaction and the first transaction in the dataset")
    amount: float = Field(..., description="Transaction amount")
    v_features: Dict[str, float] = Field(..., description="PCA transformed features V1 to V28")

    @field_validator('v_features')
    def check_v_features(cls, v):
        for i in range(1, 29):
            key = f"V{i}"
            if key not in v:
                raise ValueError(f"Missing feature: {key}")
        return v

class PredictionResponse(BaseModel):
    prediction: str
    probability: float
    risk_level: str
    confidence: float
    threshold: float
    model: str
    explanation: str
