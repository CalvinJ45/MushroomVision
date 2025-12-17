import requests
import os
import sys

URL = "https://github.com/CalvinJ45/MushroomVision/raw/main/backend/best_mushroom_cnn.keras"
OUTPUT_PATH = "backend/best_mushroom_cnn.keras"

def download_and_verify():
    print(f"Downloading model from {URL}...")
    
    try:
        response = requests.get(URL, stream=True)
        response.raise_for_status()
        
        with open(OUTPUT_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        file_size = os.path.getsize(OUTPUT_PATH)
        print(f"Download complete. File size: {file_size / (1024*1024):.2f} MB")
        
        # Validation 1: Size check (Model is ~227MB)
        if file_size < 10 * 1024 * 1024: # Less than 10MB is definitely wrong
            print("ERROR: Downloaded file is too small! It might be a Git LFS pointer or HTML error page.")
            with open(OUTPUT_PATH, 'r', errors='ignore') as f:
                print("--- File Content Preview ---")
                print(f.read(500))
                print("----------------------------")
            sys.exit(1)

        # Validation 2: Header check (HDF5 signature)
        # HDF5 magic number: \x89HDF\r\n\x1a\n
        with open(OUTPUT_PATH, 'rb') as f:
            header = f.read(8)
            print(f"File header (hex): {header.hex()}")
            
            # Keras 3 / new format often uses Zip (starts with PK) or HDF5
            # We just want to ensure it's not text (like 'version https://git-lfs')
            if b"git-lfs" in header or b"<!DOCT" in header or b"<html" in header:
                 print("ERROR: File appears to be a text file (LFS pointer or HTML).")
                 sys.exit(1)

        print("SUCCESS: Model file appears valid.")

    except Exception as e:
        print(f"ERROR during download: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure backend directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    download_and_verify()
