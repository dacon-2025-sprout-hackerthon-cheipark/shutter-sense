"""
Example usage of preprocessing utilities
"""

from scripts.preprocess import (
    create_dataset_from_images,
    normalize_settings,
    split_dataset
)
import json


def main():
    # Step 1: Create dataset from images
    print("Step 1: Creating dataset from images...")
    print("=" * 50)
    
    # Replace with your image directory
    image_dir = "./data/raw_images"
    output_csv = "./data/dataset.csv"
    
    print(f"Looking for images in: {image_dir}")
    print(f"Output will be saved to: {output_csv}")
    print()
    
    # Uncomment when you have images
    # df = create_dataset_from_images(image_dir, output_csv)
    
    # Step 2: Normalize settings
    print("\nStep 2: Normalizing camera settings...")
    print("=" * 50)
    
    # Uncomment when you have a dataset
    # df_normalized, norm_params = normalize_settings(df)
    
    # Save normalization parameters
    # with open("./data/norm_params.json", "w") as f:
    #     json.dump(norm_params, f, indent=2)
    # print(f"Normalization parameters saved")
    # print(f"Parameters: {norm_params}")
    
    # Step 3: Split dataset
    print("\nStep 3: Splitting dataset...")
    print("=" * 50)
    
    # Uncomment when you have normalized data
    # train_df, val_df, test_df = split_dataset(df_normalized)
    
    # Save splits
    # train_df.to_csv("./data/train.csv", index=False)
    # val_df.to_csv("./data/val.csv", index=False)
    # test_df.to_csv("./data/test.csv", index=False)
    
    # print(f"Train samples: {len(train_df)}")
    # print(f"Val samples: {len(val_df)}")
    # print(f"Test samples: {len(test_df)}")
    
    print("\nPreprocessing steps outlined!")
    print("Uncomment the code blocks when you have images with EXIF data.")


if __name__ == "__main__":
    main()
