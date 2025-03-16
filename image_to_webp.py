import os
import shutil
from PIL import Image

# It will get the script's directory (thats our default assumption)
script_dir = os.path.dirname(os.path.abspath(__file__))
default_assets_path = os.path.join(script_dir, "assets", "images")

# Check if the default assets path exists
if not os.path.exists(default_assets_path):
    print(" Warning: Default assets folder not found!")
    user_path = input(" Please enter the full path to your 'assets/images' folder: ").strip()
    if os.path.exists(user_path):
        default_assets_path = user_path
    else:
        print("Error: Invalid path! Exiting...")
        exit()

# Define folder paths based on detected or user-provided location
original_folder = os.path.join(default_assets_path, "original images")
webp_folder = os.path.join(default_assets_path, "webp images")

# Ensure the output folder exists
os.makedirs(webp_folder, exist_ok=True)

# Loop through images in original folder
for filename in os.listdir(original_folder):
    file_path = os.path.join(original_folder, filename)

    # Check if it's an image file
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        webp_filename = os.path.splitext(filename)[0] + ".webp"
        webp_path = os.path.join(webp_folder, webp_filename)

        #  CASE 1: If WebP already exists in `webp images/`, SKIP
        if os.path.exists(webp_path):
            print(f" Skipping {filename} (WebP already exists in webp images/)")
            continue  

        #  CASE 2: If WebP exists in `original images/`, MOVE it to `webp images/`
        original_webp_path = os.path.join(original_folder, webp_filename)
        if os.path.exists(original_webp_path):
            print(f" Moving {webp_filename} to webp images folder")
            shutil.move(original_webp_path, webp_path)
            continue  

        #  CASE 3: Convert to WebP if not found anywhere
        print(f"⚡ Converting {filename} to WebP...")
        image = Image.open(file_path)
        image.save(webp_path, "WEBP", quality=80)

print(" All conversions/movements completed successfully!")