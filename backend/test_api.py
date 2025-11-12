"""
Example script to test the backend API
"""

import requests
import sys
from pathlib import Path


def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_metadata(image_path: str):
    """Test metadata extraction"""
    print(f"Testing /metadata with {image_path}...")
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post("http://localhost:8000/metadata", files=files)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Metadata: {data['metadata']}")
    else:
        print(f"Error: {response.text}")
    print()


def test_predict(image_path: str):
    """Test settings prediction"""
    print(f"Testing /predict with {image_path}...")
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post("http://localhost:8000/predict", files=files)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Predictions: {data['predictions']}")
    else:
        print(f"Error: {response.text}")
    print()


def test_suggest(prompt: str):
    """Test LLM suggestions"""
    print(f"Testing /suggest with prompt: '{prompt}'...")
    
    payload = {
        "prompt": prompt,
        "current_settings": {
            "iso": "400",
            "aperture": "f/5.6"
        }
    }
    
    response = requests.post(
        "http://localhost:8000/suggest",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Suggestions: {data['suggestions']}")
    else:
        print(f"Error: {response.text}")
    print()


if __name__ == "__main__":
    print("ShutterSense API Test Script")
    print("=" * 50)
    print()
    
    # Test health
    try:
        test_health()
    except Exception as e:
        print(f"Health check failed: {e}")
        print("Make sure the backend is running!")
        sys.exit(1)
    
    # Test with image if provided
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        if Path(image_path).exists():
            test_metadata(image_path)
            test_predict(image_path)
        else:
            print(f"Image not found: {image_path}")
    else:
        print("No image provided. Skipping image tests.")
        print("Usage: python test_api.py <image_path>")
        print()
    
    # Test suggestions
    test_suggest("I want to take portrait photos in low light")
    test_suggest("Action photography for sports")
    
    print("=" * 50)
    print("Test complete!")
