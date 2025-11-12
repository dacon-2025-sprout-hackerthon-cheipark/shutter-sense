# ShutterSense 📸

AI-powered camera application that extracts photo metadata, predicts optimal camera settings via pretrained models, and provides intelligent parameter suggestions through natural language prompts.

## 🎯 Features

- **📊 Metadata Extraction**: Extract and analyze EXIF data from photos
- **🤖 ML-Based Predictions**: Predict optimal camera settings using deep learning models
- **💬 LLM Suggestions**: Get intelligent camera parameter recommendations from natural language prompts
- **📱 Cross-Platform**: Swift + Core ML frontend for iOS, FastAPI backend for inference
- **🔄 Model Conversion**: Complete pipeline for PyTorch → ONNX → CoreML conversion

## 🏗️ Architecture

```
shutter-sense/
├── backend/              # FastAPI backend
│   ├── app/             # API endpoints and services
│   ├── models/          # Trained ML models (ONNX)
│   └── main.py          # FastAPI application
├── ml_training/         # ML training infrastructure
│   ├── data/            # Training datasets
│   ├── models/          # Model checkpoints
│   └── scripts/         # Training and conversion scripts
└── ios_app/             # Swift iOS application
    └── ShutterSense/    # SwiftUI app with Core ML
```

## 🚀 Quick Start

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The API will be available at `http://localhost:8000`

### ML Training

```bash
cd ml_training
pip install -r requirements.txt

# Prepare dataset from images with EXIF data
python scripts/preprocess.py

# Train the model
python scripts/train_model.py \
  --train_csv data/train.csv \
  --val_csv data/val.csv \
  --output_dir models

# Convert to ONNX and CoreML
python scripts/convert_model.py \
  --pytorch_model models/best_model.pth \
  --output_dir ../backend/models \
  --format all
```

### iOS App

1. Open `ios_app/ShutterSense` in Xcode
2. Add the CoreML model to the project
3. Configure backend URL in `APIService.swift`
4. Build and run on iOS device or simulator

## 📖 API Documentation

### POST /metadata
Extract EXIF metadata from photos

```bash
curl -X POST "http://localhost:8000/metadata" \
  -F "file=@photo.jpg"
```

### POST /predict
Predict optimal camera settings

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@photo.jpg"
```

### POST /suggest
Get LLM-based parameter suggestions

```bash
curl -X POST "http://localhost:8000/suggest" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "I want to take portrait photos in low light",
    "current_settings": {"iso": 100, "aperture": "f/8"}
  }'
```

## 🔧 Technology Stack

- **Backend**: FastAPI, Python 3.8+
- **ML Framework**: PyTorch, ONNX Runtime
- **Model Conversion**: ONNX, CoreML Tools
- **Frontend**: Swift, SwiftUI, Core ML
- **LLM**: OpenAI API (optional, falls back to rule-based)

## 📋 Requirements

### Backend
- Python 3.8+
- FastAPI
- Pillow (PIL)
- ONNX Runtime
- OpenAI API key (optional)

### ML Training
- PyTorch
- torchvision
- scikit-learn
- ONNX
- CoreML Tools

### iOS App
- iOS 15.0+
- Xcode 14.0+
- Swift 5.5+

## 🧪 Model Details

The camera settings prediction model uses:
- **Architecture**: ResNet-18 backbone with custom head
- **Input**: 224×224 RGB images
- **Output**: Normalized camera parameters (ISO, aperture, shutter speed)
- **Training**: Transfer learning on ImageNet-pretrained weights

## 🌟 Use Cases

1. **Photography Learning**: Understand what settings professionals use
2. **Quick Setup**: Get instant suggestions for common scenarios
3. **Metadata Analysis**: Analyze and learn from your photo collection
4. **AI Assistant**: Natural language interface for camera settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Links

- [Backend Documentation](backend/README.md)
- [ML Training Guide](ml_training/README.md)
- [iOS App Setup](ios_app/README.md)

## 🙏 Acknowledgments

Built with ❤️ for photographers and AI enthusiasts.