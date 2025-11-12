"""
ShutterSense Backend API

FastAPI backend for AI camera application providing:
- Photo metadata extraction
- Camera settings prediction via pretrained models
- LLM-based parameter suggestions
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn

from app.metadata_extractor import extract_metadata
from app.settings_predictor import predict_settings
from app.llm_advisor import suggest_parameters

app = FastAPI(
    title="ShutterSense API",
    description="AI-powered camera settings and metadata extraction service",
    version="1.0.0"
)

# Enable CORS for Swift frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    """Request model for LLM parameter suggestions"""
    prompt: str
    current_settings: Optional[Dict[str, Any]] = None


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "ShutterSense API",
        "version": "1.0.0",
        "endpoints": {
            "/metadata": "Extract EXIF metadata from photos",
            "/predict": "Predict optimal camera settings",
            "/suggest": "Get LLM-based parameter suggestions"
        }
    }


@app.post("/metadata")
async def get_metadata(file: UploadFile = File(...)):
    """
    Extract EXIF metadata from uploaded photo
    
    Args:
        file: Image file (JPEG, PNG, etc.)
        
    Returns:
        Dict containing extracted metadata
    """
    try:
        contents = await file.read()
        metadata = extract_metadata(contents)
        return {"success": True, "metadata": metadata}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict")
async def predict_camera_settings(file: UploadFile = File(...)):
    """
    Predict optimal camera settings for an image using ML model
    
    Args:
        file: Image file for analysis
        
    Returns:
        Dict containing predicted camera settings
    """
    try:
        contents = await file.read()
        predictions = predict_settings(contents)
        return {"success": True, "predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/suggest")
async def suggest_camera_parameters(request: PromptRequest):
    """
    Get LLM-based camera parameter suggestions from natural language prompt
    
    Args:
        request: PromptRequest with user prompt and optional current settings
        
    Returns:
        Dict containing suggested camera parameters
    """
    try:
        suggestions = suggest_parameters(
            request.prompt,
            request.current_settings
        )
        return {"success": True, "suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
