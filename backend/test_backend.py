"""
Unit tests for backend API
"""

import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from PIL import Image


# Create a test image
def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


def test_root_endpoint():
    """Test root endpoint"""
    from main import app
    client = TestClient(app)
    
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "ShutterSense" in response.json()["message"]


def test_health_endpoint():
    """Test health check endpoint"""
    from main import app
    client = TestClient(app)
    
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_metadata_endpoint():
    """Test metadata extraction endpoint"""
    from main import app
    client = TestClient(app)
    
    img_bytes = create_test_image()
    
    response = client.post(
        "/metadata",
        files={"file": ("test.jpg", img_bytes, "image/jpeg")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "metadata" in data


def test_predict_endpoint():
    """Test settings prediction endpoint"""
    from main import app
    client = TestClient(app)
    
    img_bytes = create_test_image()
    
    response = client.post(
        "/predict",
        files={"file": ("test.jpg", img_bytes, "image/jpeg")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "predictions" in data


def test_suggest_endpoint():
    """Test LLM suggestions endpoint"""
    from main import app
    client = TestClient(app)
    
    response = client.post(
        "/suggest",
        json={
            "prompt": "portrait photography",
            "current_settings": {"iso": "400"}
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "suggestions" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
