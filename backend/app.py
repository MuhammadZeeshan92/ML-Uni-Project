from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
import os

from backend.schemas import TransactionInput
from backend.predict import make_prediction

app = FastAPI(title="FraudGuard AI API", description="AI-powered Fraud Detection API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid input data. Please ensure all required fields are provided and numeric."}
    )

@app.post("/predict")
async def predict_endpoint(transaction: TransactionInput):
    """
    Endpoint to predict if a transaction is fraudulent based on PCA features, Time, and Amount.
    """
    return make_prediction(transaction)

# Mount static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

if os.path.exists(frontend_dir):
    app.mount("/css", StaticFiles(directory=os.path.join(frontend_dir, "css")), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(frontend_dir, "js")), name="js")
    # For assets, we might need a fallback if it doesn't exist yet, but StaticFiles requires it to exist.
    assets_dir = os.path.join(frontend_dir, "assets")
    if not os.path.exists(assets_dir):
        os.makedirs(os.path.join(assets_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(assets_dir, "icons"), exist_ok=True)
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

@app.get("/")
async def serve_index():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
