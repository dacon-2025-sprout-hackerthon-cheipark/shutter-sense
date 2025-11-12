# ShutterSense ML Training

Machine learning training infrastructure for camera settings prediction.

## Setup

```bash
pip install -r requirements.txt
```

## Dataset Preparation

1. Collect photos with EXIF data containing camera settings
2. Run preprocessing script:

```bash
python scripts/preprocess.py
```

This will:
- Extract EXIF metadata from images
- Parse camera settings (ISO, aperture, shutter speed)
- Create a CSV dataset
- Normalize settings for training

## Training

Train the camera settings prediction model:

```bash
python scripts/train_model.py \
  --train_csv data/train.csv \
  --val_csv data/val.csv \
  --output_dir models \
  --num_epochs 50 \
  --batch_size 32
```

## Model Conversion

Convert trained PyTorch model to ONNX and CoreML:

```bash
python scripts/convert_model.py \
  --pytorch_model models/best_model.pth \
  --output_dir ../backend/models \
  --format all
```

This will create:
- `camera_settings_model.onnx` - For backend inference
- `camera_settings_model.mlmodel` - For iOS app

## Model Architecture

- **Backbone**: ResNet-18 pretrained on ImageNet
- **Input**: 224x224 RGB images
- **Output**: 3 values (normalized 0-1)
  - ISO (normalized)
  - Aperture (normalized)
  - Shutter Speed (normalized)

## Directory Structure

```
ml_training/
├── data/              # Training datasets
├── models/            # Saved model checkpoints
├── scripts/           # Training and conversion scripts
│   ├── preprocess.py       # Data preprocessing
│   ├── train_model.py      # Model training
│   └── convert_model.py    # Model conversion
└── utils/             # Utility functions
```

## Notes

- The model is trained on images with EXIF metadata
- Requires a dataset of photos with known camera settings
- Model predicts normalized values (0-1 range)
- Denormalization parameters should be saved during preprocessing
