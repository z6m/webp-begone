import os
import shutil
from PIL import Image
from tqdm import tqdm

def webp_begone(folder_path, output_format, original_webp_path):
    
    # Initialize the progress bar
    total_files = sum(len(files) for _, _, files in os.walk(folder_path))
    with tqdm(total=total_files, desc="Converting", unit="file") as pbar:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.webp'):  # Check if the file has a .webp extension
                    # Open the .webp file
                    with Image.open(os.path.join(root, file)) as img:
                        # Convert to the chosen format
                        if output_format.lower() == 'jpg':
                            converted_img = img.convert('RGB')
                        elif output_format.lower() == 'png':
                            converted_img = img.convert('RGBA')
                        else:
                            print("Unsupported output format. Please choose 'jpg' or 'png'.")
                            return
                        # Save the converted image
                        output_file = os.path.splitext(file)[0] + '.' + output_format.lower()
                        output_path = os.path.join(root, output_file)
                        if not os.path.exists(output_path):  # Check if the converted file already exists
                            converted_img.save(output_path)
                        # Copy metadata
                        shutil.copystat(os.path.join(root, file), output_path)
                        
                        # Move the original .webp file to original_webps folder
                        shutil.move(os.path.join(root, file), os.path.join(original_webp_path, file))
                pbar.update(1)

# Make folder to backup original files
original_webp_folder = './original_webps'
os.makedirs(original_webp_folder, exist_ok=True)
original_webp_path = os.path.abspath(original_webp_folder)

# Get target folder/format
folder_path = input("[*] Enter root path of the folder(s) containting .webp files: ")
output_format = input("[*] Enter the desired output format (png/jpg): ")
if output_format.startswith("."):
    output_format = output_format[1:]

# Default to "png" if no output format is provided
if not output_format:
    output_format = "png"

webp_begone(folder_path, output_format, original_webp_path)




