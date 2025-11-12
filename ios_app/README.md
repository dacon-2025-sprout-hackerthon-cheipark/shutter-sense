# ShutterSense iOS App

Swift + Core ML frontend for the AI camera application.

## Features

- **Camera/Photo Selection**: Capture or select photos from library
- **Metadata Extraction**: View EXIF data and camera settings
- **AI Predictions**: Predict optimal camera settings using ML models
- **LLM Suggestions**: Get natural language camera advice

## Architecture

### Views
- `ContentView.swift` - Main tab-based interface
- `CameraView.swift` - Camera/photo selection
- `MetadataView.swift` - EXIF metadata display
- `PredictionsView.swift` - ML-based settings predictions
- `SuggestionsView.swift` - LLM-based suggestions

### Models
- `CameraModels.swift` - Data models for API responses

### Services
- `APIService.swift` - Backend API communication
- `CoreMLService.swift` - Local CoreML inference

### ViewModels
- `CameraViewModel.swift` - Main view state management

## Setup

1. Open the project in Xcode
2. Add the CoreML model:
   - Drag `camera_settings_model.mlmodel` into the Xcode project
   - Ensure it's added to the app target
3. Configure the backend URL in `APIService.swift`:
   ```swift
   private let baseURL = "http://your-backend-url:8000"
   ```
4. Build and run on a device or simulator

## Requirements

- iOS 15.0+
- Xcode 14.0+
- Swift 5.5+

## Backend Integration

The app communicates with the FastAPI backend for:
1. Metadata extraction
2. ML inference (when CoreML is unavailable)
3. LLM-based suggestions

Ensure the backend is running and accessible from the iOS device.

## CoreML Model

The app can use a local CoreML model for on-device inference. Place the compiled `.mlmodelc` file in the app bundle or use the `.mlmodel` file which Xcode will compile automatically.

## Permissions

Add these to `Info.plist`:
```xml
<key>NSCameraUsageDescription</key>
<string>We need access to your camera to take photos</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>We need access to your photo library to select images</string>
```
