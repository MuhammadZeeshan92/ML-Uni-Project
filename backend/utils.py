def get_risk_level(probability: float) -> str:
    if probability < 0.2:
        return "Low"
    elif probability < 0.6:
        return "Medium"
    elif probability < 0.8:
        return "High"
    else:
        return "Critical"

def generate_explanation(probability: float, threshold: float) -> str:
    if probability >= threshold:
        return f"Transaction is flagged as fraudulent because the probability ({probability:.4f}) exceeds the safety threshold ({threshold:.4f})."
    else:
        return f"Transaction appears legitimate. The anomaly score ({probability:.4f}) is below the threshold ({threshold:.4f})."
