"""
Preprocessing utilities for camera settings dataset
"""

import os
import json
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
from typing import Dict, List, Tuple, Optional
import pandas as pd
from pathlib import Path


def extract_exif_data(image_path: str) -> Optional[Dict]:
    """
    Extract EXIF data from image file
    
    Args:
        image_path: Path to image file
        
    Returns:
        Dictionary with EXIF data or None if unavailable
    """
    try:
        image = Image.open(image_path)
        exif_data = image.getexif()
        
        if not exif_data:
            return None
        
        exif_dict = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if isinstance(value, bytes):
                try:
                    value = value.decode()
                except:
                    continue
            exif_dict[tag] = value
        
        return exif_dict
    except Exception as e:
        print(f"Error extracting EXIF from {image_path}: {e}")
        return None


def parse_camera_settings(exif_data: Dict) -> Optional[Dict]:
    """
    Parse camera settings from EXIF data
    
    Args:
        exif_data: EXIF dictionary
        
    Returns:
        Dictionary with parsed camera settings
    """
    settings = {}
    
    try:
        # ISO
        if "ISOSpeedRatings" in exif_data:
            settings["iso"] = float(exif_data["ISOSpeedRatings"])
        
        # Aperture (F-number)
        if "FNumber" in exif_data:
            f_number = exif_data["FNumber"]
            if isinstance(f_number, tuple):
                settings["aperture"] = float(f_number[0]) / float(f_number[1])
            else:
                settings["aperture"] = float(f_number)
        
        # Shutter speed (Exposure time)
        if "ExposureTime" in exif_data:
            exp_time = exif_data["ExposureTime"]
            if isinstance(exp_time, tuple):
                settings["shutter_speed"] = float(exp_time[0]) / float(exp_time[1])
            else:
                settings["shutter_speed"] = float(exp_time)
        
        # Focal length
        if "FocalLength" in exif_data:
            focal = exif_data["FocalLength"]
            if isinstance(focal, tuple):
                settings["focal_length"] = float(focal[0]) / float(focal[1])
            else:
                settings["focal_length"] = float(focal)
        
        # Only return if we have at least ISO, aperture, and shutter speed
        if all(k in settings for k in ["iso", "aperture", "shutter_speed"]):
            return settings
        
        return None
    except Exception as e:
        print(f"Error parsing camera settings: {e}")
        return None


def preprocess_image(
    image_path: str, 
    target_size: Tuple[int, int] = (224, 224)
) -> np.ndarray:
    """
    Preprocess image for model training
    
    Args:
        image_path: Path to image file
        target_size: Target image size (height, width)
        
    Returns:
        Preprocessed image array
    """
    image = Image.open(image_path)
    
    # Convert to RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize
    image = image.resize(target_size)
    
    # Convert to array and normalize
    img_array = np.array(image).astype(np.float32) / 255.0
    
    return img_array


def create_dataset_from_images(
    image_dir: str,
    output_path: str,
    target_size: Tuple[int, int] = (224, 224)
) -> pd.DataFrame:
    """
    Create dataset from directory of images with EXIF data
    
    Args:
        image_dir: Directory containing images
        output_path: Path to save dataset CSV
        target_size: Target image size for preprocessing
        
    Returns:
        DataFrame with image paths and camera settings
    """
    data = []
    
    image_dir = Path(image_dir)
    image_files = list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.jpeg")) + \
                  list(image_dir.glob("*.JPG")) + list(image_dir.glob("*.JPEG"))
    
    print(f"Processing {len(image_files)} images...")
    
    for img_path in image_files:
        # Extract EXIF
        exif_data = extract_exif_data(str(img_path))
        if not exif_data:
            continue
        
        # Parse settings
        settings = parse_camera_settings(exif_data)
        if not settings:
            continue
        
        # Add to dataset
        data.append({
            "image_path": str(img_path),
            "iso": settings["iso"],
            "aperture": settings["aperture"],
            "shutter_speed": settings["shutter_speed"],
            "focal_length": settings.get("focal_length", 0)
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}")
    print(f"Total samples: {len(df)}")
    
    return df


def normalize_settings(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Normalize camera settings to 0-1 range
    
    Args:
        df: DataFrame with camera settings
        
    Returns:
        Normalized DataFrame and normalization parameters
    """
    norm_params = {}
    df_normalized = df.copy()
    
    for column in ["iso", "aperture", "shutter_speed", "focal_length"]:
        if column in df.columns:
            min_val = df[column].min()
            max_val = df[column].max()
            
            norm_params[column] = {"min": float(min_val), "max": float(max_val)}
            
            # Normalize
            df_normalized[column] = (df[column] - min_val) / (max_val - min_val + 1e-8)
    
    return df_normalized, norm_params


def split_dataset(
    df: pd.DataFrame, 
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    test_ratio: float = 0.1,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split dataset into train, validation, and test sets
    
    Args:
        df: Input DataFrame
        train_ratio: Ratio for training set
        val_ratio: Ratio for validation set
        test_ratio: Ratio for test set
        random_state: Random seed
        
    Returns:
        Tuple of (train_df, val_df, test_df)
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, \
        "Ratios must sum to 1.0"
    
    # Shuffle
    df_shuffled = df.sample(frac=1, random_state=random_state).reset_index(drop=True)
    
    # Calculate split indices
    n = len(df_shuffled)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)
    
    # Split
    train_df = df_shuffled[:train_end]
    val_df = df_shuffled[train_end:val_end]
    test_df = df_shuffled[val_end:]
    
    return train_df, val_df, test_df


if __name__ == "__main__":
    # Example usage
    print("Preprocessing utilities loaded")
    print("Use create_dataset_from_images() to create a dataset from images with EXIF data")
