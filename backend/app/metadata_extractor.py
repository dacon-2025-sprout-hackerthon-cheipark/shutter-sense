"""
Metadata extraction module for photo EXIF data
"""

from PIL import Image
from PIL.ExifTags import TAGS
import io
from typing import Dict, Any


def extract_metadata(image_bytes: bytes) -> Dict[str, Any]:
    """
    Extract EXIF metadata from image bytes
    
    Args:
        image_bytes: Raw image data
        
    Returns:
        Dictionary containing extracted metadata
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        metadata = {
            "format": image.format,
            "mode": image.mode,
            "size": {
                "width": image.width,
                "height": image.height
            }
        }
        
        # Extract EXIF data if available
        exif_data = image.getexif()
        if exif_data:
            exif_info = {}
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                
                # Convert bytes to string for readability
                if isinstance(value, bytes):
                    try:
                        value = value.decode()
                    except:
                        value = str(value)
                
                exif_info[tag] = value
            
            metadata["exif"] = exif_info
            
            # Extract common camera settings
            camera_settings = {}
            
            if "ISOSpeedRatings" in exif_info:
                camera_settings["iso"] = exif_info["ISOSpeedRatings"]
            
            if "FNumber" in exif_info:
                f_number = exif_info["FNumber"]
                if isinstance(f_number, tuple):
                    camera_settings["aperture"] = f"f/{f_number[0]/f_number[1]:.1f}"
                else:
                    camera_settings["aperture"] = f"f/{f_number}"
            
            if "ExposureTime" in exif_info:
                exp_time = exif_info["ExposureTime"]
                if isinstance(exp_time, tuple):
                    camera_settings["shutter_speed"] = f"{exp_time[0]}/{exp_time[1]}s"
                else:
                    camera_settings["shutter_speed"] = f"{exp_time}s"
            
            if "FocalLength" in exif_info:
                focal = exif_info["FocalLength"]
                if isinstance(focal, tuple):
                    camera_settings["focal_length"] = f"{focal[0]/focal[1]:.1f}mm"
                else:
                    camera_settings["focal_length"] = f"{focal}mm"
            
            if "Make" in exif_info:
                camera_settings["camera_make"] = exif_info["Make"]
            
            if "Model" in exif_info:
                camera_settings["camera_model"] = exif_info["Model"]
            
            if "LensModel" in exif_info:
                camera_settings["lens_model"] = exif_info["LensModel"]
            
            if "WhiteBalance" in exif_info:
                camera_settings["white_balance"] = exif_info["WhiteBalance"]
            
            metadata["camera_settings"] = camera_settings
        
        return metadata
        
    except Exception as e:
        raise Exception(f"Failed to extract metadata: {str(e)}")
