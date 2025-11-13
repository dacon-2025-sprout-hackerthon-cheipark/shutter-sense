# ShutterSense Backend

한국어 문서: README.ko.md

FastAPI backend for AI camera application.

## Setup

```bash
uv sync

```

## Running the Server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /metadata
Extract EXIF metadata from photos.

**Request:** Multipart form data with image file

**Response:**
```json
{
  "success": true,
  "metadata": {
    "format": "JPEG",
    "size": {"width": 4032, "height": 3024},
    "camera_settings": {
      "iso": 400,
      "aperture": "f/2.8",
      "shutter_speed": "1/125s"
    }
  }
}
```

### POST /predict
Predict optimal camera settings for an image.

**Request:** Multipart form data with image file

**Response:**
```json
{
  "success": true,
  "predictions": {
    "iso": 400,
    "aperture": "f/5.6",
    "shutter_speed": "1/125s"
  }
}
```

### POST /suggest
Get LLM-based parameter suggestions from natural language.

**Request:**
```json
{
  "prompt": "I want to take a portrait photo in low light",
  "current_settings": {
    "iso": 100,
    "aperture": "f/8"
  }
}
```

**Response:**
```json
{
  "success": true,
  "suggestions": {
    "iso": 1600,
    "aperture": "f/2.8",
    "shutter_speed": "1/60s",
    "explanation": "For low light portraits..."
  }
}
```

## Environment Variables

- `OPENAI_API_KEY`: Optional, for LLM-based suggestions (falls back to rule-based if not set)
