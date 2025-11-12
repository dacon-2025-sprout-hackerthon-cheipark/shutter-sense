"""
Model conversion utilities: PyTorch -> ONNX -> CoreML
"""

import torch
import torch.nn as nn
from pathlib import Path
import argparse


def convert_to_onnx(
    pytorch_model_path: str,
    onnx_output_path: str,
    input_size: tuple = (1, 3, 224, 224)
):
    """
    Convert PyTorch model to ONNX format
    
    Args:
        pytorch_model_path: Path to PyTorch model (.pth)
        onnx_output_path: Path to save ONNX model
        input_size: Input tensor size (batch, channels, height, width)
    """
    from train_model import CameraSettingsModel
    
    print(f"Loading PyTorch model from {pytorch_model_path}")
    
    # Create model and load weights
    model = CameraSettingsModel(num_outputs=3, pretrained=False)
    
    # Load state dict
    checkpoint = torch.load(pytorch_model_path, map_location='cpu')
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)
    
    model.eval()
    
    # Create dummy input
    dummy_input = torch.randn(*input_size)
    
    # Export to ONNX
    print(f"Exporting to ONNX: {onnx_output_path}")
    torch.onnx.export(
        model,
        dummy_input,
        onnx_output_path,
        export_params=True,
        opset_version=11,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )
    
    print("ONNX export complete!")
    
    # Verify ONNX model
    try:
        import onnx
        onnx_model = onnx.load(onnx_output_path)
        onnx.checker.check_model(onnx_model)
        print("ONNX model verification passed!")
    except ImportError:
        print("Warning: ONNX not installed, skipping verification")
    except Exception as e:
        print(f"ONNX verification failed: {e}")


def convert_to_coreml(
    onnx_model_path: str,
    coreml_output_path: str,
    input_names: list = None,
    output_names: list = None
):
    """
    Convert ONNX model to CoreML format
    
    Args:
        onnx_model_path: Path to ONNX model
        coreml_output_path: Path to save CoreML model
        input_names: List of input names
        output_names: List of output names
    """
    try:
        import coremltools as ct
        from coremltools.converters.onnx import convert
    except ImportError:
        print("Error: coremltools not installed")
        print("Install with: pip install coremltools")
        return
    
    print(f"Loading ONNX model from {onnx_model_path}")
    
    # Convert to CoreML
    print(f"Converting to CoreML: {coreml_output_path}")
    
    coreml_model = convert(
        model=onnx_model_path,
        minimum_ios_deployment_target='13'
    )
    
    # Set metadata
    coreml_model.author = "ShutterSense"
    coreml_model.license = "MIT"
    coreml_model.short_description = "Camera settings prediction model"
    coreml_model.version = "1.0"
    
    # Set input/output descriptions
    if input_names:
        for name in input_names:
            coreml_model.input_description[name] = "Input image (224x224 RGB)"
    
    if output_names:
        output_desc = ["ISO (normalized)", "Aperture (normalized)", "Shutter Speed (normalized)"]
        for i, name in enumerate(output_names):
            if i < len(output_desc):
                coreml_model.output_description[name] = output_desc[i]
    
    # Save CoreML model
    coreml_model.save(coreml_output_path)
    
    print("CoreML conversion complete!")
    print(f"Model saved to: {coreml_output_path}")


def convert_pytorch_to_all(
    pytorch_model_path: str,
    output_dir: str,
    model_name: str = "camera_settings_model"
):
    """
    Convert PyTorch model to both ONNX and CoreML
    
    Args:
        pytorch_model_path: Path to PyTorch model
        output_dir: Output directory for converted models
        model_name: Base name for output models
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert to ONNX
    onnx_path = output_dir / f"{model_name}.onnx"
    convert_to_onnx(pytorch_model_path, str(onnx_path))
    
    # Convert to CoreML
    coreml_path = output_dir / f"{model_name}.mlmodel"
    convert_to_coreml(
        str(onnx_path),
        str(coreml_path),
        input_names=['input'],
        output_names=['output']
    )
    
    print("\n" + "="*50)
    print("Conversion Summary:")
    print(f"  PyTorch: {pytorch_model_path}")
    print(f"  ONNX: {onnx_path}")
    print(f"  CoreML: {coreml_path}")
    print("="*50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert models to ONNX and CoreML")
    parser.add_argument("--pytorch_model", type=str, required=True, 
                       help="Path to PyTorch model (.pth)")
    parser.add_argument("--output_dir", type=str, default="./models",
                       help="Output directory")
    parser.add_argument("--model_name", type=str, default="camera_settings_model",
                       help="Base name for output models")
    parser.add_argument("--format", type=str, choices=["onnx", "coreml", "all"],
                       default="all", help="Output format")
    
    args = parser.parse_args()
    
    if args.format == "all":
        convert_pytorch_to_all(args.pytorch_model, args.output_dir, args.model_name)
    elif args.format == "onnx":
        onnx_path = Path(args.output_dir) / f"{args.model_name}.onnx"
        convert_to_onnx(args.pytorch_model, str(onnx_path))
    elif args.format == "coreml":
        # Need ONNX first
        onnx_path = Path(args.output_dir) / f"{args.model_name}.onnx"
        if not onnx_path.exists():
            print("ONNX model not found, creating it first...")
            convert_to_onnx(args.pytorch_model, str(onnx_path))
        coreml_path = Path(args.output_dir) / f"{args.model_name}.mlmodel"
        convert_to_coreml(str(onnx_path), str(coreml_path))
