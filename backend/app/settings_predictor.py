"""
Camera settings prediction module using ML model
"""

import io
import numpy as np
from PIL import Image
from typing import Dict, Any, Optional
import os

# Try to import ONNX runtime
try:
    import onnxruntime as ort
    HAS_ONNX = True
except ImportError:
    HAS_ONNX = False


class SettingsPredictor:
    """Camera settings predictor using ONNX model"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or os.path.join(
            os.path.dirname(__file__), 
            "../models/camera_settings_model.onnx"
        )
        self.session = None
        
        if HAS_ONNX and os.path.exists(self.model_path):
            self.session = ort.InferenceSession(self.model_path)
    
    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Preprocess image for model input
        
        Args:
            image_bytes: Raw image data
            
        Returns:
            Preprocessed image array
        """
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to model input size (224x224 is common)
        image = image.resize((224, 224))
        
        # Convert to array and normalize
        img_array = np.array(image).astype(np.float32)
        img_array = img_array / 255.0
        
        # Add batch dimension and transpose to CHW format
        img_array = np.transpose(img_array, (2, 0, 1))
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Predict camera settings from image
        
        Args:
            image_bytes: Raw image data
            
        Returns:
            Dictionary with predicted settings
        """
        if self.session is None:
            # Return rule-based predictions if no model available
            return self._rule_based_prediction(image_bytes)
        
        try:
            # Preprocess image
            input_data = self.preprocess_image(image_bytes)
            
            # Run inference
            input_name = self.session.get_inputs()[0].name
            outputs = self.session.run(None, {input_name: input_data})
            
            # Parse outputs (example structure)
            predictions = {
                "iso": int(outputs[0][0][0] * 6400),  # Scale to ISO range
                "aperture": f"f/{outputs[0][0][1] * 22:.1f}",  # f/1.4 to f/22
                "shutter_speed": f"1/{int(1 / (outputs[0][0][2] * 8000))}s",
                "confidence": float(outputs[0][0][3]) if len(outputs[0][0]) > 3 else 0.8
            }
            
            return predictions
            
        except Exception as e:
            # Fallback to rule-based
            return self._rule_based_prediction(image_bytes)
    
    def _rule_based_prediction(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Simple rule-based prediction when ML model is unavailable
        
        Args:
            image_bytes: Raw image data
            
        Returns:
            Dictionary with suggested settings
        """
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to grayscale for brightness analysis
        if image.mode != 'L':
            gray_image = image.convert('L')
        else:
            gray_image = image
        
        # Calculate average brightness
        img_array = np.array(gray_image)
        avg_brightness = np.mean(img_array)
        
        # Simple rules based on brightness
        if avg_brightness < 85:  # Dark image
            iso = 1600
            aperture = "f/2.8"
            shutter = "1/60s"
        elif avg_brightness < 170:  # Medium brightness
            iso = 400
            aperture = "f/5.6"
            shutter = "1/125s"
        else:  # Bright image
            iso = 100
            aperture = "f/8.0"
            shutter = "1/500s"
        
        return {
            "iso": iso,
            "aperture": aperture,
            "shutter_speed": shutter,
            "avg_brightness": float(avg_brightness),
            "note": "Rule-based prediction (ML model not available)"
        }


# Global predictor instance
_predictor = SettingsPredictor()


def predict_settings(image_bytes: bytes) -> Dict[str, Any]:
    """
    Main function to predict camera settings
    
    Args:
        image_bytes: Raw image data
        
    Returns:
        Dictionary with predicted settings
    """
    return _predictor.predict(image_bytes)
