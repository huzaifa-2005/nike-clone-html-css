import os 
import shutil
from PIL import Image


try:
    import pillow_avif
      
except ImportError:
    print("Missing AVIF plugin! Install it using: pip install pillow-avif-plugin")
    exit()

IMAGE_EXTENSIONS = (
    '.jpg', '.jpeg', '.png', '.gif', '.webp',  # Common formats
    '.tiff', '.tif', '.bmp', '.svg', '.heic',  # Additional formats
    '.ico', '.jfif', '.pjpeg', '.pjp',         # Other formats used in browsers
    '.avif', '.raw', '.arw', '.cr2', '.nrw',   # High-quality & RAW formats
    '.orf', '.sr2', '.raf', '.dng'             # Camera RAW formats
)
  

# Getting script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
default_assets_path = os.path.join(script_dir, "assets", "images")

# Check if default assets folder exists
if not os.path.exists(default_assets_path):
    print("Warning: Default assets folder not found!")
    user_path = input("Please enter the full path to your 'assets/images' folder: ").strip()
    if os.path.exists(user_path):
        default_assets_path = user_path
    else:
        print("Error: Invalid path! Exiting...")
        exit()

# Define folder paths
original_folder = os.path.join(default_assets_path, "original images")
webp_folder = os.path.join(default_assets_path, "webp images")

os.makedirs(original_folder, exist_ok=True)
os.makedirs(webp_folder, exist_ok=True)

def check_for_images(original_folder):
    # Check if at least one image exists in the original folder.
    return any(file.lower().endswith(IMAGE_EXTENSIONS) for file in os.listdir(original_folder))

# Exit if no images are found
if not check_for_images(original_folder):
    print("Error: No image files found in 'original images/' folder! Exiting...")
    exit()

# here , start of processing images
for filename in os.listdir(original_folder):
    file_path = os.path.join(original_folder, filename)
    file_ext = filename.lower().endswith(IMAGE_EXTENSIONS)

    if file_ext:
        webp_filename = os.path.splitext(filename)[0] + ".webp"
        webp_path = os.path.join(webp_folder, webp_filename)

        # CASE 1: the image already exists as a  WebP file in `webp images/`
        if os.path.exists(webp_path):
            print(f"Skipping {filename} (WebP already exists in webp images/)")
            continue  

        # CASE 2: image WebP exists in `original images/`, so we are moving it to the `webp images/` , no need to convert
        original_webp_path = os.path.join(original_folder, webp_filename)
        if os.path.exists(original_webp_path):
            print(f"Moving {webp_filename} to webp images folder")
            shutil.move(original_webp_path, webp_path)
            continue  

        # CASE 3: Conversion into WebP when both above cases are false
        try:
            print(f" Converting {filename} to WebP...")
            image = Image.open(file_path)
            image.save(webp_path, "WEBP", quality=80)
            print(f" Successfully converted: {filename} into {webp_filename}")
        # in case , if the processing file is not not an image    
        except Exception as e:
            print(f" Error processing {filename}: {e}")

print(" All conversions/movements completed successfully!")

